import sqlite3
import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_NAME = "fridge.db"

# ✅ Recipe suggestions dictionary (with recipe title + YouTube link)
RECIPE_SUGGESTIONS = {
    "rice": [
        ("Sambar Rice", "https://www.youtube.com/watch?v=ABC123"),
        ("Traditional Sambar", "https://www.youtube.com/watch?v=XYZ456"),
        ("Curd Rice", "https://www.youtube.com/watch?v=LMN789")
    ],
    "egg": [
        ("Egg Kuzhambu", "https://www.youtube.com/watch?v=QWE111"),
        ("Egg Curry", "https://www.youtube.com/watch?v=QWE222"),
        ("Egg Fried Rice", "https://www.youtube.com/watch?v=QWE333")
    ],
    "chocolate": [
        ("Chocolate Cake", "https://www.youtube.com/watch?v=CHOC123"),
        ("Brownies", "https://www.youtube.com/watch?v=CHOC456")
    ],
    "mutton": [
        ("Mutton Gravy", "https://www.youtube.com/results?search_query=mutton+gravy+recipe"),
        ("Mutton Curry", "https://www.youtube.com/results?search_query=mutton+curry+recipe")
    ],
    "chocolate": [
        ("Chocolate Cake", "https://www.youtube.com/results?search_query=chocolate+cake+recipe"),
        ("Chocolate Mousse", "https://www.youtube.com/results?search_query=chocolate+mousse+recipe")
    ],
    "fish": [
        ("Fish Fry", "https://www.youtube.com/results?search_query=fish+fry+recipe"),
        ("Fish Curry", "https://www.youtube.com/results?search_query=fish+curry+recipe")
    ],
    "meat": [
        ("Meat Curry", "https://www.youtube.com/results?search_query=meat+curry+recipe"),
        ("Meat Fry", "https://www.youtube.com/results?search_query=meat+fry+recipe")
    ],
    "juice": [
        ("Fruit Juice", "https://www.youtube.com/results?search_query=fruit+juice+recipe"),
        ("Lemon Juice", "https://www.youtube.com/results?search_query=lemon+juice+recipe")
    ],
    "vegetables": [
        ("Vegetable Curry", "https://www.youtube.com/results?search_query=vegetable+curry+recipe"),
        ("Vegetable Fry", "https://www.youtube.com/results?search_query=vegetable+fry+recipe")
    ],
    "tomato": [
        ("Tomato Rasam", "https://www.youtube.com/results?search_query=tomato+rasam+recipe"),
        ("Tomato Chutney", "https://www.youtube.com/results?search_query=tomato+chutney+recipe")
    ],
    "fruits": [
        ("Fruit Salad", "https://www.youtube.com/results?search_query=fruit+salad+recipe"),
        ("Fruit Custard", "https://www.youtube.com/results?search_query=fruit+custard+recipe")
    ],
    "chicken": [
        ("Chicken Curry", "https://www.youtube.com/results?search_query=chicken+curry+recipe"),
        ("Chicken Fry", "https://www.youtube.com/results?search_query=chicken+fry+recipe")
    ],
    "biriyani": [
        ("Chicken Biryani", "https://www.youtube.com/results?search_query=chicken+biriyani+recipe"),
        ("Mutton Biryani", "https://www.youtube.com/results?search_query=mutton+biriyani+recipe")
    ],
    "paneer": [
        ("Paneer Butter Masala", "https://www.youtube.com/results?search_query=paneer+butter+masala+recipe"),
        ("Paneer Tikka", "https://www.youtube.com/results?search_query=paneer+tikka+recipe")
    ],
    "curd": [
        ("Curd Rice", "https://www.youtube.com/results?search_query=curd+rice+recipe"),
        ("Raita", "https://www.youtube.com/results?search_query=raita+recipe")
    ],
    "rasam": [
        ("Pepper Rasam", "https://www.youtube.com/results?search_query=pepper+rasam+recipe"),
        ("Garlic Rasam", "https://www.youtube.com/results?search_query=garlic+rasam+recipe")
    ],
    "upma": [
        ("Rava Upma", "https://www.youtube.com/results?search_query=rava+upma+recipe"),
        ("Vegetable Upma", "https://www.youtube.com/results?search_query=vegetable+upma+recipe")
    ],
    "pongal": [
        ("Ven Pongal", "https://www.youtube.com/results?search_query=ven+pongal+recipe"),
        ("Sweet Pongal", "https://www.youtube.com/results?search_query=sweet+pongal+recipe")
    ],
    "vada": [
        ("Medu Vada", "https://www.youtube.com/results?search_query=medu+vada+recipe"),
        ("Paruppu Vada", "https://www.youtube.com/results?search_query=paruppu+vada+recipe")
    ],
    "chapti": [
        ("Chapati", "https://www.youtube.com/results?search_query=chapati+recipe"),
        ("Chapati Curry", "https://www.youtube.com/results?search_query=chapati+curry+recipe")
    ],
    "lemon": [
        ("Lemon Rice", "https://www.youtube.com/results?search_query=lemon+rice+recipe"),
        ("Lemon Pickle", "https://www.youtube.com/results?search_query=lemon+pickle+recipe")
    ],
    "prawn": [
        ("Prawn Curry", "https://www.youtube.com/results?search_query=prawn+curry+recipe"),
        ("Prawn Fry", "https://www.youtube.com/results?search_query=prawn+fry+recipe")
    ],
    "chutney": [
        ("Coconut Chutney", "https://www.youtube.com/results?search_query=coconut+chutney+recipe"),
        ("Tomato Chutney", "https://www.youtube.com/results?search_query=tomato+chutney+recipe")
    ],
    "bread": [
        ("Bread Toast", "https://www.youtube.com/results?search_query=bread+toast+recipe"),
        ("Bread Upma", "https://www.youtube.com/results?search_query=bread+upma+recipe")
    ],
    "cheese": [
        ("Cheese Sandwich", "https://www.youtube.com/results?search_query=cheese+sandwich+recipe"),
        ("Cheese Pasta", "https://www.youtube.com/results?search_query=cheese+pasta+recipe")
    ],
    "cake": [
        ("Vanilla Cake", "https://www.youtube.com/results?search_query=vanilla+cake+recipe"),
        ("Chocolate Cake", "https://www.youtube.com/results?search_query=chocolate+cake+recipe")
    ],
     "veg curry": [
        ("Mixed Veg Curry", "https://www.youtube.com/results?search_query=mixed+vegetable+curry+recipe"),
        ("Veg Kurma", "https://www.youtube.com/results?search_query=veg+kurma+recipe")
    ],
    "pulao": [
        ("Veg Pulao", "https://www.youtube.com/results?search_query=veg+pulao+recipe"),
        ("Peas Pulao", "https://www.youtube.com/results?search_query=peas+pulao+recipe")
    ],
     "upma": [
        ("Rava Upma", "https://www.youtube.com/results?search_query=rava+upma+recipe"),
        ("Vegetable Upma", "https://www.youtube.com/results?search_query=vegetable+upma+recipe")
    ],
     "samosa": [
        ("Punjabi Samosa", "https://www.youtube.com/results?search_query=punjabi+samosa+recipe"),
        ("Aloo Samosa", "https://www.youtube.com/results?search_query=aloo+samosa+recipe")
    ],
    "dal": [
        ("Dal Tadka", "https://www.youtube.com/results?search_query=dal+tadka+recipe"),
        ("Dal Fry", "https://www.youtube.com/results?search_query=dal+fry+recipe")
    ],
    "dosa": [
        ("Masala Dosa", "https://www.youtube.com/results?search_query=masala+dosa+recipe"),
        ("Plain Dosa", "https://www.youtube.com/results?search_query=plain+dosa+recipe")
    ],
    "idli": [
        ("Soft Idli", "https://www.youtube.com/results?search_query=soft+idli+recipe"),
        ("Rava Idli", "https://www.youtube.com/results?search_query=rava+idli+recipe")
    ],
    "poori": [
        ("Poori Masala", "https://www.youtube.com/results?search_query=poori+masala+recipe"),
        ("Aloo Poori", "https://www.youtube.com/results?search_query=aloo+poori+recipe")
    ],
    "parotta": [
        ("Kerala Parotta", "https://www.youtube.com/results?search_query=kerala+parotta+recipe"),
        ("Parotta with Salna", "https://www.youtube.com/results?search_query=parotta+salna+recipe")
    ],
    "sambar": [
        ("Traditional Sambar", "https://www.youtube.com/results?search_query=sambar+recipe"),
        ("Arachuvitta Sambar", "https://www.youtube.com/results?search_query=arachuvitta+sambar+recipe")
    ],
    "milk": [
         ("Milk Pudding", "https://www.youtube.com/results?search_query=milk+pudding+recipe"),
         ("Payasam / Kheer", "https://www.youtube.com/results?search_query=milk+kheer+recipe"),
         ("Milkshake", "https://www.youtube.com/results?search_query=milkshake+recipe"),
    ],
    "butter": [
    ("Butter Naan", "https://www.youtube.com/results?search_query=butter+naan+recipe"),
    ("Butter Cookies", "https://www.youtube.com/results?search_query=butter+cookies+recipe"),
    ("Butter Chicken", "https://www.youtube.com/results?search_query=butter+chicken+recipe"),
    ("Garlic Butter Prawns", "https://www.youtube.com/results?search_query=garlic+butter+prawns+recipe")
],

"cocoa": [
    ("Hot Cocoa", "https://www.youtube.com/results?search_query=hot+cocoa+recipe"),
    ("Chocolate Cake", "https://www.youtube.com/results?search_query=chocolate+cake+recipe"),
    ("Brownies", "https://www.youtube.com/results?search_query=chocolate+brownies+recipe"),
    ("Chocolate Mousse", "https://www.youtube.com/results?search_query=chocolate+mousse+recipe")
],

"ghee": [
    ("Ghee Rice", "https://www.youtube.com/results?search_query=ghee+rice+recipe"),
    ("Ghee Roast Dosa", "https://www.youtube.com/results?search_query=ghee+roast+recipe"),
    ("Besan Ladoo", "https://www.youtube.com/results?search_query=besan+ladoo+recipe"),
    ("Rava Kesari", "https://www.youtube.com/results?search_query=rava+kesari+with+ghee+recipe")
],

"nuts": [
    ("Dry Fruit Laddu", "https://www.youtube.com/results?search_query=dry+fruit+laddu+recipe"),
    ("Nutty Chocolate Bark", "https://www.youtube.com/results?search_query=nutty+chocolate+bark+recipe"),
    ("Badam Milk", "https://www.youtube.com/results?search_query=badam+milk+recipe"),
    ("Dry Fruit Halwa", "https://www.youtube.com/results?search_query=dry+fruit+halwa+recipe")
],
}


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS items
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         expiry DATE NOT NULL)''')


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        item = request.form["item"].strip().lower()
        expiry = request.form["expiry"]

        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("INSERT INTO items (name, expiry) VALUES (?, ?)", (item, expiry))

        return redirect(url_for("index"))

    today = datetime.date.today()
    items = []
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("SELECT id, name, expiry FROM items").fetchall()

        for row in rows:
            expiry_date = datetime.date.fromisoformat(row[2])
            days_left = (expiry_date - today).days
            total_days = max((expiry_date - today).days + 1, 1)
            progress = max(0, min(100, int((days_left / total_days) * 100)))

            # ✅ Recipes: fetch from dictionary
            recipes_list = RECIPE_SUGGESTIONS.get(row[1].lower(), [])

            items.append({
                "id": row[0],
                "name": row[1],
                "expiry": row[2],
                "recipes": recipes_list,
                "days_left": days_left,
                "progress": progress
            })

    return render_template("index.html", items=items)


@app.route("/delete/<int:item_id>")
def delete(item_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM items WHERE id=?", (item_id,))
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

