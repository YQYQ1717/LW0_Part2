# Robotics LW0 Part 2

Robotics 2026/2027 — UFACTORY Lite 6

This repository contains the work for **LabWork 0 Part 2**.

The project uses:

- Python 3.13
- xArm Python SDK
- pytest
- PyYAML
- Docker Desktop with WSL2
- ROS 2 Jazzy
- MoveIt 2
- Gazebo Harmonic
- UFACTORY firmware simulator

---

## 1. Project structure

```text
LW0_Part2/
├── config/
│   └── robot.yaml
├── docs/
│   └── lifecycle.md
├── lite6/
│   ├── __init__.py
│   └── session.py
├── logs/
├── scripts/
│   ├── check_connection.py
│   ├── test8_read.py
│   ├── test8_move.py
│   ├── test8_fk.py
│   └── test_lifecycle.py
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 2. Python environment

Python 3.10 or newer is required.

Create a virtual environment:

```powershell
cd D:\qt\xuexi\ROBO2\LW0_Part2
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, enable scripts for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required Python packages:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Robot configuration

Robot parameters are stored in:

```text
config/robot.yaml
```

For the UFACTORY firmware simulator, the configuration is:

```yaml
robot_ip: "127.0.0.1"
is_radian: false
firmware_simulator: true

home:
  - -0.4
  - 29.8
  - 45.3
  - -0.9
  - 51.2
  - 15.3

home_speed: 20

joint_speed_limit: 54
tcp_speed_limit: 150

tcp_boundary: null
```

`tcp_boundary` is left as `null` for the firmware simulator.

For real hardware, a valid TCP boundary must be configured before `safe_session()` is used.

The real robot IP address must not be hard-coded in Python source files.

---

## 4. Intermediate-level validation — B.5

### 4.1 Run pytest

From the project root:

```powershell
python -m pytest -q
```

Expected result:

```text
1 passed
```

---

### 4.2 Check configuration loading

Run:

```powershell
python -m scripts.check_connection
```

Expected output includes:

```text
Robot IP: 127.0.0.1
Home: [-0.4, 29.8, 45.3, -0.9, 51.2, 15.3]
Joint speed limit: 54
TCP speed limit: 150
CONFIG OK
```

---

### 4.3 Test `safe_session()`

The firmware simulator must be running first.

Run:

```powershell
python -c "from lite6.session import safe_session; arm=safe_session(); print('CONNECTED:', arm.connected); arm.disconnect()"
```

Expected output includes:

```text
Firmware simulator detected.
Reduced-mode controller settings skipped in simulator.
Connected to: 127.0.0.1
CONNECTED: True
```

The firmware simulator does not reproduce all real-controller reduced-mode behaviour, so reduced-mode controller settings are not claimed to be physically enforced by this test.

---

### 4.4 Check for hard-coded robot IP addresses

Run:

```powershell
Get-ChildItem -Recurse -Filter *.py |
Where-Object { $_.FullName -notmatch '\\.venv\\' } |
Select-String -Pattern '192\.168\.\d+\.\d+'
```

Expected result:

```text
No output
```

This verifies that no `192.168.x.x` robot address is hard-coded in the project Python source.

---

### 4.5 Check Git history

Run:

```powershell
git log --oneline -3
```

The repository must contain at least one commit.

---

## 5. Lifecycle validation

The lifecycle requirements, test results, traceability matrix and V-model are stored in:

```text
docs/lifecycle.md
```

Run the lifecycle tests with the firmware simulator running:

```powershell
python -m scripts.test_lifecycle
```

Observed results:

```text
T-F1 PASS
T-F2 PASS
T-F3 PASS
T-P1 PASS
T-P2 PASS
T-S1 PASS
T-I1 PASS
T-S2 PASS
```

Measured Home maximum joint error:

```text
0.000024 deg
```

Measured Home motion time:

```text
0.373 s
```

For T-S1, the firmware simulator verifies the configured limits:

```text
Joint speed limit = 54 deg/s
TCP speed limit   = 150 mm/s
```

This does not demonstrate physical enforcement of reduced mode by the simulator.

---

## 6. ROS 2 / Docker environment

The advanced-level tests use the teaching Docker environment.

The environment used was the Windows branch of:

```text
https://github.com/cazevedo/robotica
```

Example installation:

```powershell
cd D:\qt\xuexi\ROBO2
git clone -b windows https://github.com/cazevedo/robotica.git robotica_env
cd robotica_env
```

Docker Desktop must be installed and running with the WSL2 backend.

Create the environment file if required:

```powershell
Copy-Item .env.example .env
```

The configuration used for this work was:

```text
ROS_DOMAIN_ID=0
LAB_GAZEBO=1
```

If PowerShell blocks `lab.ps1`:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Start/check the environment:

```powershell
.\lab.ps1 doctor
```

A successful setup ends with:

```text
All checks passed.
```

---

## 7. Reproducibility Test 1 — ROS 2 communication

Test 1 requires two terminals.

### Terminal 1

From Windows PowerShell:

```powershell
cd D:\qt\xuexi\ROBO2\robotica_env
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\lab.ps1 shell
```

Inside the container:

```bash
lab test 1
```

Expected output:

```text
Publishing: 'Hello World: 1'
Publishing: 'Hello World: 2'
...
```

Leave this running.

### Terminal 2

Open another PowerShell:

```powershell
cd D:\qt\xuexi\ROBO2\robotica_env
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\lab.ps1 shell
```

Inside the container:

```bash
lab test 1b
```

Expected output:

```text
I heard: [Hello World: 1]
I heard: [Hello World: 2]
...
```

Result:

```text
PASS
```

Stop both processes with `Ctrl+C`.

---

## 8. Reproducibility Test 3 — Lite 6 model in RViz

Enter the teaching container:

```powershell
cd D:\qt\xuexi\ROBO2\robotica_env
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\lab.ps1 shell
```

Inside the container run:

```bash
lab test 3
```

PASS criteria:

- RViz opens.
- The Lite 6 robot model is visible.
- The MotionPlanning panel is available.
- MoveIt loads the `lite6` planning group.

A successful run contains output similar to:

```text
Ready to take commands for planning group lite6.
```

Result:

```text
PASS
```

Stop the test using `Ctrl+C`.

---

## 9. UFACTORY firmware simulator

The firmware simulator is separate from the ROS/Gazebo container.

### 9.1 First-time installation

From Windows PowerShell:

```powershell
docker pull danielwang123321/uf-ubuntu-docker
```

Create the container:

```powershell
docker run -it --name uf_software `
-p 18333:18333 `
-p 502:502 `
-p 503:503 `
-p 504:504 `
-p 30000:30000 `
-p 30001:30001 `
-p 30002:30002 `
-p 30003:30003 `
danielwang123321/uf-ubuntu-docker
```

Inside the firmware container, start the Lite 6 profile:

```bash
/xarm_scripts/xarm_start.sh 6 9
```

Keep this terminal running.

---

### 9.2 Starting an existing firmware container

If `uf_software` has already been created:

```powershell
docker start uf_software
docker exec -it uf_software bash
```

Then inside the container:

```bash
/xarm_scripts/xarm_start.sh 6 9
```

Open UFACTORY Studio in a browser:

```text
http://127.0.0.1:18333
```

The simulated Lite 6 should be visible.

---

## 10. Reproducibility Test 8 — Python SDK vs firmware simulator

Make sure the firmware simulator is running.

Open a new Windows PowerShell:

```powershell
cd D:\qt\xuexi\ROBO2\LW0_Part2
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Read joint angles and TCP pose

Run:

```powershell
python -m scripts.test8_read
```

Observed output:

```text
Joint angles:
[-0.399982, 29.799993, 45.299991, -0.900002, 51.200024, 15.299978, 0.0]

TCP pose:
[208.161682, -2.206125, 170.838989, 168.987255, 34.178365, -18.305314]
```

---

### Execute a motion

Run:

```powershell
python -m scripts.test8_move
```

Observed result:

```text
Move code: 0
```

The simulated robot moves successfully in UFACTORY Studio.

---

### Forward-kinematics comparison

Run:

```powershell
python -m scripts.test8_fk
```

Pose A joint angles:

```text
[0.0003201415,
 0.0056982394,
 0.0050498347,
 0.0022370992,
 0.0053652270,
 -0.0001834116] deg
```

Controller forward-kinematics position:

```text
[87.0108566, 0.0004864, 154.1990204] mm
```

Test 5 tf2 position:

```text
[87.0, 0.0, 154.0] mm
```

Difference:

```text
[0.0108566, 0.0004864, 0.1990204] mm
```

Position error:

```text
0.1993169 mm
```

The error is below 1 mm.

Result:

```text
PASS
```

---

## 11. Reproducibility summary

Starting from a clean shell and following this README, the following checks were repeated successfully:

```text
B.5 validation       PASS
Test 1               PASS
Test 3               PASS
Test 8               PASS
```

The reproducibility check therefore passed.

---

## 12. Safety notes

The firmware simulator and the physical Lite 6 are not equivalent for all safety functions.

The project configuration contains the course reduced-mode limits:

```text
Joint speed limit: 54 deg/s
TCP speed limit:   150 mm/s
```

For the firmware simulator, controller reduced-mode enforcement is not assumed.

For physical hardware:

- verify the TCP workspace boundary before motion;
- keep reduced mode enabled;
- use the correct payload;
- keep the emergency stop accessible;
- test motion in simulation before executing it on the real robot;
- do not use the physical robot without teacher authorisation.

---

## 13. Delivery

Before creating the final Delivery 1 tag:

```powershell
git status
git add .
git commit -m "Complete LW0 Part 2"
```

The final submitted version should be tagged:

```powershell
git tag delivery-1
```

Check the tag:

```powershell
git tag
```

The repository submitted for Delivery 1 must contain:

```text
requirements.txt
config/robot.yaml
README.md
docs/lifecycle.md
lite6/session.py
scripts/
tests/
```