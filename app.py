from flask import Flask,request,make_response,render_template,redirect,url_for
from  datetime import  datetime
# to avoid sql injection  use markup escape
from markupsafe import  escape

myapp = Flask(__name__)
############################# create page for not found
@myapp.errorhandler(404)
def page_not_found(error):
    return render_template('not_found_page.html')
#############################3333 add static files
@myapp.route("/static",endpoint='staticfile')
def staticfiles():
    return render_template("static.html")
######################################### macros in flask --> macros -----> templates
@myapp.route('/testmacros',endpoint='flask-macros')
def user_macros():
    students=['Ahmed','ali','Mohamed']
    courses=['python','js','flask']
    return render_template('students.html',students=students,courses=courses)
########################## connection to databases
#1 install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
myapp.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db=SQLAlchemy(myapp)
################### using models
class Posts(db.Model):
    __tablename__='posts'
    id= db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    body=db.Column(db.String(1000))
    image=db.Column(db.String(300))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
############### to apply this changes to database
 #db.create_all()
 #from app import Posts
# p = Posts(title='michael',body='michael@mail.com',image='pexels-eric-mufasa-1350789_6w5liBR.jpg')

#--------------- list all posts
@myapp.route('/posts',endpoint='posts_db')
def posts_index():
    posts=Posts.query.all()
    return render_template('Posts/index.html',posts=posts)
#-------------- show one post
@myapp.route('/posts/<int:id>',endpoint='post_detail')
def post_detail(id):
    post=Posts.query.get_or_404(id)
    return render_template('Posts/show.html',post=post)
#-------------- delete one post
@myapp.route('/posts/<int:id>/delete',endpoint='post_delete')
def post_delete(id):
    post=Posts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("posts_db"))




























myapp.run(debug=True)
