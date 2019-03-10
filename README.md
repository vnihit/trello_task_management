# task_management
##Trello like Task Management Board

To run the project:

* install Docker
* In the project directory type: ```docker-compose build```
  This will build the project backend and frontend containers together with MySQL db image.
* Run the docker containers: ```docker-compose up```
* In a new terminal type: ```docker-compose exec backend bash``` to enter the backend container bash.
* Here we need to migrate the database: 
```python3 manage.py makemigrations```    
```python3 manage.py migrate```
* Go to localhost:3000 in your browser to render a basic front end.

