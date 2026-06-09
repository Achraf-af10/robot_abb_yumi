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
    task   = "T_ROB_L"    if side == "L" else "T_ROB_R"
    module = "PythonCtrl" if side == "L" else "PythonCtrlR"
    with lock:
        robot.poll_rmmp()
        robot.set_rapid_variable(f"{module}/speedVal", str(speed), task)
    print(f"Vitesse {side} → {speed}")

def set_speedR(speed):
    with lock:
        robot.poll_rmmp()
        robot.set_rapid_variable("PythonCtrlR/speedValR", str(speed), "T_ROB_R")
    print(f"Vitesse R → {speed}")

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
    x, y, z        = data[0], data[1], data[2]
    q1, q2, q3, q4 = data[3], data[4], data[5], data[6]
    cf = [int(data[7]), int(data[8]), int(data[9]), int(data[10])]
    j7 = float(data[11])

    task   = "T_ROB_L"    if side == "L" else "T_ROB_R"
    module = "PythonCtrl" if side == "L" else "PythonCtrlR"

    # Choisir la bonne cible selon le repère
    if wobj_cmd == "cmdLinPriseR":
        var_t = "pPriseR"
    elif wobj_cmd == "cmdLinPoseR":
        var_t = "pPoseR"
    else:
        var_t = "pTargetR1"
        
    if wobj_cmd == "cmdLinPriseL":
        var_t = "pPriseL"
    elif wobj_cmd == "cmdLinPoseL":
        var_t = "pPoseL"
    else:
        var_t = "pTargetL1"

    val = (f"[[{x:.3f},{y:.3f},{z:.3f}],"
           f"[{q1:.6f},{q2:.6f},{q3:.6f},{q4:.6f}],"
           f"[{cf[0]},{cf[1]},{cf[2]},{cf[3]}],"
           f"[{j7:.3f},9E+09,9E+09,9E+09,9E+09,9E+09]]")

    with lock:
        robot.poll_rmmp()
        robot.set_rapid_variable(f"{module}/{var_t}", val, task)
        robot.poll_rmmp()
        robot.set_rapid_variable(f"{module}/{wobj_cmd}", "1", task)

    wait_done(wobj_cmd, task)
    print(f"MoveL dans repère {wobj_cmd} terminé")

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


if __name__ == "__main__":
    robot.request_rmmp(timeout=15)
    time.sleep(1)
    robot.poll_rmmp()



    ###################################
    move_linear_wobj("L","cmdLinPriseL",[0,0,0,          1,-0.0319725,-0.13666,0,-1,2,-1,4,-170.409])
    move_linear_wobj("L","cmdLinPriseL",[0,0,-100,       1,-0.0319725,-0.13666,0,-1,2,-1,4,-170.409])
    openL()
    closeL()

    

"""
    move_joint("R",[106.81, -53.02, 24.38, -115.36, 88.77, -110.84, -82.26])
    openR()

    move_linear_to("R",[462.86,32.40,75.29,0,0.997264,0.073927,0,1,-1,-1,4,-176.045])
    set_speedR(10)
    #prise
    move_linear_to("R",[462.86,32.38,62.21,0,0.997264,0.0739287,0,1,-1,-1,4,-176.047])
    
    closeR()
    move_linear_to("R",[462.86,32.41,157.53,0,0.997263,0.0739327,0,1,-1,-1,4,-176.046])
    
    set_speedR(100)
    move_joint("R",[101.01, -62.22, 55.08, -124.95, 101.36, -89.4, -86.13])

    move_linear_to("R",[319.80,34.70,97.58,0,0.997263,0.0739298,0,1,-2,-1,4,-176.048])
    set_speedR(10)  
    #pose
    move_linear_to("R",[319.80,34.70,84.25,0,0.997263,0.0739293,0,1,-2,-1,4,-176.048])
    openR()
    set_speedR(100) 
    move_joint("R",[101.01, -62.22, 55.08, -124.95, 101.36, -89.4, -86.13])


    move_linear_to("R", [395.89, -4.64, 214.68, 0.000026, 0.707114, 0.707100, -0.000007, 1, -1, 2, 4, -176.667])
    time.sleep(5)
    move_linear_to("R", [395.89, -4.66, 81.46, 0.000028, 0.707117, 0.707097, -0.000016, 1, -1, 2, 4, -176.667])
    
    closeL()
    move_joint("L", [-18.67, -129.04, 44.48, 60.62, 79.66, 38.6, 111.5])

    move_joint("L", [-71.34, -128.9, 51.87, 60.65, 76.96, 0.01, 54.39])

    move_joint("L", [-89.85, -53.08, 28.38, 103.18, 92.97, -54.88, 74.58])
    openL()
    set_speed("L", 10)
 
    move_joint("L", [-99.58, -61.43, 13.96, 115.53, 84.61, -50.12, 90.38])
    closeL()
    #move_linear_to("L",[449.0271, 42.4509, 162.9624, 0.1195100, -0.1109869, -0.9854010, -0.0488265, -1, 1, -1, 4, 90.37995])


    move_joint("L", [-89.85, -53.08, 28.38, 103.18, 92.97, -54.88, 74.58])
    set_speed("L", 100)
    move_joint("L", [-77.38, -64.37, 61.13, 117.24, 97.05, -74.55, 81.21])

    set_speed("L", 10)
    move_joint("L", [-83.59, -71.27, 46.47, 132.6, 90.1, -68.59, 97.09])
    openL()
"""
"""
if __name__ == "__main__":
    robot.request_rmmp(timeout=15)
    time.sleep(1)
    robot.poll_rmmp()
    
    closeR()
    set_speedR(100)

    # Parcours de la grille 5x2
    for i in range(3):
        for j in range(0):
            # 1. Aller à la position de sécurité
            move_joint("R", [101.01, -62.22, 55.08, -124.95, 101.36, -89.4, -86.13])
            
            # 2. Récupérer les coordonnées de la pièce actuelle
            piece_pos = get_piece_data(i, j)
            
            # 3. Approche (50mm au-dessus)
            approche = list(piece_pos)
            approche[2] += 50
            move_linear_to("R", approche)
            
            # 4. Prise
            set_speedR(10)
            move_linear_to("R", piece_pos)
            closeR()
            
            # 5. Remontée
            move_linear_to("R", approche)
            
            # 6. Déplacement vers zone de pose
            set_speedR(100)
            move_linear_to("R", [319.80, 34.70, 97.58, 0, 0.997263, 0.0739298, 0, 1, -2, -1, 4, -176.048])
            
            # 7. Pose
            set_speedR(10)
            move_linear_to("R", [319.80, 34.70, 84.25, 0, 0.997263, 0.0739293, 0, 1, -2, -1, 4, -176.048])
            
            openR()
            
            # 8. Retour sécurité
            set_speedR(100)
            move_linear_to("R", [319.80, 34.70, 97.58, 0, 0.997263, 0.0739298, 0, 1, -2, -1, 4, -176.048])

    # Retour final
    move_joint("R", [101.01, -62.22, 55.08, -124.95, 101.36, -89.4, -86.13])
"""

"""

        [462.86,32.40,75.29],[3.23502E-05,0.997264,0.073927,1.08797E-05],[1,-1,-1,4],[-176.045,9E+09,9E+09,9E+09,9E+09,9E+09] point avant prise
    [462.86,32.41,157.53],[2.68911E-05,0.997263,0.0739327,1.45969E-05],[1,-1,-1,4],[-176.046,9E+09,9E+09,9E+09,9E+09,9E+09] point approche
    --- POSITION ACTUELLE (MOVE L FORMAT) ---
ROB_L (MoveL format): (266.6966, 324.9249, 194.9115, 0.0003603, -0.4252115, 0.9050940, -0.0001140, -1, 1, -1, 4, 64.03001)
ROB_R (MoveL format): (462.9659, 31.7388, 272.7169, 0.0000280, 0.9972633, 0.0739318, 0.0000133, 1, -1, -1, 4, -82.25835)

--- POSITION ACTUELLE (MOVE J FORMAT) ---
ROB_L: [-46.31, -120.74, 40.26, 134.87, 75.19, -56.72, 64.03]
ROB_R: [106.81, -53.02, 24.38, -115.36, 88.77, -110.84, -82.26]


[319.80,34.70,84.25],[2.25642E-05,0.997263,0.0739293,6.42268E-06],[1,-2,-1,4],[-176.048,9E+09,9E+09,9E+09,9E+09,9E+09] point pose
[319.80,34.70,97.58],[2.24461E-05,0.997263,0.0739298,7.09773E-06],[1,-2,-1,4],[-176.048,9E+09,9E+09,9E+09,9E+09,9E+09]point avant pose 

point approche pose 
--- POSITION ACTUELLE (MOVE L FORMAT) ---
ROB_L (MoveL format): (266.6971, 324.9241, 194.9111, 0.0003598, -0.4252109, 0.9050942, -0.0001150, -1, 1, -1, 4, 64.03001)
ROB_R (MoveL format): (320.3326, 34.0301, 292.5324, 0.0000173, 0.9972633, 0.0739325, 0.0000116, 1, -1, -1, 4, -86.12983)

--- POSITION ACTUELLE (MOVE J FORMAT) ---
ROB_L: [-46.31, -120.74, 40.26, 134.87, 75.19, -56.72, 64.03]
ROB_R: [101.01, -62.22, 55.08, -124.95, 101.36, -89.4, -86.13]

home
--- POSITION ACTUELLE (MOVE L FORMAT) ---
ROB_L (MoveL format): (262.0252, 315.9446, 187.5087, 0.0169214, 0.4189962, -0.9078068, 0.0065326, -1, 1, -1, 4, 66.25337)
ROB_R (MoveL format): (-0.1055, -176.9857, 192.3151, 0.4095618, -0.6395398, 0.5594502, -0.3320594, 0, 0, 1, 4, -134.99510)

--- POSITION ACTUELLE (MOVE J FORMAT) ---
ROB_L: [-46.31, -120.74, 40.25, 134.87, 75.25, -56.72, 66.25]
ROB_R: [0.37, -133.92, 30.39, 2.88, 37.94, 92.6, -135.0]

Inter
--- POSITION ACTUELLE (MOVE L FORMAT) ---
ROB_L (MoveL format): (262.0144, 315.9249, 187.4924, 0.0169593, 0.4189817, -0.9078127, 0.0065470, -1, 1, -1, 4, 66.25832)
ROB_R (MoveL format): (325.1313, -94.0331, 289.4751, 0.0032484, -0.9978921, 0.0648125, -0.0003529, 1, 1, 1, 5, -87.14413)

--- POSITION ACTUELLE (MOVE J FORMAT) ---
ROB_L: [-46.31, -120.74, 40.25, 134.87, 75.25, -56.72, 66.26]
ROB_R: [80.47, -62.72, 52.49, 46.42, -81.53, 94.37, -87.14]

xy
        MoveL [[461.18,-32.41,64.09],[3.50128E-05,0.997263,0.0739301,6.18691E-06],[1,-1,-1,4],[-176.052,9E+09,9E+09,9E+09,9E+09,9E+09]], v1000, z50, tPince3D;
        MoveL [[446.03,31.35,60.20],[1.68502E-05,-0.997263,-0.0739346,0.000130543],[1,-1,-1,4],[-176.066,9E+09,9E+09,9E+09,9E+09,9E+09]], v1000, z50, tPince3D;



















            set_speedR(50)
    move_joint("R",[17.71, -94.2, 48.93, -150.95, 22.07, -131.84, -72.22])
    set_speedR(50)
    move_linear_wobj("R","cmdLinPriseR",[0,0,-100,1,0,0,0,1,-2,-2,4,-139.106])
    openR()
    move_linear_wobj("R","cmdLinPriseR",[0,0,0,1,0,0,0,1,-2,-2,4,-139.106])
    closeR()
    move_linear_wobj("R","cmdLinPriseR",[0,0,-100,1,0,0,0,1,-2,-2,4,-139.106])
    move_linear_wobj("R","cmdLinPriseR",[-140,-15,-100,1,0,0,0,1,-2,-2,4,-139.106])
    move_linear_wobj("R","cmdLinPoseR",[0,0,-50,1,0,0,0,1,-2,-2,4,-139.106])
    set_speedR(5)
    move_linear_wobj("R","cmdLinPoseR",[0,0,0,1,0,0,0,1,-2,-2,4,-139.106])
    openR()
    set_speedR(50)
    move_linear_wobj("R","cmdLinPoseR",[0,0,-80,1,0,0,0,1,-2,-2,4,-139.106])
    closeR()

    move_linear_wobj("R","cmdLinPriseR",[-3.01,29.65,-100,1,0,0,0,1,-2,-2,4,-139.106])
    openR()
    move_linear_wobj("R","cmdLinPriseR",[-3.01,29.65,0,1,0,0,0,1,-2,-2,4,-139.106])
    closeR()
    move_linear_wobj("R","cmdLinPriseR",[-3.01,29.65,-100,1,0,0,0,1,-2,-2,4,-139.106])
    move_linear_wobj("R","cmdLinPriseR",[-140,-15,-100,1,0,0,0,1,-2,-2,4,-139.106])
    move_linear_wobj("R","cmdLinPoseR",[-3.01,29.65,-50,1,0,0,0,1,-2,-2,4,-139.106])
    set_speedR(5)
    move_linear_wobj("R","cmdLinPoseR",[-3.01,29.65,0,1,0,0,0,1,-2,-2,4,-139.106])
    openR()
    set_speedR(50)
    move_linear_wobj("R","cmdLinPoseR",[-3.01,29.65,-80,1,0,0,0,1,-2,-2,4,-139.106])
    closeR()


    move_linear_wobj("R","cmdLinPriseR",[-6.80,61.41,-100,1,0,0,0,1,-2,-2,4,-139.106])
    openR()
    set_speedR(5)
    move_linear_wobj("R","cmdLinPriseR",[-6.80,61.41,3,1,0,0,0,1,-2,-2,4,-139.106])
    closeR()
    move_linear_wobj("R","cmdLinPriseR",[-6.80,61.41,-100,1,0,0,0,1,-2,-2,4,-139.106])
    set_speedR(50)
    move_linear_wobj("R","cmdLinPriseR",[-140,-15,-100,1,0,0,0,1,-2,-2,4,-139.106])
    move_linear_wobj("R","cmdLinPoseR",[0,0,-50,1,0,0,0,1,-2,-2,4,-139.106])
    set_speedR(5)
    move_linear_wobj("R","cmdLinPoseR",[0,0,0,1,0,0,0,1,-2,-2,4,-139.106])
    openR()
    set_speedR(50)
    move_linear_wobj("R","cmdLinPoseR",[0,0,-80,1,0,0,0,1,-2,-2,4,-139.106])
    closeR()
    """