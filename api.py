from flask import Flask, send_from_directory, abort, jsonify
import os

# on crée un ptit objet Flask, nécessaire pour ajouter des routes
app = Flask(__name__)
app.secret_key = b'SECRET_KEY'

# Chemin du répertoire contenant les rapports
REPERTOIRE_RAPPORTS = 'var/monit'

@app.route('/rapports', methods=['GET'])
def lister_rapports():
    # On essaie de lister les fichiers dans le répertoire des rapports
    try:
        # On récupère uniquement les fichiers pour éviter de lister les sous-dossiers
        rapports = [f for f in os.listdir(REPERTOIRE_RAPPORTS) if os.path.isfile(os.path.join(REPERTOIRE_RAPPORTS, f))]
        return jsonify(rapports)
    except OSError as e:
        # Si y'a un souci, genre le dossier n'existe pas, on renvoie une erreur 500
        abort(500, description=str(e))

@app.route('/rapports/<nom_rapport>', methods=['GET'])
def recuperer_rapport(nom_rapport):
    # On essaie d'envoyer le fichier demandé
    try:
        # On utilise send_from_directory pour sécuriser l'envoi des fichiers
        return send_from_directory(REPERTOIRE_RAPPORTS, nom_rapport, as_attachment=True)
    except FileNotFoundError:
        # Si le fichier n'existe pas, on renvoie une erreur 404
        abort(404, description="Fichier non trouvé")

if __name__ == '__main__':
    # On lance le serveur sur toutes les interfaces disponibles, sur le port 5000
    # On désactive le debug en prod, c'est juste là pour le développement
    app.run(host='0.0.0.0', port=5000, debug=False)
