from flask import Flask, render_template, redirect, url_for, flash
from form import MyForm
from wtforms.validators import DataRequired, Email


app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():

    form = MyForm()

    if form.validate_on_submit():

        flash("Thank you for submitting!")

        return redirect(url_for("home"))
    else:
        return render_template("from.html", form=form)



if __name__ == "__main__":
    app.run(debug=True)