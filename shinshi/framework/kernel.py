from kanata.decorators import injectable

from shinshi.sdk.integration import IntegrationInterface
from shinshi.framework.sdk import KernelInterface


@injectable(KernelInterface)
class Kernel(KernelInterface):
    def __init__(self, integrations: tuple[IntegrationInterface, ...]) -> None:
        print(integrations)
