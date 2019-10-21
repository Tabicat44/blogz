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
    username = db.Column(db.String(120))
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

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.owner = owner
        self.submitted = False


@app.route('/')
def index():

    theblog = Blog.query.all()
    return render_template('blog.html', myblog=theblog)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        blog_name = request.form['newtitle']
        blog_content = request.form['newpost']
        blog_owner = request.form['']

        if len(blog_name) == 0 or len(blog_content) == 0:
            flash("Woah, there! You can't leave that empty!", "error_message")
        else:
            new_blog = Blog(blog_name, blog_content, blog_owner)
            db.session.add(new_blog)
            db.session.commit()

            return redirect('/blog?id=' + str(new_blog.id))
    return render_template('newpost.html')

@app.route('/show-blog', methods=['GET'])
def show_the_blog():

    blog_id = request.args.get('id')
    new_blog = Blog.query.get(blog_id)
    return render_template('show-blog.html'.format(new_blog), myblog=new_blog)

#@app.route('/signup')



@app.route('/login', methods=['GET'])
def lets_logout():
    del session['email']
    return redirect('/blog')


#@app.route('/index')



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