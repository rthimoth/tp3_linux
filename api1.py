from flask import Flask, jsonify, redirect
import os
import json

app = Flask(__name__)
app.secret_key = b'SECRET_KEY'
REPERTOIRE_RAPPORTS = 'var/monit'

@app.errorhandler(404)
def error404(e):
    return jsonify({'error': "404"}), 404

# @app.route('/')
# def rediriger_vers_rapports():
#     return redirect('/rapports')

@app.route('/rapports', methods=['GET'])
def lister_rapports_et_contenu():
    rapports = {}
    try:
        fichiers = [f for f in os.listdir(REPERTOIRE_RAPPORTS) if os.path.isfile(os.path.join(REPERTOIRE_RAPPORTS, f))]
        for fichier in fichiers:
            chemin_complet = os.path.join(REPERTOIRE_RAPPORTS, fichier)
            with open(chemin_complet, 'r', encoding='utf-8') as contenu_fichier:
                try:
                    contenu = json.load(contenu_fichier)
                except json.JSONDecodeError:
                    continue
                rapports[fichier] = contenu
        return jsonify(rapports)
    except OSError as e:
        abort(500, description=str(e))

@app.route('/rapports/<nom_rapport>', methods=['GET'])
def afficher_rapport(nom_rapport):
    chemin_complet = os.path.join(REPERTOIRE_RAPPORTS, nom_rapport)
    try:
        if os.path.isfile(chemin_complet):
            with open(chemin_complet, 'r', encoding='utf-8') as contenu_fichier:
                try:
                    contenu = json.load(contenu_fichier)
                    return jsonify(contenu)
                except json.JSONDecodeError:
                    abort(400, description="Le fichier n'est pas un JSON valide.")
        else:
            abort(404, description="Fichier non trouvé")
    except OSError as e:
        abort(500, description=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)


