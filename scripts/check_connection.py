from lite6.session import load_config

config = load_config()

print("Robot IP:", config["robot_ip"])
print("Home:", config["home"])
print("Joint speed limit:", config["joint_speed_limit"])
print("TCP speed limit:", config["tcp_speed_limit"])

print("CONFIG OK")