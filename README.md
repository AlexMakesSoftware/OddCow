# 🐄 OCD / RMT

Odd Cow Disease / Record Management Tool

## Outline

Odd Cow Disease - Report Management Tool.

A learning exercise in using django for praciticing integrtating django with an exisiting data set. Not for use in production!

The main app components:
 - A legacy database we pulled out of some ancient system, for which we do not have direct read-only access for... reasons.
 - A new (default) database which records new incidents using a new format of report. This report needs to include data which partly comes from the legacy database (coppied in) and partly gets entered by the user.

## To Setup:

Refer to: https://docs.python.org/3/library/venv.html#creating-virtual-environments
On how to create the virtual environment.

On windows, from inside the project directory:

```
python -m venv django-ocd
django-ocd\Scripts\activate
pip install -r requirements.txt
```

On linux you probably need:
```
python -m venv django-ocd
source django-ocd/bin/activate
pip install -r requirements.txt
```

Run the migrations:
```
python manage.py migrate
python manage.py migrate --database legacy
```

*NOTE:* You need to run the seperate migration for the legacy database.

Don't forget to create the admin acount too:
```
python manage.py createsuperuser
```

You might like to create some example data with:

```
python manage.py create_farms 17000 60
```

Should create 17,000 farms and distribute them roughly 60 per parish. All the data is randomly generated. No incidents though. You can currently only run this command once (with a new database) as it's not very intelligent. Maybe I'll change that one day.

