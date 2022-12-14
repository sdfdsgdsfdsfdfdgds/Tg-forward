from abc import abstractmethod
from typing import Protocol, Tuple

from ..hints import EventMessage


class MessageFilter(Protocol):

    @abstractmethod
    async def process(self, message: EventMessage) -> Tuple[bool, EventMessage]:
        """Apply filter to **message**

        Args:
            message (`EventMessage`): Source message

        Returns:
            Tuple[bool, EventMessage]: 
                Indicates that the filtered message should be forwarded

                Processed message
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.__class__.__name__


class CompositeMessageFilter(MessageFilter):
    """Composite message filter that sequentially applies the filters

    Args:
        *arg (`MessageFilter`):
            Message filters 
    """

    def __init__(self, *arg: MessageFilter) -> None:
        self._filters = list(arg)

    async def process(self, message: EventMessage) -> Tuple[bool, EventMessage]:
        for f in self._filters:
            cont, message = await f.process(message)
            if cont is False:
                return False, message
        return True, message

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: {self._filters}'