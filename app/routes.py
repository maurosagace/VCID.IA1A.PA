from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm, WeeksForm
    #EmptyForm, PostForm, 
from app.models import User, Weeks 
    #Post
from app.email import send_password_reset_email


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index_static', methods=['GET', 'POST'])
#@login_required
def index_static():

    return render_template('index_static.html', title='Home')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
#@login_required
def index():
    page = request.args.get('page', 1, type=int)
    dates = Weeks.query.filter(Weeks.user_id.is_(None)).paginate(
                page, app.config['LINES_PER_PAGE'], False)
    
    return render_template('index.html', title='Home', lines=dates.items)
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    """
  
    #form=form,
    #                      posts=posts.items, next_url=next_url,
    #                      prev_url=prev_url)


@app.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    #def und app.route = explore ursprünglich "home"
    page = request.args.get('page', 1, type=int)
    dates = Weeks.query.filter(Weeks.user_id.is_(None)).paginate(page, app.config['LINES_PER_PAGE'], False)
    next_url = url_for('home', page=dates.next_num) if dates.has_next else None
    prev_url = url_for('home', page=dates.prev_num) if dates.has_prev else None
    return render_template('home.html', title='Home', lines=dates.items, next_url=next_url, prev_url=prev_url)

"""
@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Ungültiger Benutzername oder ungültiges Passwort eingegeben')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    name=form.name.data, familyname=form.familyname.data, 
                    address=form.address.data, telephone=form.telephone.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Gratuliere, Sie haben sich nun erfolgreich registriert!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registierung', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Prüfen Sie Ihre Mails für die Instruktion, um das Passwort zurückzusetzen')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Passwort zurücksetzen', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    dates = Weeks.query.filter_by(user_id=user.id).paginate(page, app.config['LINES_PER_PAGE'], False)
    #user = User.query.filter_by(username=username).first_or_404()
    #page = request.args.get('page', 1, type=int)
    #posts = user.posts.order_by(Post.timestamp.desc()).paginate(
    #    page, app.config['POSTS_PER_PAGE'], False)
    #next_url = url_for('user', username=user.username, page=posts.next_num) \
        #if posts.has_next else None
    #prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        #if posts.has_prev else None
    #form = EmptyForm()
    return render_template('user.html', title='User', user=user, lines=dates.items)
    #posts=posts.items,next_url=next_url, 
    #prev_url=prev_url, form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.telephone = form.telephone.data
        #current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Anpassungen gespeichert.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.telephone.data = current_user.telephone
        #form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

"""
@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
"""
"""
@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
"""

@app.route('/reserve/<weeks_id>') 
@login_required
def reserve(weeks_id : str):
    weeks = Weeks.query.get(weeks_id) 
    weeks.user_id = current_user.id 
    db.session.add(weeks) 
    db.session.commit()
    flash('Reserviert date_begin {} date_end {}'.format(weeks.date_begin.strftime('%d.%m.%Y'), 
            weeks.date_end.strftime('%d.%m.%Y')))
    return redirect(url_for('user', username=current_user.username))

@app.route('/change/<weeks_id>')
@login_required
def change(weeks_id : str):
    weeks = Weeks.query.get(weeks_id)
    #weeks.user_id = current_user.id
    if weeks is None:
        flash('Weeks not found.')
        return redirect(url_for('user', username=current_user.username))
    if weeks.user_id != current_user.id:
        flash('You cannot delete this Weeks.')
        return redirect(url_for('user', username=current_user.username))
    weeks.user_id = None
    #db.session.delete(weeks)
    db.session.commit()
    flash('WEEK gelöscht.')
    return redirect(url_for('user', username=current_user.username))

"""
Alter Test um Einträge freizugeben *Error*
app.route('/deleteres/<weeks_id>')
@login_required
def deleteres(weeks_id : str):
    weeks = Weeks.query.get(weeks_id)
    weeks.user_id = current_user.id
    if weeks is None:
        flash('Weeks not found.')
        return redirect(url_for('user', username=current_user.username))
    if weeks.user_id != current_user.id:
        flash('You cannot delete this week.')
        return redirect(url_for('user', username=current_user.username))
    weeks.user_id = None
    db.session.commit()
    flash('Your Week has been deleted.')
    return redirect(url_for('user', username=current_user.username))
"""

@app.route('/admin', methods=['GET', 'POST']) 
@login_required
def admin():
    if current_user.id != 8:
        flash('Sie sind nicht berechtigt für die Adminfunktion.')
        return redirect(url_for('user', username=current_user.username))
    form = WeeksForm()
    if form.validate_on_submit():
        weeks = Weeks(date_begin=form.date_begin.data, date_end=form.date_end.data) 
        db.session.add(weeks)
        db.session.commit()
        flash('Zeitraum von {} bis {} erfasst!'.
            format(weeks.date_begin.strftime('%d.%m.%Y'),
            weeks.date_end.strftime('%d.%m.%Y'))) 
        return redirect(url_for('admin'))
    page = request.args.get('page', 1, type=int)
    dates = Weeks.query.paginate( page, app.config['LINES_PER_PAGE'], False) 
    next_url = url_for('admin', page=dates.next_num) \
        if dates.has_next else None
    prev_url = url_for('admin', page=dates.prev_num) \
        if dates.has_prev else None
    return render_template('admin.html', title='Admin', form=form,
                            lines=dates.items, next_url=next_url, 
                            prev_url=prev_url)


