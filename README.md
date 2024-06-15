# Django Caching Example

This Django project demonstrates how to implement caching for models using a custom manager and query set. It includes unit tests to verify the caching functionality.

## Requirements

- Python 3.12+
- Django 5.0+
- django-extensions (for `shell_plus`)

## Setup

1. **Clone the repository**:

    ```sh
    git clone git@github.com:cerodriguez/django-cache.git
    cd django-cache
    ```

2. **Create a virtual environment and activate it**:

    ```sh
    python -m venv env
    source env/bin/activate 
    ```

3. **Install dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations**:

    ```sh
    python manage.py migrate
    ```

5. **Playground to check runtime**:
    ```sh
    python manage.py < load.py
    ```

## Configuration

Ensure your Django settings are configured for caching. This example uses the `locmem` backend for simplicity.

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}```

## Note on Decorators
There is an implementation of decorators for adding caching functionality in foo/decorators.py. However, these decorators are not working well at the moment. 

```python
# Example of using the decorator (not currently recommended due to issues)
from myapp.decorators import cache_model

@cache_model
class MyModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
```

