Voici une proposition **complète** intégrant à la fois un **Modèle Conceptuel de Données (MCD)** et un **Modèle Logique de Données (MLD)**, construits à partir des informations disponibles (statistiques de crimes/délits par année, par force de l’ordre, par département, sur la période 2012-2022).

---

# 1. Modèle Conceptuel de Données (MCD)

Le MCD met l’accent sur les **entités**, leurs **associations** et les **cardinalités**.

## 1.1. Entités Principales

1. **INFRACTION**  
   - Représente un type de crime/délit.  
   - Attributs possibles :  
     - *id_infraction* (Identifiant unique)  
     - *libelle_infraction* (Nom ou libellé de l’infraction, ex. « Vol », « Homicide »…)  
     - *description_infraction* (Description plus détaillée, optionnel)

2. **FORCE_ORDRE**  
   - Représente l’organisme (Police Nationale, Gendarmerie Nationale, etc.) qui constate l’infraction.  
   - Attributs possibles :  
     - *id_organisation* (Identifiant unique)  
     - *nom_organisation* (ex. « Police Nationale », « Gendarmerie Nationale »)  
     - *type_organisation* (ex. « PN », « GN », si besoin)

3. **DÉPARTEMENT**  
   - Représente le département géographique.  
   - Attributs :  
     - *code_departement* (Code officiel, ex. « 75 », « 06 »…)  
     - *nom_departement* (ex. « Paris », « Alpes-Maritimes »…)  

4. **RÉGION** *(optionnel, en fonction du niveau de granularité souhaité)*  
   - Représente la région à laquelle est rattaché un département.  
   - Attributs :  
     - *id_region* (Identifiant unique)  
     - *nom_region*  

5. **FAIT**  
   - Représente l’enregistrement statistique agrégé : un certain *type d’infraction*, dans un *département*, constaté par une *force de l’ordre*, pour une *année* donnée, avec un *nombre* de cas.  
   - Attributs :  
     - *id_fait* (Identifiant unique, éventuellement auto-incrémenté)  
     - *annee* (Année, ex. 2012 à 2022)  
     - *nombre_faits* (Nombre de cas constatés)

## 1.2. Associations et Cardinalités

- **FAIT** ↔ **INFRACTION**  
  - Cardinalité : (1,n) côté Infraction → (0,n) côté Fait  
  - Signification : Une infraction peut apparaître dans plusieurs faits (pour différentes années, différents départements, etc.) ; chaque fait se rattache à une seule infraction.

- **FAIT** ↔ **FORCE_ORDRE**  
  - Cardinalité : (1,n) côté Force_Ordre → (0,n) côté Fait  
  - Signification : Une force de l’ordre peut enregistrer plusieurs faits ; chaque fait est enregistré par une seule force de l’ordre.

- **FAIT** ↔ **DÉPARTEMENT**  
  - Cardinalité : (1,n) côté Département → (0,n) côté Fait  
  - Signification : Un département peut être associé à plusieurs faits (chaque type d’infraction, chaque année, etc.) ; chaque fait concerne un seul département.

- **DÉPARTEMENT** ↔ **RÉGION** *(optionnel)*  
  - Cardinalité : (1,n) côté Région → (1,1) côté Département  
  - Signification : Une région regroupe plusieurs départements ; chaque département appartient à une seule région.

### Schéma Simplifié (Notation Textuelle)

```
           REGION
           [id_region]
           nom_region
                |
                | (1,n)
                |
      DEPARTEMENT
      [code_departement]
      nom_departement
                |
                | (1,n)
                |
               FAIT
     [id_fait, annee, nombre_faits]
               /   \  
              /     \ 
          (0,n)     (0,n)
            /         \
      INFRACTION    FORCE_ORDRE
     [id_infraction] [id_organisation]
     libelle_inf...  nom_organisation
     desc_inf...     type_organisation
```

---

# 2. Modèle Logique de Données (MLD)

Le MLD traduit le MCD en **tables**, en **champs** (avec types de données), en **clés primaires** (PK) et **clés étrangères** (FK).

## 2.1. Table INFRACTION
- **Nom de la table** : `INFRACTION`
- **Champs** :
  1. `id_infraction` : **PK**, entier (AUTO_INCREMENT ou équivalent)
  2. `libelle_infraction` : texte (varchar 100 par ex.)
  3. `description_infraction` : texte (varchar 255 ou TEXT, optionnel)

#### Contraintes
- **PK** : `(id_infraction)`

---

## 2.2. Table FORCE_ORDRE
- **Nom de la table** : `FORCE_ORDRE`
- **Champs** :
  1. `id_organisation` : **PK**, entier (AUTO_INCREMENT ou équivalent)
  2. `nom_organisation` : texte (varchar 100)
  3. `type_organisation` : texte (varchar 10 ou 20) (ex. « PN », « GN »), optionnel

#### Contraintes
- **PK** : `(id_organisation)`

---

## 2.3. Table RÉGION *(Optionnelle)*
- **Nom de la table** : `REGION`
- **Champs** :
  1. `id_region` : **PK**, entier (AUTO_INCREMENT ou équivalent)
  2. `nom_region` : texte (varchar 100)

#### Contraintes
- **PK** : `(id_region)`

---

## 2.4. Table DÉPARTEMENT
- **Nom de la table** : `DEPARTEMENT`
- **Champs** :
  1. `code_departement` : **PK**, texte (varchar 5) ou entier (selon le format choisi)
  2. `nom_departement` : texte (varchar 100)
  3. `id_region` : entier (FK vers `REGION.id_region`), **optionnel** si vous gérez la région

#### Contraintes
- **PK** : `(code_departement)`
- **FK** : `(id_region)` faisant référence à `REGION(id_region)`  
  - *ON UPDATE CASCADE / ON DELETE RESTRICT* (selon vos préférences)

---

## 2.5. Table FAIT
- **Nom de la table** : `FAIT`
- **Champs** :
  1. `id_fait` : **PK**, entier (AUTO_INCREMENT ou équivalent)
  2. `annee` : entier (ex. 2012-2022)
  3. `nombre_faits` : entier (ou bigint si volumes élevés)
  4. `id_infraction` : entier (FK vers `INFRACTION.id_infraction`)
  5. `id_organisation` : entier (FK vers `FORCE_ORDRE.id_organisation`)
  6. `code_departement` : texte (FK vers `DEPARTEMENT.code_departement`)

#### Contraintes
- **PK** : `(id_fait)`
- **FK** : `(id_infraction)` → `INFRACTION(id_infraction)`
- **FK** : `(id_organisation)` → `FORCE_ORDRE(id_organisation)`
- **FK** : `(code_departement)` → `DEPARTEMENT(code_departement)`

---

### 2.5.1. Index et clés potentielles

Selon votre usage, vous pouvez avoir besoin de créer des **clés composées** (pour éviter la duplication de la combinaison année + infraction + force de l’ordre + département). Par exemple :

- Un **index unique** sur `(annee, id_infraction, id_organisation, code_departement)`, ce qui empêcherait l’insertion de doublons pour la même année / même type de crime / même force / même département.

Exemple de contrainte :

```sql
ALTER TABLE FAIT
ADD CONSTRAINT UQ_Fait_Combinaison
UNIQUE (annee, id_infraction, id_organisation, code_departement);
```

---

# 3. Synthèse Visuelle du MLD

Une représentation tabulaire simplifiée :

```
TABLE INFRACTION
    id_infraction        PK
    libelle_infraction
    description_infraction

TABLE FORCE_ORDRE
    id_organisation      PK
    nom_organisation
    type_organisation

TABLE REGION (optionnelle)
    id_region            PK
    nom_region

TABLE DEPARTEMENT
    code_departement     PK
    nom_departement
    id_region            FK → REGION.id_region

TABLE FAIT
    id_fait             PK
    annee
    nombre_faits
    id_infraction       FK → INFRACTION.id_infraction
    id_organisation     FK → FORCE_ORDRE.id_organisation
    code_departement    FK → DEPARTEMENT.code_departement

    -- Optionnel: contrainte d'unicité pour éviter les doublons
    -- UNIQUE(annee, id_infraction, id_organisation, code_departement)
```

---

# 4. Conclusion

Ce **MCD** et ce **MLD** couvrent les besoins du projet tels que décrits :

- **INFRACTION** : définition des types d’infractions (crimes, délits…).  
- **FORCE_ORDRE** : distinction Police / Gendarmerie (ou d’autres organismes).  
- **DÉPARTEMENT** (et éventuellement **RÉGION**) : localisation géographique.  
- **FAIT** : la table *pivot* qui enregistre le *nombre de faits* pour un *type d’infraction*, dans un *département*, par une *force de l’ordre*, pour une *année* donnée.

Cette structure permet :
- L’alimentation directe via votre fichier Excel : chaque ligne correspond à un enregistrement dans `FAIT` (avec les clés étrangères vers les tables de référence).  
- La flexibilité pour ajouter ou enrichir d’autres dimensions (par exemple, la **commune**, le **mois**, le **mode opératoire**, etc.).  

Une fois implémenté, vous pourrez ensuite réaliser les requêtes analytiques souhaitées ou poursuivre la migration vers un modèle graphe (Neo4j) dans les phases ultérieures.