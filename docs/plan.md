# Plan du projet – Framino Fitness Club

Statuts : ⬜ à faire · 🔄 en cours · ✅ terminé

## Lots

| Lot | Contenu | Réf. cahier | Statut |
|-----|---------|-------------|--------|
| 0 | Plan, modèle de données, socle Django (settings, Tailwind local, layout, pytest) | §1.2 | ✅ |
| 1 | Paramètres (loader, `charger_parametres`, page admin), comptes, 5 rôles, AuditLog, `seed_demo` | §8 | ⬜ |
| 2 | Personnel + compléments Coach / Caissier (OneToOne), matricule auto | §2.1 | ⬜ |
| 3 | Clients, Disciplines, Types d'abonnement, Abonnements (fin calculée, suspension, renouvellement), Programmes sportifs, Visites (contrôle d'accès), statut client auto | §2.2–2.7 | ⬜ |
| 4 | Paiements (reçus, impression), sessions de caisse (fond, écart, totaux, répartitions), annulation journalisée | §5 | ⬜ |
| 5 | Services, Produits, Fournisseurs, Stock (mouvements, inventaire, alerte stock), vente = mouvement + paiement | §2.8–2.10, §3 | ⬜ |
| 6 | Matériel + Maintenance + coût total d'entretien par machine sur période | §4 | ⬜ |
| 7 | Charges (catégories, justificatif, payée/à payer, provisions) | §6 | ⬜ |
| 8 | Tableau de bord (indicateurs §7.1) + alertes §7.2 (délais du fichier) | §7 | ⬜ |
| 9 | Sauvegarde auto/manuelle/restauration, exports PDF/Excel, start.command / start.bat, documentations | §1.2, §10 | ⬜ |

## Décisions validées (Lot 0)

- Tous les prix de développement = 50 FCFA (valeurs réelles à saisir plus tard dans `parametres.toml`).
- Listes ajoutées à `[listes]` du fichier : `objets_paiement`, `fonctions_personnel`, `sexe`, `etats_materiel` (règle : aucune liste de choix codée en dur).
- `Caisse affectée` = entité `Caisse` simple (`nom` unique).
- Technicien de maintenance = texte libre (prestataire possible).
- Statut client : champ stocké, recalculé à chaque consultation du client et à chaque entrée en salle.
- Un reçu peut regrouper plusieurs objets : en-tête `Paiement` + `LignePaiement` (produit / service / abonnement).
- Inventaire physique : la saisie corrige le stock via un mouvement de type « Inventaire ».
- Suspension d'abonnement : réservée à l'administrateur ; un abonnement suspendu refuse l'entrée en salle.
- Renouvellement : `renouvellement_debut = "fin_ancien"` → le nouvel abonnement démarre à la fin de l'ancien même si le paiement est anticipé.
- Sauvegarde automatique : thread dans l'application (plan B : tâche planifiée OS, à trancher au Lot 9).
- Pas d'entité « Salle » : les charges sont globales à l'établissement.

## Règles transverses

- Aucune valeur métier codée en dur : tout vient de `config/parametres.toml` via `get_param()`.
- Catalogues (`TypeAbonnement`, `Discipline`, `Service`) : `code` unique, upsert par `charger_parametres`, désactivation (`actif=false`) jamais suppression.
- Prix copiés à la vente (`Abonnement.prix`, `Paiement.montant`, lignes) : un changement de tarif n'altère jamais l'historique.
- Argent : `DecimalField(max_digits=12, decimal_places=0)` ; libellé devise depuis le fichier.
- Identifiants métier générés automatiquement : matricule, code client, code abonnement, n° reçu (`REC-AAAAMMJJ-0001`).
- Actions sensibles journalisées dans `AuditLog` (user, date, action, objet).
- Tests : pytest + fixture `tests/fixtures/parametres_test.toml` (jamais le vrai fichier).
- UI en français, code et commits en anglais.

## Modèle de données

Argent : `DecimalField(max_digits=12, decimal_places=0)` partout.

### accounts
- `User` (AbstractUser) — rôle par groupes Django (Administrateur, Promoteur, Caissier, Coach, Gestionnaire stock).
- `User ← OneToOne nullable → Personnel` (lie le compte à la fiche personnel).
- `AuditLog` : `user` FK, `date`, `action`, `objet_type`, `objet_id`, `details`.

### parametres
- Pas de modèle métier. `loader.py` (tomllib + validation FR), `get_param()` avec cache, commande `charger_parametres`, page admin « Recharger les paramètres ».

### personnel
- `Personnel` : `matricule` unique auto, `nom`, `prenom`, `telephone`, `fonction` (liste fichier), `salaire`, `prime`, `date_embauche`, `actif`.
- `Coach` : OneToOne → `Personnel`, `nom_coach`, `disciplines` M2M → `Discipline`.
- `Caissier` : OneToOne → `Personnel`, `parrain` FK → `Personnel`, `caisse_affectee` FK → `Caisse`.
- Anti-doublon : une seule fiche `Personnel` par personne, extensions OneToOne.

### abonnements
- `Discipline` : `code` unique, `nom`, `type`, `description`, `tarif`, `actif`.
- `TypeAbonnement` : `code` unique, `nom`, `formule` (classique/vip), `duree_jours`, `prix`, `discipline` FK nullable, `actif`.
- `Abonnement` : `code` unique auto, `client` FK, `type_abonnement` FK, `discipline` FK nullable, `prix` (copié), `date_debut`, `date_fin` (calculée, `date_fin_inclusive`), `statut`, `renouvelle_depuis` FK self nullable.
- `Suspension` : `abonnement` FK, `date_debut`, `date_fin`, `motif` (≤ `suspension_max_jours`, prolonge la fin si configuré).

### clients
- `Client` : `code_client` unique auto, `nom`, `prenom`, `sexe`, `telephone`, `date_naissance`, `adresse`, `objectif` (liste fichier), `date_inscription`, `statut` (auto : Actif / Suspendu / Expiré).
- `ProgrammeSportif` : `client` FK, `coach` FK → `Coach`, `discipline` FK, `objectif`, `duree_semaines`, `date_debut`, `date_fin`, `programme_details` (texte), `observations`.

### visites
- `Visite` : `client` FK, `date`, `heure_entree`, `heure_sortie`, `type_seance`, `coach` FK nullable, `abonnement` FK nullable (traçabilité). Entrée refusée si aucun abonnement valide.

### services
- `Service` : `code` unique, `nom`, `description`, `prix`, `duree_minutes`, `discipline` FK nullable, `responsable` FK → `Coach` nullable, `actif`.

### caisse
- `Caisse` : `nom` unique.
- `Paiement` : `numero_recu` unique (`REC-AAAAMMJJ-0001`), `client` FK, `objet` (liste fichier), `montant`, `date_heure`, `mode_paiement` (liste fichier), `operateur_mobile`, `caissier` FK → `Caissier`, `observation`, `annule`, `motif_annulation`, `annule_par`, `annule_le`. Jamais modifié, annulation journalisée.
- `LignePaiement` : `paiement` FK, `produit` FK nullable, `service` FK nullable, `abonnement` FK nullable, `quantite`, `montant` (copié).
- `SessionCaisse` : `caissier` FK, `caisse` FK nullable, `date_ouverture`, `fond_de_caisse`, `date_cloture`, `montant_theorique`, `montant_compte`, `ecart` (alerte > `ecart_tolere`). Une session ouverte par caissier.

### stock
- `Fournisseur` : `nom`, `telephone`, `adresse`.
- `Produit` : `reference` unique, `nom`, `categorie` (liste fichier), `taille`, `sexe`, `fournisseur` FK, `prix_achat`, `prix_vente`, `stock_disponible`, `stock_minimum`.
- `MouvementStock` : `produit` FK, `date`, `type` (entrée/sortie/vente/retour/inventaire/correction), `quantite`, `utilisateur` FK, `paiement` FK nullable, `motif`.
- `Inventaire` : `date`, `utilisateur` FK + `LigneInventaire` : `produit`, `stock_theorique`, `stock_compte`, `ecart`.

### materiel
- `Materiel` : `reference` unique, `designation`, `categorie` (liste fichier), `taille`, `couleur`, `particularite`, `quantite`, `date_achat`, `prix_achat`, `fournisseur` FK nullable, `localisation`, `etat` (liste fichier), `fin_garantie`, `observation`.
- `Maintenance` : `materiel` FK, `date`, `nature_panne`, `description`, `technicien` (texte), `pieces` (texte structuré), `cout`, `prochaine_maintenance`, `observation`.

### charges
- `Charge` : `categorie` (liste fichier), `designation`, `montant`, `date`, `echeance`, `mode_paiement`, `responsable`, `justificatif` (fichier), `statut` (payée/à payer), `observation`.

### dashboard / backup
- Pas de modèles : agrégations pour le tableau de bord ; sauvegardes = fichiers (copie SQLite horodatée + rotation `nombre_conserve`).

## Conformité §9 (relations)

CLIENT → ABONNEMENT → PAIEMENT → CAISSE ✔ · CLIENT → VISITE ✔ · CLIENT → PROGRAMME → COACH → PERSONNEL ✔ · CAISSIER → PERSONNEL ✔ · PRODUIT → MOUVEMENT → VENTE → PAIEMENT ✔ · SERVICE → PAIEMENT ✔ · MATÉRIEL → MAINTENANCE → TECHNICIEN ✔ · CHARGES ✔
