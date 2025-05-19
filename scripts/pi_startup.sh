#!/bin/bash
set -euxo pipefail

export PATH="${HOME}/.local/bin:${PATH}"
sleep 10 #wait for network to connect

REPO_URL="https://github.com/fkaduk/raspi_baby_mobile.git"
REPO_DIR="${HOME}/raspi_baby_mobile"
BRANCH="add-startup-script"

if [ ! -f "${HOME}/.local/bin/uv" ]; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

rm -rf "${REPO_DIR}" #sometimes broken repo due to cutting power
git clone -b ${BRANCH} ${REPO_URL}
uv run "${REPO_DIR}/src/raspi_baby_mobile/main.py"
