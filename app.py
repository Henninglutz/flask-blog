from flask import Flask, render_template, request, redirect, url_for, abort

from storage import load_post, save_posts, next_id

app = Flask(__name__)


# follow the white rabbit - this ist the way / root
# give it to render_template as posts_posts
@app.route("/")
def index():
    posts = load_post()
    return render_template("index.html", posts=posts)

# post/ get request for showing and adding author, title, content (ID = mandatory by function next_id()
@app.route("/add", methods=["GET", "POST"])
def add():
    """POST with template form for adding a new post"""
    if request.method == "POST":
        author = request.form.get("author", "").strip()
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not author or not title or not content:
            return "Please fill all fields (author, title, content).", 400       #implementing an extra route for 400

        posts = load_post()
        post = {
            "id": next_id(posts),
            "author": author,
            "title": title,
            "content": content
        }
        posts.append(post)
        save_posts(posts)
        return redirect(url_for("index"))

    return render_template("add.html")


# delete function. saves the new list of posts without the post to delete
@app.route("/delete/<int:post_id>")
def delete(post_id: int):
    posts = load_post()
    new_posts = [p for p in posts if p.get("id") != post_id]
    if len(new_posts) == len(posts):
        abort(404, description="Post not found")
    save_posts(new_posts)
    return redirect(url_for("index"))


#update functian via Post and index.^
@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id: int):
    posts = load_post()
    index_post = None
    for i, p in enumerate(posts):
        if p.get("id") == post_id:
            index_post = i
            break

    if index_post is None:
        abort(404, description="Post not found")

    if request.method == "POST":
        author = request.form.get("author", "").strip()
        title  = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not author or not title or not content:
            return "Please fill all fields (author, title, content).", 400

        posts[index_post]["author"] = author
        posts[index_post]["title"] = title
        posts[index_post]["content"] = content
        save_posts(posts)
        return redirect(url_for("index"))

#return = values are
    return render_template("update.html", post=posts[index_post])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
