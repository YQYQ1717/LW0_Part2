from lite6.session import load_config
from xarm.wrapper import XArmAPI
import math

config = load_config()

arm = XArmAPI(
    config["robot_ip"],
    is_radian=config["is_radian"],
    baud_checkset=False,
    check_joint_limit=False
)

# Test 5 Pose A，原来是 rad
pose_a_rad = [
    5.587522406131035e-06,
    9.945303918793798e-05,
    8.813624298200012e-05,
    3.904474605806171e-05,
    9.364087586291135e-05,
    -3.201136365532878e-06
]

# SDK 现在使用 degrees
pose_a_deg = [math.degrees(x) for x in pose_a_rad]

code, fk_pose = arm.get_forward_kinematics(pose_a_deg)

print("FK code:", code)
print("Pose A angles (deg):", pose_a_deg)
print("FK pose:", fk_pose)

# Test 5 tf2 的 Pose A，单位从 m 转成 mm
tf2_xyz_mm = [87.0, 0.0, 154.0]

dx = fk_pose[0] - tf2_xyz_mm[0]
dy = fk_pose[1] - tf2_xyz_mm[1]
dz = fk_pose[2] - tf2_xyz_mm[2]

error = math.sqrt(dx**2 + dy**2 + dz**2)

print("TF2 xyz (mm):", tf2_xyz_mm)
print("Difference xyz (mm):", [dx, dy, dz])
print("Position error (mm):", error)

arm.disconnect()