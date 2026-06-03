import time
import threading
import numpy as np
from abb_robot_client.rws import RWS

# Connexion au contrôleur
robot = RWS("http://10.2.30.126")

# --- Mouvement Articulaire (Joints) ---
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
    print(f"MoveAbsJ {side} lancé")

# --- Mouvement Linéaire (XYZ + Quaternion) ---
def move_linear_to(side, data):
    """
    side: "L" ou "R"
    data: liste [x, y, z, q1, q2, q3, q4]
    """
    # Extraction des données depuis la liste unique
    x, y, z = data[0], data[1], data[2]
    q1, q2, q3, q4 = data[3], data[4], data[5], data[6]
    
    task = "T_ROB_L" if side == "L" else "T_ROB_R"
    var_t = "pTargetL1" if side == "L" else "pTargetR1"
    var_c = "cmdLinL" if side == "L" else "cmdLinR"

    # Construction de la chaîne de caractères pour le RAPID
    # On utilise [0,0,0,0] pour laisser le robot gérer sa configuration librement
    val = f"[[{x:.3f},{y:.3f},{z:.3f}],[{q1:.6f},{q2:.6f},{q3:.6f},{q4:.6f}],[0,0,0,0],[0,9E9,9E9,9E9,9E9,9E9]]"
    
    robot.poll_rmmp()
    robot.set_rapid_variable(var_t, val, task=task)
    robot.set_rapid_variable(var_c, "1", task)
    
    print(f"MoveL {side} lancé vers X:{x}, Y:{y}, Z:{z}")

def move_both_joint(pos_l, pos_r):
    """Déplace les deux robots simultanément en articulaire."""
    t1 = threading.Thread(target=move_joint, args=("L", pos_l))
    t2 = threading.Thread(target=move_joint, args=("R", pos_r))
    
    t1.start()
    t2.start()
    
    t1.join() # Attend la fin du robot L
    t2.join() # Attend la fin du robot R
    print("Mouvements articulaires simultanés terminés.")

def move_both_linear(data_l, data_r):
    """
    data_l et data_r doivent être des listes : [x, y, z, q1, q2, q3, q4]
    """
    # Fonction locale pour wrapper move_linear_to avec unpack
    def run_l(): move_linear_to("L", *data_l)
    def run_r(): move_linear_to("R", *data_r)
    
    t1 = threading.Thread(target=run_l)
    t2 = threading.Thread(target=run_r)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    print("Mouvements linéaires simultanés terminés.")
# --- Mouvement Relatif (RelTool) ---
def move_relative(side, dx, dy, dz):
    task = "T_ROB_L" if side == "L" else "T_ROB_R"
    prefix = "PythonCtrl" if side == "L" else "PythonCtrlR"
    suffix = "" if side == "L" else "R"
    
    robot.set_rapid_variable(f"{prefix}/dx{suffix}", str(dx), task)
    robot.set_rapid_variable(f"{prefix}/dy{suffix}", str(dy), task)
    robot.set_rapid_variable(f"{prefix}/dz{suffix}", str(dz), task)
    robot.set_rapid_variable(f"{prefix}/cmdRel{suffix}", "1", task)
    time.sleep(2)

# --- Contrôle Pince ---
def openL(): robot.set_rapid_variable("PythonCtrl/cmdGripL", "1", "T_ROB_L"); time.sleep(1)
def closeL(): robot.set_rapid_variable("PythonCtrl/cmdGripL", "2", "T_ROB_L"); time.sleep(1)
def openR(): robot.set_rapid_variable("PythonCtrlR/cmdGrip", "1", "T_ROB_R"); time.sleep(1)
def closeR(): robot.set_rapid_variable("PythonCtrlR/cmdGrip", "2", "T_ROB_R"); time.sleep(1)

# --- EXEMPLE D'UTILISATION ---
if __name__ == "__main__":



    closeL()
    move_both_joint([-30.92, -137.31, 43.44, 83.75, 75.81, 27.93, 112.1], [38.7, -120.73, 38.1, -59.66, 57.79, 124.54, -117.72])

    move_joint("L",[-107.02, -109.98, 25.33, 75.85, 81.35, -23.28, 39.65])
    
    move_joint("L",[-116.55, -114.29, 30.93, 169.27, 118.6, -30.94, 51.15])



    openL()
    time.sleep(1.5)
    move_joint("L",[-116.52, -115.74, 25.86, 171.07, 112.93, -29.67, 51.57])
    time.sleep(1.5)
    closeL()
    time.sleep(1.5)

    move_joint("L",[-116.74, -112.62, 34.49, 167.29, 123.22, -32.2, 50.46])

    move_joint("L",[-98.74, -132.22, 54.83, 181.6, 120.6, -33.52, 71.99])


    move_joint("L",[-98.14, -133.46, 51.22, 182.46, 116.15, -32.6, 72.15])
    time.sleep(1)
    openL()
    time.sleep(1)

    move_relative("L",-200,0,-20)