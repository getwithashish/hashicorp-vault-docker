import os
import pulumi


global_config = pulumi.Config()
hashicorp_vault_config = pulumi.Config("hashicorp_vault")
koyeb_config = pulumi.Config("koyeb")

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
VAULT_ADDR = os.environ.get("VAULT_ADDR", "http://0.0.0.0:8200")
VAULT_INIT_JSON = os.environ.get("VAULT_INIT_JSON")

KOYEB_TOKEN = os.environ.get("KOYEB_TOKEN")
