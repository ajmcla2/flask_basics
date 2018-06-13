from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy #flask_sqlalchemy is the module and SQLAlchemy is the Class
from datetime import datetime

app = Flask(__name__)

#define environment variables for the project and database we are going to use

#general purpose python dictionary
#SQLALCHEMY_DATABASE_URI='database://userid:password@server:port/databasename'
app.config.update(

    SECRET_KEY='alpha3786',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:alpha3786@localhost:5433/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

#SQLAlchemy is our class here
#db is our database instance
#we pass our flask application instance into the database instance
db = SQLAlchemy(app)

@app.route('/index')
@app.route('/')
def hello_flask():
    return 'Hello Flask!'

@app.route('/new')
def query_strings():
    query_val = request.args.get('greeting')
    return '<h1> the greeting is : {0} </h1>'.format(query_val)

#Getting Rid of Ugly Query Strings
@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='unknown person'):
    return '<h1> Hello there, {} </h1>'.format(name)

#Strings
@app.route('/text/<string:name>')
def working_with_strings(name):
    return '<h1> here is a string: ' + name + '</h1>'

#We will run into a TYPE ERROR
#Numbers and Strings
@app.route('/numbers/<int:num>')
def working_with_numbers(num):
    return '<h1> here is a number: ' + num + '</h1>'

#Numbers (integers)
#Quote the html, then .format then add in the remainig html quote to finish it off
#Note: 10 will work, 10.0 will not
@app.route('/add/<int:num1>/<int:num2>')
def add_integers(num1,num2):
    return '<h1>the sum is: {0}'.format(num1+num2) + '</h1>'

#Floats
#Note: 10.0 is a float, 10 is an int.  10 will not work, but 10.0 will.
@app.route('/product/<float:num1>/<float:num2>')
def product_two_numbers(num1,num2):
    return '<h1>the sum is: {0}'.format(num1+num2) + '</h1>'

#Render HTML Templates
@app.route('/temp')
def using_templates():
    return render_template('hello.html')

#Work with Jinja using PYTHON Variables and Logic within HTML
@app.route('/watch')
def movies_2017():
    movie_list = ['autopsy of jane doe','ghost in a shell','kong: skull island','john wick2','spiderman - homecoming']
    return render_template('movies.html',movies=movie_list,name='Marry')

#Work with HTML Tables
@app.route('/tables')
def movies_plus():
    movies_dict = {'autopsy of jane': 02.14,'neon demon': 3.20,'ghost in a shell': 1.50,'john wick 2': 02.52,'spiderman - homecoming': 1.48}
    return render_template('table_data.html',movies=movies_dict,name='Sally')

@app.route('/filters')
def filter_data():
    movies_dict = {'autopsy of jane': 02.14,'neon demon': 3.20,'ghost in a shell': 1.50,'john wick 2': 02.52,'spiderman - homecoming': 1.48}
    return render_template('filter_data.html',movies=movies_dict,name=None,film='a christmas carol')

@app.route('/macros')
def jinja_macros():
    movies_dict = {'autopsy of jane': 02.14,'neon demon': 3.20,'ghost in a shell': 1.50,'john wick 2': 02.52,'spiderman - homecoming': 1.48}
    return render_template('using_macros.html',movies=movies_dict)


#Create SQL tables
class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'The id is {}, Name is {}'.format(self.name)

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())
    #Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    #pub_date is a default value, so do not specify
    #primary keys are auto-generated, so do not specify
    def __init__(self,title,author,avg_rating,book_format,image,num_pages,pub_id):
        self.title=title
        self.author=author
        self.avg_rating=avg_rating
        self.format=book_format
        self.image=image
        self.num_pages=num_pages
        self.pub_id=pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)

if __name__ == '__main__':
    db.create_all() #creates all the tables if they don't exist
    app.run(debug=True)
