from abc import ABC, abstractmethod


class CloudProvider(ABC):
    """
    An abstract base class representing a generic cloud provider
    deployment interface.

    This class defines the contract for cloud provider deployment operations,
    ensuring that specific cloud provider implementations must implement
    the required deployment method.

    Subclasses must implement the `deploy()` method to provide
    cloud-specific deployment logic.

    Attributes:
        None

    Methods:
        deploy(): An abstract method to be implemented by subclasses
                  for deploying resources in a specific cloud environment.
    """

    @abstractmethod
    def deploy(self):
        """
        Abstract method to deploy resources in a cloud environment.

        This method must be implemented by subclasses to define
        the specific deployment strategy for a particular cloud provider.
        """
        pass
