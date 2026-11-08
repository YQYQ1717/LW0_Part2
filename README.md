# Robotics LW0 Part 2

Robotics 2026/2027 — UFACTORY Lite 6

This repository contains the work for **LabWork 0 Part 2: Development Lifecycle and Development Environment**.

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
│   └── lifecycle.txt
├── scripts/
│   ├── check_connection.py
│   ├── lifecycle_check.py
│   ├── test8_read.py
│   ├── test8_move.py
│   └── test8_fk.py
├── tests/
│   └── test_smoke.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 2. Python environment

Python 3.10 or newer is required.

Go to the project directory:

```powershell
cd D:\qt\xuexi\ROBO2\LW0_Part2
```

Create the virtual environment if it does not already exist:

```powershell
python -m venv .venv
```

If PowerShell blocks activation scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

A successful activation shows:

```text
(.venv) PS D:\qt\xuexi\ROBO2\LW0_Part2>
```

Install the required packages:

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

The configuration used with the firmware simulator is:

```yaml
robot_ip: "127.0.0.1"
is_radian: false

# true = firmware simulator at home
# false = real Lite 6
firmware_simulator: true

home:
  - -0.4
  - 29.8
  - 45.3
  - -0.9
  - 51.2
  - 15.3

home_speed: 20

# Course hardware safety limits
joint_speed_limit: 54
tcp_speed_limit: 150

# Real bench boundary was not obtained.
# Do not invent values.
tcp_boundary: null
```

`robot_ip` is `127.0.0.1` when using the local UFACTORY firmware simulator.

The real robot IP must not be hard-coded in Python source files.

`tcp_boundary` is left as `null` because the real bench boundary was not recorded. No boundary value was invented.

For real hardware, a valid TCP boundary must be configured before using the robot.

---

# 4. Intermediate-level validation — B.5

## 4.1 pytest

From the project root:

```powershell
python -m pytest
```

Observed result:

```text
tests\test_smoke.py . [100%]

1 passed in 0.02s
```

Result:

```text
PASS
```

---

## 4.2 Configuration loading

Run:

```powershell
python -m scripts.check_connection
```

Observed output:

```text
SDK_VERSION: 1.18.4
Robot IP: 127.0.0.1
Home: [-0.4, 29.8, 45.3, -0.9, 51.2, 15.3]
Joint speed limit: 54
TCP speed limit: 150
CONFIG OK
```

Result:

```text
PASS
```

---

## 4.3 Check for hard-coded robot IP addresses

Run:

```powershell
Get-ChildItem -Recurse -Filter *.py |
Where-Object { $_.FullName -notmatch '\\.venv\\' } |
Select-String -Pattern '192\.168\.\d+\.\d+'
```

Observed result:

```text
No output
```

Therefore no `192.168.x.x` robot address is hard-coded in the project Python source.

Result:

```text
PASS
```

---

## 4.4 Git history

Run:

```powershell
git log --oneline -3
```

Observed history included:

```text
9ff2d9d Complete LW0 Part 2
26ae5f0 Initial LW0 Part 2 setup
```

The repository contains commits.

Result:

```text
PASS
```

---

## 4.5 Test safe_session()

The firmware simulator must be running first.

Start it as described in Section 14.

Then run:

```powershell
python -c "from lite6.session import safe_session; arm=safe_session(); print('CONNECTED:', arm.connected); arm.disconnect()"
```

Observed successful output:

```text
SDK_VERSION: 1.18.4
ROBOT_IP: 127.0.0.1, VERSION: v2.4.0
Firmware simulator detected.
Reduced-mode controller settings skipped in simulator.
Connected to: 127.0.0.1
CONNECTED: True
```

Result:

```text
PASS
```

The firmware simulator does not reproduce every safety feature of a physical controller. Reduced-mode controller enforcement is therefore not claimed to be physically verified by this simulator test.

---

# 5. Lifecycle exercise

The lifecycle requirements, test results, traceability matrix and V-model are stored in:

```text
docs/lifecycle.md
```

The tests are implemented in:

```text
scripts/lifecycle_check.py
```

Start the firmware simulator before running the lifecycle tests.

Run:

```powershell
python -m scripts.lifecycle_check
```

To run the test and save the output:

```powershell
python -m scripts.lifecycle_check | Tee-Object -FilePath logs\lifecycle.txt
```

Observed results:

```text
T-F1: PASS
T-F2: PASS
T-F3: PASS
T-P1: PASS
T-P2: PASS
T-S1: PASS
T-I1: PASS
T-S2: PASS
```

---

## 5.1 T-F1 — Controller connection

Observed:

```text
connected=True
ip=127.0.0.1
```

Result:

```text
PASS
```

---

## 5.2 T-F2 — safe_session

Observed:

```text
safe_session completed without non-zero SDK return codes
```

Result:

```text
PASS
```

---

## 5.3 T-F3 — Home configuration

Target home:

```text
[-0.4, 29.8, 45.3, -0.9, 51.2, 15.3] deg
```

Measured joint angles:

```text
[-0.399982,
 29.799993,
 45.299991,
 -0.900002,
 51.200024,
 15.299978] deg
```

Result:

```text
PASS
```

---

## 5.4 T-P1 — Home joint-position accuracy

Measured maximum joint error:

```text
0.000024 deg
```

Threshold:

```text
0.5 deg
```

Target:

```text
0.2 deg
```

Result:

```text
PASS
```

---

## 5.5 T-P2 — Home motion time

Measured:

```text
0.361 s
```

Threshold:

```text
15 s
```

Target:

```text
10 s
```

Result:

```text
PASS
```

---

## 5.6 T-S1 — Safety configuration

Configured values:

```text
Joint speed limit = 54 deg/s
TCP speed limit   = 150 mm/s
```

The test was executed against the firmware simulator.

The simulator confirms that the safety limits are present in the configuration, but this does not demonstrate physical enforcement of reduced mode by a real controller.

Result:

```text
PASS
```

---

## 5.7 T-I1 — Configuration interface

No hard-coded `192.168.x.x` robot addresses were found in Python source files.

Result:

```text
PASS
```

---

## 5.8 T-S2 — SDK return-code handling

A synthetic non-zero SDK return code correctly raised `RuntimeError`.

Result:

```text
PASS
```

---

# 6. Advanced ROS 2 / Docker environment

The advanced-level work uses the teaching Docker environment.

The Windows branch used for this work is:

```text
https://github.com/cazevedo/robotica
```

Clone it with:

```powershell
cd D:\qt\xuexi\ROBO2

git clone -b windows https://github.com/cazevedo/robotica.git robotica_env

cd robotica_env
```

Docker Desktop must be installed and running with the WSL2 backend.

If `.env` does not exist:

```powershell
Copy-Item .env.example .env
```

The configuration used during these tests was:

```text
ROS_DOMAIN_ID=0
LAB_GAZEBO=1
```

`ROS_DOMAIN_ID=0` was used during this work with teacher permission.

If PowerShell blocks `lab.ps1`:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Start the teaching container:

```powershell
.\lab.ps1 up
```

Check the environment:

```powershell
.\lab.ps1 doctor
```

Observed successful result:

```text
ROS_DISTRO             jazzy
ROS_DOMAIN_ID          0
RMW                    rmw_fastrtps_cpp
Gazebo switch          ON

ros2                   ok
colcon                 ok
rviz2                  ok
gz                     ok
rosdep                  ok

Gazebo Sim, version 8.15.0

xarm/uf_ packages      10 found
xarm_moveit_config     ok
moveit_ros_move_group  ok
ros_gz_sim             ok
gz_ros2_control        ok

All checks passed.
```

Enter the container:

```powershell
.\lab.ps1 shell
```

---

# 7. Advanced Test 1 — ROS 2 communication

Test 1 requires two container terminals.

## Terminal 1

From Windows PowerShell:

```powershell
cd D:\qt\xuexi\ROBO2\robotica_env

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\lab.ps1 up

.\lab.ps1 shell
```

Inside the container:

```bash
lab test 1
```

Observed output:

```text
Publishing: 'Hello World: 1'
Publishing: 'Hello World: 2'
Publishing: 'Hello World: 3'
...
```

Leave the talker running.

## Terminal 2

Open another Windows PowerShell:

```powershell
cd D:\qt\xuexi\ROBO2\robotica_env

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\lab.ps1 shell
```

Inside the container:

```bash
lab test 1b
```

Observed output:

```text
I heard: [Hello World: 50]
I heard: [Hello World: 51]
I heard: [Hello World: 52]
...
```

Result:

```text
PASS
```

Stop both processes with:

```text
Ctrl+C
```

---

# 8. Advanced Test 2 — UFACTORY packages

Inside the teaching container:

```bash
lab test 2
```

Observed packages included:

```text
uf_ros_lib
xarm_api
xarm_controller
xarm_description
xarm_gazebo
xarm_moveit_config
xarm_moveit_servo
xarm_msgs
xarm_planner
xarm_sdk
```

Observed result:

```text
PASS - 10 packages found
```

Result:

```text
PASS
```

---

# 9. Advanced Test 3 — Lite 6 model in RViz

Inside the teaching container:

```bash
lab test 3
```

The following were verified:

- RViz opened successfully.
- The Lite 6 model was visible.
- The MotionPlanning panel was available.
- MoveIt loaded the `lite6` planning group.

Observed output included:

```text
Ready to take commands for planning group lite6.
```

Result:

```text
PASS
```

---

# 10. Advanced Test 4 — TF kinematic chain

Test 3 was left running.

In another teaching-container terminal:

```bash
lab test 4
```

A `frames_<timestamp>.pdf` file was generated.

The observed TF chain was:

```text
world
└── link_base
    └── link1
        └── link2
            └── link3
                └── link4
                    └── link5
                        └── link6
                            └── link_eef
```

The frames used for the following test were:

```text
link_base
link_eef
```

Result:

```text
PASS
```

---

# 11. Advanced Test 5 — TF transform

The transform used was:

```text
link_base -> link_eef
```

Two poses were recorded.

## 11.1 Pose A

Pose A was the MoveIt home / near-zero configuration.

Joint angles in radians:

```text
[
  5.587522406131035e-06,
  9.945303918793798e-05,
  8.813624298200012e-05,
  3.904474605806171e-05,
  9.364087586291135e-05,
  -3.201136365532878e-06
]
```

Approximate joint angles in degrees:

```text
[
  0.00032014,
  0.00569824,
  0.00504983,
  0.00223710,
  0.00536523,
  -0.00018341
]
```

Translation:

```text
[0.087, 0.000, 0.154] m
```

4×4 matrix:

```text
 1.000  0.000  0.000  0.087
 0.000 -1.000  0.000  0.000
 0.000  0.000 -1.000  0.154
 0.000  0.000  0.000  1.000
```

---

## 11.2 Pose B

Joint angles in radians:

```text
[
  0.09199615655033247,
  0.060157472114878874,
  0.7897077568470088,
  0.04183593100166868,
  0.8946869235263795,
  0.06159451689486377
]
```

Approximate joint angles in degrees:

```text
[
  5.271,
  3.447,
  45.247,
  2.397,
  51.262,
  3.529
]
```

Translation:

```text
[0.217, 0.022, 0.270] m
```

4×4 matrix:

```text
 0.986  0.000 -0.166  0.217
 0.003 -1.000  0.017  0.022
-0.166 -0.018 -0.986  0.270
 0.000  0.000  0.000  1.000
```

Result:

```text
PASS
```

---

# 12. Advanced Test 6 — Gazebo physics

Inside the teaching container:

```bash
lab test 6
```

Gazebo opened the shapes scene.

After pressing Play, the objects responded to gravity and physics.

Observed behaviour included objects rolling, tilting and falling.

Result:

```text
PASS
```

---

# 13. Advanced Test 7 — Lite 6 in Gazebo controlled by MoveIt

Inside the teaching container:

```bash
lab test 7
```

The test starts:

- Gazebo with the Lite 6 robot;
- RViz with MotionPlanning;
- `ros2_control`;
- the Lite 6 trajectory controller.

An initial attempt showed a controller action-server connection failure.

After restarting Test 7, trajectory execution succeeded.

Observed successful messages included:

```text
Received new action goal
Accepted new action goal
lite6_traj_controller started execution
Goal request accepted!
Goal reached, success!
Controller 'lite6_traj_controller' successfully finished
Completed trajectory execution with status SUCCEEDED
Execution completed: SUCCEEDED
Execute request success!
```

Both the RViz robot and the Gazebo robot moved.

Observed difference between Gazebo and RViz:

> In Gazebo, the robot showed physical dynamics such as lag and settling during the motion, whereas RViz displayed the ideal planned trajectory without physical dynamics.

Result:

```text
PASS
```

---

# 14. UFACTORY firmware simulator

The UFACTORY firmware simulator is separate from the ROS/Gazebo teaching container.

## 14.1 First-time installation

Pull the image:

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

Inside the container start the Lite 6 profile:

```bash
/xarm_scripts/xarm_start.sh 6 9
```

---

## 14.2 Starting an existing firmware container

Start the container:

```powershell
docker start uf_software
```

Enter it:

```powershell
docker exec -it uf_software /bin/bash
```

Inside:

```bash
/xarm_scripts/xarm_start.sh 6 9
```

A successful start shows a controller screen similar to:

```text
xarm_controller_screen (Detached)
```

Exit the interactive shell:

```bash
exit
```

Open UFACTORY Studio:

```text
http://127.0.0.1:18333
```

The simulated Lite 6 should be visible.

---

# 15. Advanced Test 8 — Python SDK against firmware simulator

The firmware simulator must be running.

Open a Windows PowerShell:

```powershell
cd D:\qt\xuexi\ROBO2\LW0_Part2

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\.venv\Scripts\Activate.ps1
```

---

## 15.1 Read joint angles and TCP pose

Run:

```powershell
python -m scripts.test8_read
```

Observed output:

```text
SDK_VERSION: 1.18.4

ROBOT_IP: 127.0.0.1
VERSION: v2.4.0
PROTOCOL: V1

Joint angles:
0 [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

TCP pose:
0 [87.0, -0.0, 154.199997, 180.00002, 0.0, -0.0]
```

Result:

```text
PASS
```

---

## 15.2 Home motion

Run:

```powershell
python -m scripts.test8_move
```

Observed result:

```text
Move code: 0
```

Target home:

```text
[-0.4, 29.8, 45.3, -0.9, 51.2, 15.3] deg
```

Measured joint angles:

```text
[-0.399982,
 29.799993,
 45.299991,
 -0.900002,
 51.200024,
 15.299978,
 0.0]
```

Measured TCP pose:

```text
[208.161682,
 -2.206125,
 170.838989,
 168.987255,
 34.178365,
 -18.305314]
```

The simulated Lite 6 moved successfully in UFACTORY Studio.

Result:

```text
PASS
```

---

## 15.3 Forward-kinematics comparison

Run:

```powershell
python -m scripts.test8_fk
```

Pose A joint angles converted to degrees:

```text
[
  0.000320141451806091,
  0.00569823940521803,
  0.005049834745008128,
  0.002237099161286994,
  0.005365226976853281,
  -0.00018341160339088147
]
```

SDK forward-kinematics pose:

```text
[
  87.01085662841797,
  0.0004864000075031072,
  154.1990203857422,
  180.00000500895632,
  0.006013631800480795,
  -0.0017335461174292036
]
```

SDK position:

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

Measured Euclidean position error:

```text
0.19931687561905603 mm
```

Therefore:

```text
0.1993 mm < 1 mm
```

Result:

```text
PASS
```

---

# 16. Reproducibility check

The reproducibility check was performed from clean shells using this README.

The required items were repeated:

```text
B.5
Test 1
Test 3
Test 8
```

Observed final status:

```text
B.5 validation       PASS
Test 1               PASS
Test 3               PASS
Test 8               PASS
```

Therefore:

```text
REPRODUCIBILITY CHECK: PASS
```

---

## 16.1 Reproducibility B.5

From a clean Windows PowerShell:

```powershell
cd D:\qt\xuexi\ROBO2\LW0_Part2

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\.venv\Scripts\Activate.ps1
```

Run:

```powershell
python -m pytest
```

Observed:

```text
1 passed in 0.02s
```

Run:

```powershell
python -m scripts.check_connection
```

Observed:

```text
Robot IP: 127.0.0.1
Home: [-0.4, 29.8, 45.3, -0.9, 51.2, 15.3]
Joint speed limit: 54
TCP speed limit: 150
CONFIG OK
```

Check for hard-coded robot addresses:

```powershell
Get-ChildItem -Recurse -Filter *.py |
Where-Object { $_.FullName -notmatch '\\.venv\\' } |
Select-String -Pattern '192\.168\.\d+\.\d+'
```

Observed:

```text
No output
```

Check Git:

```powershell
git log --oneline -3
```

The repository contained commits.

With the firmware simulator running:

```powershell
python -c "from lite6.session import safe_session; arm=safe_session(); print('CONNECTED:', arm.connected); arm.disconnect()"
```

Observed:

```text
Connected to: 127.0.0.1
CONNECTED: True
```

Result:

```text
PASS
```

---

## 16.2 Reproducibility Test 1

The teaching Docker environment was restarted from a clean shell:

```powershell
cd D:\qt\xuexi\ROBO2\robotica_env

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\lab.ps1 up

.\lab.ps1 doctor
```

Observed:

```text
All checks passed.
```

Terminal 1:

```bash
lab test 1
```

Observed:

```text
Publishing: 'Hello World: 1'
Publishing: 'Hello World: 2'
...
```

Terminal 2:

```bash
lab test 1b
```

Observed:

```text
I heard: [Hello World: 50]
I heard: [Hello World: 51]
I heard: [Hello World: 52]
...
```

Result:

```text
PASS
```

---

## 16.3 Reproducibility Test 3

Inside the teaching container:

```bash
lab test 3
```

RViz opened successfully.

The Lite 6 was visible.

The MotionPlanning panel was available.

Observed output included:

```text
Ready to take commands for planning group lite6.
```

Result:

```text
PASS
```

---

## 16.4 Reproducibility Test 8

The teaching ROS environment was stopped:

```powershell
cd D:\qt\xuexi\ROBO2\robotica_env

.\lab.ps1 down
```

The firmware simulator was started:

```powershell
docker start uf_software

docker exec -it uf_software /bin/bash
```

Inside:

```bash
/xarm_scripts/xarm_start.sh 6 9
```

Test 8 scripts were then repeated from the Python project:

```powershell
cd D:\qt\xuexi\ROBO2\LW0_Part2

.\.venv\Scripts\Activate.ps1

python -m scripts.test8_read

python -m scripts.test8_move

python -m scripts.test8_fk
```

Observed:

```text
Joint angles: code 0
TCP pose: code 0
Move code: 0
FK code: 0
Position error: 0.19931687561905603 mm
```

The FK position error remained below 1 mm.

Result:

```text
PASS
```

---

# 17. Safety notes

The firmware simulator and the physical Lite 6 are not equivalent for every safety function.

The course reduced-mode limits stored in the configuration are:

```text
Joint speed limit: 54 deg/s
TCP speed limit:   150 mm/s
```

For the firmware simulator, physical controller enforcement of reduced mode is not assumed.

For real hardware:

- configure and verify a valid TCP workspace boundary;
- keep reduced mode enabled;
- use the correct TCP payload;
- keep the emergency stop accessible;
- test motion in simulation first;
- do not execute physical-robot motion without teacher authorisation.

The real bench TCP boundary was not recorded, therefore no value was invented.

---

# 18. Stopping the environments

Stop the firmware simulator:

```powershell
docker stop uf_software
```

Stop the teaching ROS environment:

```powershell
cd D:\qt\xuexi\ROBO2\robotica_env

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\lab.ps1 down
```

Check running containers:

```powershell
docker ps
```

If only the table header appears, no containers are running.

---

# 19. Git and Delivery 1

Check the repository:

```powershell
cd D:\qt\xuexi\ROBO2\LW0_Part2

git status
```

Stage the final files:

```powershell
git add .
```

Check again:

```powershell
git status
```

Commit the final LW0 Part 2 version:

```powershell
git commit -m "Finalize LW0 Part 2 reproducibility"
```

Push the main branch:

```powershell
git push origin main
```

The final Delivery 1 version must be tagged:

```text
delivery-1
```

If an older `delivery-1` tag already exists, it must be updated to point to the final validated commit before submission.

The repository submitted for Delivery 1 contains:

```text
requirements.txt
config/robot.yaml
README.md
docs/lifecycle.md
lite6/session.py
logs/lifecycle.txt
scripts/
tests/
```

---

# 20. Final completion status

```text
Python environment                         PASS
requirements.txt                           PASS
config/robot.yaml                          PASS
pytest                                     PASS
safe_session                               PASS
No hard-coded robot IP                     PASS
Git repository                             PASS

Lifecycle functional requirements          PASS
Lifecycle performance requirements         PASS
Lifecycle interface requirement            PASS
Lifecycle safety requirements              PASS
Lifecycle tests                            PASS
Lifecycle traceability matrix              PASS
Lifecycle V-model                          PASS
Lifecycle log                              SAVED

Advanced Test 1                            PASS
Advanced Test 2                            PASS
Advanced Test 3                            PASS
Advanced Test 4                            PASS
Advanced Test 5                            PASS
Advanced Test 6                            PASS
Advanced Test 7                            PASS
Advanced Test 8                            PASS
Test 8 FK comparison                       PASS

Reproducibility B.5                        PASS
Reproducibility Test 1                     PASS
Reproducibility Test 3                     PASS
Reproducibility Test 8                     PASS

Part 2 experimental work                   COMPLETE
```