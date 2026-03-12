import os
import random
import string
import subprocess
from datetime import datetime
import holidays # Bibliothèque pour les jours fériés

# --- CONFIGURATION ---
COUNTRY = 'FR' # 'FR' pour la France, 'BE' pour la Belgique, 'CA' pour le Canada, etc.
CONFIG = {
    ".php": ("/*", "*/"),
    ".js": ("/*", "*/"),
    ".css": ("/*", "*/"),
    ".html": ("")
}

def is_workday():
    today = datetime.now().date()
    fr_holidays = holidays.CountryHoliday(COUNTRY)
    
    # 1. Vérifie si c'est le week-end (5 = Samedi, 6 = Dimanche)
    if today.weekday() >= 5:
        print(f"--- WEEK-END ({today}) : Pas de commit ---")
        return False
        
    # 2. Vérifie si c'est un jour férié
    if today in fr_holidays:
        print(f"--- JOUR FÉRIÉ ({fr_holidays.get(today)}) : Pas de commit ---")
        return False
        
    return True

def generate_noise(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def run_chaos():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if base_dir != "":
        os.chdir(base_dir)
    
    all_eligible_files = []
    for root, dirs, files in os.walk("."):
        if ".git" in dirs:
            dirs.remove(".git")
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in CONFIG:
                all_eligible_files.append((os.path.join(root, file), ext))

    if not all_eligible_files:
        return 0

    num_to_modify = random.randint(1, len(all_eligible_files))
    files_to_process = random.sample(all_eligible_files, num_to_modify)
    
    modified_count = 0
    for file_path, ext in files_to_process:
        start, end = CONFIG[ext]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        noise = generate_noise()
        comment = f"\n{start} Auto-Gen: {timestamp} | ID: {noise} {end}\n"
        
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(comment)
            modified_count += 1
        except Exception as e:
            print(f"[ERREUR] {file_path}: {e}")
    return modified_count

def git_sync():
    try:
        subprocess.run(["git", "add", "."], check=True)
        msg = f"chore: automated update {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("--- SYNC GIT REUSSIE ---")
    except subprocess.CalledProcessError as e:
        print(f"--- ERREUR GIT : {e} ---")

if __name__ == "__main__":
    # Vérification des jours ouvrables + fériés
    if is_workday():
        count = run_chaos()
        if count > 0:
            print(f"--- {count} FICHIERS MODIFIÉS ---")
            git_sync()
    else:
        # Le script s'arrête gentiment si c'est un jour de repos
        exit()
