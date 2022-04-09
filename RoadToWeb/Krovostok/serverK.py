from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello World'


@app.route('/about')
def about():
    return 'The About Page'


@app.route('/blog')
def blog():
    return render_template('03.html', title="LETSGOOOOOOOOOOOO")


@app.route('/blog/<int:blog_id>')
def blogpost(blog_id):
    return 'This is blog post number' + str(blog_id)


if __name__ == '__main__':
    app.run()