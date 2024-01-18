import argparse
import json
import os
import datetime
import logging
from datetime import datetime, timedelta
import glob
from monitoring import check_system

def setup_logging():
    log_file_path = 'var/monit.log'  # Chemin relatif pour le fichier log
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    logging.basicConfig(filename=log_file_path, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        encoding='utf-8')  # Ajout de l'encodage UTF-8


def save_report(data):
    report_directory = 'var/monit'  # Chemin relatif pour le répertoire de rapport
    os.makedirs(report_directory, exist_ok=True)  # Crée le répertoire s'il n'existe pas
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
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
        if args.arguments and args.arguments[0] == 'last':
            report_directory = 'var/monit'
            try:
                # Liste tous les fichiers de rapport et trouve le plus récent
                report_files = [os.path.join(report_directory, f) for f in os.listdir(report_directory) if os.path.isfile(os.path.join(report_directory, f))]
                latest_report = max(report_files, key=os.path.getmtime)
                
                # Ouvre et affiche le contenu du dernier rapport
                with open(latest_report, 'r') as file:
                    report_data = json.load(file)
                    print(json.dumps(report_data, indent=4))
            except ValueError:
                print("Aucun rapport n'a été trouvé.")
            except Exception as e:
                print(f"Erreur lors de la lecture du rapport : {e}")
    
        if args.arguments and args.arguments[0] == 'avg':
            try:
                hours = int(args.arguments[1])  # Convertit le deuxième argument en nombre d'heures
                cutoff_time = datetime.now() - timedelta(hours=hours)
                print(f"Cutoff time: {cutoff_time}")

                report_directory = 'var/monit'
                report_files = glob.glob(f"{report_directory}/*.json")
                print(f"Tous les rapports: {report_files}")

                # Filtrez les rapports des X dernières heures
                recent_reports = [file for file in report_files if datetime.fromtimestamp(os.path.getmtime(file)) > cutoff_time]
                print(f"Rapports récents: {recent_reports}") 
                # Initialisation des variables pour le calcul des moyennes
                total_ram, total_cpu, count = 0, 0, 0

                for report_file in recent_reports:
                    with open(report_file, 'r') as file:
                        data = json.load(file)
                        total_ram += data['ram']['percent']
                        total_cpu += data['cpu']['cpu_percent']
                        count += 1

                if count > 0:
                    avg_ram = total_ram / count
                    avg_cpu = total_cpu / count
                    print(f"Moyenne sur les {hours} dernières heures:\nRAM: {avg_ram}%\nCPU: {avg_cpu}%")
                else:
                    print("Aucun rapport trouvé dans la période spécifiée.")

            except IndexError:
                print("Veuillez spécifier le nombre d'heures.")
            except ValueError:
                print("Veuillez fournir un nombre valide d'heures.")

if __name__ == "__main__":
    main()

