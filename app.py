import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def read_posts_file():
    with open('static/posts.json', 'r') as file:
        blog_posts = json.load(file)
    return blog_posts


def write_post(blog_posts):
    with open('static/posts.json', 'w') as file:
        json.dump(blog_posts, file)


def add_post(blog_posts):
    blog_posts.append({
        'id': len(blog_posts) + 1,
        'author': request.form.get('author', ''),
        'title': request.form.get('title', ''),
        'content': request.form.get('content', '')
    })
    return blog_posts


@app.route('/')
def index():
    return render_template('index.html', posts=read_posts_file())


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = read_posts_file()
        add_post(blog_posts)
        write_post(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == "__main__":
    app.run()
