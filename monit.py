import argparse
import json
import os
import datetime
import logging
from monitoring import check_system

def setup_logging():
    log_file_path = 'var/monit.log'  # Utilisez le chemin relatif pour le fichier log
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_report(data):
    report_directory = 'var/monit'  # Chemin relatif pour le répertoire de rapport
    os.makedirs(report_directory, exist_ok=True)  # Crée le répertoire s'il n'existe pas
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    report_path = f"{report_directory}/report_{timestamp}.json"
    with open(report_path, 'w') as file:
        json.dump(data, file, separators=(',', ':'))  # Supprime les espaces inutiles
    return report_path

def parse_arguments():
    parser = argparse.ArgumentParser(description="monit.py - Outil de monitoring système")
    parser.add_argument('command', choices=['check', 'list', 'get'], help='Commande à exécuter')
    parser.add_argument('arguments', nargs='*', help='Arguments supplémentaires pour la commande')
    return parser.parse_args()

def main():
    args = parse_arguments()
    setup_logging()

    if args.command == 'check':
        tcp_ports = [80, 443]  # À remplacer par la configuration réelle
        report_data = check_system(tcp_ports)
        report_path = save_report(report_data)
        logging.info(f"Check effectué, rapport enregistré sous : {report_path}")

    elif args.command == 'list':
    report_directory = 'var/monit'  # Chemin relatif pour le répertoire de rapport
    # Vérifiez que le répertoire existe
    if not os.path.exists(report_directory):
        print("Aucun rapport n'a été trouvé.")
        return
    
    # Utilisez glob pour lister tous les fichiers JSON dans le répertoire
    reports = glob.glob(f"{report_directory}/*.json")
    
    if reports:
        print("Rapports disponibles :")
        for report in reports:
            print(os.path.basename(report))  # Affiche uniquement le nom de fichier, pas le chemin complet
    else:
        print("Aucun rapport n'a été trouvé.")

    elif args.command == 'get':
        # Récupérer un rapport spécifique
        pass

if __name__ == "__main__":
    main()

