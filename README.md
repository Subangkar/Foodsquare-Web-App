# FoodSquare
An online restaurant hub to manage food items, offers & delivery for each restaurant individually by their respective owners.  
This repo contains the web app for this system implemented in Django-2.2 with Model-View-Template design pattern. This was an Information System Design project, part of an academic course of CSE, BUET. So some of the best practices of system design could not be maintained properly.
  
**Spec:**
  - Web Framework: Django 2.2
  - Database Server: PostgreSQL 12.3
  
**How to run:**
 - Clone the [github repo](https://github.com/Subangkar/Foodsquare-Web-App)
 - Now you can either run in [docker containers](https://www.docker.com/) of a [pre-built image on docker hub](https://hub.docker.com/r/subangkar/foodsquare) of this repo **or** create an python & database environment yourself
    - **Docker**
        - install [docker](https://docs.docker.com/engine/install/) & [docker-compose](https://docs.docker.com/compose/install/) on your system (if not installed)
        - move to the project directory & start the docker containers using the following commands
        ```shell
        docker-compose build
        docker-compose up
        ```
        - now browse the site at http://localhost:8000/ 
        - **N.B.** Here [remote docker image](https://hub.docker.com/r/subangkar/foodsquare) is used in docker compose. Alternately, you can build a new docker image using `Dockerfile` & use it in composer.

    - Or, **Python Environment/Database setup**
        - install postgres database
        - create a new database in your postgres server named `foodsquare` with owner as `postgres`, password as  `postgres`   
        - start the postgres server on port 5432 
        - move to the project directory 
        - create a virtual environment & activate it
        ```shell
        python3 -m pip install --upgrade pip
        python3 -m venv venv
        source venv/bin/activate
        ```
        - install dependencies & make migrations
        ```shell
        python3 -m pip install -r requirements.txt
        python3 manage.py makemigrations
        python3 manage.py migrate
        ```
        - now run the server finally
        ```shell
        python3 manage.py runserver
        ```
        - now browse the site at http://localhost:8000/ 
        - **N.B.** a facebook login app needs to be set up & its credentials are to be addded into database properly to access login pages.  
          For ease, an app is created & its credentials are provided into a dumped json file which can be loaded into the database using:
        ```shell
        python3 manage.py loaddata data.json
        ```
 - **N.B.** Facebook/Google login may not work properly as those login apps credentials might be outdated now.          
          
          
**Some Basic Functionalities Implemented:**
- User Session Handling
- Third Party Authentication
- Sub-domain Handling
- Shopping Cart Management
- Local Storage Handling
- Online Payment Handling
- Review-Rating Management

Docker Hub Repo: https://hub.docker.com/r/subangkar/foodsquare
