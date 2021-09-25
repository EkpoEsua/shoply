# Shoply

A simple shopping cart web app in Django;
* Items can be added to the cart, and removed.
* The Quantity of an item in the cart can be modfied.
* The Cart can be checked out (cleared).
* The Product inventory can also be managed by an admin user.

`Forms` | `ModelFormSet`

## Installing the app

Requires `Python3 => v3.8.10` | `git`

* Clone git folder. 
        
        git clone https://github.com/ekpoesua/shoply.git

* Change directory. 

        cd shoply

* Setup virtual environment. 

        python3 -m venv venv

* Activate virtual environment.

        source venv/bin/activate

* Install app dependencies. 
        
        pip install -r requirements.txt

* Run database setup. 
    
        python manage.py makemigrations
        python manage.py migrate

* Run Tests (Optional)

        python manage.py test

* Start app

        python manage.py runserver

* Use the app on [http://127.0.0.1:8000/](http://127.0.0.1:8000/)


## Configure admin

* Stop app if running.

* Configure admin login

        python manage.py createsuperuser

* Start app and login with credentials on [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
