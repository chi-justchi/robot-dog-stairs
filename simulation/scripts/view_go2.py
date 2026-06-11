import mujoco
import mujoco.viewer
import os

# Load from anywhere by setting the path explicitly
model_path = os.path.expanduser(
    "~/Documents/robot-dog-stairs/external/mujoco_menagerie/unitree_go2/simple_stairs.xml"
)

model = mujoco.MjModel.from_xml_path(model_path)
data = mujoco.MjData(model)

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()