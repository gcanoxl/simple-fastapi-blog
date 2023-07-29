# simple-fastapi-blog
A simple blog api server written with Python and FastAPI

# Installation 
```sh
git clone https://github.com/gcanoxl/simple-fastapi-blog.git
python3 -m venv venv
source /venv/bin/activate
pip install -r requirements.txt
```
# Run
**Make sure you are in the root directory of the project folder.**
```sh
uvicorn app:main:app --reload
```

Then, open http://localhost:8000/docs in your browser to see the API documentation generated by Swagger.

# Test
```sh
pytest
```

# Deployment
```sh
uvicorn main:app --host 0.0.0.0 --port 80
```


# TODO 
- [ ] User Info 
- [ ] User Update
- [ ] User Delete
