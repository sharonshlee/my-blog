"""
Blog application using Flask
Designing routes,
working with HTTP methods,
rendering templates,
and managing data.
"""
import json

from typing import List, Dict
from flask import Flask, render_template, request, redirect, url_for, Response

app = Flask(__name__)

FILE_PATH = 'static/posts.json'


def read_posts_file():
    """
    Read blog posts from a file
    """
    with open(FILE_PATH, 'r', encoding='utf8') as file:
        return json.load(file)


def write_post(blog_posts):
    """
    Write blog posts to a file
    """
    with open(FILE_PATH, 'w', encoding='utf8') as file:
        json.dump(blog_posts, file)


@app.route('/')
def index():
    """
    Render home page, index.html
    Display a list of blog posts
    returns: render index.html
    with posts (List[Dict]) argument
    """
    return render_template('index.html', posts=read_posts_file())


def add_post(blog_posts: List[Dict]):
    """
    Add post with info from add.html form
    param blog_posts: List[Dict]
    """
    blog_posts.append({
        'id': blog_posts[-1]['id'] + 1,
        'author': request.form.get('author', ''),
        'title': request.form.get('title', ''),
        'content': request.form.get('content', ''),
        'likes': 0
    })


@app.route('/add', methods=['GET', 'POST'])
def add() -> Response | str:
    """
    Add a new blog post with info from add.html form
    Redirect back to home page
    returns: GET: rendering add.html (str) or
             POST: redirect to index.html (flask.Response)
    """
    if request.method == 'POST':
        blog_posts = read_posts_file()
        add_post(blog_posts)
        write_post(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


def delete_post(blog_posts: List[Dict], post_id: int):
    """
    Delete a post given post_id
    param blog_posts: List[Dict]
    param post_id: int
    """
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id: int) -> Response:
    """
    Delete existing blog post by its id
    Redirect back to the home page
    param post_id: int
    returns: redirect to index.html (flask.Response)
    """
    blog_posts = read_posts_file()
    delete_post(blog_posts, post_id)
    write_post(blog_posts)
    return redirect(url_for('index'))


def fetch_post_by_id(post_id: int) -> Dict | None:
    """
    Fetch a post by post_id
    param post_id: int
    returns: the specific post or None
    """
    blog_posts = read_posts_file()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


def update_post(blog_posts: List[Dict], post_id: int):
    """
    Update existing post with new info
    from update.html form
    param blog_posts: List[Dict]
    param post_id: int
    """
    for post in blog_posts:
        if post['id'] == post_id:
            post.update({'author': request.form.get('author', ''),
                         'title': request.form.get('title', ''),
                         'content': request.form.get('content', ''),
                         })


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id: int) -> tuple[str, int] | Response | str:
    """
    Update existing blog post
    with details from update.html form
    param post_id: int
    returns:
        post not found message and status code (tuple[str, int])
        redirect to index.html (flask.Response)
        render update.html with post argument (str)
    """
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)

    if post is None:
        return 'Post not found', 404

    if request.method == 'POST':
        # Update the post in the JSON file
        # Redirect back to index
        blog_posts = read_posts_file()
        update_post(blog_posts, post_id)
        write_post(blog_posts)
        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


def update_likes(blog_posts: List[Dict], post_id: int):
    """
    Update likes value in the existing post
    param blog_posts: List[Dict]
    param post_id: int
    """
    for post in blog_posts:
        if post['id'] == post_id:
            post.update({'likes': post['likes'] + 1})


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id: int) -> Response:
    """
    Increase the ‘likes’ value of the post with the given id,
    and then redirect back to the index page.
    param post_id: int
    returns: redirect to index.html
    """
    blog_posts = read_posts_file()
    update_likes(blog_posts, post_id)
    write_post(blog_posts)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
