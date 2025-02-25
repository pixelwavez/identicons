from abc import ABC, abstractmethod
from typing import Any

# 20x20 grid
class Bendy(ABC):
  @abstractmethod
  def bendit(name: str) -> Any:
    pass