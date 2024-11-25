# repo pour tester la gestion des fichiers ply

# prerequis packages
pip install flask requests

Lancer le serveur.py
python serveur.py

Lancer le client si besoin ou alors les commandes curl ci dessous pour tester les routes
python client.py





# lister les fichiers ply accessibles
curl http://127.0.0.1:5000/files

# recuperer un fichier ply
curl -O http://127.0.0.1:5000/download/fichier7.ply

# clean les fichiers ply
curl -X POST http://127.0.0.1:5000/clean

# autorisation pour le port 5000 sous linux pour communiquer entre deux PC
sudo ufw allow 5000 
# attention se mettre en ethernet pour etre sure que tout fonctionne

# test_flask
