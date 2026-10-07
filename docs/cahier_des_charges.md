**CAHIER DES CHARGES**

Logiciel de gestion de

**FRAMINO FITNESS CLUB**

*Application exécutée en local*

Version 1.0 · Octobre 2026

## 1. Présentation du projet

### 1.1 Objet

Ce document décrit les besoins pour un logiciel de gestion de la salle
de sport **Framino Fitness Club**. Le logiciel couvre :

- les clients, abonnements et visites ;

- le personnel (coachs, caissiers) ;

- les produits, les services et le stock ;

- le matériel et sa maintenance ;

- la caisse et les charges ;

- le tableau de bord du promoteur.

### 1.2 Contraintes d'exécution

| **Exigence** | **Description** |
|----|----|
| Exécution locale | L'application tourne directement sur le poste de la salle, sans serveur distant ni hébergement cloud. |
| Fonctionnement hors ligne | Toutes les fonctions sont disponibles sans connexion Internet. |
| Base de données locale | Les données sont stockées dans une base locale (par exemple SQLite). |
| Sauvegarde | Sauvegarde automatique quotidienne et sauvegarde manuelle (clé USB, disque externe), avec une fonction de restauration. |
| Multi-postes (option) | Possibilité d'utiliser le logiciel sur plusieurs postes reliés au réseau local de la salle (accueil, caisse, bureau). |
| Ergonomie | Interface simple en français, utilisable par du personnel non technique. |
| Impressions et exports | Impression des reçus et export des rapports en PDF et Excel. |

## 2. Données gérées (objets métier)

### 2.1 Personnel

Le **Personnel** est une fiche unique pour chaque personne. Les coachs
et les caissiers **sont des membres du personnel** : leurs fiches
**complètent** la fiche Personnel sans la dupliquer.

| **Champ**       | **Description**                                          |
|-----------------|----------------------------------------------------------|
| Matricule       | Identifiant unique                                       |
| Nom, Prénom     |                                                          |
| Téléphone       |                                                          |
| Fonction        | Administrateur, coach, caissier, agent d'entretien, etc. |
| Salaire         | Montant mensuel                                          |
| Prime           |                                                          |
| Date d'embauche |                                                          |
| Statut          | Actif / inactif                                          |

#### Complément Coach

| **Champ**              | **Description**                        |
|------------------------|----------------------------------------|
| Personnel              | Lien vers la fiche Personnel           |
| Nom de coach           | Nom d'usage                            |
| Domaines de compétence | Lien vers une ou plusieurs disciplines |

#### Complément Caissier

| **Champ**       | **Description**              |
|-----------------|------------------------------|
| Personnel       | Lien vers la fiche Personnel |
| Parrain         | Membre du personnel référent |
| Caisse affectée |                              |

|  |
|----|
| **Règle anti-doublon :** une même personne n'a qu'une seule fiche Personnel, même si elle occupe plusieurs fonctions (par exemple coach et caissier). |

### 2.2 Client

| **Champ** | **Description** |
|----|----|
| Code client | Identifiant unique |
| Nom, Prénom |  |
| Sexe |  |
| Téléphone |  |
| Date de naissance |  |
| Adresse |  |
| Objectif sportif | Perte de poids, prise de masse, remise en forme, etc. |
| Date d'inscription |  |
| Statut | Actif / suspendu / expiré (statut mis à jour automatiquement selon les abonnements) |

### 2.3 Discipline

| **Champ**       | **Description**        |
|-----------------|------------------------|
| Nom             |                        |
| Type            |                        |
| Description     |                        |
| Tarif           |                        |
| Coachs associés | Un ou plusieurs coachs |

### 2.4 Type d'abonnement (catalogue)

- **Formule :** classique, VIP / Personal Training.

- **Durée :** mensuel, trimestriel, annuel.

- **Données à saisir :** nom, formule, durée en jours, prix et
  discipline éventuelle.

### 2.5 Abonnement (souscrit par un client)

| **Champ** | **Description** |
|----|----|
| Code abonnement | Identifiant unique |
| Client |  |
| Discipline |  |
| Type d'abonnement | Lien vers le catalogue |
| Prix |  |
| Date de début / Date de fin | La date de fin est calculée automatiquement |
| Statut | Actif / expiré / suspendu |
| Paiement associé | Lien vers le paiement, qui donne le mode de paiement et le caissier |

### 2.6 Programme sportif

| **Champ**                         | **Description** |
|-----------------------------------|-----------------|
| Client                            |                 |
| Coach                             |                 |
| Discipline                        |                 |
| Objectif                          |                 |
| Durée, Date de début, Date de fin |                 |
| Programme détaillé                |                 |
| Observations                      |                 |

### 2.7 Visite (passage en salle)

| **Champ**                        | **Description** |
|----------------------------------|-----------------|
| Client                           |                 |
| Date                             |                 |
| Heure d'entrée / Heure de sortie |                 |
| Type de séance                   |                 |
| Coach                            | Facultatif      |

|  |
|----|
| Au moment de l'entrée, le logiciel vérifie automatiquement que l'abonnement du client est valide. |

### 2.8 Service / prestation

| **Champ**           | **Description** |
|---------------------|-----------------|
| Nom                 |                 |
| Description         |                 |
| Prix                |                 |
| Durée               |                 |
| Discipline          | Facultatif      |
| Responsable / coach |                 |
| Statut              | Actif / inactif |

**Services prévus :** inscription, abonnement classique, abonnement VIP,
Personal Training, prise de paramètres, massage à la chaise,
kinésithérapie, challenges, marche sportive, campagnes et activités
spéciales.

### 2.9 Produit

| **Champ**                        | **Description**    |
|----------------------------------|--------------------|
| Référence                        | Identifiant unique |
| Nom                              |                    |
| Catégorie                        | Voir la section 3  |
| Taille, Sexe                     | Si applicable      |
| Fournisseur                      |                    |
| Prix d'achat / Prix de vente     |                    |
| Stock disponible / Stock minimum |                    |

### 2.10 Fournisseur

Nom, téléphone, adresse et produits ou matériel fournis.

## 3. Produits et gestion du stock

### 3.1 Catégories de produits

| **Catégorie** | **Exemples** |
|----|----|
| Articles sportifs | Serviettes, tenues, chaussures, gants, polos, t-shirts |
| Boissons | Boissons naturelles, boissons énergisantes, eau minérale |

|  |
|----|
| Les prestations (marche sportive, massage, kinésithérapie, etc.) sont gérées comme des **services** (section 2.8) et non comme des produits en stock. |

### 3.2 Fonctions de stock

- Entrées en stock (réceptions des fournisseurs).

- Sorties de stock (ventes, pertes, casse).

- Ventes et retours.

- Inventaire physique avec calcul des écarts.

- **Alerte de stock faible** dès que le stock disponible est inférieur
  ou égal au stock minimum.

- Historique complet des mouvements : date, type, quantité et
  utilisateur.

## 4. Matériel de sport

### 4.1 Fiche matériel

| **Champ**                      | **Description**                        |
|--------------------------------|----------------------------------------|
| Numéro / référence             | Identifiant unique                     |
| Désignation                    |                                        |
| Catégorie                      | Cardio, musculation, accessoires, etc. |
| Taille, Couleur, Particularité |                                        |
| Quantité                       |                                        |
| Date d'achat / Prix d'achat    |                                        |
| Fournisseur                    |                                        |
| Localisation                   |                                        |
| État                           | Neuf / bon / à réparer / hors service  |
| Fin de garantie                |                                        |
| Observation                    |                                        |

**Exemples :** tapis de course, vélos, rameurs, haltères, barres,
disques, bancs, machines de musculation, steps, tapis de sol.

### 4.2 Maintenance

| **Champ**                     | **Description** |
|-------------------------------|-----------------|
| Matériel concerné             |                 |
| Date                          |                 |
| Nature de la panne            |                 |
| Description de l'intervention |                 |
| Technicien                    |                 |
| Pièces changées et quantité   |                 |
| Coût                          |                 |
| Prochaine maintenance         |                 |
| Observation                   |                 |

|  |
|----|
| Le logiciel calcule le **coût total d'entretien de chaque machine** sur une période donnée. |

## 5. Paiements et caisse

### 5.1 Paiement

| **Champ** | **Description** |
|----|----|
| Numéro de reçu | Unique, généré automatiquement |
| Client |  |
| Objet | Inscription, abonnement, produit, service, Personal Training, autre |
| Montant |  |
| Date et heure |  |
| Mode de paiement | Espèces, Mobile Money, virement, carte bancaire, autre |
| Caissier |  |
| Observation |  |

### 5.2 Gestion de la caisse

- Ouverture et clôture de la caisse par caissier, avec le fond de
  caisse.

- Calcul de l'**écart de caisse** entre le montant théorique et le
  montant compté.

- Totaux encaissés par jour, par semaine et par mois.

- Répartition des encaissements par caissier, par type de service, par
  mode de paiement, et pour les ventes de produits.

- Impression du reçu client.

## 6. Charges de la salle

### 6.1 Catégories de charges

| **Catégorie** | **Exemples** |
|----|----|
| Charges fixes | Salaires, électricité, eau, Wi-Fi / Internet |
| Entretien | Produits d'entretien, nettoyage, petites réparations, entretien des locaux |
| Provision / Réserve | Épargne régulière pour les dépenses futures ou imprévues |

### 6.2 Fiche charge

Type, désignation, montant, date, échéance, mode de paiement,
responsable, justificatif (fichier joint), statut (payée / à payer) et
observation.

## 7. Tableau de bord du promoteur

### 7.1 Indicateurs

| **Clients et activité** | **Finances** | **Exploitation** |
|----|----|----|
| Nombre total de clients | Chiffre d'affaires du jour | Produits vendus |
| Clients actifs | Chiffre d'affaires du mois | État des stocks |
| Nouveaux clients | Charges du mois | Matériel en maintenance |
| Abonnements actifs | Bénéfice estimatif | Salaires à payer |
| Abonnements bientôt expirés | Provisions disponibles |  |
| Nombre de visites |  |  |

### 7.2 Alertes

- Abonnement arrivant à expiration (délai paramétrable, par exemple 7
  jours)

- Stock faible

- Maintenance à effectuer

- Salaire à payer

- Charge à payer

- Garantie de matériel arrivant à expiration

## 8. Gestion des utilisateurs et des droits d'accès

Chaque utilisateur se connecte avec un identifiant et un mot de passe.
Il ne voit et ne modifie que les données liées à son rôle.

| **Rôle** | **Accès principal** |
|----|----|
| Administrateur | Tous les modules, gestion des utilisateurs, paramètres, sauvegardes |
| Promoteur | Tableau de bord, rapports, finances, charges (consultation et validation) |
| Caissier | Paiements, caisse, ventes, inscriptions |
| Coach | Ses clients, programmes sportifs, visites |
| Gestionnaire de stock et de matériel (option) | Stock, inventaire, matériel, maintenance |

|  |
|----|
| Toutes les actions sensibles (suppression, modification de paiement, correction de stock) sont **journalisées** : utilisateur, date et action. |

## 9. Relations entre les éléments

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td><p><strong>CLIENT → ABONNEMENT → PAIEMENT → CAISSE</strong></p>
<p><strong>CLIENT → VISITE</strong></p>
<p><strong>CLIENT → PROGRAMME SPORTIF → COACH → PERSONNEL</strong></p>
<p><strong>CAISSIER → PERSONNEL</strong></p>
<p><strong>PRODUIT → MOUVEMENT DE STOCK → VENTE → PAIEMENT</strong></p>
<p><strong>SERVICE → PAIEMENT</strong></p>
<p><strong>MATÉRIEL → MAINTENANCE → TECHNICIEN</strong></p>
<p><strong>SALLE → CHARGES → DÉPENSES</strong></p></td>
</tr>
</tbody>
</table>

Cette structure permet au développeur de construire une base de données
cohérente, sans doublons.

## 10. Livrables attendus

- L'application installable en local, avec son guide d'installation.

- La base de données initialisée, avec les catalogues de disciplines, de
  services et de catégories pré-remplis.

- Un manuel utilisateur pour chaque rôle.

- La procédure de sauvegarde et de restauration.
