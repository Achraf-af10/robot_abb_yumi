from abb_robot_client.rws import RWS
import numpy as np
import threading
import requests
import time

robot = RWS("http://10.2.30.126")
BASE  = "http://10.2.30.126"
HDR   = {"Content-Type": "application/x-www-form-urlencoded"}

# Authentification et Mastership
print("GRANT sur FlexPendant...")
robot.request_rmmp(timeout=15)
time.sleep(1)
robot.poll_rmmp()
print("Mastership OK \n")

# === UTILITAIRES ===

def reset_cmds():
    robot.poll_rmmp()
    for var, task in [
        ("cmd",      "T_ROB_L"), ("cmdLinL",  "T_ROB_L"), ("cmdGripL", "T_ROB_L"),
        ("cmdR",     "T_ROB_R"), ("cmdLinR",  "T_ROB_R"), ("cmdGrip",  "T_ROB_R")
    ]:
        robot.set_rapid_variable(var, "0", task)
    print("CMD reset ✓")

def check_rapid():
    if "stopped" in str(robot.get_execution_state()):
        input("Appuie Entrée quand prêt...")
    reset_cmds()
    time.sleep(0.2)

def wait_done(var_cmd, task, timeout=200):
    for i in range(timeout):
        robot.poll_rmmp()
        if "0" in str(robot.get_rapid_variable(var_cmd, task)):
            return i * 0.1
        time.sleep(0.1)
    return -1

# === MOUVEMENT ARTICULAIRE (MoveAbsJ) ===

def move_joint(side, pos):
    if side == "L":
        task, var_t, var_c, mech, module = "T_ROB_L", "jTarget",  "cmd",  "ROB_L", "PythonCtrl"
    else:
        task, var_t, var_c, mech, module = "T_ROB_R", "jTargetR", "cmdR", "ROB_R", "PythonCtrlR"

    j7 = float(robot.get_jointtarget(mechunit=mech).extax[0])
    target_rad = [np.deg2rad(pos), np.deg2rad([j7, 0, 0, 0, 0, 0])]

    robot.poll_rmmp()
    robot.set_rapid_variable_jointtarget(var_t, target_rad, task=task)
    robot.poll_rmmp()
    robot.set_rapid_variable(var_c, "1", task)
    print(f"  MoveAbsJ {side} → {[round(v,2) for v in pos]}")

    t = wait_done(var_c, task)
    if t >= 0:
        j = robot.get_jointtarget(mechunit=mech)
        print(f"  {t:.1f}s | {[round(float(v),2) for v in j.robax]}")
    else:
        print(f"  timeout")

def move_both_joint(pos_l, pos_r):
    t1 = threading.Thread(target=move_joint, args=("L", pos_l))
    t2 = threading.Thread(target=move_joint, args=("R", pos_r))
    t1.start(); t2.start()
    t1.join();  t2.join()
    print("  --- MoveAbsJ terminé ---")

# === MOUVEMENT LINÉAIRE (MoveL) ===

def move_linear(side, xyz, quat):
    if side == "L":
        task, var_t, var_c, module = "T_ROB_L", "pTargetL", "cmdLinL", "PythonCtrl"
    else:
        task, var_t, var_c, module = "T_ROB_R", "pTargetR", "cmdLinR", "PythonCtrlR"

    x, y, z       = xyz
    q1, q2, q3, q4 = quat
    value = (f"[[{x},{y},{z}],"
             f"[{q1},{q2},{q3},{q4}],"
             f"[0,0,0,0],"
             f"[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]]")

    robot.poll_rmmp()
    r = requests.post(
        f"{BASE}/rw/rapid/symbol/data/RAPID/{task}/{module}/{var_t}?action=set",
        headers=HDR, data={"value": value}, auth=robot.auth
    )
    print(f"  MoveL {side} set status : {r.status_code}")

    robot.poll_rmmp()
    robot.set_rapid_variable(var_c, "1", task)
   

    t = wait_done(var_c, task)
    if t >= 0:
        print(f"   {t:.1f}s")
    else:
        print(f"  timeout")

def move_both_linear(xyz_l, xyz_r, quat_l, quat_r):
    t1 = threading.Thread(target=move_linear, args=("L", xyz_l, quat_l))
    t2 = threading.Thread(target=move_linear, args=("R", xyz_r, quat_r))
    t1.start(); t2.start()
    t1.join();  t2.join()
    print("  --- MoveL terminé ---")



# CONFIGURATION DES CIBLES

TARGET_L_JOINT = [-53.32, -56.44, 39.23, -33.26, 38.17, 86.08]
TARGET_R_JOINT = [ 59.36, -73.71, 25.65, -14.68, 61.86, 151.29]

TARGET_L_XYZ  = [282.95,  182.37, 207.2]
TARGET_L_QUAT = [0.0254, -0.1135, 0.7684, -0.6294]
TARGET_R_XYZ  = [347.77, -199.54, 200.72]
TARGET_R_QUAT = [0.6876, -0.7124, 0.0252,  0.1382]


# PROGRAMME PRINCIPAL
check_rapid()

# Sauvegarder positions initiales
pos_l_init = [float(v) for v in robot.get_jointtarget(mechunit="ROB_L").robax]
pos_r_init = [float(v) for v in robot.get_jointtarget(mechunit="ROB_R").robax]
print(f"Position initiale L : {[round(v,2) for v in pos_l_init]}")
print(f"Position initiale R : {[round(v,2) for v in pos_r_init]}\n")

# Aller vers cible articulaire
move_both_joint(TARGET_L_JOINT, TARGET_R_JOINT)
time.sleep(1)

# Aller vers cible linéaire
move_both_linear(TARGET_L_XYZ, TARGET_R_XYZ, TARGET_L_QUAT, TARGET_R_QUAT)
time.sleep(1)

# Retour position initiale
move_both_joint(pos_l_init, pos_r_init)