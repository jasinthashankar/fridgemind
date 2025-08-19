import sqlite3
import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_NAME = "fridge.db"

# ✅ Recipe suggestions dictionary (with links)
RECIPE_SUGGESTIONS = {
    "rice": ("Sambar Rice", "https://www.youtube.com/results?search_query=sambar+rice+recipe"),
    "tomato": ("Tomato Rasam", "https://www.youtube.com/results?search_query=tomato+rasam+recipe"),
    "onion": ("Onion Uthappam", "https://www.youtube.com/results?search_query=onion+uthappam+recipe"),
    "potato": ("Aloo Masala for Dosa", "https://www.youtube.com/results?search_query=aloo+masala+for+dosa+recipe"),
    "egg": ("South Indian Egg Curry", "https://www.youtube.com/results?search_query=south+indian+egg+curry+recipe"),
    "chicken": ("Chettinad Chicken Curry", "https://www.youtube.com/results?search_query=chettinad+chicken+curry+recipe"),
    "fish": ("Kerala Fish Curry", "https://www.youtube.com/results?search_query=kerala+fish+curry+recipe"),
    "prawn": ("Andhra Prawn Curry", "https://www.youtube.com/results?search_query=andhra+prawn+curry+recipe"),
    "idli": ("Soft Idli with Sambar", "https://www.youtube.com/results?search_query=soft+idli+with+sambar+recipe"),
    "dosa": ("Crispy Masala Dosa", "https://www.youtube.com/results?search_query=crispy+masala+dosa+recipe"),
    "rava": ("Rava Upma", "https://www.youtube.com/results?search_query=rava+upma+recipe"),
    "curd": ("Curd Rice (Thayir Sadam)", "https://www.youtube.com/results?search_query=curd+rice+recipe"),
    "lemon": ("Lemon Rice (Elumichai Sadam)", "https://www.youtube.com/results?search_query=lemon+rice+recipe"),
    "tamarind": ("Tamarind Rice (Puliyodarai)", "https://www.youtube.com/results?search_query=tamarind+rice+recipe"),
    "pongal": ("Ven Pongal with Ghee", "https://www.youtube.com/results?search_query=ven+pongal+recipe"),
    "sambar": ("Hotel Style Sambar", "https://www.youtube.com/results?search_query=hotel+style+sambar+recipe"),
    "rasam": ("Pepper Rasam", "https://www.youtube.com/results?search_query=pepper+rasam+recipe"),
    "appam": ("Kerala Appam with Stew", "https://www.youtube.com/results?search_query=kerala+appam+with+stew+recipe"),
    "puttu": ("Kerala Puttu with Kadala Curry", "https://www.youtube.com/results?search_query=kerala+puttu+kadala+curry+recipe"),
    "parotta": ("Parotta with Salna", "https://www.youtube.com/results?search_query=parotta+with+salna+recipe"),
    "biryani": ("Hyderabadi Biryani", "https://www.youtube.com/results?search_query=hyderabadi+biryani+recipe")
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

        # ✅ Auto-generate recipe with name|link
        suggestion = RECIPE_SUGGESTIONS.get(name.lower(), None)
        if suggestion:
            recipe = f"{suggestion[0]}|{suggestion[1]}"
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

            # ✅ Progress bar (0 expired, 100 fresh)
            total_days = max((expiry_date - today).days + 1, 1)
            progress = max(0, min(100, int((days_left / total_days) * 100)))
        except:
            days_left = None
            progress = 0

        # ✅ Split recipe into name and link
        if row[3] and "|" in row[3]:
            recipe_name, recipe_link = row[3].split("|", 1)
        else:
            recipe_name, recipe_link = row[3], "#"

        items.append({
            "id": row[0],
            "name": row[1],
            "expiry": row[2],
            "recipe_name": recipe_name,
            "recipe_link": recipe_link,
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
