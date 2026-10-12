from pathlib import Path

import yaml
from xarm.wrapper import XArmAPI


def load_config():
    config_path = Path(__file__).parent.parent / "config" / "robot.yaml"

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_code(code, name):
    """Raise immediately when an SDK call returns a non-zero code."""
    if code != 0:
        raise RuntimeError(f"{name} failed, code={code}")


def safe_session():
    config = load_config()

    is_sim = config.get("firmware_simulator", False)

    arm = XArmAPI(
        config["robot_ip"],
        is_radian=config["is_radian"],
        # Firmware simulator may not provide a valid SN,
        # which breaks SDK-side joint-limit parsing.
        check_joint_limit=not is_sim,
    )

    try:
        # Standard activation sequence
        check_code(arm.clean_warn(), "clean_warn")
        check_code(arm.clean_error(), "clean_error")
        check_code(arm.motion_enable(enable=True), "motion_enable")
        check_code(arm.set_mode(0), "set_mode")
        check_code(arm.set_state(0), "set_state")

        if is_sim:
            # The v2.4.0 firmware simulator has incomplete SN / reduced-mode
            # behaviour, so hardware safety settings are not written here.
            print("Firmware simulator detected.")
            print("Reduced-mode controller settings skipped in simulator.")

        else:
            # Real hardware only
            check_code(
                arm.set_reduced_max_joint_speed(
                    config["joint_speed_limit"]
                ),
                "set_reduced_max_joint_speed",
            )

            check_code(
                arm.set_reduced_max_tcp_speed(
                    config["tcp_speed_limit"]
                ),
                "set_reduced_max_tcp_speed",
            )

            boundary = config.get("tcp_boundary")

            if boundary is None:
                raise RuntimeError(
                    "Real hardware requires a configured tcp_boundary"
                )

            if len(boundary) != 6:
                raise ValueError(
                    "tcp_boundary must contain "
                    "[x_max, x_min, y_max, y_min, z_max, z_min]"
                )

            check_code(
                arm.set_reduced_tcp_boundary(boundary),
                "set_reduced_tcp_boundary",
            )

            check_code(
                arm.set_reduced_mode(True),
                "set_reduced_mode",
            )

        print("Connected to:", config["robot_ip"])
        return arm

    except Exception:
        arm.disconnect()
        raise


def go_home(arm):
    config = load_config()

    code = arm.set_servo_angle(
        angle=config["home"],
        speed=config["home_speed"],
        wait=True,
    )

    check_code(code, "go_home")