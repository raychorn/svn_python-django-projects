# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Django settings for this project.

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

from vyperlogix.google.gae import gae_utils

_is_running_local = gae_utils.is_running_local()

#if (_is_running_local):
    #DATABASE_ENGINE = 'mysql'      # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
    #DATABASE_NAME = 'resources'    # Or path to database file if using sqlite3.
    #DATABASE_USER = 'root'         # Not used with sqlite3.
    #DATABASE_PASSWORD = 'peekab00' # Not used with sqlite3.
    #DATABASE_HOST = 'sql2005'      # Set to empty string for localhost. Not used with sqlite3.
    #DATABASE_PORT = '3306'         # Set to empty string for default. Not used with sqlite3.
#else:
DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

from google.appengine.api import memcache

_navigation_menu_type = memcache.get("_navigation_menu_type")
if (_navigation_menu_type is None):
    from vyperlogix.django import tabs
    _navigation_menu_types = tabs._navigation_menu_types
    _navigation_menu_type = _navigation_menu_types[2]

    if not memcache.add("_navigation_menu_type", _navigation_menu_type, 60):
        logging.error("Memcache set failed for _navigation_menu_type.")
    
_navigation_tabs = memcache.get("_navigation_tabs")
if (_navigation_tabs is None):
    _navigation_tabs = []
    _navigation_tabs.append(tuple(['/','Home','"Vyper Logix Corp specializes in building products and systems based entirely on the Python Language."']))
    _navigation_tabs.append(tuple(['http://www.pypi.info/','Blog','Visit your <u>Py</u>thon <u>P</u>remier <u>I</u>nformation&trade; site.']))
    _navigation_tabs.append(tuple(['/about/','About','About this site.']))
    
    if (_is_running_local):
        _navigation_tabs.append(tuple(['/_admin/','Admin Mode','Administrative functions.']))
    
    if not memcache.add("_navigation_tabs", _navigation_tabs, 60):
        logging.error("Memcache set failed for _navigation_tabs.")

_title = memcache.get("_title")
if (_title is None):
    _title = 'Vyper Logix Corp, The Python Resource Company'
    if not memcache.add("_title", _title, 60):
        logging.error("Memcache set failed for _title.")
        
conn_str = memcache.get("conn_str")
if (conn_str is None):
    conn_str = 'mysql://root:peekab00@sql2005:3306/resources'
    if not memcache.add("conn_str", conn_str, 60):
        logging.error("Memcache set failed for conn_str.")

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'  # i.e., Mountain View

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Whether to append trailing slashes to URLs.
APPEND_SLASH = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = '37d09f2c-d51f-4c24-8ba9-6bc49123d1e9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

if (_is_running_local):
    ROOT_URLCONF = 'urls'
else:
    ROOT_URLCONF = 'pypi-resources.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

if (_is_running_local):
    INSTALLED_APPS = (
        #'django.contrib.admin',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'resources'
    )
else:
    INSTALLED_APPS = (
        #'django.contrib.admin',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'pypi-resources'
    )
