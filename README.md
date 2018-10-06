# Hack NC 2018

## Get Started

### Setup

```
git clone https://github.com/DersJ/hackNC2018
cd hackNC2018
mkvirtualenv --python python3.6 hackNC
setvirtualenvproject
```

### DB Config

```
hacknc/manage.py migrate
hacknc/manage.py createsuperuser
```

### Run the Server

```
hacknc/manage.py runserver
```
