from client.cloud_provider_base import CloudProvider


class DeployerService:
    """
    A service class responsible for deploying cloud services through a
    specified cloud provider.

    This class acts as a wrapper around different cloud provider
    deployment strategies,
    allowing for a unified deployment interface across multiple
    cloud providers.

    Attributes:
        _cloud_provider (CloudProvider): The cloud provider instance used for
        deployment.
    """

    def __init__(self, cloud_provider: CloudProvider) -> None:
        self._cloud_provider = cloud_provider

    def deploy_service(self):
        """
        Deploy a service using the configured cloud provider.

        Returns:
            The result of the deployment process from the cloud provider.
            The exact return type depends on the specific cloud
            provider implementation.
        """

        deployed_service = self._cloud_provider.deploy()

        return deployed_service
