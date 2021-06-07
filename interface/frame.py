import abc
import numpy as np


class FrameInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_color(self) -> np.ndarray:
        raise NotImplemented

    @abc.abstractmethod
    def get_depth(self) -> np.ndarray:
        raise NotImplemented

    @abc.abstractmethod
    def get_colorized_depth(self) -> np.ndarray:
        raise NotImplemented
