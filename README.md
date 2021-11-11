# Clothing Store
Clothing Store is a website for purchases clothes. The project were made in Flask witch is a micro-framework Python, I did this project to improve my habilities for web and for my final project in CS50x Harvard University.

## Dependencies
This project depends on many libraries to run, this libraries are in requirements.txt, you can run:
```
pip3 -r install requirements.txt
```

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

# __init__ File
This file contain our flask and our libraries setup, I use a method called Factory Function, this is to prevent circular imports witch thats is commom in Python and to organize our libraries instances objects.

# admin File
This file contain our administration interface, we can add sections to our app to manage products and users. Basicly, I put three classes to manage our users, products and products categories.

# auth File
This file contain our routes to sign in, sign up and logout users and have more control of authentication methods.

# cli File
This file contain our cli (Command Line Interface) to create a new user, give admin to an specify user, create database, drop database and delete a user. Its very helpful to do things when we don't have a administration interface.