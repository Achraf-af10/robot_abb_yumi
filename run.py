import threading
import numpy as np
from abb_robot_client.rws import RWS
from pince import openL, closeL,closeR,openR,openRL,closeRL
import time

# Connexion unique
robot = RWS("http://10.2.30.126")
lock = threading.Lock()

def move_joint(side, pos_list):
    joints = [float(d) for d in pos_list[:6]]
    j7 = float(pos_list[6])
    task, var_t, var_c = ("T_ROB_L", "jTarget", "cmd") if side == "L" else ("T_ROB_R", "jTargetR", "cmdR")
    
    target_data = [
        [float(np.deg2rad(d)) for d in joints],
        [float(np.deg2rad(j7)), 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]
    ]
    
    robot.poll_rmmp()
    robot.set_rapid_variable_jointtarget(var_t, target_data, task=task)
    robot.set_rapid_variable(var_c, "1", task)
    print(f"MoveAbsJ {side} lancé avec J7={j7}")

def move_both_joint(pos_l, pos_r):
    t1 = threading.Thread(target=move_joint, args=("L", pos_l))
    t2 = threading.Thread(target=move_joint, args=("R", pos_r))
    t1.start(); t2.start()
    t1.join(); t2.join()

def move_linear(side, data):
    xyz = data[0:3]; quat = data[3:7]; conf = data[7:11]; e1 = data[11]
    task, var_t, var_c = ("T_ROB_L", "pTargetL1", "cmdLinL") if side == "L" else ("T_ROB_R", "pTargetR1", "cmdLinR")
    
    val = f"[[{xyz[0]:.3f},{xyz[1]:.3f},{xyz[2]:.3f}],[{quat[0]:.6f},{quat[1]:.6f},{quat[2]:.6f},{quat[3]:.6f}],[{int(conf[0])},{int(conf[1])},{int(conf[2])},{int(conf[3])}],[{e1:.3f},9E+09,9E+09,9E+09,9E+09,9E+09]]"
    
    robot.poll_rmmp()
    robot.set_rapid_variable(var_t, val, task=task)
    robot.set_rapid_variable(var_c, "1", task)
    print(f"MoveL {side} lancé")

def move_linear_to_to(side, data):
    x, y, z = data[0], data[1], data[2]
    q1, q2, q3, q4 = data[3], data[4], data[5], data[6]
    cf = [int(data[7]), int(data[8]), int(data[9]), int(data[10])] if len(data) > 7 else [0, 0, 0, 0]

    task = "T_ROB_L" if side == "L" else "T_ROB_R"
    module = "PythonCtrl" if side == "L" else "PythonCtrlR"
    var_t = "pTargetL1" if side == "L" else "pTargetR1"
    var_c = "cmdLinL" if side == "L" else "cmdLinR"

    # Récupération de l'axe externe actuel pour ne pas le modifier
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
    print(f"MoveL {side} lancé vers XYZ: {x:.1f}, {y:.1f}, {z:.1f}")

def move_both_linear(data_l, data_r):
    t1 = threading.Thread(target=move_linear, args=("L", data_l))
    t2 = threading.Thread(target=move_linear, args=("R", data_r))
    t1.start(); t2.start()
    t1.join(); t2.join()

def move_relativeL(robot, x, y, z):
    # Mise à jour des offsets pour le module PythonCtrl
    robot.set_rapid_variable("PythonCtrl/dx", str(x), "T_ROB_L")
    robot.set_rapid_variable("PythonCtrl/dy", str(y), "T_ROB_L")
    robot.set_rapid_variable("PythonCtrl/dz", str(z), "T_ROB_L")
    
    # Déclenchement du mouvement relatif
    robot.set_rapid_variable("PythonCtrl/cmdRel", "1", "T_ROB_L")
    time.sleep(2) # Temps nécessaire à l'exécution

# --- Fonctions pour le Robot Droit (T_ROB_R) ---
def move_relativeR(robot, x, y, z):
    # Mise à jour des offsets pour le module PythonCtrlR
    robot.set_rapid_variable("PythonCtrlR/dxR", str(x), "T_ROB_R")
    robot.set_rapid_variable("PythonCtrlR/dyR", str(y), "T_ROB_R")
    robot.set_rapid_variable("PythonCtrlR/dzR", str(z), "T_ROB_R")
    
    # Déclenchement du mouvement relatif
    robot.set_rapid_variable("PythonCtrlR/cmdRelR", "1", "T_ROB_R")
    time.sleep(2)

# --- Fonction combinée pour déplacer les deux simultanément ---
def move_relativeRL(robot, dx, dy, dz):
    """Déplace les deux robots de la même valeur relative simultanément"""
    t1 = threading.Thread(target=move_relativeL, args=(robot, dx, dy, dz))
    t2 = threading.Thread(target=move_relativeR, args=(robot, dx, dy, dz))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

def move_linear_to(side, data):
    x, y, z = data[0], data[1], data[2]
    q1, q2, q3, q4 = data[3], data[4], data[5], data[6]
    
    task = "T_ROB_L" if side == "L" else "T_ROB_R"
    var_t = "pTargetL1" if side == "L" else "pTargetR1"
    var_c = "cmdLinL" if side == "L" else "cmdLinR"

    val = f"[[{x:.3f},{y:.3f},{z:.3f}],[{q1:.6f},{q2:.6f},{q3:.6f},{q4:.6f}],[0,0,0,0],[0,9E9,9E9,9E9,9E9,9E9]]"

    with lock:
        robot.set_rapid_variable(var_t, val, task=task)
        robot.set_rapid_variable(var_c, "1", task)

def update_wobj(side, x, y, z):
    """Met à jour le WObj sur le robot avec un formatage strict."""
    task = "T_ROB_L" if side == "L" else "T_ROB_R"
    module = "PythonCtrl" if side == "L" else "PythonCtrlR"
    var = "mon_repere" if side == "L" else "mon_repereR"
    
    # Formatage strict : [robframe, objframe, name, uframe, oframe]
    # uframe contient la position (x,y,z) et l'orientation (q1,q2,q3,q4)
    val = f"[FALSE,TRUE,'',[[{x:.3f},{y:.3f},{z:.3f}],[1,0,0,0]],[[0,0,0],[1,0,0,0]]]"
    
    with lock:
        # On utilise le format Module/Variable pour cibler précisément la PERS
        robot.set_rapid_variable(f"{module}/{var}", val, task=task)
    print(f"Succès : {module}/{var} mis à jour à ({x}, {y}, {z})")
    

if __name__ == "__main__":
    robot.request_rmmp(timeout=15)


    #depar
    """
    move_joint("L", [-18.67, -129.04, 44.48, 60.62, 79.66, 38.6, 111.5])
    time.sleep(10)
    move_joint("L", [-71.34, -128.9, 51.87, 60.65, 76.96, 0.01, 54.39])
    time.sleep(10)
    move_joint("L", [-89.85, -53.08, 28.38, 103.18, 92.97, -54.88, 74.58])
    time.sleep(10)
    move_joint("L", [-99.58, -61.43, 13.96, 115.53, 84.61, -50.12, 90.38])
    time.sleep(10)
    move_joint("L", [-89.85, -53.08, 28.38, 103.18, 92.97, -54.88, 74.58])
    time.sleep(10)
    move_joint("L", [-77.38, -64.37, 61.13, 117.24, 97.05, -74.55, 81.21])
    time.sleep(10)
    move_joint("L", [-83.59, -71.27, 46.47, 132.6, 90.1, -68.59, 97.09])

    """

    update_wobj("L", 449.0226, 42.4695, 162.9474)
    move_linear_to("L", [0, 0, 20, 0, 1, 0, 0])














    #move_relativeL(robot,-346,-100,-20)


    #move_linear("L",[467.1626, 28.1624, 205.9581, 0.0180023, 0.0326980, -0.9992210, -0.0128108, -1, 2, 0, 4, 51.15013])
    #move_relativeL(robot,0,10,0)

    """
    
    move_joint("L",[-116.55, -114.29, 30.93, 169.27, 118.6, -30.94, 51.15])
    openL(robot)
    time.sleep(1)

    move_linear("L",[467.5986, 28.4683, 176.2053, 0.0193078, 0.0332280, -0.9991617, -0.0141072, -1, 2, 0, 4, 51.57437])
    closeL(robot)
    
    time.sleep(1)
    move_linear("L",[467.1468, 28.9932, 229.8698, 0.0179916, 0.0326997, -0.9992220, -0.0127408, -1, 2, 0, 4, 50.45849])

    time.sleep(1)
    move_joint("L",[-98.74, -132.22, 54.83, 181.6, 120.6, -33.52, 71.99])

    time.sleep(1)
    move_linear("L",[340.6070, 28.9951, 198.5536, 0.0179895, 0.0326956, -0.9992222, -0.0127458, -1, 2, 0, 4, 72.14550])    
    openL(robot)

    time.sleep(1)

    """

    