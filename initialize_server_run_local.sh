#!/bin/bash

set -e

CONTAINER_NAME=vault-container
VAULT_IMAGE=hashicorp/vault:latest
HOST_DIR=$(pwd)
VAULT_CONFIG_FILE="$HOST_DIR/vault.hcl"
INIT_OUTPUT_FILE="$HOST_DIR/keys.json"

VAULT_ADDR="http://127.0.0.1:8200"

MAX_RETRIES=30

echo "Waiting for Vault to become ready..."
RETRY=0
while [ $RETRY -lt $MAX_RETRIES ]; do
  STATUS=$(curl -s $VAULT_ADDR/v1/sys/health || true)
  if echo "$STATUS" | grep -q '"initialized":true'; then
    echo "❌ Vault is already initialized. Exiting..."
    docker stop "$CONTAINER_NAME"
    exit 1
  elif echo "$STATUS" | grep -q '"initialized":false'; then
    echo "✅ Vault is uninitialized. Proceeding..."
    break
  fi
  echo "⏳ Vault not ready yet... retry $((RETRY + 1))/$MAX_RETRIES"
  sleep 2
  RETRY=$((RETRY + 1))
done

if [ $RETRY -eq $MAX_RETRIES ]; then
  echo "❌ Vault did not become ready within expected time."
  docker stop "$CONTAINER_NAME"
  exit 1
fi

echo "Vault is reachable and not initialized"

docker exec $CONTAINER_NAME vault operator init -key-shares=5 -key-threshold=3 -format=json > "$INIT_OUTPUT_FILE"
echo "Vault initialized. Keys written to $INIT_OUTPUT_FILE"

docker stop $CONTAINER_NAME > /dev/null
docker rm $CONTAINER_NAME > /dev/null
echo "Vault container stopped and removed"
