from flask.helpers import make_response
from app import app
from flask import redirect, render_template, request, session
from users import create_new_user, sign_in
from search import get_groups_by_time
from search import get_posts_in_group
from groups import create_group, check_group_existance
from utility import get_user_id, get_group_info
from posts import create_new_post, save_image, get_image


@app.route("/")
def index():
    #groups_by_time = get_groups_by_time()
    return render_template("index.html", groups=[])


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/new", methods=["POST"])
def new():
    username = request.form["username"]
    user_id = request.form["user_id"]
    password = request.form["password"]
    repeat = request.form["repeat password"]
    if repeat != password:
        return redirect("/login")
    if create_new_user(username, user_id, password):
        session["username"] = user_id
        return redirect("/")
    return redirect("/login")


@app.route("/sign-in")
def sign():
    return render_template("logger.html")


@app.route("/old", methods=["POST"])
def old():
    user_id = request.form["user_id"]
    password = request.form["password"]
    if sign_in(user_id, password):
        session["username"] = user_id
        return redirect("/")
    return redirect("/sign-in")


@app.route("/logout")
def logout():
    if "username" in session:
        del session["username"]
    return redirect("/")


@app.route("/create-group")
def group_creator():
    return render_template("groupCreator.html")


@app.route("/group-create", methods=["POST"])
def group_create():
    group_name = request.form["group_name"]
    if check_group_existance(group_name):
        return redirect("/create-group")
    public = "A" not in request.form.getlist("public")
    description = request.form["description"]
    creator_id = get_user_id(session["username"])
    if create_group(creator_id, public, group_name, description):
        return redirect("/")
    return redirect("/create-group")


@app.route("/group<int:id>")
def group(id):
    group_info = get_group_info(id)
    posts = get_posts_in_group(id)
    return render_template("group.html", posts=posts, name=group_info[0], description=group_info[1], group_id=id)


@app.route("/group<int:group>/create-post")
def post_creator(group):
    return render_template("postCreator.html", group=group)


@app.route("/group<int:group>/post-create", methods=["POST"])
def post_create(group):
    file = request.files["picture"]
    picture = save_image(file)
    if picture is None:
        return redirect(f"/group{group}/create-post") 
    title = request.form["title"]
    if create_new_post(get_user_id(session["username"]), group, title, picture):
        return redirect(f"/group{group}")
    return redirect(f"/group{group}/create-post")

@app.route("/group<int:group>/post<int:id>")
def post(group, id):
    return redirect(f"/group{group}")


@app.route("/image/<int:id>")
def image(id):
    picture = get_image(id)
    response = make_response(bytes(picture))
    response.headers.set("Content-Type", "image/jpeg")
    return response