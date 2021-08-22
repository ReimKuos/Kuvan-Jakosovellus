from flask.helpers import make_response
from app import app
from flask import redirect, render_template, request, session
from users import create_new_user, sign_in
from search import get_groups_by_time
from search import get_posts_in_group
from groups import create_group, check_group_existance
from utility import get_user_id, get_group_info
from posts import create_new_post, save_image, get_image
from comments import get_comments, add_comment

@app.route("/")
def index():
    groups_by_time = get_groups_by_time()
    return render_template("index.html", groups=groups_by_time)


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
        return "Repeat password didn't match (This a temporary error message style)"
    if create_new_user(username, user_id, password):
        session["username"] = user_id
        return redirect("/")
    return "Some error occurred during database insertion (This a temporary error message style)"


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
    return "Incorrect password/user ID (This a temporary error message style)"


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
        return "Group with this name already exists (This a temporary error message style)"
    public = "A" not in request.form.getlist("public")
    description = request.form["description"]
    creator_id = get_user_id(session["username"])
    if create_group(creator_id, public, group_name, description):
        return redirect("/")
    return "Some error occurred during database insertion (This a temporary error message style)"


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
        return "image could't be saved or it's file fromat was not JPG (This a temporary error message style)"
    title = request.form["title"]
    if create_new_post(get_user_id(session["username"]), group, title, picture):
        return redirect(f"/group{group}")
    return "Some error occurred during database insertion (This a temporary error message style)"

@app.route("/group<int:group>/post<int:id>")
def post(group, id):
    comments = get_comments(id)
    print(comments)
    return render_template("post.html", name="Hello", id=id, group=group, comments=comments)

@app.route("/comment/<int:group_id>/<int:post_id>", methods=["POST"])
def comment(group_id, post_id):
    user_id = get_user_id(session["username"])
    comment = request.form["comment"]
    if add_comment(user_id, post_id, comment):
        return redirect(f"/group{group_id}/post{post_id}")
    return "An error occurred and comment was not created!"

@app.route("/image/<int:id>")
def image(id):
    picture = get_image(id)
    response = make_response(bytes(picture))
    response.headers.set("Content-Type", "image/jpeg")
    return response