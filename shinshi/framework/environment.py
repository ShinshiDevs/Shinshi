import os

from kanata.decorators import injectable

from shinshi.framework.sdk.ienvironment import IEnvironment


@injectable(IEnvironment)
class Environment:
    ROOT_PATH: str = os.getcwd()

    @property
    def root_path(self) -> str:
        return self.ROOT_PATH
