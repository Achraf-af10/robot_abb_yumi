import threading
import numpy as np
from abb_robot_client.rws import RWS
from pince import openL, closeL,closeR,openR,openRL,closeRL
import time

# Connexion unique
robot = RWS("http://10.2.30.126")

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

if __name__ == "__main__":
    robot.request_rmmp(timeout=15)


    #depart
    closeL(robot)
    move_both_joint([-30.92, -137.31, 43.44, 83.75, 75.81, 27.93, 112.1], [38.7, -120.73, 38.1, -59.66, 57.79, 124.54, -117.72])

    move_joint("L",[-107.02, -109.98, 25.33, 75.85, 81.35, -23.28, 39.65])
    
    move_joint("L",[-116.55, -114.29, 30.93, 169.27, 118.6, -30.94, 51.15])



    openL(robot)
    time.sleep(1.5)
    move_joint("L",[-116.52, -115.74, 25.86, 171.07, 112.93, -29.67, 51.57])
    time.sleep(1.5)
    closeL(robot)
    time.sleep(1.5)

    move_joint("L",[-116.74, -112.62, 34.49, 167.29, 123.22, -32.2, 50.46])

    move_joint("L",[-98.74, -132.22, 54.83, 181.6, 120.6, -33.52, 71.99])


    move_joint("L",[-98.14, -133.46, 51.22, 182.46, 116.15, -32.6, 72.15])
    time.sleep(1)
    openL(robot)
    time.sleep(1)

    
 
    #move_relativeL(robot,-200,0,-20)














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

    