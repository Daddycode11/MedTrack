# 01. Project Structure


## 01.1 Main Folders and Files
The root directory of the project contains the following files and folders:

```plaintext
medtrack-django/
├── .github/
├── docs/
├── medtrack/
├── .gitignore
├── LICENSE
├── README.md
```
### `docs/`
This directory contains the documentation for the project. It includes guides,
tutorials, and references to help you understand and use the project
effectively.
### `medtrack/`
This is the main application directory. It contains the core code for the
project, including models, views, templates, and static files.
### `.gitignore`
This file specifies files and directories that should be ignored by Git. This is
used to prevent sensitive information and unnecessary files from being tracked
in the repository.
### `LICENSE`
This file contains the license information for the project. It specifies the
terms under which the project can be used, modified, and distributed.
### `README.md`
This file provides an overview of the project, including its purpose, features,
and how to get started. It is the first place new users should look for
information about the project.

## 01.2 How a Django Project Works

A Django project is structured around the Model-View-Template (MVT)
architecture. This architecture separates the data model, user interface, and
control logic into distinct components, making it easier to manage and maintain
the codebase.

Within the `medtrack/` directory, you will find folders for each application in
the project. An **application** is a self-contained module that provides a
specific functionality within the project. Each application has its own models,
views, templates, and static files, allowing for modular development and easier
code reuse.

At the root of the `medtrack/` directory, you will also find the following
files:
- `manage.py`: This file is a command-line utility that allows administrators to
  interact with the Django project. It provides commands for deploying, testing,
  and managing the project.
- `requirements.txt`: This file lists the Python packages required to run the
  project. It is used to install dependencies using pip.
- `db.sqlite3`: This file is the default SQLite database for the project and
  will be created automatically when the project is initialized. It stores all
  the data for the project, including user accounts, medication records, and
  other information. To facilitate the demonstration of the project, a set of
  initial data is provided that can be loaded into the database by using the
  `initialize` functionality. This is defined in the
  `medtrack/management/commands/initialize.py` file and relies on the scripts
  available at the `medtrack/utils/initialization/` folder.

### What is MVT?

![MVT Architecture](https://miro.medium.com/v2/resize:fit:640/1*74GXFhRc14JeeWQyzqva-w.jpeg)

The Model-View-Template (MVT) architecture is a design pattern used in Django to
separate the data model, user interface, and control logic into distinct
components. This separation allows for better organization of code and easier
maintenance.

- **Model**: The model represents the data structure of the application. It
  defines the fields and behaviors of the data you are storing. In Django,
  models are defined as Python classes that inherit from
  `django.db.models.Model`. Each model corresponds to a database table when
  running migrations.
- **View**: The view is responsible for processing user requests and returning
  responses. It contains the business logic of the application and interacts
  with the model to retrieve or modify data. In Django, views are defined as
  Python functions or classes that handle HTTP requests and return HTTP
  responses.
- **Template**: The template is responsible for rendering the user interface. It
  defines how the data should be presented to the user. In Django, templates are
  defined using HTML and Django's template language, which allows for dynamic
  content generation.
- **URL Dispatcher**: The URL dispatcher is responsible for routing incoming
  requests to the appropriate view based on the URL pattern. In Django, this is
  done using a URLconf, which is a mapping of URL patterns to views.
- **Static Files**: Static files are files that do not change and are served
  directly to the user. This includes CSS, JavaScript, and images. In Django,
  static files are managed using the `django.contrib.staticfiles` app, which
  provides a way to collect and serve static files in development and
  production.



## 01.3 Applications

### `medtrack/medtrack/`

This is the main application directory for the project. It contains the
`settings.py` file, which is used to configure the project, including database
settings, installed applications, middleware, and other settings.

The `urls.py` file is used to define the URL patterns for the project. It maps
URLs to views, allowing users to access different parts of the application
through their web browser. It also includes the URL patterns for each
application in the project, allowing for modular development and easier code
reuse.
