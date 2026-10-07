"""Lot 0 smoke tests: settings, layout, test fixture."""

import tomllib
from pathlib import Path

import pytest
from django.conf import settings

BASE_DIR = Path(settings.BASE_DIR)


def test_environnement_settings():
    assert settings.LANGUAGE_CODE == "fr-FR"
    assert settings.TIME_ZONE == "Africa/Douala"
    assert settings.PORT == 8000
    assert "sqlite" in settings.DATABASES["default"]["ENGINE"]


def test_all_project_apps_installed():
    expected = [
        "parametres", "accounts", "personnel", "clients", "abonnements",
        "visites", "services", "stock", "materiel", "caisse", "charges",
        "dashboard", "backup",
    ]
    for app in expected:
        assert app in settings.INSTALLED_APPS


def test_parametres_test_fixture_exists_and_prices_are_50():
    fixture = BASE_DIR / "tests" / "fixtures" / "parametres_test.toml"
    assert fixture.exists()
    with open(fixture, "rb") as f:
        data = tomllib.load(f)
    assert data["inscription"]["frais_inscription"] == 50
    for abo in data["abonnements"]:
        assert abo["prix"] == 50
    for discipline in data["disciplines"]:
        assert discipline["tarif"] == 50
    for service in data["services"]:
        assert service["prix"] == 50


def test_tailwind_css_is_local():
    css = BASE_DIR / "static" / "css" / "tailwind.css"
    assert css.exists()
    content = css.read_text()
    assert "cdn.tailwindcss.com" not in content
    assert len(content) > 1000


def test_htmx_is_local():
    js = BASE_DIR / "static" / "js" / "htmx.min.js"
    assert js.exists()
    assert len(js.read_text()) > 10000


def test_logo_configured_and_served():
    with open(BASE_DIR / "config" / "parametres.toml", "rb") as f:
        logo = tomllib.load(f)["general"]["logo"]
    assert logo, "logo path must be set in parametres.toml"
    assert (BASE_DIR / "static" / logo).exists()


@pytest.mark.django_db
def test_base_layout_served(client):
    response = client.get("/accounts/connexion/")
    assert response.status_code == 200
    assert b"Framino Fitness Club" in response.content


@pytest.mark.django_db
def test_home_requires_login(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/accounts/connexion/" in response["Location"]


@pytest.mark.django_db
def test_wrong_credentials_show_french_error(client, django_user_model):
    django_user_model.objects.create_user(username="u1", password="secret123")
    response = client.post(
        "/accounts/connexion/", {"username": "u1", "password": "wrong"}
    )
    assert response.status_code == 200
    assert "Identifiant ou mot de passe incorrect." in response.rendered_content


@pytest.mark.django_db
def test_login_redirects_to_home(client, django_user_model):
    django_user_model.objects.create_user(username="u2", password="secret123")
    response = client.post(
        "/accounts/connexion/", {"username": "u2", "password": "secret123"}
    )
    assert response.status_code == 302
    assert response["Location"] == "/"
    response = client.get("/")
    assert response.status_code == 200
    assert "Tableau de bord" in response.rendered_content


@pytest.mark.django_db
def test_menu_filtered_by_role(client, django_user_model):
    from django.contrib.auth.models import Group

    user = django_user_model.objects.create_user(username="u3", password="secret123")
    user.groups.add(Group.objects.get_or_create(name="Caissier")[0])
    client.force_login(user)
    content = client.get("/").rendered_content
    assert "Paiements" in content
    assert "Paramètres" not in content
    assert "Stock" not in content