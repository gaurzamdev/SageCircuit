# Android app project

This directory contains a Chaquopy project for running SageCircuit's Python
engine on Android and presenting its local chat page in a WebView.

See [`docs/ANDROID.md`](../docs/ANDROID.md) for complete instructions on
preparing the model, building the app, configuring signing, and calling the
engine directly.

To stage the model and engine from the repository root:

```bash
# From the repository root
mkdir -p android/app/src/main/assets
cp /path/to/TenSeiAi.tsei android/app/src/main/assets/TenSeiAi.tsei
bash android/sync_engine.sh
```

Next, open this folder in Android Studio and choose Run. The model file is
excluded from Git; obtain it from a release or create it from source.

If a native Android package is unnecessary, use the simpler Termux workflow:

```bash
pkg install -y python python-numpy
python TenSeiAi.pyz TenSeiAi.tsei
```
