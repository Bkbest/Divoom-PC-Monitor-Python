#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="divoom-streamer"
RUN_USER="bkbest21"

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$APP_DIR/.venv"

if [[ "$(id -un)" != "$RUN_USER" ]]; then
  echo "Please run this script as user '$RUN_USER' (current: $(id -un))."
  exit 1
fi

# Initialize virtual environment and install tracking dependencies
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install psutil requests

UNIT_PATH="/etc/systemd/system/${SERVICE_NAME}.service"

# Generate the background systemd service unit file
sudo tee "$UNIT_PATH" >/dev/null <<EOF
[Unit]
Description=Raspberry Pi Data Streamer to Divoom TimesGate
After=network.target

[Service]
Type=simple
User=${RUN_USER}
WorkingDirectory=${APP_DIR}
ExecStart=${VENV_DIR}/bin/python stream_to_divoom.py --interval_in_seconds 10 --verbose
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Reload the systemd daemon to recognize the new unit
sudo systemctl daemon-reload

# Enable and boot up the monitoring service
sudo systemctl enable --now "${SERVICE_NAME}.service"
sudo systemctl restart "${SERVICE_NAME}.service"

echo "Deployed. Divoom streaming service is installed and enabled: ${SERVICE_NAME}.service"
echo "Check system telemetry status with: sudo systemctl status ${SERVICE_NAME}.service"
echo "Follow streaming logs: sudo journalctl -u ${SERVICE_NAME}.service -f"
