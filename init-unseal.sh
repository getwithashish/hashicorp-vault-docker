#!/bin/sh
set -e

# Start Vault server in background
vault server -config=/vault/config/vault.hcl > /tmp/vault.log 2>&1 &

export VAULT_ADDR=http://localhost:8200

KEY_THRESHOLD=3

echo "🕒 Waiting for Vault to become healthy..."
MAX_WAIT=300
WAITED=0

until curl -s $VAULT_ADDR/v1/sys/health | grep -q 'initialized'; do
  echo "⌛ Checking Vault health..."
  sleep 2
  WAITED=$((WAITED+2))
  if [ "$WAITED" -ge "$MAX_WAIT" ]; then
    echo "❌ Vault did not become healthy within $MAX_WAIT seconds"
    exit 1
  fi
done

echo "✅ Vault is up!"

# Verify Vault is initialized
IS_INITIALIZED=$(curl -s $VAULT_ADDR/v1/sys/init | jq -r '.initialized')

if [ "$IS_INITIALIZED" != "true" ]; then
  echo "❌ Vault is not initialized. Cannot proceed with unsealing."
  exit 1
fi

# If init.json does not exist, try to create it from env variable
if [ ! -f /vault/keys.json ]; then
  echo "⚠️  /vault/keys.json not found."
  if [ -z "$VAULT_INIT_JSON" ]; then
    echo "❌ Environment variable VAULT_INIT_JSON not set. Cannot unseal Vault."
    exit 1
  fi
  echo "💾 Writing keys.json from environment variable..."
  echo "$VAULT_INIT_JSON" > /vault/keys.json
fi

echo "🔓 Unsealing Vault with $KEY_THRESHOLD key shares..."

for i in $(seq 0 $((KEY_THRESHOLD - 1))); do
  KEY=$(jq -r ".unseal_keys_b64[$i]" /vault/keys.json)
  vault operator unseal "$KEY"
done


echo "✅ Unseal complete."

echo "Cleaning up keys..."
unset VAULT_INIT_JSON

# Keep container alive
tail -f /dev/null
