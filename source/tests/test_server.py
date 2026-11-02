import http.client
import json
import os
import sys
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tensei import server  # noqa: E402


class StubThinker:
    def ask(self, question):
        return {
            "answer": "Echo: " + question,
            "steps": [],
            "sources": [],
            "mode": "test",
            "confidence": 1.0,
            "took_s": 0.01,
        }


class StubApp:
    def __init__(self):
        self.thinker = StubThinker()


class TestRequestValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_app = server.APP
        server.APP = StubApp()
        cls.httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.host, cls.port = cls.httpd.server_address

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join(timeout=3)
        server.APP = cls.original_app

    def post(self, path, body):
        if not isinstance(body, bytes):
            body = json.dumps(body).encode("utf-8")
        connection = http.client.HTTPConnection(self.host, self.port, timeout=3)
        try:
            connection.request(
                "POST",
                path,
                body=body,
                headers={
                    "Content-Type": "application/json",
                    "Connection": "close",
                },
            )
            response = connection.getresponse()
            return response.status, json.loads(response.read())
        finally:
            connection.close()

    def test_malformed_json_returns_bad_request(self):
        status, body = self.post("/api/ask", b'{"q":')
        self.assertEqual(status, 400)
        self.assertEqual(body, {"error": "malformed JSON body"})

    def test_non_object_json_returns_bad_request(self):
        status, body = self.post("/api/ask", ["question"])
        self.assertEqual(status, 400)
        self.assertEqual(body, {"error": "JSON body must be an object"})

    def test_oversized_json_returns_payload_too_large(self):
        with patch.object(server, "MAX_REQUEST_BYTES", 8):
            status, body = self.post("/api/ask", {"q": "too long"})
        self.assertEqual(status, 413)
        self.assertEqual(body, {"error": "request body is too large"})

    def test_invalid_utf8_returns_bad_request(self):
        status, body = self.post("/api/ask", b'{"q":"\xff"}')
        self.assertEqual(status, 400)
        self.assertEqual(body, {"error": "malformed JSON body"})

    def test_chunked_request_body_is_rejected(self):
        connection = http.client.HTTPConnection(self.host, self.port, timeout=3)
        try:
            connection.request(
                "POST",
                "/api/ask",
                body=b'{"q":"hello"}',
                headers={"Transfer-Encoding": "chunked"},
            )
            response = connection.getresponse()
            self.assertEqual(response.status, 400)
            self.assertEqual(
                json.loads(response.read()),
                {"error": "Transfer-Encoding is not supported"},
            )
        finally:
            connection.close()

    def test_question_must_be_text(self):
        status, body = self.post("/api/ask", {"q": 42})
        self.assertEqual(status, 400)
        self.assertEqual(body, {"error": "question must be a string"})

    def test_openai_messages_must_be_well_formed(self):
        cases = (
            ({"messages": {}}, "messages must be an array"),
            ({"messages": ["invalid"]}, "each message must be an object"),
            (
                {"messages": [{"role": "user", "content": 7}]},
                "user message content must be a string",
            ),
        )
        for payload, expected in cases:
            with self.subTest(payload=payload):
                status, body = self.post("/v1/chat/completions", payload)
                self.assertEqual(status, 400)
                self.assertEqual(body["error"]["message"], expected)

    def test_valid_openai_message_still_returns_completion(self):
        status, body = self.post(
            "/v1/chat/completions",
            {"messages": [{"role": "user", "content": "hello"}]},
        )
        self.assertEqual(status, 200)
        self.assertEqual(body["choices"][0]["message"]["content"], "Echo: hello")

    def test_openai_engine_error_returns_server_error(self):
        with patch.object(server.APP.thinker, "ask", side_effect=RuntimeError):
            status, body = self.post(
                "/v1/chat/completions",
                {"messages": [{"role": "user", "content": "hello"}]},
            )
        self.assertEqual(status, 500)
        self.assertEqual(body, {"error": {"message": "internal server error"}})


if __name__ == "__main__":
    unittest.main()
