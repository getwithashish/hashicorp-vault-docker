# Vault-on-S3

[![Docker](https://img.shields.io/badge/Docker-ready-blue)](https://www.docker.com/)
[![Vault](https://img.shields.io/badge/HashiCorp-Vault-000000?logo=vault)](https://www.vaultproject.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Deploy **HashiCorp Vault** backed by **Amazon S3** (or any S3-compatible endpoint) with minimal setup and secure defaults.

## Features

* 🐳 Docker-based deployment using official Vault image
* 🔐 S3 as storage backend (with custom endpoint support)
* 🛡️ Secure unseal via entrypoint script (no keys in logs)
* 📜 Init script to safely generate unseal keys

## Usage

1. Setup Environment variables:

   ```bash
   export VAULT_INIT_JSON=<the keys in json format>
   <!-- It should follow this structure:
    {
        "unseal_keys_b64": [
            "unseal_key_1",
            "unseal_key_2",
            "unseal_key_3"
        ]
    }
    -->

   export AWS_ACCESS_KEY_ID=<access key for S3>
   export AWS_SECRET_ACCESS_KEY=<secret key for S3>
   export VAULT_ADDR=<vault server address. Eg: http://localhost:8200>
   <!-- If you are using TLS, use "https" -->
   ```

2. **Run** Initialization Script (Optional)
    
    If you want to initialize the server and get the unseal keys.
    ```bash
    ./initialize_server_run_local.sh
    <!-- Runs the vault server container locally itself, generates the unseal keys, saves it to keys.json, removes the container, and exits -->
    <!-- Recommended to run this locally and keep the keys safe -->
    ```

3. **Configure** `vault.hcl` with your S3 backend
    ```hcl
    storage "s3" {
    bucket             = <add bucket name>
    region             = <add region>
    endpoint           = <add s3 endpoint here, remove if using amazon s3>
    s3_force_path_style = true
    }

    listener "tcp" {
    address       = "0.0.0.0:8200"
    tls_disable   = <true or false>
    <!-- Configure and add tls certs, if tls_disable is set to false -->
    }

    disable_mlock = <true or false>
    <!-- If mlock is set to true, make sure that you specify --cap-add=IPC lock when running docker -->
    api_addr = "http://localhost:8200"
    ui = true

    ```

4. **Build** Vault image:

   ```bash
   docker build -t vault-image .
   ```

5. **Run** Vault container:

   ```bash
   docker run --name vault-container -p 8200:8200 -e VAULT_INIT_JSON="$VAULT_INIT_JSON" -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" -e VAULT_ADDR="$VAULT_ADDR" vault-image
   <!-- Instead of specifying each environment variable, you can also pass in a .env file -->
   ```

## Notes

* Unsealing is handled automatically in the container via `init-unseal.sh`
* Designed to avoid logging or exposing unseal keys
* Can run locally for testing using Docker
* Recommended to use a reverse proxy in front of the vault

---
