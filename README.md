
# ID Docs App

A work in progress

## Notes

## Choosing a state

Clickable maps sound nice.  Some possible solutions:

* https://newsignature.github.io/us-map/
* https://www.amcharts.com/download/ (costs money)
* http://createaclickablemap.com/ (but it depends on their server :()

## Things to solve for deployment

* add site search: https://support.google.com/customsearch/answer/4541888?hl=en
* backups.  See (this)[https://github.com/django-dbbackup/django-dbbackup] and (this)[https://github.com/nathan-osman/django-archive/blob/master/docs/settings.rst]
* Read (this)[https://www.djangorocks.com/tutorials/setting-up-your-server-to-run-django.html]
* set STATIC_ROOT in settings.py, then run `python manage.py collectstatic`.  More (here)[https://docs.djangoproject.com/en/1.10/howto/static-files/].
* figure out the db we will use
