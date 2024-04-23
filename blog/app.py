from flask import Flask, render_template, request, redirect, url_for, g, flash
import sqlite3
from datetime import datetime
import re

DATABASE = 'database.db'

app = Flask(__name__)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@app.route("/")
def homepage():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, title FROM category ORDER BY title")
    categories = cursor.fetchall()
    cursor.execute("SELECT id, title, date, content FROM article ORDER BY date DESC LIMIT 10")
    articles = cursor.fetchall()
    return render_template("homepage.html", articles=articles, categories=categories)

@app.route("/categories/<int:category_id>")
def category(category_id):
    db = get_db()
    category = db.execute("SELECT title FROM category WHERE id = ?", (category_id,)).fetchone()
    if category is None:
        return "Category not found", 404
    articles = db.execute(
        "SELECT article.id, article.title, article.content, article.date "
        "FROM article WHERE category_id = ? "
        "ORDER BY date DESC",
        (category_id,)
    ).fetchall()
    return render_template("category.html", category=category, articles=articles)

@app.route("/article/<int:article_id>")
def article(article_id):
    return "not implemented"

def format_datetime(value, format='%Y-%m-%d'):
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f').strftime(format)

app.jinja_env.filters['datetime'] = format_datetime

@app.route("/article/create", methods=['GET', 'POST'])
def article_create():
    db = get_db()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form['category']
        if not title or not content or not category_id:
            flash('All fields are required!')
            return redirect(url_for('article_create'))
        db.execute("INSERT INTO article (title, content, date, category_id) VALUES (?, ?, ?, ?)",
                   (title, content, datetime.now(), category_id))
        db.commit()
        return redirect(url_for('homepage'))
    categories = db.execute("SELECT id, title FROM category").fetchall()
    return render_template("create_article.html", categories=categories)

if __name__ == "__main__":
    app.run(debug=True)
