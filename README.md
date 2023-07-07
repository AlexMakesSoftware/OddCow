# 🐄 OCD / RMT

Odd Cow Disease / Record Management Tool

## Outline

Odd Cow Disease - Report Management Tool.

An exercise in using django for praciticing integrtating django with an exisiting data set.

The basic idea:

There's a legacy database we pulled out of some horrible system that cost the taxpayer way too much money, for which we do not have direct read-only access. We get a bi-weekly copy of it (which often fails to update).

In addition to this, we create a model-first database which records new disease outbreaks using a new format of report. This report needs to include data which partly comes from the legacy database (coppied in) and partly gets entered by the user.

## To Build:

From inside the project directory:

python -m venv django-ocd
django-ocd\Scripts\activate
pip install -r requirements.txt

You might need to create the models seperately, like so:
```
python manage.py makemigrations farms
python manage.py makemigrations reports
```

Then run the migrations:
```
python manage.py migrate
python manage.py migrate --database legacy
```

You need to run the seperate migration for the legacy database, don't ask me why.

Don't forget to create the admin acount too:
```
python .\manage.py createsuperuser
```

