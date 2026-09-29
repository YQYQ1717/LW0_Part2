from pathlib import Path
import yaml
from xarm.wrapper import XArmAPI


def load_config():
    config_path = Path(__file__).parent.parent / "config" / "robot.yaml"

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def safe_session():
    config = load_config()

    arm = XArmAPI(
        config["robot_ip"],
        is_radian=config["is_radian"]
    )

    arm.clean_warn()
    arm.clean_error()

    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(0)

    print("Connected to:", config["robot_ip"])

    return arm