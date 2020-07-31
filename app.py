from flask import Flask, render_template, request, redirect, url_for, flash
from forms import RegForm, LoginForm
from email_validator import validate_email, EmailNotValidError
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '4cbe5e9583e244e40821c4be4d5ea0bd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

db = SQLAlchemy(app)  # linking our app to database


# each class represents is a table in database or a peace of data in database


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(40), nullable=False)
    posts = db.relationship('Blogpost', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file})"



class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # author = db.Column(db.String(20), nullable=False, default='N/A')
    dated_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return 'Blogposts' + str(self.id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():  # inserting data from form to database
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        add_post = Blogpost(title=post_title, content=post_content, author=post_author)
        db.session.add(add_post)
        db.session.commit()
        return redirect('/posts')
    else:
        posts_all = Blogpost.query.order_by(Blogpost.dated_posted).all()
        return render_template('posts.html', posts=posts_all)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post_delete = Blogpost.query.get_or_404(id)
    db.session.delete(post_delete)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    edit_posts = Blogpost.query.get_or_404(id)
    if request.method == 'POST':
        edit_posts.title = request.form['title']
        edit_posts.author = request.form['author']
        edit_posts.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=edit_posts)


@app.route('/posts/newpost', methods=['GET', 'POST'])
def newpost():
    posts()
    return render_template('new_post.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    if request.method == 'POST':

        if form.validate_on_submit():

            flash(f'Account Created successfully {form.Username.data}!', 'success')
            return redirect(url_for('posts'))
    # if not flag or True:
    #     request.form.get()
    #     try:
    #         # Validate.
    #         valid = validate_email(email)
    #
    #     except EmailNotValidError as e:
    #         # email is not valid, exception message is human-readable
    #
    #         flash('Please check the info your given!', 'warning')

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.Email.data == 'admin@gmail.com' and form.Password.data == "admin":
            flash("Logged successful!",'success')
            return redirect(url_for("posts"))
        else:
            flash("login Unsuccessful!, please check your credentials", "danger")
    return render_template('login.html', title='Logged', form=form)


if __name__ == "__main__":
    app.run(debug=True)
