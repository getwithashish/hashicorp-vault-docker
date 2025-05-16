FROM hashicorp/vault:latest

RUN apk add curl
RUN apk add jq

COPY vault.hcl /vault/config/vault.hcl
COPY init-unseal.sh /init-unseal.sh

RUN chmod +x /init-unseal.sh

EXPOSE 8200

ENTRYPOINT ["/init-unseal.sh"]
