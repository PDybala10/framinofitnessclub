# Prompts à copier-coller dans OpenCode

1 lot = 1 session (`/new`). `Tab` bascule Plan ↔ Build. Validez toujours le plan avant Build.

---
## Lot 0 – Plan, modèle de données, socle  (mode PLAN)
Lis AGENTS.md, docs/cahier_des_charges.md, config/parametres.toml, config/environnement.toml et docs/decisions.md.
1. Liste les points encore ambigus et pose-moi les questions.
2. Propose le modèle de données Django complet (apps, modèles, champs, relations, contraintes d'unicité) en respectant la §9, la règle anti-doublon du Personnel et le champ `code` des catalogues.
3. Propose le découpage en lots 1 à 9.
N'écris rien tant que je n'ai pas validé.

→ Après validation (mode BUILD) :
Écris docs/plan.md. Initialise le projet Django : .venv, requirements.txt, settings (fr-FR, fuseau et port lus depuis config/environnement.toml, SQLite), Tailwind en fichier local, base layout avec menu par rôle, pytest configuré. Lance `python manage.py check` et `pytest`. Commit "Lot 0".

## Lot 1 – Paramètres, comptes, rôles, journal (§8)
Réalise le lot 1 :
- App `parametres` exactement comme décrit dans AGENTS.md (loader + validation en français, get_param avec cache, commande `charger_parametres --dry-run`, page Administrateur avec bouton « Recharger les paramètres »).
- Connexion/déconnexion, 5 rôles (groupes Django), contrôle d'accès par rôle, modèle AuditLog, commande `seed_demo` (comptes de test de docs/decisions.md).
Tests : fichier invalide → rien n'est modifié et l'erreur est lisible ; un prix modifié dans le fichier est appliqué après rechargement ; un élément retiré passe à actif=false ; un caissier ne peut pas ouvrir la page Paramètres.

## Lot 2 – Personnel (§2.1)
Réalise le lot 2 : CRUD Personnel, compléments Coach et Caissier en OneToOne, matricule auto. Test : une personne coach ET caissier n'a qu'une seule fiche Personnel.

## Lot 3 – Clients, disciplines, abonnements, programmes, visites (§2.2 – 2.7)
Réalise le lot 3. Catalogues disciplines et types d'abonnement chargés via `charger_parametres` (pas de data migration). Date de fin et suspension selon [regles_abonnement] ; statut client automatique ; visite refusée si aucun abonnement valide. Le prix est copié dans l'abonnement à la vente. Tests : changer le prix d'un type d'abonnement ne modifie pas les abonnements existants.

## Lot 4 – Paiements et caisse (§5)
Réalise le lot 4 : paiements, n° de reçu selon [recu], impression du reçu (format, adresse, logo, message depuis le fichier), modes de paiement depuis [caisse], ouverture/clôture avec fond de caisse, écart (alerte au-delà de ecart_tolere), totaux et répartitions. Annulation journalisée. Tests : écart de caisse, unicité des reçus.

## Lot 5 – Services, produits, fournisseurs, stock (§2.8 – 2.10, §3)
Réalise le lot 5 : services depuis le fichier, catégories produits depuis [listes], mouvements de stock, inventaire avec écarts, alerte stock ≤ minimum, historique. Une vente crée un mouvement ET un paiement. Tests : stock après vente/retour, alerte.

## Lot 6 – Matériel et maintenance (§4)
Réalise le lot 6 : fiche matériel (catégories depuis [listes]), maintenances, coût total d'entretien par machine sur une période. Tests : coût total.

## Lot 7 – Charges (§6)
Réalise le lot 7 : charges (catégories depuis [listes]), justificatif joint, statut payée/à payer. Tests : total des charges du mois, provisions disponibles.

## Lot 8 – Tableau de bord et alertes (§7)
Réalise le lot 8 : indicateurs §7.1, alertes §7.2 avec les délais de [alertes], page Promoteur/Admin. Tests pour chaque indicateur et : changer un délai dans le fichier modifie l'alerte après rechargement.

## Lot 9 – Sauvegarde, exports, livrables (§1.2, §10)
Réalise le lot 9 : sauvegarde auto selon [sauvegarde] (copie SQLite horodatée + rotation), sauvegarde manuelle vers un dossier choisi, restauration avec confirmation, exports PDF/Excel, scripts `start.command` (Mac) et `start.bat` (Windows) qui lancent `charger_parametres` puis le serveur, docs/INSTALL.md, docs/MANUEL_<ROLE>.md et docs/MODIFIER_LES_PARAMETRES.md (guide simple pour l'administrateur).

---
## Boucle de vérification (fin de CHAQUE lot)
1. `@spec-checker vérifie les sections <§ du lot>`
2. `@reviewer relis le lot <X>`
3. `Lance python manage.py runserver 8000 en arrière-plan, puis @tester teste : <scénarios du lot>`
4. `Corrige tous les Missing, High et KO. Relance pytest. Mets à jour docs/plan.md puis commit "Lot <X>".`

---
## Ajouter un NOUVEAU paramètre plus tard (projet déjà livré)
> Ajoute dans config/parametres.toml le paramètre `<section>.<nom>` = <valeur> (<explication>). Mets à jour le loader et sa validation, remplace toute valeur codée en dur correspondante par get_param, ajoute un test, puis commit.
