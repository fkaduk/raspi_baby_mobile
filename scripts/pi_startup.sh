#!/bin/bash
set -euxo pipefail

export PATH="${HOME}/.local/bin:${PATH}"
sleep 10 #wait for network to connect

REPO_URL="https://github.com/fkaduk/raspi_baby_mobile.git"
REPO_DIR="${HOME}/raspi_baby_mobile"
BRANCH="main"

if [ ! -f "${HOME}/.local/bin/uv" ]; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

rm -rf "${REPO_DIR}" #cutting power sometimes breaks repo
git clone -b ${BRANCH} ${REPO_URL}
cd ${REPO_DIR}
uv sync
uv run "/src/raspi_baby_mobile/main.py"
