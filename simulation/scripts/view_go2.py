import mujoco
import mujoco.viewer
import os
import cv2
import numpy as np

model_path = os.path.expanduser(
    "~/Documents/robot-dog-stairs/external/mujoco_menagerie/unitree_go2/simple_stairs.xml"
)

model = mujoco.MjModel.from_xml_path(model_path)
data = mujoco.MjData(model)

mujoco.mj_resetDataKeyframe(model, data, 0)
mujoco.mj_forward(model, data)

cam_id = mujoco.mj_name2id(
    model,
    mujoco.mjtObj.mjOBJ_CAMERA,
    "realsense_depth"
)

renderer = mujoco.Renderer(model, height=480, width=640)

# cv2.namedWindow("Camera Controls", cv2.WINDOW_NORMAL)
# cv2.namedWindow("RGB", cv2.WINDOW_NORMAL)
# cv2.namedWindow("Depth", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("Camera Controls", 700, 300)
# cv2.moveWindow("Camera Controls", 50, 50)
# cv2.moveWindow("RGB", 800, 50)
# cv2.moveWindow("Depth", 800, 400)

def nothing(x):
    pass

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        mujoco.mj_step(model, data)
        mujoco.mj_forward(model, data)
        viewer.sync()

        renderer.update_scene(data, camera="realsense_depth")
        rgb = renderer.render()

        renderer.enable_depth_rendering()
        renderer.update_scene(data, camera="realsense_depth")
        depth = renderer.render()
        renderer.disable_depth_rendering()

        depth_vis = np.clip(depth, 0, 5.0)
        depth_norm = (depth_vis / 5.0 * 255).astype(np.uint8)
        depth_color = cv2.applyColorMap(depth_norm, cv2.COLORMAP_JET)

        cv2.imshow("RGB", cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
        # cv2.imshow("Depth", depth_color)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

# Slider values are scaled
# X/Y/Z: value 500 means 0.00, each step = 0.001 m
# cv2.createTrackbar("X", "Camera Controls", 850, 1200, nothing)   # 0.350 m
# cv2.createTrackbar("Y", "Camera Controls", 500, 1000, nothing)   # 0.000 m
# cv2.createTrackbar("Z", "Camera Controls", 620, 1000, nothing)   # 0.120 m

# # Angles: value 180 means 0 degrees
# cv2.createTrackbar("Roll",  "Camera Controls", 180, 360, nothing)
# cv2.createTrackbar("Pitch", "Camera Controls", 140, 360, nothing)  # -40 deg
# cv2.createTrackbar("Yaw",   "Camera Controls", 180, 360, nothing)

# cv2.createTrackbar("FOVY", "Camera Controls", 58, 120, nothing)

# with mujoco.viewer.launch_passive(model, data) as viewer:
#     while viewer.is_running():
#         # Read sliders
#         x = (cv2.getTrackbarPos("X", "Camera Controls") - 500) / 1000.0
#         y = (cv2.getTrackbarPos("Y", "Camera Controls") - 500) / 1000.0
#         z = (cv2.getTrackbarPos("Z", "Camera Controls") - 500) / 1000.0

#         roll_deg  = cv2.getTrackbarPos("Roll", "Camera Controls") - 180
#         pitch_deg = cv2.getTrackbarPos("Pitch", "Camera Controls") - 180
#         yaw_deg   = cv2.getTrackbarPos("Yaw", "Camera Controls") - 180

#         roll = np.deg2rad(roll_deg)
#         pitch = np.deg2rad(pitch_deg)
#         yaw = np.deg2rad(yaw_deg)

#         fovy = cv2.getTrackbarPos("FOVY", "Camera Controls")
#         if fovy < 1:
#             fovy = 1

#         # Update camera position
#         model.cam_pos[cam_id] = [x, y, z]

#         # Update camera rotation
#         quat = np.zeros(4)
#         mujoco.mju_euler2Quat(quat, np.array([roll, pitch, yaw]), "xyz")
#         model.cam_quat[cam_id] = quat

#         # Update FOV
#         model.cam_fovy[cam_id] = fovy

#         mujoco.mj_step(model, data)
#         mujoco.mj_forward(model, data)
#         viewer.sync()

#         # Render RGB
#         renderer.update_scene(data, camera="realsense_depth")
#         rgb = renderer.render()

#         # Render depth
#         renderer.enable_depth_rendering()
#         renderer.update_scene(data, camera="realsense_depth")
#         depth = renderer.render()
#         renderer.disable_depth_rendering()

#         depth_vis = np.clip(depth, 0, 5.0)
#         depth_norm = (depth_vis / 5.0 * 255).astype(np.uint8)
#         depth_color = cv2.applyColorMap(depth_norm, cv2.COLORMAP_JET)

#         cv2.imshow("RGB", cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
#         cv2.imshow("Depth", depth_color)

#         controls_img = np.zeros((120, 500, 3), dtype=np.uint8)
#         cv2.putText(
#             controls_img,
#             f"pos=({x:.3f}, {y:.3f}, {z:.3f}) euler=({roll_deg}, {pitch_deg}, {yaw_deg}) fovy={fovy}",
#             (10, 60),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.5,
#             (255, 255, 255),
#             1,
#         )
#         cv2.imshow("Camera Controls", controls_img)

#         key = cv2.waitKey(1)
#         if key == ord("q"):
#             break

#         print(
#             f"\rpos=({x:.3f}, {y:.3f}, {z:.3f}) "
#             f"euler=({roll_deg}, {pitch_deg}, {yaw_deg}) "
#             f"fovy={fovy}",
#             end=""
#         )

cv2.destroyAllWindows()