from flask import Flask, send_from_directory, abort, jsonify
import os
import json

app = Flask(__name__)
app.secret_key = b'SECRET_KEY'

REPERTOIRE_RAPPORTS = 'var/monit'

@app.route('/rapports', methods=['GET'])
def lister_rapports():
    try:
        rapports = [f for f in os.listdir(REPERTOIRE_RAPPORTS)
                    if os.path.isfile(os.path.join(REPERTOIRE_RAPPORTS, f))]
        return jsonify(rapports)
    except OSError as e:
        abort(500, description=str(e))

@app.route('/rapports/<nom_rapport>', methods=['GET'])
def recuperer_rapport(nom_rapport):
    try:
        chemin_complet = os.path.join(REPERTOIRE_RAPPORTS, nom_rapport)
        if os.path.exists(chemin_complet) and os.path.isfile(chemin_complet):
            with open(chemin_complet, 'r') as f:
                contenu_rapport = json.load(f)
            return jsonify(contenu_rapport)
        else:
            abort(404, description="Fichier non trouvé")
    except json.JSONDecodeError as e:
        abort(500, description="Erreur de décodage JSON: " + str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
