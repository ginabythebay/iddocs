
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
* backups.  See https://github.com/django-dbbackup/django-dbbackup and https://github.com/nathan-osman/django-archive/blob/master/docs/settings.rst
* can we turn off http? (first try redirected to .../public, which is borken)
* set up (sitemaps)[https://docs.djangoproject.com/en/1.10/ref/contrib/sitemaps/]
* Read (this)[https://www.djangorocks.com/tutorials/setting-up-your-server-to-run-django.html]
* figure out the db we will use
