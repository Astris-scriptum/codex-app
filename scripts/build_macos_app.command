#!/bin/zsh
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
APP_DIR="$REPO_ROOT/dist/Codex Studio.app"
CONTENTS="$APP_DIR/Contents"; MACOS="$CONTENTS/MacOS"
rm -rf "$APP_DIR"; mkdir -p "$MACOS"
cat > "$CONTENTS/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict><key>CFBundleName</key><string>Codex Studio</string><key>CFBundleIdentifier</key><string>com.astris-scriptum.codex-studio</string><key>CFBundleVersion</key><string>0.2.0</string><key>CFBundleShortVersionString</key><string>0.2-alpha</string><key>CFBundlePackageType</key><string>APPL</string></dict></plist>
PLIST
cat > "$MACOS/Codex Studio" <<EOF
#!/bin/zsh
cd "$REPO_ROOT"
exec /usr/bin/python3 -m studio.python_backend.codex_studio_backend.server
EOF
chmod +x "$MACOS/Codex Studio"
echo "Built: $APP_DIR"
