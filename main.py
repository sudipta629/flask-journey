from flask import Flask, render_template, redirect, url_for, flash, request
from form import MyForm
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "static/images")
app.config["ALLOWED_EXTENSIONS"] = ["png", "jpg", "jpeg"]

db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100) )



    profile = db.relationship(
        'Profile',
        back_populates='user',
        uselist = False
    )


    def __repr__(self):
        return f"User('{self.name}','{self.email}')"

class Profile(db.Model):
    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        unique=True
    )

    user = db.relationship(
        "User",
        back_populates="profile"
    )

    def __repr__(self):
        return f"Profile('{self.age}')"




class Blogs(db.Model):
    __tablename__ = "blogs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(200), nullable=False,default="default.jpg")
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Blogs('{self.title}','{self.content}')"




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

        new_profile = Profile(
            bio=form.bio.data,
            user=new_user
        )
        db.session.add(new_profile)
        db.session.commit()

        flash("New user added")

        return redirect(url_for("users"))
    else:
        return render_template("users/create.html", form=form)



@app.route("/users/<int:id>")
def show_user(id):
    user = db.get_or_404(User, id)
    return render_template("users/show_user.html", user=user)

           #blogs route start
@app.route('/blogs')
def blogs():
    blogs = Blogs.query.order_by(Blogs.date_posted.desc()).all()
    return render_template("blogs/index.html" , blogs=blogs)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



@app.route('/blogs/new', methods=["GET", "POST"])
def create_blog():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        file = request.files["image_file"]
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = "default.jpg"

        new_blog = Blogs(title=title, content=content,image_file=filename)
        db.session.add(new_blog)
        db.session.commit()
        flash("Blog created successfully!")
        return redirect(url_for("blogs"))

    return render_template("blogs/create.html")

@app.route('/show-blogs', methods=["GET", "POST"])
def show_blogs():
    return render_template("blogs/show.html")



@app.route('/register', methods=["GET", "POST"])
def register():
    return render_template("auth/register.html")





if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True,
            host="0.0.0.0",
            port=5000,
            threaded=True)

