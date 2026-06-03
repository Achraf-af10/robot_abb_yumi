from abb_robot_client.rws import RWS

# Connexion
robot = RWS("http://10.2.30.126")

def print_formatted_data(mech_unit):
    """Affiche la RobTarget au format (X, Y, Z, Q1, Q2, Q3, Q4, C1, C4, C6, CX, E1)"""
    rt = robot.get_robtarget(mech_unit)
    jt = robot.get_jointtarget(mech_unit)
    e1 = jt.extax[0]
    
    # Formatage : (X, Y, Z, Q1, Q2, Q3, Q4, C1, C4, C6, CX, E1)
    out = (f"({rt.trans[0]:.4f}, {rt.trans[1]:.4f}, {rt.trans[2]:.4f}, "
           f"{rt.rot[0]:.7f}, {rt.rot[1]:.7f}, {rt.rot[2]:.7f}, {rt.rot[3]:.7f}, "
           f"{int(rt.robconf[0])}, {int(rt.robconf[1])}, {int(rt.robconf[2])}, {int(rt.robconf[3])}, "
           f"{e1:.5f})")
    
    print(f"{mech_unit} (MoveL format): {out}")

def get_joints_list(mech_unit):
    """Retourne les joints + Axe 7 dans une seule liste [J1..J6, J7]"""
    jt = robot.get_jointtarget(mech_unit)
    # On convertit les robax en liste et on ajoute l'axe externe (J7)
    joints = [round(float(v), 2) for v in jt.robax]
    e1 = round(float(jt.extax[0]), 2)
    joints.append(e1)
    return joints

# --- AFFICHAGE ---
print("--- POSITION ACTUELLE (MOVE L FORMAT) ---")
print_formatted_data("ROB_L")
print_formatted_data("ROB_R")

print("\n--- POSITION ACTUELLE (MOVE J FORMAT) ---")
print(f"ROB_L: {get_joints_list('ROB_L')}")
print(f"ROB_R: {get_joints_list('ROB_R')}")