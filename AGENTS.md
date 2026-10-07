# Framino Fitness Club – Project rules

## Sources of truth
- docs/cahier_des_charges.md = functional spec. Never add features that are not in it.
- config/parametres.toml = ALL business values (prices, durations, catalogs, lists, alert delays, receipt, backup).
- config/environnement.toml = technical settings (timezone, port, multi-postes).
- docs/decisions.md = business rules that complete the spec + test accounts.
- docs/plan.md = lot plan and data model (created in Lot 0).
- If something is unclear and not covered by these files: STOP and ask me. Never invent a rule.

## Parameters (MANDATORY)
- NEVER hardcode a price, duration, delay, list of choices, currency or receipt text in Python, templates or migrations.
- App `parametres` owns everything related to config/parametres.toml:
  - `parametres/loader.py`: reads the file with `tomllib`, validates it (types, required keys, unique codes, prices >= 0, known discipline codes) and returns clear FRENCH error messages with the section and line.
  - `get_param("alertes.abonnement_expire_dans_jours")` helper with an in-memory cache, cleared on reload.
  - Command `python manage.py charger_parametres [--dry-run]`: validates, then upserts catalogs (TypeAbonnement, Discipline, Service) by `code`, sets `actif=false` on items removed from the file (never delete), writes a summary (added / updated / deactivated) and an AuditLog entry. If the file is invalid: change NOTHING and print the errors.
  - Called automatically at startup by start.command / start.bat.
  - Admin-only page "Paramètres": shows current values (read-only), last load date, and a "Recharger les paramètres" button.
- Catalog models keep a unique `code` field. Sales copy the price at sale time (Abonnement.prix, Paiement.montant): a price change never alters history.
- Choice lists (objectifs, catégories, modes de paiement) come from the file, not from Django `choices=`.

## Stack (fixed)
- Python 3.12, Django 5, SQLite, HTMX, Tailwind CSS as a LOCAL file (no CDN: the app must work offline).
- PDF: reportlab. Excel: openpyxl. Tests: pytest + pytest-django.
- Virtual env in .venv. Dependencies in requirements.txt.
- Apps: parametres, accounts, personnel, clients, abonnements, visites, services, stock, materiel, caisse, charges, dashboard, backup.

## Conventions
- UI text in French, simple, for non-technical staff. Code, comments and commit messages in English.
- Money: DecimalField(max_digits=12, decimal_places=0); currency label from parametres.toml.
- Unique business IDs (matricule, code client, code abonnement, référence, n° reçu) are generated automatically.
- Personnel = single record; Coach and Caissier are OneToOne extensions (anti-duplicate rule, spec §2.1).
- Role-based access (spec §8) enforced in views, not only hidden in templates.
- Sensitive actions (delete, payment cancel, stock correction, parameters reload) are written to AuditLog (user, date, action, object).

## Workflow
- Work lot by lot (docs/plan.md). One lot = one session.
- Plan first, then build. Keep changes limited to the current lot.
- Every business rule has a pytest test. Tests must use a test copy of parametres.toml (tests/fixtures/parametres_test.toml), never the real file.
- Run `pytest` before saying a lot is done.
- At the end of a lot: update docs/plan.md (status), then `git commit -m "Lot X: ..."`.
