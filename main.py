from flask import Flask, render_template, redirect, url_for, flash
from form import MyForm
from flask_wtf import FlaskForm
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

@app.route("/users", methods=["GET", "POST"])
def users():
    users = User.query.all()
    return render_template("users/index.html", users=users)

@app.route("/users/<int:id>/edit", methods=["GET", "POST"])
def edit_user(id):
    user = db.get_or_404(User, id)
    form = MyForm(obj=user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data

        db.session.commit()

        flash("User updated successfully!")

        return redirect(url_for("users"))

    return render_template(
        "users/edit.html",
        form=form,
        user=user
    )

@app.route("/users/<int:id>/delete", methods=["GET", "POST"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!")
    return redirect(url_for("users"))


@app.route("/new-users", methods=["GET", "POST"])
def new_users():

    form = MyForm()

    if form.validate_on_submit():


        new_user = User(
            name=form.name.data,
            email=form.email.data
        )
        db.session.add(new_user)
        db.session.commit()

        flash("New user added")

        return redirect(url_for("users"))
    else:
        return render_template("users/create.html", form=form)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True,
            host="0.0.0.0",
            port=5000,
            threaded=True)

