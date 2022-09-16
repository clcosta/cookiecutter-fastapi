# Welcome to {{ cookiecutter.project_name }}
{{ cookiecutter.description }}  


### Basic Usage
```bash
{% if cookiecutter.python == 'python venv' %}pip install -r requirements.txt{% elif cookiecutter.python == 'poetry' %}poetry install{% endif %}
# OR
make install ${PYTHON_PATH} 
# default value is "python.exe"
```
For more informations:
```bash
make help
```

# Autor
| [<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/-Insert_image_here-.svg/1280px--Insert_image_here-.svg.png" width=120><br><sub>@{{cookiecutter.github_user}}</sub>](https://github.com/{{cookiecutter.github_user}}) |
| :---: |
