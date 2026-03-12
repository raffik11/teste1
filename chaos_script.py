import os
import random
import string
import subprocess
from datetime import datetime
import holidays

# --- CONFIGURATION ---
COUNTRY = 'FR' 
# Définition précise des balises de commentaires
CONFIG = {
    ".php": ("/*", "*/"),
    ".js": ("/*", "*/"),
    ".css": ("/*", "*/"),
    ".html": ("")
}

def is_workday():
    today = datetime.now().date()
    fr_holidays = holidays.CountryHoliday(COUNTRY)
    
    # Vérification Week-end
    if today.weekday() >= 5:
        print(f"--- REPOS (Week-end) ---")
        return False
        
    # Vérification Jour Férié
    if today in fr_holidays:
        print(f"--- REPOS (Férié : {fr_holidays.get(today)}) ---")
        return False
        
    return True

def generate_noise(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def run_chaos():
    # Force le script à travailler dans son propre dossier
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if base_dir != "":
        os.chdir(base_dir)
    
    all_eligible_files = []
    for root, dirs, files in os.walk("."):
        if ".git" in dirs:
            dirs.remove(".git")
        if "venv" in dirs: # On ne touche pas aux fichiers de l'environnement virtuel
            dirs.remove("venv")
            
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in CONFIG:
                all_eligible_files.append((os.path.join(root, file), ext))

    if not all_eligible_files:
        print("Aucun fichier .php, .js, .css ou .html détecté.")
        return 0

    # --- RANDOMISATION DES FICHIERS ---
    # On choisit un nombre aléatoire de fichiers à modifier (entre 1 et le total)
    num_to_modify = random.randint(1, len(all_eligible_files))
    # On sélectionne les fichiers au hasard sans doublons
    files_to_process = random.sample(all_eligible_files, num_to_modify)
    
    print(f"Sélection aléatoire : {num_to_modify} fichiers sélectionnés sur {len(all_eligible_files)}")
    
    modified_count = 0
    for file_path, ext in files_to_process:
        start, end = CONFIG[ext]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        noise = generate_noise()
        
        # Construction du commentaire
        comment = f"\n{start} Chaos-Update: {timestamp} | ID: {noise} {end}\n"
        
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(comment)
            modified_count += 1
            print(f"  [OK] Modifié : {file_path}")
        except Exception as e:
            print(f"  [ERREUR] Impossible de modifier {file_path}: {e}")
            
    return modified_count

def git_sync():
    try:
        subprocess.run(["git", "add", "."], check=True)
        msg = f"chore: daily update {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("--- SYNC GIT REUSSIE ---")
    except subprocess.CalledProcessError as e:
        print(f"--- ERREUR GIT : {e} ---")

if __name__ == "__main__":
    # 1. Vérifie si on est un jour ouvré
    if not is_workday():
        exit()

    # 2. Ajout d'une chance de "ne rien faire" même en semaine (30% de repos)
    # Pour simuler une journée où tu n'as pas codé.
    if random.random() < 0.3:
        print("--- JOURNÉE SANS CODE (Aléatoire) ---")
        exit()

    # 3. Exécution
    count = run_chaos()
    if count > 0:
        print(f"Total : {count} fichiers modifiés.")
        git_sync()
