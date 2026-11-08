# LW0 Part 2 — Lifecycle Exercise

## 1. Requirements

| ID | Type | Requirement | Test |
|---|---|---|---|
| F1 | Functional | The system shall connect to the Lite 6 controller using the IP address stored in `config/robot.yaml`. | T-F1 |
| F2 | Functional | `safe_session()` shall initialise the controller successfully without non-zero SDK return codes. | T-F2 |
| F3 | Functional | The system shall command the Lite 6 to the configured home joint position and read back the resulting joint angles. | T-F3 |
| P1 | Performance | After a home command, the maximum absolute joint-position error shall be below 0.5° (threshold), with a target below 0.2°. | T-P1 |
| P2 | Performance | The home motion shall complete in less than 15 s (threshold), with a target below 10 s. | T-P2 |
| I1 | Interface | Robot addresses shall be obtained from `config/robot.yaml`; no `192.168.x.x` robot address shall be hard-coded in Python source files. | T-I1 |
| S1 | Safety | The configuration shall limit joint speed to 54°/s and TCP speed to 150 mm/s for hardware operation. | T-S1 |
| S2 | Safety | A non-zero SDK return code shall be treated as an error and shall raise a `RuntimeError`. | T-S2 |

## 2. Test Results

The tests were executed against the UFACTORY Lite 6 firmware simulator using `robot_ip: 127.0.0.1`.

| Test | Result | Measured / Observed Value |
|---|---|---|
| T-F1 | PASS | Connection successful; `connected=True`, IP=`127.0.0.1` |
| T-F2 | PASS | `safe_session()` completed without non-zero SDK return codes |
| T-F3 | PASS | Target = `[-0.4, 29.8, 45.3, -0.9, 51.2, 15.3]°`; actual = `[-0.399982, 29.799993, 45.299991, -0.900002, 51.200024, 15.299978]°` |
| T-P1 | PASS | Maximum joint error = `0.000024°`; threshold = `0.5°`; target = `0.2°` |
| T-P2 | PASS | Home motion time = `0.361 s`; threshold = `15 s`; target = `10 s` |
| T-S1 | PASS | Configured joint-speed limit = `54°/s`; TCP-speed limit = `150 mm/s`; firmware simulator enabled |
| T-I1 | PASS | No hard-coded `192.168.x.x` robot addresses found |
| T-S2 | PASS | A synthetic non-zero SDK return code correctly raised `RuntimeError` |

The firmware simulator was detected automatically. Reduced-mode controller settings were not applied to the simulator; therefore T-S1 verifies the configured safety limits rather than physical enforcement by a real robot controller. The real-bench TCP boundary was not recorded and was therefore not invented; `tcp_boundary` remains `null`.

## 3. Traceability Matrix

| Requirement | Module / Configuration | Test | Result |
|---|---|---|---|
| F1 | `lite6/session.py`, `config/robot.yaml` | T-F1 | PASS |
| F2 | `lite6/session.py` | T-F2 | PASS |
| F3 | `scripts/lifecycle_check.py`, `config/robot.yaml` | T-F3 | PASS |
| P1 | `scripts/lifecycle_check.py` | T-P1 | PASS — 0.000024° |
| P2 | `scripts/lifecycle_check.py` | T-P2 | PASS — 0.361 s |
| I1 | `config/robot.yaml`, Python source files | T-I1 | PASS |
| S1 | `config/robot.yaml`, `lite6/session.py` | T-S1 | PASS |
| S2 | `lite6/session.py`, `scripts/lifecycle_check.py` | T-S2 | PASS |

## 4. Course V-Model

```text
                 FINAL CHALLENGE
                /               \
               /                 \
       Requirements             Validation
             /                     \
          LW1                       LW4 tests
     Forward kinematics        Integration tests
           /                         \
        LW2                           LW3 tests
   Inverse kinematics             Verification
         /                             \
      LW3                               LW2 tests
 Jacobian / velocity                  Verification
       /                                 \
    LW4                                  LW1 tests
 Trajectory generation               Unit tests
              \                       /
               \                     /
                 IMPLEMENTATION
              Python modules + Git
```

The left branch represents specification and development through LW1–LW4. The right branch represents the corresponding verification activities. The Final Challenge is the system-level validation at the top of the V.