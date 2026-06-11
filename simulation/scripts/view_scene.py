from pathlib import Path
import mujoco
import mujoco.viewer

scene_path = Path("simulation/scenes/simple_stairs.xml")

model = mujoco.MjModel.from_xml_path(str(scene_path))
data = mujoco.MjData(model)

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()