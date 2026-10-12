from lite6.session import load_config
from xarm.wrapper import XArmAPI

config = load_config()

arm = XArmAPI(
    config["robot_ip"],
    is_radian=config["is_radian"],
    baud_checkset=False,
    check_joint_limit=False
)

arm.clean_warn()
arm.clean_error()
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(0)

code = arm.set_servo_angle(
    angle=config["home"],
    speed=20,
    wait=True
)

print("Move code:", code)

code, angles = arm.get_servo_angle()
print("Joint angles:", code, angles)

code, pose = arm.get_position()
print("TCP pose:", code, pose)

arm.disconnect()