from flask import Flask, send_from_directory, abort, jsonify, redirect
import os

# Création de l'objet Flask
app = Flask(__name__)
app.secret_key = b'SECRET_KEY'

# Chemin du répertoire contenant les rapports
REPERTOIRE_RAPPORTS = 'var/monit'

@app.route('/')
def accueil():
    # Redirection vers la liste des rapports
    return redirect('/rapports', code=302)

@app.route('/rapports', methods=['GET'])
def lister_rapports():
    # Essaie de lister les fichiers dans le répertoire des rapports
    try:
        # Récupération uniquement des fichiers pour éviter de lister les sous-dossiers
        rapports = [f for f in os.listdir(REPERTOIRE_RAPPORTS) if os.path.isfile(os.path.join(REPERTOIRE_RAPPORTS, f))]
        return jsonify(rapports)
    except OSError as e:
        # En cas de problème (ex: dossier inexistant), renvoie une erreur 500
        abort(500, description=str(e))

@app.route('/rapports/<nom_rapport>', methods=['GET'])
def recuperer_rapport(nom_rapport):
    # Essaie d'envoyer le fichier demandé
    try:
        # Utilise send_from_directory pour sécuriser l'envoi des fichiers
        return send_from_directory(REPERTOIRE_RAPPORTS, nom_rapport, as_attachment=True)
    except FileNotFoundError:
        # Si le fichier n'existe pas, renvoie une erreur 404
        abort(404, description="Fichier non trouvé")

if __name__ == '__main__':
    # Lancement du serveur sur toutes les interfaces disponibles, sur le port 5000
    # Désactivation du mode debug en production
    app.run(host='0.0.0.0', port=5000, debug=False)