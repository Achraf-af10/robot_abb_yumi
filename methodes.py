from abb_robot_client.rws import RWS

robot = RWS("http://192.168.1.100")

# Lister toutes les méthodes disponibles
methodes = [m for m in dir(robot) if not m.startswith("_")]
for m in methodes:
    print(m)