
from flask import Flask, request, send_from_directory, jsonify
import os
from pathlib import Path
import time

app = Flask(__name__)

# Configuration
PLY_FOLDER = "./ply_files"
MAX_FILES = 10

# Assurez-vous que le dossier existe
os.makedirs(PLY_FOLDER, exist_ok=True)

def clean_old_ply_files(directory, max_files=10):
    # Liste tous les fichiers .ply dans le répertoire
    ply_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".ply")]
    
    # Si le nombre de fichiers dépasse max_files
    if len(ply_files) > max_files:
        # Trie les fichiers par date de modification
        ply_files.sort(key=os.path.getmtime)
        # Supprime les fichiers les plus anciens
        deleted_files = []
        for file in ply_files[:-max_files]:
            os.remove(file)
            deleted_files.append(file)
        return deleted_files
    return []

@app.route('/clean', methods=['POST'])
def clean_files():
    # Appelle la fonction de nettoyage
    deleted_files = clean_old_ply_files(PLY_FOLDER)
    if deleted_files:
        return jsonify({"status": "success", "deleted_files": deleted_files})
    else:
        return jsonify({"status": "success", "message": "No files deleted. Directory is within limits."})


@app.route("/upload", methods=["POST"])
def upload_file():
    """Permet d'ajouter un fichier .ply."""
    if "file" not in request.files:
        return "No file part in the request", 400

    file = request.files["file"]

    if file.filename == "":
        return "No file selected for uploading", 400

    if not file.filename.endswith(".ply"):
        return "Only .ply files are allowed", 400

    save_path = os.path.join(PLY_FOLDER, file.filename)
    file.save(save_path)
    print(f"Uploaded file: {save_path}")

    # Nettoyer les anciens fichiers
    clean_old_files()

    return "File uploaded successfully", 200


@app.route("/files", methods=["GET"])
def list_files():
    """Liste les fichiers .ply disponibles."""
    files = [f.name for f in Path(PLY_FOLDER).glob("*.ply")]
    return jsonify(files)


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    """Permet de télécharger un fichier spécifique."""
    if not filename.endswith(".ply"):
        return "Invalid file type requested", 400

    try:
        return send_from_directory(PLY_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404


if __name__ == "__main__":
    #app.run(debug=True)    
    # Écouter sur toutes les interfaces réseau, pas seulement localhost
    app.run(host='0.0.0.0', port=5000, debug=True)
