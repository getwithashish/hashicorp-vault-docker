from client.koyeb import KoyebCloudProvider
from client.cloud_provider_base import CloudProvider


class CloudProviderFactory:
    """
    A factory class for creating cloud provider instances.

    This class provides a centralized mechanism for instantiating
    cloud provider
    objects based on their name. It supports dynamic addition of new
    cloud providers
    through the __cloud_providers class dictionary.

    Attributes:
        __cloud_providers (dict): A private dictionary mapping provider names
                                  to their corresponding cloud
                                  provider classes.
    """

    __cloud_providers = {"koyeb": KoyebCloudProvider}

    @classmethod
    def get_cloud_provider(cls, provider_name: str) -> CloudProvider:
        """
        Retrieve a cloud provider instance based on the given provider name.

        Args:
            provider_name (str): The name of the cloud provider to retrieve.

        Returns:
            CloudProvider: An instance of the specified cloud provider.

        Raises:
            ValueError: If the specified cloud provider is not supported.
        """

        cloud_provider = cls.__cloud_providers.get("provider_name")
        if not cloud_provider:
            raise ValueError(
                f"""Cloud provider '{provider_name}' is not supported.
                Available providers: {list(cls.__cloud_providers.keys())}"""
            )

        return cloud_provider
