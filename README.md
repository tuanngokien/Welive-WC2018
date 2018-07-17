# WELIVE
WC2018 livescore chatbot

## Screenshots
Livescore             |  Schedule
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/26508575/42835648-7c298dbc-8a23-11e8-9a9c-4b04cf832d3f.png)  |  ![](https://user-images.githubusercontent.com/26508575/42835673-8b656ce2-8a23-11e8-8b6d-68ff44fee00f.png)

## Build
It is best to use the python `virtualenv` tool to build locally:

```sh
$ virtualenv venv -p python3
$ source venv/bin/activate
$ cd t4w
$ pip install -r requirements.txt
$ Setup DB connection and SECRET_KEY in .env
$ source .env
$ python manage.py migrate
$ python manage.py runserver
```

Then visit `http://localhost:8000` to enjoy the app.
