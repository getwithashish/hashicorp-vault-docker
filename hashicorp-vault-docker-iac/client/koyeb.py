from typing import List
import pulumi
import pulumi_koyeb as koyeb
from client.cloud_provider_base import CloudProvider
from config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    KOYEB_TOKEN,
    VAULT_ADDR,
    VAULT_INIT_JSON,
    hashicorp_vault_config,
    koyeb_config,
)


class KoyebCloudProvider(CloudProvider):
    """
    A cloud provider implementation for deploying services on Koyeb
    using Pulumi.

    This class handles the creation and configuration of a Koyeb service,
    including GitHub source, instance configuration, ports,
    and environment variables.

    Attributes:
        _provider (koyeb.Provider): The Koyeb provider for resource management.
    """

    def __init__(self, provider: koyeb.Provider = None) -> None:
        self._provider = provider
        if self._provider is None:
            self._provider = koyeb.Provider(
                koyeb_config.require("resource_name"), token=KOYEB_TOKEN
            )

    def _create_github_source(self) -> koyeb.ServiceGithubSourceArgs:
        """
        Create GitHub source configuration for the Koyeb service.

        Returns:
            koyeb.ServiceGithubSourceArgs: Configuration for the GitHub
            repository source.
        """

        return koyeb.ServiceGithubSourceArgs(
            repository=hashicorp_vault_config.require("github_repo"),
            branch=hashicorp_vault_config.require("github_repo_branch"),
            dockerfile_path=hashicorp_vault_config.require("dockerfile_path"),
        )

    def _create_instance_config(self) -> koyeb.ServiceInstanceTypesArgs:
        """
        Create instance type configuration for the Koyeb service.

        Returns:
            koyeb.ServiceInstanceTypesArgs: Configuration for the
            service instance including type, CPU, memory,
            and disk specifications.
        """

        return koyeb.ServiceInstanceTypesArgs(
            type=koyeb_config.require("service_type"),
            vCPU=koyeb_config.require_float("service_instance_vcpu"),
            memory=koyeb_config.require_int("service_instance_memory"),
            disk=koyeb_config.require_int("service_instance_disk"),
        )

    def _create_ports(self) -> List[koyeb.ServicePortArgs]:
        """
        Create port configuration for the Koyeb service.

        Returns:
            List[koyeb.ServicePortArgs]: A list containing port and
            protocol configuration.
        """

        port, protocol = koyeb_config.require("service_instance_port").split(",")
        return [koyeb.ServicePortArgs(port=int(port), protocol=protocol)]

    def _create_env_vars(self) -> List[koyeb.ServiceEnvVarArgs]:
        """
        Create environment variables for the Koyeb service.

        Returns:
            List[koyeb.ServiceEnvVarArgs]: A list of environment variables
            including AWS and Vault-related credentials.
        """

        return [
            koyeb.ServiceEnvVarArgs(key="AWS_ACCESS_KEY_ID", value=AWS_ACCESS_KEY_ID),
            koyeb.ServiceEnvVarArgs(
                key="AWS_SECRET_ACCESS_KEY", value=AWS_SECRET_ACCESS_KEY
            ),
            koyeb.ServiceEnvVarArgs(key="VAULT_ADDR", value=VAULT_ADDR),
            koyeb.ServiceEnvVarArgs(key="VAULT_INIT_JSON", value=VAULT_INIT_JSON),
        ]

    def deploy(self):
        """
        Deploy the Koyeb service with the configured settings.

        Creates a Koyeb service using the predefined GitHub source,
        instance configuration, ports, and environment variables.

        Returns:
            koyeb.Service: The deployed Koyeb service instance.
        """

        koyeb_service = koyeb.Service(
            koyeb_config.require("service_name"),
            name=koyeb_config.require("service_name"),
            definition=koyeb.ServiceDefinitionArgs(
                github=self._create_github_source(),
                instance_types=self._create_instance_config(),
                ports=self._create_ports(),
                env=self._create_env_vars(),
            ),
            opts=pulumi.ResourceOptions(provider=self._provider),
        )

        return koyeb_service
