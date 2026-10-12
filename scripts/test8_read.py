from lite6.session import load_config
from xarm.wrapper import XArmAPI

config = load_config()

arm = XArmAPI(
    config["robot_ip"],
    is_radian=config["is_radian"],
    check_joint_limit=False
)

code, angles = arm.get_servo_angle()
print("Joint angles:", code, angles)

code, pose = arm.get_position()
print("TCP pose:", code, pose)

arm.disconnect()