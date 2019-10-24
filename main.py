from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogzapp@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "Iwishtherewerentants"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    submitted = db.Column(db.Boolean)

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
        self.submitted = False

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','blog', 'usersblogs']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method =='POST':
        the_username = request.form['username']
        the_password = request.form['password']
        user = User.query.filter_by(username=the_username).first()

        # if not user:
        #     flash("Oops!  That username does not exist here!")
        # elif user.password != the_password:
        #     flash("Whoopsie daisy. That ain't right.")
        if user and user.password == the_password:
            session['username'] = the_username
            flash("Logg in")
            return redirect('/newpost')
        else:
            flash("Username or password is incorrect")
            # session['username'] = the_username
            # flash("Logged in")
            # return redirect('/newpost')

    return render_template('login.html')


@app.route('/blog', methods=['POST', 'GET'])
def home():    
    blog_id = str(request.args.get("id"))
    this_blog = Blog.query.get(blog_id)
    owner = User.query.filter_by(username=session['username']).first()

    retrievedblog = Blog.query.all()
    takenowner = User.query.all()
    return render_template('blog.html', theblog=retrievedblog, perblog = this_blog, theowner=takenowner)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        blog_name = request.form['newtitle']
        blog_content = request.form['newpost']
        blog_owner = User.query.filter_by(username=session['username']).first()

        if len(blog_name) == 0 or len(blog_content) == 0:
            flash("Woah, there! You can't leave that empty!", "error_message")
        else:
            new_blog = Blog(blog_name, blog_content, blog_owner)
            db.session.add(new_blog)
            db.session.commit()

            return redirect('/blog?id=' + str(new_blog.id))            

    return render_template('newpost.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()
        if len(username) == 0 or len(password) == 0 or len(verify) == 0:
            flash("I'm so sorry, but you cannot leave anything here blank.")
        
        elif password != verify:
            flash('What the heck!?  The "password" and "verify" fields were supposed to match!')
        elif not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/blog')
        # else:
        #     return "<h1>That username is taken. Sorry! Try something else.</h1>"

    return render_template('signup.html')
        


@app.route('/logout', methods=['POST'])
def lets_logout():
    del session['username']
    return redirect('/blog')

@app.route('/singleUser')
def list_all_users():
    if request.args.get('id'):
        blog_id = str(request.args.get('id'))
        blog = Blog.query.get(blog_id)
        retrievedblog = Blog.query.filter_by(owner=blog).all()
        return render_template('usersblogs.html', theblog = retrievedblog)
    theowner = User.query.all()
    useful_id = request.args.get(id)
    # if request.method == 'POST':
    #     return redirect('/blog?id=' + str(the_owner.id))
    return render_template('singleUser.html', givenowner = theowner)
        




#     # tasks = Task.query.filter_by(completed=False).all()
#     # completed_tasks = Task.query.filter_by(completed=True).all()
#     # return render_template('thepages.html',title="Blogapalooza", 
#     #     tasks=tasks, completed_tasks=completed_tasks)


# # @app.route('/delete-task', methods=['POST'])
# # def delete_task():

# #     task_id = int(request.form['task-id'])
# #     task = Task.query.get(task_id)
# #     task.completed = True
# #     db.session.add(task)
# #     db.session.commit()

# #     return redirect('/')


if __name__ == '__main__':
    app.run()