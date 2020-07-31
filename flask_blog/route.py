from flask_blog.models import Blogpost, User
from flask import render_template, request, redirect, url_for, flash
from flask_blog.forms import RegForm, LoginForm
from flask_blog import app
from flask_blog import db


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():  # inserting data from form to database
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        add_post = Blogpost(title=post_title, content=post_content,user_id=post_author)
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
        edit_posts.user_id = request.form['author']
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
            flash("Logged successful!", 'success')
            return redirect(url_for("posts"))
        else:
            flash("login Unsuccessful!, please check your credentials", "danger")
    return render_template('login.html', title='Logged', form=form)