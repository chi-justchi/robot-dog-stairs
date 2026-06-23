from pathlib import Path
import time
import mujoco
import mujoco.viewer
import os
import numpy as np

model_path = os.path.expanduser(
    "~/Documents/robot-dog-stairs/external/mujoco_menagerie/unitree_go2/simple_stairs.xml"
)

model = mujoco.MjModel.from_xml_path(model_path)
data = mujoco.MjData(model)

mujoco.mj_resetDataKeyframe(model, data, 0)

# Home joint positions are after the floating base qpos:
# qpos = [base_pos(3), base_quat(4), 12 joint positions]
target_qpos = model.key_qpos[0][7:].copy()

kp = 40.0
kd = 1.0

print("Target joint positions:")
print(target_qpos)

with mujoco.viewer.launch_passive(model, data) as viewer:
    start = time.time()

    while viewer.is_running():
        # Current 12 joint positions and velocities
        qpos = data.qpos[7:].copy()
        qvel = data.qvel[6:].copy()

        # PD control torque
        torque = kp * (target_qpos - qpos) - kd * qvel

        # Clip torque to actuator limits
        data.ctrl[:] = np.clip(torque, model.actuator_ctrlrange[:, 0], model.actuator_ctrlrange[:, 1])

        mujoco.mj_step(model, data)
        viewer.sync()

        if time.time() - start > 10:
            break