import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort, flash
import db
import config
import posts, users, comments


app = Flask(__name__)
app.secret_key = config.secret_key


def checklogin():
    if "user_id" not in session:
        abort(403)


@app.route("/")
def index():
    all_posts = posts.get_posts()
    return render_template("index.html", posts=all_posts)

@app.route("/findpost")
def findpost():
    query = request.args.get("query")
    if query:
        result = posts.find_post(query)
    else:
        query = ""
        result = []
    return render_template("findpost.html", query=query, result=result)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = posts.get_post(post_id)
    post_comments = comments.get_comments(post_id)
    averagerating = comments.average_rating(post_id)
    if not post:
        abort(404)
    classes = posts.get_classes(post_id)
    return render_template("showpost.html", post=post, classes=classes, post_comments=post_comments, averagerating=averagerating)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    posts = users.get_posts(user_id)
    return render_template("showuser.html", user=user, posts=posts)





@app.route("/comment/<int:post_id>")
def comment(post_id):
    checklogin()
    post = posts.get_post(post_id)
    if not post:
        abort(404)

    return render_template("comment.html", post=post)

@app.route("/createcomment", methods=["POST"])
def createcomment():
    checklogin()

    commenter_id = session["user_id"]
    post_id = request.form["post_id"]
    rating = request.form["rating"]
    comment = request.form["comment"]

    comments.add_comment(commenter_id, post_id, rating, comment)

    return redirect("/post/" + str(post_id))





@app.route("/newpost")
def newpost():
    checklogin()
    classes = posts.get_all_classes()
    return render_template("newpost.html", classes=classes)

@app.route("/createpost", methods=["POST"])
def createpost():
    checklogin()
    title = request.form["title"]
    if not title or len(title) > 80:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    user_id = session["user_id"]

    all_classes = posts.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            if parts[0] not in all_classes:
                abort(403)
            if parts[1] not in all_classes[parts[0]]:
                abort(403)
            classes.append((parts[0], parts[1]))

    posts.add_post(title, description, user_id, classes)

    return redirect("/")

@app.route("/editpost/<int:post_id>")
def editpost(post_id):
    checklogin()
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    if post["user_id"] != session["user_id"]:
        abort(403)
    all_classes = posts.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in posts.get_classes(post_id):
        classes[entry["title"]] = entry["value"]

    return render_template("editpost.html", post=post, classes=classes, all_classes=all_classes)

@app.route("/updatepost", methods=["POST"])
def updatepost():
    checklogin()
    post_id = request.form["post_id"]
    title = request.form["title"]
    if not title or len(title) > 80:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    if post["user_id"] != session["user_id"]:
        abort(403)

    all_classes = posts.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            if parts[0] not in all_classes:
                abort(403)
            if parts[1] not in all_classes[parts[0]]:
                abort(403)
            classes.append((parts[0], parts[1]))

    posts.update_post(post_id, title, description, classes)

    return redirect("/post/" + str(post_id))

@app.route("/removepost/<int:post_id>", methods=["GET", "POST"])
def removepost(post_id):
    checklogin()
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    if post["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("removepost.html", post=post)

    if request.method == "POST":
        if "remove" in request.form:
            posts.remove_post(post_id)
            return redirect("/")
        else:
            return redirect("/post/" + str(post_id))


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    if not username:
        abort(403)
    password1 = request.form["password1"]
    if not password1:
        abort(403)
    password2 = request.form["password2"]
    if not password2:
        abort(403)
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    flash("Tunnus luotu")
    return redirect("/")




@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        if not username:
            return redirect("/")
        password = request.form["password"]
        if not password:
            return redirect("/")

        user_id = users.login_check(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")


