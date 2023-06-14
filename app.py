import json

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    with open('static/posts.json', 'r') as file:
        blog_posts = json.load(file)

    return render_template('index.html', posts=blog_posts)


if __name__ == "__main__":
    app.run()
