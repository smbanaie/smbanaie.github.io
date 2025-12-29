"""
Sample user configuration used by the Tornado admin handlers.

Edit the values below to match your local environment. The Tornado app
imports this module and expects at least `USER_DIR`, `AUTHORS`, and
`CATEGORIES` to be defined.

Your public site: https://github.com/smbanaie/smbanaie.github.io
"""

from pathlib import Path

# Local path to the Pelican project (change this to your local clone)
USER_DIR = r"e:\Projects\pelicanwebsitebuilder\user_area\smbanaie\smbanaie"

# Convenience: content directory inside USER_DIR
CONTENT_DIR = str(Path(USER_DIR) / "content")

# Author list used by the admin form
AUTHORS = ['مجتبی بنائی']

# Categories used by the admin UI. Format expected by the handler:
# CATEGORIES['cat_list'] is a list of tuples (id, display_name)
# CATEGORIES['default_category'] is the default category ID for new articles
# CATEGORIES['status'] is a dict mapping category ID to status ('active' or 'inactive')
CATEGORIES = {
    "cat_list": [
        ("Culture", "فرهنگ و جامعه"),
        ("Diary", "روزنوشت"),
        ("Meditation", "بر بلندای شعر و عرفان"),
        ("Self-Contemplation", "پرواز اندیشه"),
        ("Misc", "از گوشه و کنار"),
        ("Tech", "فناوری")
    ],
    "default_category": "Diary",
    "status": {
        "Culture": "active",
        "Diary": "active",
        "Misc": "active",
        "Self-Contemplation": "active",
        "Tech": "active",
        "Meditation": "active"
    }
}

# Default author for new articles
DEFAULT_AUTHOR = "مجتبی بنائی"

# Author status mapping (active/inactive)
AUTHOR_STATUS = {'مجتبی بنائی': 'active'}

# Optional: remote repo where you publish the built site
SITE_REPO = "https://github.com/smbanaie/smbanaie.github.io"

# Optional image directory (relative to static or CONTENT_DIR as you prefer)
DEFAULT_IMAGE_PATH = str(Path(USER_DIR) / "images")
