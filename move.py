import time
from abb_robot_client.rws import RWS

# Connexion
robot = RWS("http://10.2.30.126")

def wait_for_ready(var_name, task="T_ROB_L"):
    """Attend que la commande soit remise à 0 par RAPID"""
    # Ajout d'un timeout de sécurité pour éviter de bloquer indéfiniment
    start_time = time.time()
    while "0" not in str(robot.get_rapid_variable(var_name, task)):
        time.sleep(0.1)
        if time.time() - start_time > 10: # Timeout 10s
            print(f"Erreur: Timeout sur {var_name}")
            break

def move_j(joints_deg):
    """Déplacement articulaire avec conversion correcte"""
    robot.poll_rmmp()
    # On récupère l'axe 7 actuel pour ne pas le perdre lors du MoveJ
    jt_current = robot.get_jointtarget("ROB_L")
    ext_ax = jt_current.extax
    
    target = [ [d * 3.14159/180 for d in joints_deg], [float(ext_ax[0]) * 3.14159/180, 9E+09, 9E+09, 9E+09, 9E+09, 9E+09] ]
    robot.set_rapid_variable_jointtarget("jTarget", target, "T_ROB_L")
    robot.set_rapid_variable("cmd", "1", "T_ROB_L")
    wait_for_ready("cmd")

def move_l(x, y, z, q1, q2, q3, q4, cf1, cf4, cf6, cfx, e1):
    """Construction sécurisée de la robtarget pour MoveL"""
    robot.poll_rmmp()
    # Formatage strict de la chaîne RAPID attendue par le contrôleur
    robtarget_str = f"[[{x:.3f},{y:.3f},{z:.3f}],[{q1:.6f},{q2:.6f},{q3:.6f},{q4:.6f}],[{int(cf1)},{int(cf4)},{int(cf6)},{int(cfx)}],[{e1:.3f},9E+09,9E+09,9E+09,9E+09,9E+09]]"
    
    robot.set_rapid_variable("pTargetL1", robtarget_str, "T_ROB_L")
    robot.set_rapid_variable("cmdLinL", "1", "T_ROB_L")
    wait_for_ready("cmdLinL")

if __name__ == "__main__":
    robot.request_rmmp(timeout=15)
    
    # 1. Aller à un point articulaire
    #move_j([-123.65, -118.64, 73.19, 66.61, 97.06, 105.78])
    print("MoveJ terminé")

    # 2. Récupérer la position réelle pour construire le MoveL sans erreur
    move_l(443.9821, 214.9470, 238.5663, 0.7190464, 0.6936707, 0.0262500, -0.0332282, -1, 1, 2, 4, 16.72019)
    print("MoveL")
    move_l(443.9821, 214.9465, 340.3785, 0.7190471, 0.6936699, 0.0262508, -0.0332300, -1, 1, 2, 4, 6.85925)

    
    