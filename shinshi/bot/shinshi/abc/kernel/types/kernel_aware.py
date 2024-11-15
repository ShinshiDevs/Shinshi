from typing import Protocol, runtime_checkable

from shinshi.abc.kernel.ikernel import IKernel


@runtime_checkable
class KernelAware(Protocol):
    _kernel: IKernel | None = None

    @classmethod
    def set_kernel(cls, kernel: IKernel) -> None:
        cls._kernel = kernel

    @property
    def kernel(self) -> IKernel:
        assert self._kernel is not None
        return self._kernel
