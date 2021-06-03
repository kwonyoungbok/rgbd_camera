import abc
from enum import Enum
from typing import Optional


from .frame import FrameInterface


class DeviceStatus(Enum):
    Init = 0
    Enable = 1
    Disable = 2


class DeviceInterface(metaclass=abc.ABCMeta):
    _status:DeviceStatus = DeviceStatus.Disable

    @abc.abstractmethod
    def get_device_id(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def set_enable(self) -> bool:
        raise NotImplemented

    @abc.abstractmethod
    def set_disable(self) -> bool:
        raise NotImplemented

    @abc.abstractmethod
    def get_status(self) -> DeviceStatus:
        raise NotImplemented

    @abc.abstractmethod
    def poll_for_frames(self) -> Optional[FrameInterface]:
        raise NotImplemented

    @abc.abstractmethod
    def get_depth_scale(self) -> str: # 어떤값 반환하는지 확인 해야한다.
        raise NotImplemented

