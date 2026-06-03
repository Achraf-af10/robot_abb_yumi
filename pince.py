import time
import threading

# --- Fonctions Pince Gauche ---
def openL(robot):
    robot.set_rapid_variable("PythonCtrl/cmdGripL", "1", "T_ROB_L")
    time.sleep(2)

def closeL(robot):
    robot.set_rapid_variable("PythonCtrl/cmdGripL", "2", "T_ROB_L")
    time.sleep(2)

# --- Fonctions Pince Droite ---
def openR(robot):
    # Utilise le chemin PythonCtrlR défini dans votre RAPID
    robot.set_rapid_variable("PythonCtrlR/cmdGrip", "1", "T_ROB_R")
    time.sleep(2)

def closeR(robot):
    robot.set_rapid_variable("PythonCtrlR/cmdGrip", "2", "T_ROB_R")
    time.sleep(2)

# --- Fonctions Combinées (Simultanées) ---
def openRL(robot):
    """Ouvre les deux pinces simultanément"""
    t1 = threading.Thread(target=openR, args=(robot,))
    t2 = threading.Thread(target=openL, args=(robot,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

def closeRL(robot):
    """Ferme les deux pinces simultanément"""
    t1 = threading.Thread(target=closeR, args=(robot,))
    t2 = threading.Thread(target=closeL, args=(robot,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()