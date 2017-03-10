
# ID Docs App

A work in progress

## Notes

## Choosing a state

Clickable maps sound nice.  Some possible solutions:

* https://newsignature.github.io/us-map/
* https://www.amcharts.com/download/ (costs money)
* http://createaclickablemap.com/ (but it depends on their server :()

## Things to solve for deployment

* Read (this)[https://www.djangorocks.com/tutorials/setting-up-your-server-to-run-django.html]
* switch between live and dev, (here)[https://www.djangorocks.com/snippets/seamless-switching-between-live-and-development.html]
* set STATIC_ROOT in settings.py, then run `python manage.py collectstatic`.  More (here)[https://docs.djangoproject.com/en/1.10/howto/static-files/].
* figure out the db we will use
