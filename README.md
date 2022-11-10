# Invera ToDo-List Challenge (Python/Django Jr-SSr)

&nbsp;  
## Getting started
### Requirements
```
Django==4.1.3
djangorestframework==3.14.0
```

### 1. Cloning the project
```
git clone https://github.com/ostizjuan/todo-challenge.git
```
After that, follow these steps depending on whether you use Docker or not.
&nbsp;  
&nbsp;  

### 2.A. Docker
- If you are using ***Docker Compose***, run (in the root folder of the project):
```
docker compose up
```
&nbsp;  

- Otherwise, you will have to build it manually. To build the image:
```
docker build -t inv_todo:1 .
```
Next, we run the container:
```  
docker run -p 8000:8000 inv_todo:1
```
&nbsp;  
&nbsp;  

### 2.A.1. Tests with Docker
- To run tests with ***Docker Compose***:
```
docker compose run api python manage.py test
```

- Without ***Docker Compose***:
```
docker run -p 8000:8000 inv_todo:1 python manage.py test
```
&nbsp;  
&nbsp;  

### 2.B. Manual installation
1. ****Optional***: i recommend you create a virtual environment:
```
python -m venv ./venv
```
&nbsp;  

2. *To activate the venv:
  - On Windows:
  ```
  venv/Scripts/activate
  ```
  - On Linux:
  ```
  source bin/activate
  ```
&nbsp;  

3. Install the requirements:
```
pip3 install -r requirements.txt
```
&nbsp;  

4. Run the server:
```
python manage.py runserver
```
&nbsp;  
&nbsp;  

### 2.B.1. Test
- To manually run the tests:
```
python manage.py test
```
&nbsp;  
&nbsp;  

## Endpoints

| HTTP Methods  | URL           | Optional params  |
| ------------- |:-------------- |:----------------- |
| `GET`           | `http://127.0.0.1:8000/api/tasks/` | `pk/id` or `?content='something'` and/or `created_at='some date'` |
| `POST`          | `http://127.0.0.1:8000/api/tasks/?content=”This%20is%20a%20new%20task”` |    |
| `PATCH`         | `http://127.0.0.1:8000/api/tasks/<id>/` |    |
| `DELETE`        | `http://127.0.0.1:8000/api/tasks/<id>/`  |    |

&nbsp;  
&nbsp;  

## Usage
The database comes with a superuser who will be in charge of testing. The API works with Basic Auth.
&nbsp;  
| Username  | Password  |
| :-------- |:----------|
| `admin`   | `1234`    |

&nbsp;  

### 1. Using Postman
Go to the `Authorization` tab, select `Basic Auth` and enter the user information.
&nbsp;  

<img src="https://user-images.githubusercontent.com/81332665/201179985-d9641ba1-14b0-4039-bcc7-6a6d391ad29f.png" width=75% alt="postman" />
&nbsp;  
Now you can make any request you wish.

&nbsp;  

### 2. Using the Python requests library
Example code:
```
import requests

url = "http://127.0.0.1:8000/api/tasks/"
username = "admin"
password = "1234"
response = requests.get(url, auth=(username, password))
print(response.status_code)
print(response.json())
```
&nbsp;  

### 3. Using a browser

1. First, you need to log in to [`http://127.0.0.1:8000/admin/login/`](http://127.0.0.1:8000/admin/login/)
2. Now, you can access to `http://127.0.0.1:8000/api/tasks/`.
