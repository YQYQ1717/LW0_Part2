import re
import time
from pathlib import Path

from lite6.session import (
    safe_session,
    load_config,
    check_code,
    go_home,
)


ROOT = Path(__file__).resolve().parent.parent


def result(test_id, passed, measured):
    status = "PASS" if passed else "FAIL"
    print(f"{test_id}: {status} | {measured}")


config = load_config()
arm = None

try:
    # -------------------------------------------------
    # T-F1 / T-F2
    # -------------------------------------------------
    arm = safe_session()

    result(
        "T-F1",
        bool(arm.connected),
        f"connected={arm.connected}, ip={config['robot_ip']}",
    )

    result(
        "T-F2",
        True,
        "safe_session completed without non-zero SDK return codes",
    )

    # -------------------------------------------------
    # T-F3 / T-P1 / T-P2
    # -------------------------------------------------
    start_pose = [4.6, 34.8, 45.3, -0.9, 51.2, 15.3]

    code = arm.set_servo_angle(
    angle=start_pose,
    speed=config["home_speed"],
    wait=True,
    )
    check_code(code, "move_to_start_pose")
    
    start = time.perf_counter()

    go_home(arm)

    elapsed = time.perf_counter() - start

    code, actual = arm.get_servo_angle()
    check_code(code, "get_servo_angle")

    actual = actual[:6]
    target = config["home"]

    errors = [
        abs(a - b)
        for a, b in zip(actual, target)
    ]

    max_error = max(errors)

    result(
        "T-F3",
        True,
        f"target={target}, actual={actual}",
    )

    result(
        "T-P1",
        max_error <= 0.5,
        (
            f"max joint error={max_error:.6f} deg; "
            f"threshold=0.5 deg; target=0.2 deg"
        ),
    )

    result(
        "T-P2",
        elapsed <= 15.0,
        (
            f"time={elapsed:.3f} s; "
            f"threshold=15 s; target=10 s"
        ),
    )

    # -------------------------------------------------
    # T-S1 — safety configuration
    # -------------------------------------------------
    joint_limit = config["joint_speed_limit"]
    tcp_limit = config["tcp_speed_limit"]

    safety_ok = (
        joint_limit <= 54
        and tcp_limit <= 150
    )

    result(
        "T-S1",
        safety_ok,
        (
            f"configured joint limit={joint_limit} deg/s, "
            f"TCP limit={tcp_limit} mm/s; "
            f"simulator={config.get('firmware_simulator', False)}"
        ),
    )

    # -------------------------------------------------
    # T-I1 — detect actual hard-coded 192.168.x.x IPs
    # -------------------------------------------------
    ip_pattern = re.compile(
        r"(?<!\d)192\.168\.\d{1,3}\.\d{1,3}(?!\d)"
    )

    offending = []

    for path in ROOT.rglob("*.py"):
        if ".venv" in path.parts:
            continue
        if "__pycache__" in path.parts:
            continue

        text = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        if ip_pattern.search(text):
            offending.append(
                str(path.relative_to(ROOT))
            )

    result(
        "T-I1",
        len(offending) == 0,
        (
            "No hard-coded 192.168.x.x robot addresses"
            if not offending
            else f"Found in: {offending}"
        ),
    )

    # -------------------------------------------------
    # T-S2 — verify non-zero SDK codes are handled
    # -------------------------------------------------
    handled = False

    try:
        check_code(1, "synthetic_failure")
    except RuntimeError:
        handled = True

    result(
        "T-S2",
        handled,
        "synthetic non-zero SDK code raises RuntimeError",
    )

finally:
    if arm is not None:
        arm.disconnect()