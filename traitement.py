import sqlite3

# Connexion à la base de données (le fichier .db sera créé si il n'existe pas)
conn = sqlite3.connect('infractions.db')

# Création d'un curseur pour exécuter des requêtes SQL
cursor = conn.cursor()

# Création des tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS infractions (
    code_infr INT PRIMARY KEY,
    lib_infr VARCHAR(50)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS départements (
    code_dep VARCHAR(50) PRIMARY KEY,
    nom_dep VARCHAR(50) NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS force_odre (
    force_odre VARCHAR(50) PRIMARY KEY
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS annee (
    annee VARCHAR(50) PRIMARY KEY
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS périmètres (
    lib_perimetre VARCHAR(50) PRIMARY KEY,
    force_odre VARCHAR(50) NOT NULL,
    FOREIGN KEY(force_odre) REFERENCES force_odre(force_odre)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS brigade (
    id_brigade VARCHAR(50) PRIMARY KEY,
    lib_brigade VARCHAR(50) NOT NULL,
    lib_perimetre VARCHAR(50),
    code_dep VARCHAR(50) NOT NULL,
    force_odre VARCHAR(50) NOT NULL,
    FOREIGN KEY(lib_perimetre) REFERENCES périmètres(lib_perimetre),
    FOREIGN KEY(code_dep) REFERENCES départements(code_dep),
    FOREIGN KEY(force_odre) REFERENCES force_odre(force_odre)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS fait (
    code_infr INT,
    id_brigade VARCHAR(50),
    annee VARCHAR(50),
    nb_infraction INT,
    PRIMARY KEY(code_infr, id_brigade, annee),
    FOREIGN KEY(code_infr) REFERENCES infractions(code_infr),
    FOREIGN KEY(id_brigade) REFERENCES brigade(id_brigade),
    FOREIGN KEY(annee) REFERENCES annee(annee)
)
''')

# Enregistrement des modifications
conn.commit()

# Fermeture de la connexion
conn.close()

print("Base de données 'infractions.db' créée avec succès!")
