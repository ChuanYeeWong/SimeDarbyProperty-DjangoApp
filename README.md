# Simedarby VMS

## Requirements

```note
Python 3.5 or above
```

## Setup Instruction

This follow setup is for development stage. Which uses Sqlite as DB.

### 1. Setting up Environment

Run the following command.

```python
root:home$ virtualenv env
root:home$ . env/bin/activate
```

Result

```python
(env) root:home$
```

### 2. Install requirements

```python
(env) root:home$ pip install --no-cache-dir -r requirements.txt
```

### 3. Run server

```python
(env) root:home$ python manage.py runserver 0.0.0.0:8000
```

## Update CSS Theme

```bash
sass static/jet/css/themes/simedarby/base.scss static/jet/css/themes/simedarby/base.css
```