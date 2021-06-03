from typing import List, Dict
import pyrealsense2 as rs

from interface.device_context import DeviceContextInterface, DeviceContextStatus
from interface.frame import FrameInterface
from interface.device import DeviceInterface
from .rs2_device import Realsense2Device


class Realsense2DeviceContext(DeviceContextInterface):
    def __init__(self, context: rs.context, pipeline_configuration: rs.config) -> None:
        assert isinstance(context, type(rs.context()))
        assert isinstance(pipeline_configuration, type(rs.config()))
        self._context: rs.context = context
        self._enabled_devices_dic: Dict[str, DeviceInterface] = {}
        self._config = pipeline_configuration

    def get_connected_device_id_list(self) -> List[str]:
        if self._context is None:
            raise RuntimeError("RS2 context is None")
        ret = []
        for d in self._context.devices:
            if d.get_info(rs.camera_info.name).lower() != 'platform camera':
                ret.append(d.get_info(rs.camera_info.serial_number))
        return ret

    def _create_all_devices(self) -> Dict[str, DeviceInterface]:
        connected_id_list: List[str] = self.get_connected_device_id_list()
        print("디버깅용으로 연결된 장치 리스트: ", connected_id_list)
        ret: Dict[str, DeviceInterface] = {}
        for connected_device_id in connected_id_list:
            ret[connected_device_id] = Realsense2Device(connected_device_id, self._config)
        return ret

    def enable_all_devices(self) -> bool:
        if self._status is DeviceContextStatus.Enable:
            return True
        self._enabled_devices_dic = self._create_all_devices()
        for device in self._enabled_devices_dic.values():
            device.set_enable() # 초기화 실패 하면 어떻게 해야하나?
        self._status = DeviceContextStatus.Enable
        return True

    def capture_all_device(self) -> List[FrameInterface]:
        if self._status is DeviceContextStatus.Disable:
            raise RuntimeError("DeviceContextStatus is Disable")
        enabled_devices_length = len(self._enabled_devices_dic)
        if enabled_devices_length == 0:
            raise RuntimeError("enabled_devices is zero")
        device_frames = []
        while len(device_frames) < enabled_devices_length:
            for (_, device) in self._enabled_devices_dic.items():
                frame = device.poll_for_frames()
                if frame is None:
                    continue
                device_frames.append(frame)
        return device_frames

    def disable_all_device(self) -> bool:
        pass
