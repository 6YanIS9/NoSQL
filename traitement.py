import pandas as pd
import sqlite3

# Charger le fichier Excel
file_path = "/mnt/data/crimes-et-delits-enregistres-par-les-services-de-gendarmerie-et-de-police-depuis-2012.xlsx"
xls = pd.ExcelFile(file_path)

# Connexion à SQLite
conn = sqlite3.connect("forces_ordre.db")
cursor = conn.cursor()

# Création des tables en fonction du MCD
cursor.execute("""
CREATE TABLE IF NOT EXISTS infractions (
    code_infr TEXT PRIMARY KEY,
    lib_infr TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS annee (
    annee INTEGER PRIMARY KEY
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS brigade (
    id_brigade INTEGER PRIMARY KEY,
    lib_brigade TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS perimetres (
    lib_perimetre TEXT PRIMARY KEY
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS force_ordre (
    force_ordre TEXT PRIMARY KEY
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS departements (
    code_dep TEXT PRIMARY KEY,
    nom_dep TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS fait (
    id_fait INTEGER PRIMARY KEY AUTOINCREMENT,
    nb_infraction INTEGER,
    code_infr TEXT,
    annee INTEGER,
    id_brigade INTEGER,
    FOREIGN KEY (code_infr) REFERENCES infractions(code_infr),
    FOREIGN KEY (annee) REFERENCES annee(annee),
    FOREIGN KEY (id_brigade) REFERENCES brigade(id_brigade)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS intervenir (
    id_brigade INTEGER,
    lib_perimetre TEXT,
    PRIMARY KEY (id_brigade, lib_perimetre),
    FOREIGN KEY (id_brigade) REFERENCES brigade(id_brigade),
    FOREIGN KEY (lib_perimetre) REFERENCES perimetres(lib_perimetre)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS se_situer (
    id_brigade INTEGER,
    code_dep TEXT,
    PRIMARY KEY (id_brigade, code_dep),
    FOREIGN KEY (id_brigade) REFERENCES brigade(id_brigade),
    FOREIGN KEY (code_dep) REFERENCES departements(code_dep)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appartenir (
    id_brigade INTEGER,
    force_ordre TEXT,
    PRIMARY KEY (id_brigade, force_ordre),
    FOREIGN KEY (id_brigade) REFERENCES brigade(id_brigade),
    FOREIGN KEY (force_ordre) REFERENCES force_ordre(force_ordre)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS faire_partie (
    lib_perimetre TEXT,
    force_ordre TEXT,
    PRIMARY KEY (lib_perimetre, force_ordre),
    FOREIGN KEY (lib_perimetre) REFERENCES perimetres(lib_perimetre),
    FOREIGN KEY (force_ordre) REFERENCES force_ordre(force_ordre)
)
""")

# Valider les changements
conn.commit()

# Enregistrer la base de données dans un fichier .db

# Récupérer les noms des feuilles
sheets = xls.sheet_names


print("Base de données créée et peuplée avec succès !")
