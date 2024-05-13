"""
WSGI config for wxappDjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wxappDjango.settings")

application = get_wsgi_application()


#
import os
from os.path import join,dirname,abspath
PROJECT_DIR = dirname(dirname(abspath(__file__)))


import sys
sys.path.insert(0,PROJECT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "examsys.settings")


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
 
#added
# from os.path import join,dirname,abspath 
# import sys

# PROJECT_DIR = dirname(dirname(abspath(__file__))) 	
# sys.path.insert(0,PROJECT_DIR)


#new
# import os
# from os.path import join,dirname,abspath#1.
# PROJECT_DIR = dirname(dirname(abspath(__file__)))#2.

# import sys
# sys.path.insert(0,PROJECT_DIR)#3.
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "examsys.settings")

# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()


