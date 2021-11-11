### Clothing Store
Clothing Store is a website for purchases clothes. The project were made in Flask witch is a micro-framework Python, I did this project to improve my habilities for web and for my final project in CS50x Harvard University.

## Dependencies
This project depends on many libraries to run, this libraries are in requirements.txt, you can run:
```
pip3 -r install requirements.txt
```

## Design
The project were basead on Design Patters MVC (model, view, control) with some changes, Flask by default use the design MVT (model, view, template) basicly is the same like MVC, in this patter we can divide the functionalities to get better when we are manufacturing or refactoring the code.

# Model Layer
This layer is for any data to persist in database, in my project this layer contain the database tables in classes format because I'm using Flask-SQLAlchemy, this is a ORM, basicly this library transform our classes to table and our atributes to columns in database.

# View Layer
This layer is to control our application and is intermediate between our template layer and our model layer its in this layer witch we run our logic to do calculus, validation, bussiness logic, etc.

# Template Layer
The template layer is the part that user can see, in there, we store our html files.