# Kit agentique – Framino Fitness Club
OpenCode (harness) + Hugging Face Inference Providers + 3 sous-agents, prêt à lancer sur Mac.

## Contenu
| Fichier | Rôle |
|---|---|
| `setup.sh` | Installe tout (Homebrew, Node, Git, Python, OpenCode, Playwright) et vérifie les paramètres |
| `config/parametres.toml` | **Tous les paramètres métier** : prix, abonnements, services, disciplines, listes, alertes, reçu, sauvegarde. Modifiable à tout moment |
| `config/environnement.toml` | Paramètres techniques : fuseau horaire, port, multi-postes |
| `docs/decisions.md` | Règles métier complémentaires + comptes de test |
| `opencode.json` | Config du harness : modèles, permissions, navigateur MCP |
| `AGENTS.md` | Règles du projet (dont : aucun prix codé en dur) |
| `.opencode/agents/` | Sous-agents `@reviewer`, `@tester`, `@spec-checker` |
| `docs/cahier_des_charges.md` | Cahier des charges converti pour les agents |
| `docs/prompts.md` | Prompts prêts à copier pour chaque lot |

## ⚠️ Zones à modifier vous-même
| # | Où | Quoi | Quand |
|---|---|---|---|
| 1 | huggingface.co → Settings → Access Tokens | Token *Fine-grained* avec « Make calls to Inference Providers » | Avant de démarrer |
| 2 | huggingface.co → Settings → Billing | Ajouter du crédit (≈ 5–10 $) | Avant de démarrer |
| 3 | `config/parametres.toml` | Valeurs `⚠️` : devise, prix, frais d'inscription, délais, Mobile Money… | Avant le Lot 0 (des valeurs provisoires suffisent) |
| 4 | `config/environnement.toml` | Fuseau horaire | Avant le Lot 0 |
| 5 | `docs/decisions.md` | Mots de passe des comptes de test, règles propres à la salle | Avant le Lot 0 |
| 6 | `opencode.json` → `model` / `small_model`, `spec-checker.md` → `model` | Remplacer si « model not found » (`/models`) | Si erreur |

## Modifier les paramètres après la création du projet
1. Ouvrir `config/parametres.toml` (TextEdit, VS Code…) et changer les valeurs.
2. Appliquer :
   - relancer le logiciel (`start.command` / `start.bat`), **ou**
   - `python manage.py charger_parametres` (ajouter `--dry-run` pour vérifier sans appliquer), **ou**
   - menu Administrateur → Paramètres → « Recharger les paramètres ».
3. Si le fichier contient une erreur, **rien n'est modifié** et un message indique la ligne fautive.

| Changement | Effet |
|---|---|
| Prix d'un abonnement / service | Nouvelles ventes uniquement ; l'historique garde l'ancien prix |
| Ajouter un abonnement / service / discipline | Copier un bloc `[[...]]`, nouveau `code` unique |
| Retirer un élément | `actif = false` (jamais supprimer le bloc d'un élément déjà vendu) |
| Délais d'alerte, reçu, listes, sauvegarde | Pris en compte immédiatement après rechargement |
| Fuseau, port, multi-postes (`environnement.toml`) | Après redémarrage du logiciel |

## Démarrage (15 min)
```bash
cd ~/projets && unzip ~/Downloads/framino-kit.zip && cd framino
chmod +x setup.sh && ./setup.sh
opencode auth login              # Hugging Face → hf_...
open -e config/parametres.toml   # zones ⚠️
open -e docs/decisions.md
opencode                         # /models, puis Tab (Plan) → prompt Lot 0
```

## Déroulé d'un lot
1. Mode **Plan** : coller le prompt du lot → relire → répondre aux questions.
2. `Tab` → **Build** : « Réalise le plan. »
3. Boucle de vérification (`@spec-checker`, `@reviewer`, `@tester`) – bas de `docs/prompts.md`.
4. Commit, puis `/new` pour le lot suivant.

## Lancer l'application
```bash
source .venv/bin/activate
python manage.py migrate
python manage.py charger_parametres
python manage.py seed_demo
python manage.py runserver 8000      # http://localhost:8000
```

## Dépannage
| Problème | Solution |
|---|---|
| `model not found` | `/models` dans OpenCode, reporter l'ID dans `opencode.json` |
| Erreur 429 | Limite du fournisseur : attendre ou changer de modèle |
| Erreur 402 / crédit | Recharger dans Settings → Billing |
| Sous-agents introuvables | Renommer `.opencode/agents` en `.opencode/agent` (anciennes versions) |
| Erreur dans parametres.toml | Lire le message (section + ligne) ; vérifier guillemets et nombres sans espaces |
| L'agent tourne en rond | `/new`, prompt plus court, ou modèle plus gros temporairement |
| L'agent a cassé le code | `git diff` puis `git checkout .` |

## Sécurité
Projet personnel uniquement : les prompts partent chez des fournisseurs tiers via Hugging Face. Aucun code ni donnée ENGIE dans ce dossier.
