#!/usr/bin/env bash
# Installation du kit agentique Framino sur macOS
# Usage : cd framino && chmod +x setup.sh && ./setup.sh
set -e

echo "== 1. Homebrew =="
if ! command -v brew >/dev/null; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

echo "== 2. Node, Git, Python 3.12 =="
brew install node git python@3.12

echo "== 3. OpenCode (harness) =="
command -v opencode >/dev/null || npm install -g opencode-ai
opencode --version

echo "== 4. Navigateur Playwright (agent @tester) =="
npx -y playwright install chromium

echo "== 5. Vérification du fichier de paramètres =="
python3.12 -c "import tomllib; tomllib.load(open('config/parametres.toml','rb')); print('config/parametres.toml : syntaxe OK')" \
  || { echo "❌ Erreur de syntaxe dans config/parametres.toml"; exit 1; }

echo "== 6. Git =="
if [ ! -d .git ]; then
  git init -q && git add . && git commit -qm "Kit agentique initial"
fi

echo "== 7. Zones restantes à compléter =="
for f in config/parametres.toml config/environnement.toml docs/decisions.md; do
  n=$(grep -c "⚠️" "$f" || true)
  [ "$n" -gt 0 ] && echo "⚠️  $f : $n zone(s)"
done

echo ""
echo "✅ Installation terminée."
echo "Ensuite : opencode auth login  → Hugging Face → token hf_..."
echo "Puis    : opencode  → Tab (Plan) → prompt du Lot 0 dans docs/prompts.md"
