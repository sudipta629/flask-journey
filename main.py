from flask import Flask, render_template, redirect, url_for, flash
from form import MyForm
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


    def __repr__(self):
        return f"User('{self.name}','{self.email}')"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():

    form = MyForm()

    if form.validate_on_submit():
        print("Form Valid")

        new_user = User(
            name=form.name.data,
            email=form.email.data
        )
        db.session.add(new_user)
        db.session.commit()

        flash("New user added")

        return redirect(url_for("home"))
    else:
        return render_template("from.html", form=form)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)