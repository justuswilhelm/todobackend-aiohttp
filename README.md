# Todo-Backend implemented in Python 3.5.0 / aiohttp

Live: http://todobackend-aiohttp.herokuapp.com

## Quickstart
```sh
virtualenv env  # Make sure that the venv has Python 3.5.0
source env/bin/activate
pip install -r requirements.txt
python run_server.py
```

Upon successfully launching, you can open up http://www.todobackend.com/specs/index.html?http://localhost:8000 in your browser and test against a reference Todo-MVC implementation.

## Deployment

If you intend to run the server in production, make sure to provide a reachable
hostname using the `HOST` environment variable. This gets used for returning a
valid task `url` attribute.

## Requirements

- Python 3.5.0
- Virtualenv
