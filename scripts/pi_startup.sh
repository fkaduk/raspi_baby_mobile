#!/bin/bash
set -euxo pipefail

export PATH="${HOME}/.local/bin:${PATH}"

HOST=8.8.8.8
TRIES=10
REPO_URL="https://github.com/fkaduk/raspi_baby_mobile.git"
REPO_DIR="${HOME}/raspi_baby_mobile"
BRANCH="dev"

for i in $(seq 1 $TRIES); do
  if ping -c1 -W1 "$HOST" &>/dev/null; then
    echo "🌐 Network is up (ping to $HOST succeeded)"
    if [ ! -f "${HOME}/.local/bin/uv" ]; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    fi
    rm -rf "${REPO_DIR}" #cutting power sometimes breaks repo
    git clone -b "$BRANCH" "$REPO_URL" "$REPO_DIR"
    cd ${REPO_DIR}
    uv sync
    break
  fi
  echo "Waiting for network… attempt $i/$TRIES"
  sleep 1
  if [ "$i" -eq "$TRIES" ]; then
    cd ${REPO_DIR}
    echo "❗ Could not reach $HOST after $TRIES tries"
    exit 1
  fi
done
cd $REPO_DIR
uv run "src/raspi_baby_mobile/main.py"
