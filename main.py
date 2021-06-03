import pyrealsense2 as rs
import cv2


from realsense2.rs2_device_context import Realsense2DeviceContext

if __name__ == '__main__':
    c = rs.config()
    c.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)
    c.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 15)

    rs2_ctx = Realsense2DeviceContext(rs.context(), c)
    rs2_ctx.enable_all_devices()
    result = rs2_ctx.capture_all_device()
    print(result[0].get_color().shape)
    cv2.namedWindow('displaymywindows', cv2.WINDOW_NORMAL)
    cv2.imshow("displaymywindows", result[0].get_color())
    cv2.waitKey(3000)
    cv2.destroyAllWindows()

