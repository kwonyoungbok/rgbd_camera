import pyrealsense2 as rs
from typing import Optional
from enum import IntEnum


from .rs2_frame import RealsenseFrame
from interface.device import DeviceInterface, DeviceStatus
from interface.frame import FrameInterface


class Preset(IntEnum):
    Custom = 0
    Default = 1
    Hand = 2
    HighAccuracy = 3
    HighDensity = 4
    MediumDensity = 5


class Realsense2Device(DeviceInterface):
    def __init__(self, device_id: str, config: rs.config):
        assert isinstance(config, type(rs.config()))

        self._device_id: str = device_id
        self._config = config
        self._pipeline = None
        self._pipeline_profile = None

    def _start(self):
        if self._status is DeviceStatus.Enable:
            return
        self._pipeline = rs.pipeline()
        self._config.enable_device(self._device_id)
        self._pipeline_profile = self._pipeline.start(self._config)

    def _set_default_property_of_depth_sensor(self):
        depth_sensor = self._get_depth_sensor()
        depth_sensor.set_option(rs.option.min_distance, 0)
        depth_sensor.set_option(rs.option.visual_preset, Preset.HighAccuracy)

    def _set_default_property_of_color_sensor(self):
        color_sensor = self._get_color_sensor()
        color_sensor.set_option(rs.option.enable_auto_exposure, False)
        color_sensor.set_option(rs.option.enable_auto_white_balance, False)
        color_sensor.set_option(rs.option.exposure, 100)
        color_sensor.set_option(rs.option.gain, 256)
        color_sensor.set_option(rs.option.brightness, 0)
        color_sensor.set_option(rs.option.saturation, 50)
        color_sensor.set_option(rs.option.sharpness, 100)
        color_sensor.set_option(rs.option.white_balance, 4500)

    def _set_default_property_of_sensor(self):
        self._set_default_property_of_depth_sensor()
        self._set_default_property_of_color_sensor()

    def _get_depth_sensor(self) -> rs.sensor:
        if self._pipeline_profile is None:
            raise RuntimeError("depth sensor is none")
        return self._pipeline_profile.get_device().first_depth_sensor()

    def _get_color_sensor(self) -> rs.sensor:
        if self._pipeline_profile is None:
            raise RuntimeError("depth sensor is none")
        return self._pipeline_profile.get_device().first_color_sensor()

    # [ public method area ] ########################################################################
    def get_device_id(self) -> str:
        return self._device_id

    def get_depth_scale(self) -> str:
        depth_sensor = self._get_depth_sensor()
        if depth_sensor is None:
            raise RuntimeError("depth sensor is none")
        return depth_sensor.get_depth_scale()

    def set_enable(self) -> None:
        self._start()
        self._set_default_property_of_sensor()
        self._status = DeviceStatus.Enable

    def get_status(self) -> DeviceStatus:
        return self._status

    def poll_for_frames(self) -> Optional[FrameInterface]:
        if self._pipeline is None:
            raise RuntimeError("pipeline is None")
        frames = self._pipeline.poll_for_frames()  # 여기서도 널 반환함
        streams = self._pipeline_profile.get_streams()
        if frames is None:
            return None
        if frames.size() != len(streams):
            return None
        return RealsenseFrame(frames, streams, True)

    def set_disable(self) -> bool:
        pass

