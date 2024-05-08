from flask import Flask,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,ValidationError,Length
app=Flask(__name__)
db=SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.secret_key="wordpass123"
app.json.compact=False
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(40),nullable=False,unique=True)
    password=db.Column(db.String,nullable=False)

class RegisterForm(FlaskForm):
    name=StringField(validators=[Length(min=4,max=20),InputRequired('Cannot enter an empty name')],render_kw={"place_holder":"Enter a name"})
    password=PasswordField(validators=[InputRequired("Must enter a password"),Length(min=10,max=50)],render_kw={"Password":"Password"})
    submit=SubmitField("Register")
    def validate_name(self,name):
        existing_user_name=User.query.filter(User.username==name) .first()
        if existing_user_name:
            raise ValidationError("Username already eixsts")

class LoginForm(FlaskForm):
    name=StringField(validators=[Length(min=4,max=20),InputRequired('Cannot enter an empty name')],render_kw={"place_holder":"Enter a name"})
    password=PasswordField(validators=[InputRequired("Must enter a password"),Length(min=10,max=50)],render_kw={"Password":"Password"})
    submit=SubmitField("Login")
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login",methods=["POST","GET"])
def login():
    return render_template("login.html" ,form=LoginForm)

@app.route("/register")
def register():
    return render_template("register.html",form=RegisterForm)
if __name__=="__main__":
    app.run(port=5555,debug=True)