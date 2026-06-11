import time
import threading
import numpy as np
from abb_robot_client.rws import RWS

robot = RWS("http://10.2.30.126")
lock = threading.Lock()

def wait_done(var_cmd, task, timeout=30):
    """Attendre que RAPID finisse le mouvement"""
    for _ in range(timeout * 10):
        robot.poll_rmmp()
        val = robot.get_rapid_variable(var_cmd, task)
        if "0" in str(val):
            return True
        time.sleep(0.1)
    print(f"⚠ timeout {var_cmd}")
    return False

def move_joint(side, pos_list):
    joints = [float(d) for d in pos_list[:6]]
    j7     = float(pos_list[6])
    task   = "T_ROB_L"    if side == "L" else "T_ROB_R"
    module = "PythonCtrl" if side == "L" else "PythonCtrlR"
    var_t  = "jTarget"    if side == "L" else "jTargetR"
    var_c  = "cmd"        if side == "L" else "cmdR"

    target_data = [
        [float(np.deg2rad(d)) for d in joints],
        [float(np.deg2rad(j7)), 9E+09, 9E+09, 9E+09, 9E+09, 9E+09]
    ]

    with lock:
        robot.poll_rmmp()
        robot.set_rapid_variable_jointtarget(f"{module}/{var_t}", target_data, task=task)
        robot.poll_rmmp()
        robot.set_rapid_variable(f"{module}/{var_c}", "1", task)

    # Attendre fin du mouvement
    wait_done(var_c, task)
    print(f"MoveAbsJ {side} terminé")

def move_linear_to(side, data):
    x, y, z        = data[0], data[1], data[2]
    q1, q2, q3, q4 = data[3], data[4], data[5], data[6]
    cf = [int(data[7]), int(data[8]), int(data[9]), int(data[10])]
    
    # MODIFICATION : Utilisez directement le J7 de la liste 'data' (index 11)
    j7 = float(data[11]) 

    task   = "T_ROB_L"    if side == "L" else "T_ROB_R"
    module = "PythonCtrl" if side == "L" else "PythonCtrlR"
    var_t  = "pTargetL1"  if side == "L" else "pTargetR1"
    var_c  = "cmdLinL"    if side == "L" else "cmdLinR"

    val = (f"[[{x:.3f},{y:.3f},{z:.3f}],"
           f"[{q1:.6f},{q2:.6f},{q3:.6f},{q4:.6f}],"
           f"[{cf[0]},{cf[1]},{cf[2]},{cf[3]}],"
           f"[{j7:.3f},9E+09,9E+09,9E+09,9E+09,9E+09]]")

    with lock:
        robot.poll_rmmp()
        robot.set_rapid_variable(f"{module}/{var_t}", val, task=task)
        robot.poll_rmmp()
        robot.set_rapid_variable(f"{module}/{var_c}", "1", task)

    wait_done(var_c, task)
    print(f"MoveL {side} terminé à J7: {j7}")

def move_relative(side, dx, dy, dz):
    task   = "T_ROB_L"    if side == "L" else "T_ROB_R"
    prefix = "PythonCtrl" if side == "L" else "PythonCtrlR"
    suffix = ""           if side == "L" else "R"

    with lock:
        robot.poll_rmmp()
        robot.set_rapid_variable(f"{prefix}/dx{suffix}",     str(dx), task)
        robot.set_rapid_variable(f"{prefix}/dy{suffix}",     str(dy), task)
        robot.set_rapid_variable(f"{prefix}/dz{suffix}",     str(dz), task)
        robot.set_rapid_variable(f"{prefix}/cmdRel{suffix}", "1",     task)

    wait_done(f"cmdRel{suffix}", task)
    print(f"MoveRelative {side} terminé")

def openL():
    with lock: robot.poll_rmmp(); robot.set_rapid_variable("PythonCtrl/cmdGripL", "1", "T_ROB_L")
    wait_done("cmdGripL", "T_ROB_L", timeout=5)

def closeL():
    with lock: robot.poll_rmmp(); robot.set_rapid_variable("PythonCtrl/cmdGripL", "2", "T_ROB_L")
    wait_done("cmdGripL", "T_ROB_L", timeout=5)

def openR():
    with lock: robot.poll_rmmp(); robot.set_rapid_variable("PythonCtrlR/cmdGripR", "1", "T_ROB_R")
    wait_done("cmdGripR", "T_ROB_R", timeout=5)

def closeR():
    with lock: robot.poll_rmmp(); robot.set_rapid_variable("PythonCtrlR/cmdGripR", "2", "T_ROB_R")
    wait_done("cmdGripR", "T_ROB_R", timeout=5)

def move_both_joint(pos_l, pos_r):
    t1 = threading.Thread(target=move_joint, args=("L", pos_l))
    t2 = threading.Thread(target=move_joint, args=("R", pos_r))
    t1.start(); t2.start()
    t1.join();  t2.join()

def set_speed(side, speed):
    """
    Définit la vitesse pour le bras L ou R de manière cohérente.
    """
    task   = "T_ROB_L"    if side == "L" else "T_ROB_R"
    module = "PythonCtrl" if side == "L" else "PythonCtrlR"
    
    # On utilise 'speedVal' pour L et 'speedValR' pour R 
    # pour correspondre exactement à vos déclarations PERS dans le RAPID
    var_name = "speedVal" if side == "L" else "speedValR"
    
    with lock:
        robot.poll_rmmp()
        robot.set_rapid_variable(f"{module}/{var_name}", str(speed), task)
    
    print(f"Vitesse {side} → {speed}")

def get_piece_data(i, j):
    """
    i : ligne (0 à 4)
    j : colonne (0 ou 1, mais sera écrasé par le motif)
    """
    # Votre motif pour i=0, 1, 2, 3, 4
    # i=0 -> 1, i=1 -> 0, i=2 -> 1, i=3 -> 0, i=4 -> 1
    motif_j = [1, 0, 1, 0, 1]
    
    # On force la valeur de j en fonction de la ligne i
    j_force = motif_j[i]
    
    origin = np.array([462.86, 32.38, 62.21])
    vec_x = (np.array([461.18, -32.41, 64.09]) - origin) / 4
    vec_y = (np.array([446.03, 31.35, 60.20]) - origin)
    
    # Utilisation du j issu du motif
    pos = origin + (i * vec_x) + (j_force * vec_y)
    
    return [pos[0], pos[1], pos[2], 0.0, 0.997264, 0.0739287, 0.0, 1, -1, -1, 4, -176.047]

def set_wobj(side, wobj_name, xyz, quat):
    """Définir un repère depuis Python"""
    task   = "T_ROB_L"    if side == "L" else "T_ROB_R"
    module = "PythonCtrl" if side == "L" else "PythonCtrlR"
    x, y, z        = xyz
    q1, q2, q3, q4 = quat
    val = (f"[FALSE,TRUE,'',"
           f"[[{x:.3f},{y:.3f},{z:.3f}],"
           f"[{q1:.6f},{q2:.6f},{q3:.6f},{q4:.6f}]],"
           f"[[0,0,0],[1,0,0,0]]]")
    with lock:
        robot.poll_rmmp()
        robot.set_rapid_variable(f"{module}/{wobj_name}", val, task)
    print(f"Repère {wobj_name} → [{x:.2f},{y:.2f},{z:.2f}]")

def move_linear_wobj(side, wobj_cmd, data):
    """MoveL dans un repère spécifique"""
    # ... (x, y, z, q1...j7 extrait ici) ...
    x, y, z          = data[0], data[1], data[2]
    q1, q2, q3, q4   = data[3], data[4], data[5], data[6]
    cf               = [int(data[7]), int(data[8]), int(data[9]), int(data[10])]
    j7               = float(data[11])

    task   = "T_ROB_L"    if side == "L" else "T_ROB_R"
    module = "PythonCtrl" if side == "L" else "PythonCtrlR"

    # CORRECTION : Une seule structure if/elif pour éviter l'écrasement
    if side == "L":
        if wobj_cmd == "cmdLinPriseL": var_t = "pPriseL"
        elif wobj_cmd == "cmdLinPoseL": var_t = "pPoseL"
        else: var_t = "pTargetL1"
    else: # Side "R"
        if wobj_cmd == "cmdLinPriseR": var_t = "pPriseR"
        elif wobj_cmd == "cmdLinPoseR": var_t = "pPoseR"
        else: var_t = "pTargetR1"

    val = (f"[[{x:.3f},{y:.3f},{z:.3f}],"
           f"[{q1:.6f},{q2:.6f},{q3:.6f},{q4:.6f}],"
           f"[{cf[0]},{cf[1]},{cf[2]},{cf[3]}],"
           f"[{j7:.3f},9E+09,9E+09,9E+09,9E+09,9E+09]]")

    with lock:
        # print(f"DEBUG: Envoi vers {module}/{var_t}") # Décommentez pour voir le chemin
        robot.poll_rmmp()
        robot.set_rapid_variable(f"{module}/{var_t}", val, task)
        robot.poll_rmmp()
        robot.set_rapid_variable(f"{module}/{wobj_cmd}", "1", task)

    wait_done(wobj_cmd, task)
    print(f"MoveL {side} terminé")

def move_relative_wobj(side, wobj_cmd, dx, dy, dz):
    """MoveL relatif dans un repère spécifique"""
    task   = "T_ROB_L"    if side == "L" else "T_ROB_R"
    module = "PythonCtrl" if side == "L" else "PythonCtrlR"
    suffix = "R" if side == "R" else ""

    with lock:
        robot.poll_rmmp()
        robot.set_rapid_variable(f"{module}/dx{suffix}", str(dx), task)
        robot.set_rapid_variable(f"{module}/dy{suffix}", str(dy), task)
        robot.set_rapid_variable(f"{module}/dz{suffix}", str(dz), task)
        robot.set_rapid_variable(f"{module}/{wobj_cmd}", "1", task)

    wait_done(wobj_cmd, task)
    print(f"MoveRelative dans repère {wobj_cmd} terminé")

def handover_R_to_L():
    """Transfert pièce R to L"""
    print("Handover R to L...")
    t1 = threading.Thread(target=lambda: (
        robot.poll_rmmp(),
        robot.set_rapid_variable("PythonCtrl/cmdReceiveL", "1", "T_ROB_L"),
        wait_done("cmdReceiveL", "T_ROB_L", timeout=60)
    ))
    t2 = threading.Thread(target=lambda: (
        robot.poll_rmmp(),
        robot.set_rapid_variable("PythonCtrlR/cmdHandoverR2", "1", "T_ROB_R"),
        wait_done("cmdHandoverR2", "T_ROB_R", timeout=60)
    ))
    t1.start(); t2.start()
    t1.join();  t2.join()
    print("Handover R to L terminé")


if __name__ == "__main__":
    robot.request_rmmp(timeout=15)
    time.sleep(1)
    robot.poll_rmmp()



    ###################################
    # home


      
    move_joint("L",[-88.34, -72.62, 45.01, 157.49, 88.1, -84.14, 93.34])
    move_linear_wobj("L","cmdLinPoseL",[0,0,-100,       1,0,0,0,-1,2,-1,4,175.56])

    
    
    



