from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    rating: Mapped[int]

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    books = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()
    print(type(books))
    return render_template("index.html", books=books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"],
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add.html")

@app.route("/book/<int:id>", methods=['GET', 'POST'])
def edit(id):
    book = db.get_or_404(Book, id)
    if request.method == "POST":
        new_rating = request.form.get('rating')
        book.rating = new_rating
        book.verified = True
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit_rating.html", book=book)

@app.route("/book/<int:id>/delete")
def delete(id):
    book = db.get_or_404(Book, id)
    if book is not None:
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
