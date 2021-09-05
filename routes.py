from os import error
from flask.helpers import make_response
from secrets import token_hex
from app import app
from flask import redirect, render_template, request, session, abort
from users import create_new_user, sign_in
from search import get_groups_by_time, get_posts_in_group
from search import get_groups_by_creator, get_groups_by_popularity, get_groups_by_activity
from groups import create_group, check_group_existance
from utility import get_user_id, get_group_info, get_post_info
from utility import like_post, remove_like, check_like
from posts import create_new_post, save_image, get_image
from comments import get_comments, add_comment

@app.route("/")
def index():
    groups_by_time = get_groups_by_time()
    return render_template("index.html", groups=groups_by_time)

@app.route("/mine")
def mine():
    if "username" not in session:
        redirect("/")
    id = get_user_id(session["username"])
    groups = get_groups_by_creator(id)
    return render_template("index.html", groups=groups)


@app.route("/order:<string:style>")
def ordered(style):
    if style == "popularity":
        groups = get_groups_by_popularity()
    elif style == "activity":
        groups = get_groups_by_activity()
    else:
        groups = get_groups_by_time()
    return render_template("index.html", groups=groups)

@app.route("/login:error=<string:error>")
def login(error):
    if error == "None":
        error = ""
    return render_template("login.html", message=error)


@app.route("/new", methods=["POST"])
def new():
    alert = None
    username = request.form["username"]
    user_id = request.form["user_id"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if not 5 < len(username) < 20:
        alert = "name must be 5 to 20 symbols"
    elif not 5 < len(user_id) < 20:
        alert = "ID must be 5 to 20 symbols"
    elif not 8 < len(password1) < 20:
        alert = "password must be 8 to 20 symbols"
    elif password1 != password2:
        alert = "passwords do not much"
    if alert is not None:
        return redirect(f"/login:error={alert}")
    if create_new_user(username, user_id, password1):
        session["username"] = user_id
        session["csrf_token"] = token_hex(16)
        return redirect("/")
    return redirect("/login:error=Unknown error")

@app.route("/sign-in:error=<string:error>")
def sign(error):
    if error == "None":
        error = ""
    return render_template("logger.html", message=error)


@app.route("/old", methods=["POST"])
def old():
    user_id = request.form["user_id"]
    password = request.form["password"]
    if sign_in(user_id, password):
        session["username"] = user_id
        session["csrf_token"] = token_hex(16)
        return redirect("/")
    return redirect("/sign-in:error=Wrong password or username")


@app.route("/logout")
def logout():
    if "username" in session:
        del session["username"]
        del session["csrf_token"]
    return redirect("/")


@app.route("/create-group:error=<string:error>")
def group_creator(error):
    if "username" not in session:
        redirect("/")
    if error == "None":
        return render_template("groupCreator.html", message="")
    else:
        return render_template("groupCreator.html", message=error)

@app.route("/group-create", methods=["POST"])
def group_create():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    group_name = request.form["group_name"]
    if not 5 <= len(group_name) <= 50:
        return redirect("/create-group:error=Name should be between 5 to 50 symbols")
    if check_group_existance(group_name):
        return redirect("/create-group:error=Group with this name already exists")
    description = request.form["description"]
    creator_id = get_user_id(session["username"])
    if create_group(creator_id, group_name, description):
        return redirect("/")
    return redirect("/create-group:error=Database error try again")


@app.route("/group<int:id>")
def group(id):
    group_info = get_group_info(id)
    posts = get_posts_in_group(id)
    return render_template("group.html", posts=posts, name=group_info[0], description=group_info[1], group_id=id)


@app.route("/group<int:group>/create-post:error=<string:error>")
def post_creator(group, error):
    if "username" not in session:
        redirect("/")
    if error == "None":
        error = ""
    return render_template("postCreator.html", group=group, message=error)


@app.route("/group<int:group>/post-create", methods=["POST"])
def post_create(group):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    title = request.form["title"]
    if not 6 <= len(title) <= 50:
        return redirect(f"/group{group}/create-post:error=Title must be 6 to 50 symbols")
    file = request.files["picture"]
    picture = save_image(file)
    if type(picture) is str:
        return redirect(f"/group{group}/create-post:error={picture}")
    if picture is None:
        return redirect(f"/group{group}/create-post:error=No picture")
    if create_new_post(get_user_id(session["username"]), group, title, picture):
        return redirect(f"/group{group}")
    return redirect(f"/group{group}/create-post:error=Unknown error")


@app.route("/group<int:group>/post<int:id>")
def post(group, id):
    comments = get_comments(id)
    info = get_post_info(id)
    if "username" in session:
        user_id = get_user_id(session["username"])
        liked = check_like(id, user_id)
        if liked:
            direction = f"/group{group}/post{id}/dislike"
            token = "remove Like"
        else:
            direction = f"/group{group}/post{id}/like"
            token = "Like"
    else:
        direction = "/"
        token = "Like"
    return render_template("post.html", name=info[1], id=id, group=group, comments=comments, liked=direction, token=token)

@app.route("/comment/<int:group_id>/<int:post_id>", methods=["POST"])
def comment(group_id, post_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    user_id = get_user_id(session["username"])
    comment = request.form["comment"]
    if comment == "":
        return redirect(f"/group{group_id}/post{post_id}")
    if add_comment(user_id, post_id, comment):
        return redirect(f"/group{group_id}/post{post_id}")
    return redirect(f"/comment/{group_id}/{post_id}")

@app.route("/image/<int:id>")
def image(id):
    picture = get_image(id)
    response = make_response(bytes(picture))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/group<int:group>/post<int:post>/like")
def like(group, post):
    if "username" not in session:
        return redirect(f"/group{group}")
    user_id = get_user_id(session["username"])
    like_post(post, user_id)
    return redirect(f"/group{group}/post{post}")

@app.route("/group<int:group>/post<int:post>/dislike")
def dislike(group, post):
    if "username" not in session:
        return redirect(f"/group{group}/post{post}")
    user_id = get_user_id(session["username"])
    remove_like(post, user_id)
    return redirect(f"/group{group}/post{post}")
