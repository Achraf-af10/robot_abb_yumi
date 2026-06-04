import time
import threading
import numpy as np
from abb_robot_client.rws import RWS

# Connexion au contrôleur
robot = RWS("http://10.2.30.126")
lock = threading.Lock() # Sécurise les accès réseau

# --- Mouvement Articulaire ---
def move_joint(side, pos_list):
    joints = [float(d) for d in pos_list[:6]]
    j7 = float(pos_list[6])
    task = "T_ROB_L" if side == "L" else "T_ROB_R"
    module = "PythonCtrl" if side == "L" else "PythonCtrlR"
    var_t = "jTarget" if side == "L" else "jTargetR"
    var_c = "cmd" if side == "L" else "cmdR"

    target_data = [
        [float(np.deg2rad(d)) for d in joints],
        [float(np.deg2rad(j7)), 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]
    ]

    with lock:
        robot.poll_rmmp()
        robot.set_rapid_variable_jointtarget(f"{module}/{var_t}", target_data, task=task)
        robot.set_rapid_variable(f"{module}/{var_c}", "1", task)
    print(f"MoveAbsJ {side} lancé")

# --- Mouvement Linéaire (XYZ + Quaternion) ---
def move_linear_to(side, data):
    x, y, z = data[0], data[1], data[2]
    q1, q2, q3, q4 = data[3], data[4], data[5], data[6]
    cf = [int(data[7]), int(data[8]), int(data[9]), int(data[10])] if len(data) > 7 else [0, 0, 0, 0]

    task = "T_ROB_L" if side == "L" else "T_ROB_R"
    module = "PythonCtrl" if side == "L" else "PythonCtrlR"
    var_t = "pTargetL1" if side == "L" else "pTargetR1"
    var_c = "cmdLinL" if side == "L" else "cmdLinR"

    mech = "ROB_L" if side == "L" else "ROB_R"
    j7 = float(robot.get_jointtarget(mechunit=mech).extax[0])

    val = (f"[[{x:.3f},{y:.3f},{z:.3f}],"
           f"[{q1:.6f},{q2:.6f},{q3:.6f},{q4:.6f}],"
           f"[{cf[0]},{cf[1]},{cf[2]},{cf[3]}],"
           f"[{j7:.3f},9E+09,9E+09,9E+09,9E+09,9E+09]]")

    with lock:
        robot.poll_rmmp()
        robot.set_rapid_variable(f"{module}/{var_t}", val, task=task)
        robot.set_rapid_variable(f"{module}/{var_c}", "1", task)
    print(f"MoveL {side} lancé vers {x}, {y}, {z}")

# --- Mouvement Relatif (RelTool) ---
def move_relative(side, dx, dy, dz):
    task = "T_ROB_L" if side == "L" else "T_ROB_R"
    prefix = "PythonCtrl" if side == "L" else "PythonCtrlR"
    suffix = "" if side == "L" else "R"
    
    with lock:
        robot.set_rapid_variable(f"{prefix}/dx{suffix}", str(dx), task)
        robot.set_rapid_variable(f"{prefix}/dy{suffix}", str(dy), task)
        robot.set_rapid_variable(f"{prefix}/dz{suffix}", str(dz), task)
        robot.set_rapid_variable(f"{prefix}/cmdRel{suffix}", "1", task)
    time.sleep(2)

# --- Contrôle Pince ---
def openL(): 
    with lock: robot.set_rapid_variable("PythonCtrl/cmdGripL", "1", "T_ROB_L")
def closeL(): 
    with lock: robot.set_rapid_variable("PythonCtrl/cmdGripL", "2", "T_ROB_L")
def openR(): 
    with lock: robot.set_rapid_variable("PythonCtrlR/cmdGrip", "1", "T_ROB_R")
def closeR(): 
    with lock: robot.set_rapid_variable("PythonCtrlR/cmdGrip", "2", "T_ROB_R")

# --- Mouvements Simultanés ---
def move_both_joint(pos_l, pos_r):
    t1 = threading.Thread(target=move_joint, args=("L", pos_l))
    t2 = threading.Thread(target=move_joint, args=("R", pos_r))
    t1.start(); t2.start()
    t1.join(); t2.join()

if __name__ == "__main__":
    
    robot.request_rmmp(timeout=15)
    closeL()
    move_joint("L", [-18.67, -129.04, 44.48, 60.62, 79.66, 38.6, 111.5])
    time.sleep(8)
    move_joint("L", [-71.34, -128.9, 51.87, 60.65, 76.96, 0.01, 54.39])
    time.sleep(8)
    openL()
    move_joint("L", [-89.85, -53.08, 28.38, 103.18, 92.97, -54.88, 74.58])
    time.sleep(8)
    
    move_joint("L", [-99.58, -61.43, 13.96, 115.53, 84.61, -50.12, 90.38])
    time.sleep(8)
    closeL()
    move_joint("L", [-89.85, -53.08, 28.38, 103.18, 92.97, -54.88, 74.58])
    time.sleep(8)
    move_joint("L", [-77.38, -64.37, 61.13, 117.24, 97.05, -74.55, 81.21])
    time.sleep(8)
    move_joint("L", [-83.59, -71.27, 46.47, 132.6, 90.1, -68.59, 97.09])
    openL()

    #move_joint("L", [-89.85, -53.08, 28.38, 103.18, 92.97, -54.88, 74.58])