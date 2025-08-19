import sqlite3
import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_NAME = "fridge.db"

# ✅ Recipe suggestions dictionary (with multiple YouTube links)
RECIPE_SUGGESTIONS = {
     "rice": (
        "Sambar Rice",
        [
            "https://www.youtube.com/results?search_query=sambar+rice+recipe",
            "https://www.youtube.com/results?search_query=how+to+make+sambar+rice",
            "https://www.youtube.com/results?search_query=traditional+sambar+sadham"
        ]
    ),
     
     "paneer": (
        "Paneer Dishes",
        [
            "https://www.youtube.com/results?search_query=paneer+butter+masala",
            "https://www.youtube.com/results?search_query=palak+paneer+recipe",
            "https://www.youtube.com/results?search_query=chilli+paneer+recipe"
        ]
    ),
    "idli": (
        "Soft Idli with Sambar",
        [
            "https://www.youtube.com/results?search_query=soft+idli+recipe",
            "https://www.youtube.com/results?search_query=idli+sambar+recipe",
            "https://www.youtube.com/results?search_query=south+indian+idli"
        ]
    ),
    "dosa": (
        "Crispy Masala Dosa",
        [
            "https://www.youtube.com/results?search_query=masala+dosa+recipe",
            "https://www.youtube.com/results?search_query=mysore+masala+dosa",
            "https://www.youtube.com/results?search_query=south+indian+dosa+recipe"
        ]
    ),
    "curd": (
        "Curd Rice (Thayir Sadam)",
        [
            "https://www.youtube.com/results?search_query=curd+rice+recipe",
            "https://www.youtube.com/results?search_query=thayir+sadam",
            "https://www.youtube.com/results?search_query=south+indian+curd+rice"
        ]
    ),
    "rasam": (
        "Pepper Rasam",
        [
            "https://www.youtube.com/results?search_query=pepper+rasam+recipe",
            "https://www.youtube.com/results?search_query=tomato+rasam+recipe",
            "https://www.youtube.com/results?search_query=rasam+south+indian"
        ]
    ),
    "sambar": (
        "Hotel Style Sambar",
        [
            "https://www.youtube.com/results?search_query=hotel+style+sambar",
            "https://www.youtube.com/results?search_query=sambar+for+idli+dosa",
            "https://www.youtube.com/results?search_query=south+indian+sambar"
        ]
    ),
    "upma": (
        "Rava Upma",
        [
            "https://www.youtube.com/results?search_query=rava+upma+recipe",
            "https://www.youtube.com/results?search_query=sooji+upma",
            "https://www.youtube.com/results?search_query=south+indian+upma"
        ]
    ),
    "pongal": (
        "Ven Pongal with Ghee",
        [
            "https://www.youtube.com/results?search_query=ven+pongal+recipe",
            "https://www.youtube.com/results?search_query=khara+pongal",
            "https://www.youtube.com/results?search_query=ghee+pongal"
        ]
    ),
    "vada": (
        "Medu Vada",
        [
            "https://www.youtube.com/results?search_query=medu+vada+recipe",
            "https://www.youtube.com/results?search_query=ulundu+vada",
            "https://www.youtube.com/results?search_query=south+indian+vada"
        ]
    ),
    "chapati": (
        "Chapati with Curry",
        [
            "https://www.youtube.com/results?search_query=chapati+recipe",
            "https://www.youtube.com/results?search_query=soft+chapati+recipe",
            "https://www.youtube.com/results?search_query=chapati+and+curry"
        ]
    ),
    "pulao": (
        "Vegetable Pulao",
        [
            "https://www.youtube.com/results?search_query=vegetable+pulao+recipe",
            "https://www.youtube.com/results?search_query=south+indian+pulao",
            "https://www.youtube.com/results?search_query=easy+pulao+recipe"
        ]
    ),
    "lemon": (
        "Lemon Rice",
        [
            "https://www.youtube.com/results?search_query=lemon+rice+recipe",
            "https://www.youtube.com/results?search_query=elumichai+sadam",
            "https://www.youtube.com/results?search_query=south+indian+lemon+rice"
        ]
    ),
    "tamarind": (
        "Tamarind Rice (Puliyodarai)",
        [
            "https://www.youtube.com/results?search_query=tamarind+rice+recipe",
            "https://www.youtube.com/results?search_query=puliyodarai",
            "https://www.youtube.com/results?search_query=imli+rice+south+indian"
        ]
    ),
    "appam": (
        "Kerala Appam with Stew",
        [
            "https://www.youtube.com/results?search_query=kerala+appam+recipe",
            "https://www.youtube.com/results?search_query=appam+and+stew",
            "https://www.youtube.com/results?search_query=palappam"
        ]
    ),
    "puttu": (
        "Kerala Puttu with Kadala Curry",
        [
            "https://www.youtube.com/results?search_query=puttu+recipe",
            "https://www.youtube.com/results?search_query=puttu+kadala+curry",
            "https://www.youtube.com/results?search_query=kerala+puttu"
        ]
    ),
    "parotta": (
        "Parotta with Salna",
        [
            "https://www.youtube.com/results?search_query=parotta+recipe",
            "https://www.youtube.com/results?search_query=parotta+with+salna",
            "https://www.youtube.com/results?search_query=madurai+parotta"
        ]
    ),
    "fish": (
        "Kerala Fish Curry",
        [
            "https://www.youtube.com/results?search_query=kerala+fish+curry+recipe",
            "https://www.youtube.com/results?search_query=meen+curry",
            "https://www.youtube.com/results?search_query=fish+curry+kerala+style"
        ]
    ),
    "prawn": (
        "Andhra Prawn Curry",
        [
            "https://www.youtube.com/results?search_query=andhra+prawn+curry+recipe",
            "https://www.youtube.com/results?search_query=spicy+prawn+curry",
            "https://www.youtube.com/results?search_query=royyala+iguru"
        ]
    ),
    "egg": (
        "Egg Kuzhambu",
        [
            "https://www.youtube.com/results?search_query=egg+kuzhambu+recipe",
            "https://www.youtube.com/results?search_query=south+indian+egg+curry",
            "https://www.youtube.com/results?search_query=muttai+kuzhambu"
        ]
    ),
    "chutney": (
        "Coconut Chutney",
        [
            "https://www.youtube.com/results?search_query=coconut+chutney+recipe",
            "https://www.youtube.com/results?search_query=thengai+chutney",
            "https://www.youtube.com/results?search_query=south+indian+coconut+chutney"
        ]
    ),
    "bread": (
        "Bread Snacks",
        [
            "https://www.youtube.com/results?search_query=bread+pakora+recipe",
            "https://www.youtube.com/results?search_query=bread+sandwich+recipe",
            "https://www.youtube.com/results?search_query=bread+toast+recipe"
        ]
    ),
    "cheese": (
        "Cheese Dishes",
        [
            "https://www.youtube.com/results?search_query=cheese+sandwich+recipe",
            "https://www.youtube.com/results?search_query=cheese+pasta+recipe",
            "https://www.youtube.com/results?search_query=cheese+paratha+recipe"
        ]
    ),
    "tomato": (
        "Tomato Dishes",
        [
            "https://www.youtube.com/results?search_query=tomato+rasam+recipe",
            "https://www.youtube.com/results?search_query=tomato+curry+recipe",
            "https://www.youtube.com/results?search_query=tomato+chutney+recipe"
        ]
    ),
    "fruits": (
        "Fruit Salads & Juices",
        [
            "https://www.youtube.com/results?search_query=fruit+salad+recipe",
            "https://www.youtube.com/results?search_query=fruit+juice+recipe",
            "https://www.youtube.com/results?search_query=smoothie+recipe"
        ]
    ),
    "vegetables": (
        "Mixed Vegetable Dishes",
        [
            "https://www.youtube.com/results?search_query=mixed+vegetable+curry",
            "https://www.youtube.com/results?search_query=vegetable+stir+fry",
            "https://www.youtube.com/results?search_query=vegetable+soup+recipe"
        ]
    ),
    "chocolate": (
        "Chocolate Desserts",
        [
            "https://www.youtube.com/results?search_query=chocolate+cake+recipe",
            "https://www.youtube.com/results?search_query=chocolate+brownie+recipe",
            "https://www.youtube.com/results?search_query=homemade+chocolate+mousse"
        ]
    ),
    "juice": (
        "Fresh Juices",
        [
            "https://www.youtube.com/results?search_query=fresh+fruit+juice+recipe",
            "https://www.youtube.com/results?search_query=mixed+fruit+juice+recipe",
            "https://www.youtube.com/results?search_query=healthy+detox+juice"
        ]
    ),
    "bread": (
        "Bread Dishes",
        [
            "https://www.youtube.com/results?search_query=bread+upma+recipe",
            "https://www.youtube.com/results?search_query=bread+pakora+recipe",
            "https://www.youtube.com/results?search_query=garlic+bread+recipe"
        ]
    ),
     "chicken": (
        "Chicken Dishes",
        [
            "https://www.youtube.com/results?search_query=chicken+curry+recipe",
            "https://www.youtube.com/results?search_query=chicken+65+recipe",
            "https://www.youtube.com/results?search_query=butter+chicken+recipe"
        ]
    ),
    "meat": (
        "Mutton / Meat Dishes",
        [
            "https://www.youtube.com/results?search_query=mutton+curry+recipe",
            "https://www.youtube.com/results?search_query=mutton+chukka+recipe",
            "https://www.youtube.com/results?search_query=chettinad+mutton+curry"
        ]
    ),
    "biriyani": (
        "Biryani Varieties",
        [
            "https://www.youtube.com/results?search_query=chicken+biryani+recipe",
            "https://www.youtube.com/results?search_query=mutton+biryani+recipe",
            "https://www.youtube.com/results?search_query=veg+biryani+recipe"
        ]
    ),
    "cake": (
        "Cakes & Baking",
        [
            "https://www.youtube.com/results?search_query=chocolate+cake+recipe",
            "https://www.youtube.com/results?search_query=vanilla+cake+recipe",
            "https://www.youtube.com/results?search_query=sponge+cake+recipe"
        ]
    ),
}



def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            expiry TEXT NOT NULL,
            recipe TEXT
        )
    """)
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        expiry = request.form["expiry"]

        # ✅ Auto-generate recipe with multiple links
        suggestion = RECIPE_SUGGESTIONS.get(name.lower(), None)
        if suggestion:
            recipe_name, links = suggestion
            recipe = f"{recipe_name}|{'|'.join(links)}"
        else:
            recipe = "No recipe available|#"

        c.execute("INSERT INTO items (name, expiry, recipe) VALUES (?, ?, ?)", (name, expiry, recipe))
        conn.commit()
        return redirect(url_for("index"))

    # Fetch all items
    c.execute("SELECT id, name, expiry, recipe FROM items")
    rows = c.fetchall()
    conn.close()

    today = datetime.date.today()
    items = []

    for row in rows:
        try:
            expiry_date = datetime.date.fromisoformat(row[2])
            days_left = (expiry_date - today).days
            total_days = max((expiry_date - today).days + 1, 1)
            progress = max(0, min(100, int((days_left / total_days) * 100)))
        except:
            days_left = None
            progress = 0

        # ✅ Split recipe into name and multiple links
        if row[3] and "|" in row[3]:
            parts = row[3].split("|")
            recipe_name = parts[0]
            recipe_links = parts[1:]
        else:
            recipe_name, recipe_links = row[3], []

        items.append({
            "id": row[0],
            "name": row[1],
            "expiry": row[2],
            "recipe_name": recipe_name,
            "recipe_links": recipe_links,
            "days_left": days_left,
            "progress": progress
        })

    return render_template("index.html", items=items)


@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
