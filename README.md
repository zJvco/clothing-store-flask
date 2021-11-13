# Clothing Store
Clothing Store is a website for purchases clothes. The project were made in Flask witch is a micro-framework Python, I did this project to improve my habilities for web and for my final project in CS50x Harvard University.

#### Video Demo: <https://www.youtube.com/watch?v=rF4OugBhkxU>

## Dependencies
This project depends on many libraries to run, this libraries are in requirements.txt, you can run:
```
pip3 install -r requirements.txt
```
I'm using SQLite3, this database comes with python by default and you don't have to install that.

## Design
The project were basead on Design Patters MVC (model, view, control) with some changes, Flask by default use the design MVT (model, view, template) basicly is the same like MVC, in this patter we can divide the functionalities to get better when we are manufacturing or refactoring the code.

### Model Layer
This layer is for any data to persist in database, in my project this layer contain the database tables in classes format because I'm using Flask-SQLAlchemy, this is a ORM, basicly this library transform our classes to table and our atributes to columns in database.

### View Layer
This layer is to control our application and is intermediate between our template layer and our model layer its in this layer witch we run our logic to do calculus, validation, bussiness logic, etc.

### Template Layer
The template layer is the part that user can see, in there, we store our html files.

## Project
Inside my app folder we have the application files, I will explain what each files do and contain in sections below.

### __init__.py File
This file contain our flask and our libraries setup, I use a method called Factory Function, this is to prevent circular imports witch thats is commom in Python and to organize our libraries instances objects.

### admin.py File
This file contain our administration interface, we can add sections to our app to manage products and users. Basicly, I put three classes to manage our users, products and products categories.

### auth.py File
This file contain our routes to sign in, sign up and logout users and have more control of authentication methods. I'm using auth blueprint to auth file.

### cli.py File
This file contain our cli (Command Line Interface) to create a new user, give admin to an specify user, create database, drop database and delete a user. Its very helpful to do things when we don't have a administration interface.

Create user command:
```
flask create_user -u [username] -e [email] -p [password]
```
Delete user command:
```
flask delete_user -id [user id]
```
Make user admin command:
```
flask make_admin --email / -e [user email]
```
Create database command:
```
flask create_db
```
Drop database command:
```
flask drop_db
```

### forms.py File
This file contain our html forms using a library WTF-Forms, this library render our html form in server-side and give to our html file through jinja. Inside this file we have sign up form, sign in form, address form, edit address form, profile form and deposit form.

### models.py File
This file is responsible to our data models to persist in the database, we are using a ORM named SQLAlchemy, this library made easy to us to put data and make relationship between table. Inside this file we have user class, product class, category class, address class, order details class and order class.

### utils.py File
This file is only to store our function or utilities code to use in our web application.

### views.py File
This file contain our majority routes and is the logic of our application. Inside this we have many routes, for example our home, store, profile, cart, buy, address and deposit pages. I'm using a single blueprint to views file, because it is a small project, so, this blueprint is to separete our routes to mantain our application more organized.

## Migrations
The library Flask-Migrate give us to modify our database struct without altering data.