import os
import random
import string
import subprocess
from datetime import datetime

# Configuration des extensions et des formats de commentaires
# Format : { extension: (début, fin) }
CONFIG = {
    ".php": ("/*", "*/"),
    ".js": ("/*", "*/"),
    ".css": ("/*", "*/"),
    ".html": ("")
}

def generate_noise(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def run_chaos():
    # Définition du répertoire de travail (celui du script)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    
    modified_count = 0
    
    for root, dirs, files in os.walk("."):
        if ".git" in dirs:
            dirs.remove(".git")
            
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in CONFIG:
                file_path = os.path.join(root, file)
                start, end = CONFIG[ext]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                noise = generate_noise()
                
                comment = f"\n{start} Auto-Gen: {timestamp} | ID: {noise} {end}\n"
                
                try:
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write(comment)
                    modified_count += 1
                except Exception as e:
                    print(f"[ERREUR FICHIER] {file_path}: {e}")

    return modified_count

def git_sync():
    try:
        # Ajout, Commit et Push
        subprocess.run(["git", "add", "."], check=True)
        msg = f"chore: automated update {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("--- SYNC GIT REUSSIE ---")
    except subprocess.CalledProcessError as e:
        print(f"--- ERREUR GIT : {e} ---")

if __name__ == "__main__":
    count = run_chaos()
    if count > 0:
        print(f"--- {count} FICHIERS MODIFIES ---")
        git_sync()
    else:
        print("--- AUCUN FICHIER COMPATIBLE TROUVE ---")
