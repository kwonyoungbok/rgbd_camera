import abc
from typing import List, Dict
from enum import Enum


from .device import DeviceInterface
from .frame import FrameInterface


class DeviceContextStatus(Enum):
    Enable = 1
    Disable = 2


class DeviceContextInterface(metaclass=abc.ABCMeta):
    _status: DeviceContextStatus = DeviceContextStatus.Disable
    _enabled_devices_dic: Dict[str, DeviceInterface] = {}

    # @abc.abstractmethod
    # def _create_all_devices(self) -> List[DeviceInterface]:
    #     raise NotImplemented

    @abc.abstractmethod
    def enable_all_devices(self) -> bool:
        raise NotImplemented

    @abc.abstractmethod
    def disable_all_device(self) -> bool:
        raise NotImplemented

    @abc.abstractmethod
    def capture_all_device(self) -> List[FrameInterface]:
        raise NotImplemented

    @abc.abstractmethod
    def get_connected_device_id_list(self) -> List[str]:
        raise NotImplemented


