import pulumi

from service import DeployerService
from client.cloud_provider_factory import CloudProviderFactory
from config import global_config


def main():
    """
    Main entry point for deploying HashiCorp Vault service using
    Pulumi infrastructure as code.

    This function orchestrates the deployment process by:
    1. Retrieving the cloud provider configuration
    2. Creating a cloud provider instance using the CloudProviderFactory
    3. Initializing a DeployerService with the selected cloud provider
    4. Deploying the Vault service
    5. Exporting the service URL as a Pulumi output

    The deployment leverages dynamic cloud provider selection and a
    service deployment
    abstraction to create a flexible and reusable infrastructure
    deployment mechanism.

    Exports:
        service_url (str): The URI of the deployed Vault service, available as a Pulumi stack output
    """

    cloud_provider_name = global_config.require("cloud_provider")
    cloud_provider = CloudProviderFactory.get_cloud_provider(
        provider_name=cloud_provider_name
    )

    deployer_service = DeployerService(cloud_provider=cloud_provider)

    vault_service = deployer_service.deploy_service()

    pulumi.export("service_url", vault_service.status.apply(lambda status: status.uri))


main()
