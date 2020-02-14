#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from os import listdir
from os.path import isfile, join
import yaml, json, sys


AUTHOR = 'سید مجتبی بنائی'
SITENAME = 'سایت شخصی سید مجتبی بنائی'
SITEDESCRIPTION = 'روزنوشت‌ها و مطالب شخصی سید مجتبی بنائی'
SITEURL = 'http://banaie.ir'
# SITEURL = ''
DISPLAY_PAGES_ON_HOME = True
ARTICLE_PATHS = ['blog']
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{slug}.html'

OUTPUT_PATH = 'public'

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight','pygments_style':'native'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}




#DEFAULT_PAGINATION = 10

# plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = [
			'i18n_subsites',
			'tipue_search',
			'sitemap',
			'pelican_persian_date',
			'ga_page_view'
]
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

# theme and theme localization
THEME = 'themes/pelican-fh5co-marble'
I18N_GETTEXT_LOCALEDIR = 'themes/pelican-fh5co-marble/locale/'
I18N_GETTEXT_DOMAIN = 'messages'
I18N_GETTEXT_NEWSTYLE = True

TIMEZONE = 'Asia/Tehran'

DEFAULT_DATE_FORMAT = {
    'fa': '%A %d %B %Y'
}
DATE_FORMATS = {
    'fa': '%A %d %B %Y'
}

I18N_TEMPLATES_LANG = 'fa_IR'
DEFAULT_LANG = 'fa'
LOCALE = 'fa_IR'

# content paths
PATH = 'content'

STATIC_PATHS = ['images','extra/CNAME','extra/favicon.ico','extra/robots.txt','extra/staticman.yml']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/CNAME': {'path': 'CNAME'},
	'extra/staticman.yml': {'path': 'staticman.yml'},
}

PAGE_PATHS = ['pages/fa']
ARTICLE_PATHS = ['blog/fa']

# i18n
I18N_SUBSITES = {
  'en': {
    'PAGE_PATHS': ['pages/en'],
    'ARTICLE_PATHS': ['blog/en'],
    'LOCALE': 'en_EN'
  }
}

# logo path, needs to be stored in PATH Setting
LOGO = '/images/logo.jpg'

# Social widget
SOCIAL = (
  ('Github', 'https://www.github.com/smbanaie'),
  ('Facebook', 'https://www.facebook.com/smbanaie'),
  ('Twitter', 'https://www.twitter.com/smbanaie'),
  ('Linkedin', 'https://www.linkedin.com/in/smbanaie/')
)

ABOUT = {
  'image': '/images/static/book.jpg',
  'mail': 'mojtaba.banaie@gmail.com',
  # keep it a string if you dont need multiple languages
  'text': {
    'en': 'Learn more about the creator of this theme or just drop a message.',
    'de': 'Lernen Sie den Author kennen oder hinterlassen Sie einfach eine Nachricht',
	'fa' : 'به جهان خرم از آنم که جهان خرم ازوست .... عاشقم بر همه عالم که همه عالم ازوست'
  },
  'link': 'contact.html',
  # the address is also taken for google maps
  'address': 'دانشگاه بزرگمهر قائنات',
  'phone': '056-31006600-4'
}

# navigation and homepage options
DISPLAY_PAGES_ON_MENU = True
DISPLAY_PAGES_ON_HOME = True
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_TAGS_ON_MENU = False
USE_FOLDER_AS_CATEGORY = True
PAGE_ORDER_BY = 'order'

MENUITEMS = [
  ('Archive', 'archives.html'),
  ('Contact', 'contact.html')
]

DIRECT_TEMPLATES = [
  'index',
  'tags',
  'categories',
  'authors',
  'archives',
  'search', # needed for tipue_search plugin
  'contact' # needed for the contact form
]

# setup disqus
#DISQUS_SHORTNAME = 'gitcd-dev'
#DISQUS_ON_PAGES = False # if true its just displayed on every static page, like this you can still enable it per page

# setup google maps
#GOOGLE_MAPS_KEY = 'AIzaSyCefOgb1ZWqYtj7raVSmN4PL2WkTrc-KyA'

GOOGLE_TRACKING_ID = "UA-13075446-1"

# Sitemap
SITEMAP = {
'format': 'xml',
'priorities': {
'articles': 0.5,
'indexes': 0.5,
'pages': 0.5
},
'changefreqs': {
'articles': 'monthly',
'indexes': 'daily',
'pages': 'monthly'
}
}

#Staticman Comments
commentsPath = "./content/comments"
import codecs 
def ymlToJson(file):
    with codecs.open(commentsPath + "/" + file,"r","utf-8") as stream:
        return yaml.safe_load(stream)

commentsYML = [f for f in listdir(commentsPath) if isfile(join(commentsPath,f))]
COMMENTS = list(map(ymlToJson, commentsYML))



#GA Page VIEWS
GOOGLE_SERVICE_ACCOUNT = 'banaieir@banaieir.iam.gserviceaccount.com '
GOOGLE_KEY_FILE = 'banaieir-85b57c291398.json'
GA_START_DATE = '2018-07-20'
GA_END_DATE = 'today'
GA_METRIC = 'ga:pageviews'
POPULAR_POST_START = '1monthAgo'
