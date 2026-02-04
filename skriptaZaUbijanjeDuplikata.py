'''ovo je program koji treba da obrise slike iz skupnog foldera, koje postoje u nekoj bekap strukturi na eksternom recimo. '''

import os
import tkinter.messagebox as messagebox

from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import hashlib

def compute_hash(filepath):
    with open(filepath, 'rb') as f:
        hash_md5 = hashlib.md5()
        data = f.read(262144)  # Read in 256KB chunks
        hash_md5.update(data)
    return hash_md5.hexdigest()

#obavezno obrisati sve razmake iz putanje

root = tk.Tk()
root.withdraw()  # Hide the main window
putanjaDzumle = filedialog.askdirectory(title='Pronadji direktorijum gde je sve dzumle')

if not putanjaDzumle:
    messagebox.showerror("Error", "No directory selected for dzumle")
    os.sys.exit("No directory selected for dzumle")

try:
    putanjaDzumle = putanjaDzumle.replace("'", "").replace('"', "").replace(" ", "")
    putanjaDzumle = Path(putanjaDzumle).resolve()
except Exception as e:
    os.sys.exit(f"Error processing dzumle path: {e}")

if not os.path.exists(putanjaDzumle):
    os.sys.exit(f"nije dobra putanja Dzumle:\n {putanjaDzumle}")



# root.withdraw()  # Hide the main window
putanjaBekap = filedialog.askdirectory(title='Pronadji direktorijum gde je sve bekapovano i postoji struktura')

if not putanjaBekap:
    messagebox.showerror("Error", "No directory selected for bekap")
    os.sys.exit("No directory selected for bekap")

try:
    putanjaBekap = putanjaBekap.replace("'", "").replace('"', "").replace(" ", "")
    putanjaBekap = Path(putanjaBekap).resolve()
except Exception as e:
    messagebox.showerror("Error", f"processing bekap path: {e}")
    os.sys.exit(f"Error processing bekap path: {e}")

if not os.path.exists(putanjaBekap):
    messagebox.showerror("Error", f"nije dobra putanja gde postoji struktura:\n {putanjaBekap}")
    os.sys.exit(f"nije dobra putanja gde postoji struktura:\n {putanjaBekap}")

# Collect all file hashes from backup directory
backup_hashes = set()
for root, _, files in os.walk(putanjaBekap):
    for file in files:
        filepath = os.path.join(root, file)
        h = compute_hash(filepath)
        if h:
            backup_hashes.add(h)
            print(f"hesiranfajl: {filepath} sa hash-om {h}")

def compare_and_delete_files_recursive(directory1, backup_hashes):
    obrisani = 0
    for root, _, files in os.walk(directory1):
        for file in files:
            filepath = os.path.join(root, file)
            print(f"Proveravam fajl: {filepath}")
            h = compute_hash(filepath)
            if h in backup_hashes:
                try:
                    os.remove(filepath)
                    obrisani += 1
                    print(f"Obrisano {filepath}; obrisani broj {obrisani}")
                except OSError as e:
                    print(f"Greska u brisanju {filepath}: {e}")
    
    print(f"Ukupno obrisanih fajlova: {obrisani}")
      
    messagebox.showinfo("Info", f"Ukupno obrisanih fajlova: {obrisani}")

# Example usage:
directory1 = putanjaDzumle
directory2 = putanjaBekap
compare_and_delete_files_recursive(directory1, backup_hashes)
print("zavrsen pregled fajlova------------------------------------------------------------------")
messagebox.showinfo("Info", "Zavrsen pregled fajlova")
