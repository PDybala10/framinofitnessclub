"""Expose general display info (name, logo) from config/parametres.toml.

Minimal read-only reader; the full loader with validation arrives in Lot 1
and will replace the internals without changing the template variables.
"""

import tomllib
from pathlib import Path
from django.conf import settings

_CACHE = {"data": None}


def _read_general():
    if _CACHE["data"] is None:
        path = Path(settings.BASE_DIR) / "config" / "parametres.toml"
        try:
            with open(path, "rb") as f:
                _CACHE["data"] = tomllib.load(f).get("general", {})
        except (OSError, tomllib.TOMLDecodeError):
            _CACHE["data"] = {}
    return _CACHE["data"]


def site_infos(request):
    general = _read_general()
    return {
        "nom_salle": general.get("nom_salle", "Framino Fitness Club"),
        "logo_salle": general.get("logo", ""),
    }