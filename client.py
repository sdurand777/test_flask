
import requests

SERVER_URL = "http://127.0.0.1:5000"

# Upload a file
def upload_file(file_path):
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{SERVER_URL}/upload", files=files)
        print("Upload response:", response.text)

# List available files
def list_files():
    response = requests.get(f"{SERVER_URL}/files")
    if response.status_code == 200:
        print("Available files:", response.json())
    else:
        print("Error listing files:", response.text)

# Download a specific file
def download_file(filename, save_path):
    response = requests.get(f"{SERVER_URL}/download/{filename}")
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"File {filename} downloaded to {save_path}")
    else:
        print("Error downloading file:", response.text)


def call_clean_endpoint():
    try:
        # Faire une requête POST au serveur
        #response = requests.post(SERVER_URL)
        response = requests.post(f"{SERVER_URL}/clean")

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Afficher la réponse JSON
            print("Réponse du serveur :", response.json())
        else:
            print(f"Erreur : {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite : {e}")


if __name__ == "__main__":
    # Example usage:
    # Upload a file
    #upload_file("example.ply")

    # List files
    list_files()

    # Download a file
    download_file("3.ply", "downloaded_example.ply")

    # call clean endpoint
    call_clean_endpoint()
