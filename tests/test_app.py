from app import app
from recipes import RECIPES, recipe_by_slug


def test_recipe_collection_has_expected_counts():
    assert len(RECIPES) == 30
    assert sum(recipe["cuisine"] == "Thai" for recipe in RECIPES) == 10
    assert len({recipe["slug"] for recipe in RECIPES}) == 30


def test_every_recipe_has_beginner_content():
    for recipe in RECIPES:
        assert len(recipe["ingredients"]) >= 6
        assert len(recipe["steps"]) >= 5
        assert recipe["tip"]
        assert recipe_by_slug(recipe["slug"]) == recipe


def test_pages_and_filters():
    client = app.test_client()
    assert client.get("/").status_code == 200
    assert client.get("/recipes").status_code == 200
    thai = client.get("/recipes?cuisine=thai")
    assert thai.status_code == 200
    assert b"<strong>10</strong> recipes found" in thai.data
    assert client.get("/recipe/pad-thai").status_code == 200
    assert client.get("/recipe/not-real").status_code == 404
