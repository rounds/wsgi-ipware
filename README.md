This is a fork of wsgi-ipware (itself a fork for django-ipware).

This repo was forked in order to add support for Flask. 
the previous fork (wisgi-ipware) was still limited to django in assuming that headers are provided in CAPITAL, underscore format (like X_FORWARDED_FOR). It appears headers in flask can only be retreived in lowercase/dash format (like x-forwarded-for).

also re-organized file to form a valid package that can be pip installed.
