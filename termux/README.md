# Termux installation

Use Termux to run the full SageCircuit engine on Android without root privileges
or an Android Studio setup.

```bash
pkg update -y
pkg install -y python python-numpy curl
REPO="gaurzamdev/SageCircuit"
mkdir -p ~/TenSeiAi && cd ~/TenSeiAi
curl -fL -o TenSeiAi.pyz "https://github.com/$REPO/releases/latest/download/TenSeiAi.pyz"
curl -fL -o TenSeiAi.tsei "https://github.com/$REPO/releases/latest/download/TenSeiAi.tsei"
python TenSeiAi.pyz TenSeiAi.tsei
```

To add the `tensei` command using the local files:

```bash
bash termux/install.sh ./TenSeiAi.pyz ./TenSeiAi.tsei
tensei ask "Why do earthquakes happen?"
```

To launch the browser interface:

```bash
python TenSeiAi.pyz serve --port 8765
```

Visit `http://127.0.0.1:8765` in a browser on the phone. Termux does not ship
with a browser; install one or use `termux-open-url` provided by
`termux-tools`.

See [`docs/ANDROID.md`](../docs/ANDROID.md) for the complete Android guide.
