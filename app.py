from flask import Flask, abort, render_template, request

from recipes import RECIPES, recipe_by_slug


app = Flask(__name__)


@app.get("/")
def home():
    featured = [recipe for recipe in RECIPES if recipe["featured"]][:6]
    return render_template("home.html", recipes=RECIPES, featured=featured)


@app.get("/recipes")
def recipes():
    query = request.args.get("q", "").strip().lower()
    cuisine = request.args.get("cuisine", "all").strip().lower()
    speed = request.args.get("speed", "all").strip().lower()

    filtered = RECIPES
    if query:
        filtered = [
            recipe
            for recipe in filtered
            if query in recipe["name"].lower()
            or query in recipe["description"].lower()
            or query in " ".join(recipe["tags"]).lower()
        ]
    if cuisine != "all":
        filtered = [recipe for recipe in filtered if recipe["cuisine"].lower() == cuisine]
    if speed == "under-30":
        filtered = [recipe for recipe in filtered if recipe["minutes"] <= 30]

    return render_template(
        "recipes.html",
        recipes=filtered,
        query=request.args.get("q", ""),
        selected_cuisine=cuisine,
        selected_speed=speed,
        cuisines=sorted({recipe["cuisine"] for recipe in RECIPES}),
    )


@app.get("/recipe/<slug>")
def recipe_detail(slug: str):
    recipe = recipe_by_slug(slug)
    if recipe is None:
        abort(404)
    related = [
        item
        for item in RECIPES
        if item["slug"] != slug and item["cuisine"] == recipe["cuisine"]
    ][:3]
    return render_template("recipe.html", recipe=recipe, related=related)


@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
