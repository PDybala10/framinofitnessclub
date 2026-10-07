"""Expose the user's role name to templates (used by the menu)."""

GROUP_TO_ROLE = {
    "Promoteur": "promoteur",
    "Caissier": "caissier",
    "Coach": "coach",
    "Gestionnaire stock": "stock",
}


def role(request):
    user = getattr(request, "user", None)
    role_name = ""
    if user is not None and user.is_authenticated:
        if user.is_superuser:
            role_name = "administrateur"
        else:
            for group in user.groups.all():
                if group.name in GROUP_TO_ROLE:
                    role_name = GROUP_TO_ROLE[group.name]
                    break
    return {"role": role_name}