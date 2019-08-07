import os
from .development import *

"""
set your all testing environment here.
"""

# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
        # 'default': {
        #     'ENGINE': 'django.contrib.gis.db.backends.mysql',
        #     'NAME': 'ka01BFfxz2',
        #     'USER': 'ka01BFfxz2',
        #     'PASSWORD': '01wpjKuCj4',
        #     'HOST': '37.59.55.185',
        #     'PORT': '3306',
        # },
        'default': {
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'ENGINE': 'django.db.backends.sqlite3',
        },
}
