import numpy as np
from typing import List, Dict, Optional
import pyrealsense2 as rs
import cv2


from interface.frame import FrameInterface
align_to = rs.stream.color
align = rs.align(align_to)


class RealsenseFrame(FrameInterface):
    def __init__(self, frames: List[rs.frame], streams: List[rs.stream], is_align: bool = False):
        self._frames = frames
        self._streams = streams
        if is_align:
            self._frames = align.process(frames)

    def get_frame_dic(self) -> Optional[Dict[str, rs.frame]]:
        frame_dic = {}
        for stream in self._streams:
            if rs.stream.infrared == stream.stream_type():
                frame = self._frames.get_infrared_frame(stream.stream_index())
                key_ = (stream.stream_type(), stream.stream_index())
            else:
                frame = self._frames.first_or_default(stream.stream_type())
                key_ = stream.stream_type()
            frame_dic[key_] = frame
        if len(frame_dic) == 0:
            return None
        return frame_dic

    def _restructure_frameset(self):
        """
            { <stream.depth: 1>: <pyrealsense2.frame Z16 #58>, <stream.color: 2>: <pyrealsense2.frame BGR8 #46> }
            이런식으로 프레임셋이 나와서
            {
                depth:...
                color:...
            }로 변환
        """
        frames = self.get_frame_dic()
        if frames is None:
            return None
        ret = {}
        for frame in list(frames.values()):
            name = frame.__str__()
            if "BGR8" in name:
                ret["color"] = frame
            elif "Z16" in name:
                ret["depth"] = frame
        return ret

    ###############################################################################################################
    def get_color(self) -> Optional[np.ndarray]:
        frame_set = self._restructure_frameset()
        if frame_set is None:
            return None
        return np.array(frame_set["color"].get_data())

    def get_depth(self) -> Optional[np.ndarray]:
        frame_set = self._restructure_frameset()
        if frame_set is None:
            return None
        depth_data = frame_set["depth"].get_data()
        # np.dstack 할 필요가 있을지도..?
        return np.array(depth_data)

    def get_colorized_depth(self) -> np.ndarray:
        return cv2.applyColorMap(cv2.convertScaleAbs(self.get_depth(), alpha=0.03), cv2.COLORMAP_JET)



