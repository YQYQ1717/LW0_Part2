# LW0 Part 2 — Lifecycle Exercise

## 1. Requirements

| ID | Type | Requirement | Test ID |
|---|---|---|---|
| FR1 | Functional | `safe_session()` shall connect successfully to the controller configured in `config/robot.yaml`. | T-F1 |
| FR2 | Functional | `safe_session()` shall clear warnings/errors, enable motion, set position mode, and set the controller to the ready state. | T-F2 |
| FR3 | Functional | The home behaviour shall command the Lite 6 to the configured home joint vector. | T-F3 |
| PR1 | Performance | The absolute error of every joint after reaching Home shall be no greater than 0.5° (threshold), with a target of no greater than 0.2°. | T-P1 |
| PR2 | Performance | The Home motion shall complete within 15 s (threshold), with a target of 10 s. | T-P2 |
| IR1 | Interface | Robot connection parameters shall be loaded from `config/robot.yaml`; robot IP addresses shall not be hard-coded in Python source files. | T-I1 |
| SR1 | Safety | Hardware sessions shall use reduced-mode limits of no more than 54°/s joint speed and 150 mm/s TCP speed. | T-S1 |
| SR2 | Safety | Every motion command shall check its SDK return code and report a non-zero result as a failure. | T-S2 |

## 2. Test Results

| Test ID | Requirement | Environment | Expected | Measured | Result |
|---|---|---|---|---|---|
| T-F1 | FR1 | Firmware simulator | Successful connection | `connected=True`, IP=`127.0.0.1` | PASS |
| T-F2 | FR2 | Firmware simulator | Session initialisation completes with all SDK return codes equal to 0 | `safe_session()` completed successfully | PASS |
| T-F3 | FR3 | Firmware simulator | Robot reaches configured Home joint vector | Target `[-0.4, 29.8, 45.3, -0.9, 51.2, 15.3]`; measured `[-0.399982, 29.799993, 45.299991, -0.900002, 51.200024, 15.299978]` | PASS |
| T-P1 | PR1 | Firmware simulator | Maximum absolute joint error ≤ 0.5°; target ≤ 0.2° | Maximum joint error = `0.000024°` | PASS |
| T-P2 | PR2 | Firmware simulator | Home motion time ≤ 15 s; target ≤ 10 s | Measured time = `0.373 s` | PASS |
| T-I1 | IR1 | Source inspection | No hard-coded `192.168.x.x` robot address in Python source | No hard-coded `192.168.x.x` addresses found | PASS |
| T-S1 | SR1 | Configuration inspection / firmware simulator | Joint speed ≤ 54°/s and TCP speed ≤ 150 mm/s | Configured joint limit = `54°/s`; TCP limit = `150 mm/s` | PASS |
| T-S2 | SR2 | Source/test inspection | Non-zero SDK return code causes failure handling | Synthetic non-zero SDK code raised `RuntimeError` | PASS |

### Notes

The firmware simulator was running firmware v2.4.0 and the local xArm Python SDK was v1.18.4.

The firmware simulator does not reliably reproduce the real controller's reduced-mode behaviour. Therefore, T-S1 verifies the configured safety limits rather than claiming that the simulator physically enforces them.

The Home timing test was executed from a different starting joint configuration before returning to the configured Home pose.

## 3. Traceability Matrix

| Requirement | Module / Configuration | Test | Result |
|---|---|---|---|
| FR1 | `lite6/session.py`, `config/robot.yaml` | T-F1 | PASS |
| FR2 | `lite6/session.py` | T-F2 | PASS |
| FR3 | `lite6/session.py::go_home()` | T-F3 | PASS |
| PR1 | `lite6/session.py::go_home()` | T-P1 | PASS |
| PR2 | `lite6/session.py::go_home()` | T-P2 | PASS |
| IR1 | `config/robot.yaml`, Python source tree | T-I1 | PASS |
| SR1 | `config/robot.yaml`, `lite6/session.py` | T-S1 | PASS |
| SR2 | `lite6/session.py::check_code()` | T-S2 | PASS |

## 4. V-Model

```text
                  Final Challenge
                 /               \
        System requirements     System validation
              /                     \
     Architecture / interfaces   Integration verification
            /                         \
          LW1 -------------------- LW1 tests
           \                         /
            LW2 ---------------- LW2 tests
             \                   /
              LW3 ------------ LW3 tests
               \               /
                LW4 -------- LW4 tests
                   \         /
                  Implementation