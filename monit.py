import argparse
import json
import os
import datetime
import logging
from monitoring import check_system

def setup_logging():
    log_file_path = 'var/monit.log'
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_report(data):
    # Enregistrez le rapport dans /var/monit/ avec un timestamp unique
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    report_path = f"/var/monit/report_{timestamp}.json"
    with open(report_path, 'w') as file:
        json.dump(data, file)
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
        # Ici, vous devez lire la configuration pour obtenir la liste des ports TCP à surveiller
        tcp_ports = [80, 443]  # Exemple de ports, à remplacer par la configuration réelle
        report_data = check_system(tcp_ports)
        report_path = save_report(report_data)
        logging.info(f"Check effectué, rapport enregistré sous : {report_path}")

    elif args.command == 'list':
        # Lister les rapports disponibles dans /var/monit/
        pass  # Implémentez la logique pour lister les fichiers de rapport

    elif args.command == 'get':
        # Récupérer un rapport spécifique
        pass  # Implémentez la logique pour récupérer et afficher un rapport spécifique

if __name__ == "__main__":
    main()

