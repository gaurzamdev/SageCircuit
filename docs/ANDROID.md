# Running SageCircuit on Android

SageCircuit has two Android options: launch it directly in Termux, or build a native
app using Chaquopy. Both approaches keep the model on the device.

## Termux: quick setup without root

Termux can run the full engine without Android Studio:

```bash
pkg update -y
pkg install -y python python-numpy curl
REPO="gaurzamdev/SageCircuit"
mkdir -p ~/TenSeiAi && cd ~/TenSeiAi
curl -fL -o TenSeiAi.pyz "https://github.com/$REPO/releases/latest/download/TenSeiAi.pyz"
curl -fL -o TenSeiAi.tsei "https://github.com/$REPO/releases/latest/download/TenSeiAi.tsei"
python TenSeiAi.pyz TenSeiAi.tsei
```

To use the browser-based chat, start the local server:

```bash
python TenSeiAi.pyz serve --port 8765
```

Open `http://127.0.0.1:8765` on the phone. Termux does not include a browser;
install one or use `termux-open-url` from the `termux-tools` package.

For a local installation, the repository provides `termux/install.sh`:

```bash
bash termux/install.sh ./TenSeiAi.pyz ./TenSeiAi.tsei
tensei ask "Why do earthquakes happen?"
```

## Native Android project with Chaquopy

The Gradle project under `android/` embeds CPython and numpy through Chaquopy,
then shows the local chat page in a WebView.

### Requirements

- Android Studio with Android SDK 34.
- A released `TenSeiAi.tsei` file.
- Network access for the first Gradle/Chaquopy dependency download.

### Add the model and synchronize the engine

```bash
git clone https://github.com/gaurzamdev/SageCircuit.git
cd SageCircuit
mkdir -p android/app/src/main/assets
cp /path/to/TenSeiAi.tsei android/app/src/main/assets/TenSeiAi.tsei
bash android/sync_engine.sh
```

`sync_engine.sh` transfers `source/tensei/` into the Android app. Set
`TENSEI_MODEL` to select a model stored at another location:

```bash
TENSEI_MODEL=/path/to/TenSeiAi.tsei bash android/sync_engine.sh
```

On Windows PowerShell:

```powershell
.\android\sync_engine.ps1 -Model "C:\path\to\TenSeiAi.tsei"
```

### Compile and launch

Open `android/` in Android Studio and select **Run**. The initial build can
take a few minutes while Gradle fetches the Chaquopy Python runtime and numpy.

For command-line builds, install Gradle 8.x yourself; no wrapper is included.
Run the command from `android/`:

```bash
gradle assembleDebug
```

Gradle writes the APK to `android/app/build/outputs/apk/debug/`.

No prebuilt APK is published from this project. Building locally lets you
choose both the signing key and model version.

### First-start sequence

1. `MainActivity` initializes Chaquopy and launches Python.
2. If not already present, the app places the model in its private files area.
3. `tensei.android.start(home)` starts the engine and hosts the page on
   `127.0.0.1`.
4. The WebView opens the locally served interface.

Startup takes longer the first time because the model must be extracted and
loaded. Later sessions reuse the app's private copy.

## Calling the engine from Kotlin

If an app has its own native interface, it can call the engine directly:

```kotlin
val home = filesDir.absolutePath
val answer = Python.getInstance()
    .getModule("tensei.android")
    .callAttr("ask", home, "What is Big O notation?")
    .toString()
```

To start the local server and receive its address:

```kotlin
val url = Python.getInstance()
    .getModule("tensei.android")
    .callAttr("start", home)
    .toString()
webView.loadUrl(url)
```

## Signing credentials

The repository does not supply a keystore. Create your own key and store it
outside the project. Never commit `.jks` or `.keystore` files or their
passwords.

For a release build, configure Gradle signing with a private keystore using
local properties or environment variables. Refer to Android's `apksigner` and
Gradle signing documentation.

## Known constraints

- Expect a sizable APK and initial extraction; the model is about 80 MB.
- The app displays the same local web page used by the desktop runtime.
- Online research is optional and needs an internet connection.
- numpy is recommended to improve execution speed.
- This repository provides an integration example rather than a Play Store app.
