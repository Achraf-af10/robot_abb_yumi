from abb_robot_client.rws import RWS

# Connexion
robot = RWS("http://10.2.30.126")

# Récupération des logs parsés par la bibliothèque
logs = robot.read_event_log()

# Sécurité : On prend les 5 derniers, ou la totalité s'il y en a moins de 5
derniers_logs = logs[-5:] if len(logs) >= 5 else logs

print(f"=== AFFICHAGE DES {len(derniers_logs)} DERNIERS ÉVÉNEMENTS ===")
for entry in derniers_logs:
    # Optionnel : On ajoute un émoji selon s'il s'agit d'une erreur (type 3) ou d'un warning (type 2)
    statut = "ℹ️"
    if getattr(entry, 'type', None) == '3' or "error" in entry.title.lower():
        statut = "❌"
    elif getattr(entry, 'type', None) == '2' or "warning" in entry.title.lower():
        statut = "⚠️"

    print(f"{statut} Code = {entry.code} : {entry.title}")
    # Nettoyage des sauts de lignes superflus dans la description
    desc_propre = entry.desc.strip() if entry.desc else "Pas de description."
    print(f"   {desc_propre}")
    print("-" * 50)