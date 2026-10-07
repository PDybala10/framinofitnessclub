# Décisions métier – Framino Fitness Club

Les **valeurs** (prix, durées, délais, listes) sont dans `config/parametres.toml` : modifiables à tout moment.
Ce fichier contient uniquement les **règles** qui complètent le cahier des charges et les comptes de test.
⚠️ = à compléter avant le Lot 0.

## Règles
- Statut client : Actif si ≥ 1 abonnement actif ; Suspendu si son abonnement est suspendu ; Expiré sinon. Recalculé automatiquement.
- Un paiement n'est jamais modifié : il est annulé par l'administrateur avec un motif (journalisé), puis ressaisi.
- Prix figé à la vente : Abonnement.prix et Paiement.montant sont copiés au moment de la vente ; un changement de tarif ne modifie jamais l'historique.
- Bénéfice estimatif (§7.1) = encaissements du mois − charges du mois.
- Une vente de produit crée un mouvement de stock ET un paiement.
- Un reçu peut regrouper plusieurs objets (abonnement, services, produits) : en-tête Paiement + lignes.
- L'inventaire physique corrige le stock via un mouvement de type « Inventaire » (écart calculé).
- Suspension d'abonnement : administrateur uniquement ; un abonnement suspendu refuse l'entrée en salle.
- Renouvellement (`renouvellement_debut = "fin_ancien"`) : le nouvel abonnement démarre à la fin de l'ancien, même si le paiement est anticipé.
- Technicien de maintenance : texte libre (prestataire externe possible).
- Statut client : champ stocké, recalculé à chaque consultation du client et à chaque entrée en salle.
- Sauvegarde automatique : thread dans l'application (plan B : tâche planifiée OS).
- Valeurs de développement : tous les prix à 50 FCFA ; clients et abonnements de test créés par `seed_demo`.
- ⚠️ Autres règles propres à la salle : ...

## Comptes de test (développement uniquement)
| Rôle | Identifiant | Mot de passe ⚠️ |
|---|---|---|
| Administrateur | admin | ⚠️ |
| Promoteur | promoteur | ⚠️ |
| Caissier | caissier | ⚠️ |
| Coach | coach | ⚠️ |
| Gestionnaire stock | stock | ⚠️ |
