#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import string
import os.path
import uuid
import jdatetime
import random
from tornado.template import Template, Loader


class CustomLoader(Loader):
    """Custom template loader that resolves extends paths relative to template root."""

    def load(self, name, parent_path=None):
        """Load a template, resolving extends paths correctly."""
        import os.path

        # If name contains '/' and doesn't start with '/' or '..',
        # it's likely an extends path that should be relative to root, not parent
        if '/' in name and not name.startswith('/') and not name.startswith('..'):
            # For extends like "admin/base.html", ignore parent_path and load from root
            return super(CustomLoader, self).load(name, None)
        else:
            # Use default behavior for other paths
            return super(CustomLoader, self).load(name, parent_path)


class TornadoRequestBase(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(TornadoRequestBase, self).__init__(application, request, **kwargs)
    
    def initialize(self):
        # Override template loader to fix path resolution
        import os
        template_path = os.path.join(os.path.dirname(__file__), "..", "templates")
        # Use our custom loader instead of Tornado's default
        self.template_loader = CustomLoader(template_path)
        
    def render(self, template_name, **kwargs):
        """Override render to ensure proper template path resolution."""
        # Ensure template_name is relative and doesn't contain '..'
        template_name = template_name.replace('..', '').lstrip('/')
        return super(TornadoRequestBase, self).render(template_name, **kwargs)
        
    def create_template_loader(self, template_path):
        """Override to ensure proper template path resolution."""
        import os
        # Use absolute path to templates directory
        abs_template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))
        return CustomLoader(abs_template_path)

    def _get_userconf_path(self):
        """Get the path to the userconf.py file."""
        import os
        from user_area.smbanaie.smbanaie.userconf import USER_DIR
        return os.path.join(USER_DIR, 'userconf.py')

    def _read_userconf_data(self):
        """Read the current userconf data."""
        from user_area.smbanaie.smbanaie.userconf import AUTHORS, CATEGORIES, DEFAULT_AUTHOR, AUTHOR_STATUS
        return {
            'AUTHORS': AUTHORS.copy(),
            'CATEGORIES': CATEGORIES.copy(),
            'DEFAULT_AUTHOR': DEFAULT_AUTHOR,
            'AUTHOR_STATUS': AUTHOR_STATUS.copy()
        }

    def _get_article_counts(self):
        """Scan content directory and count articles by author and category."""
        import os
        import glob
        import re
        from utils.logger_setup import logger

        author_counts = {}
        category_counts = {}

        # Get userconf data for mapping
        from user_area.smbanaie.smbanaie.userconf import AUTHORS, CATEGORIES

        # Create mapping from display names to IDs for categories
        category_display_to_id = {}
        for cat_id, cat_display in CATEGORIES.get('cat_list', []):
            category_display_to_id[cat_display] = cat_id

        # Add mappings for Persian category names found in articles
        persian_category_mappings = {
            'فرهنگ و جامعه': 'Culture',
            'روزنوشت': 'Diary',
            'تخصص': 'Tech',
            'تکنولوژی': 'Tech',
            'تخصصی': 'Tech',
            'فناوری': 'Tech',
            'بر بلندای شعر و عرفان': 'Meditation',
            'پرواز اندیشه': 'Self-Contemplation',
            'خواندنیها': 'Misc',
            'گوناگون': 'Misc',
            'متفرقه': 'Misc',
            'روحانیات': 'Meditation',
            'مراقبه': 'Meditation',
            'آرامش ذهنی و مراقبه': 'Meditation'
        }
        category_display_to_id.update(persian_category_mappings)

        # Get content directory path
        from user_area.smbanaie.smbanaie.userconf import CONTENT_DIR

        # Find all markdown files in blog directory
        blog_pattern = os.path.join(CONTENT_DIR, 'blog', '**', '*.md')
        blog_files = glob.glob(blog_pattern, recursive=True)

        # Log some file paths for debugging
        meditation_files = [f for f in blog_files if 'Meditation' in f]
        logger.info(f"Found {len(meditation_files)} Meditation files: {meditation_files[:3]}")

        for file_path in blog_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()


                # Extract metadata using regex
                authors_match = re.search(r'^authors:\s*(.+)$', content, re.MULTILINE)
                category_match = re.search(r'^category:\s*(.+)$', content, re.MULTILINE)

                # Debug for Meditation files
                if 'Meditation' in str(file_path):
                    logger.info(f"Processing Meditation file: {os.path.basename(file_path)}, category: {category_match.group(1).strip() if category_match else 'NO CATEGORY'}")

                # Count authors - map to userconf author names
                if authors_match:
                    author_line = authors_match.group(1).strip()
                    # Handle multiple authors (comma-separated)
                    article_authors = [a.strip() for a in author_line.split(',')]

                    for article_author in article_authors:
                        # Try to find matching author in userconf
                        matched_author = None
                        for userconf_author in AUTHORS:
                            if article_author == userconf_author:
                                matched_author = userconf_author
                                break

                        if matched_author:
                            author_counts[matched_author] = author_counts.get(matched_author, 0) + 1

                # Count categories - map display names to IDs
                if category_match:
                    category_display = category_match.group(1).strip()
                    category_id = category_display_to_id.get(category_display)

                    if category_id:
                        category_counts[category_id] = category_counts.get(category_id, 0) + 1
                        if 'Meditation' in str(file_path):
                            logger.info(f"MEDITATION: Mapped '{category_display}' to '{category_id}' for file {os.path.basename(file_path)}")
                    else:
                        logger.warning(f"Could not match article category '{category_display}' to any userconf category. Available: {list(category_display_to_id.keys())}")
                        if 'Meditation' in str(file_path):
                            logger.warning(f"MEDITATION FILE FAILED: {os.path.basename(file_path)} with category '{category_display}'")

            except Exception as e:
                # Skip files that can't be read or parsed
                logger.error(f"Error processing file {file_path}: {e}")
                continue

        return {
            'authors': author_counts,
            'categories': category_counts
        }

    def _write_userconf_data(self, data):
        """Write the userconf data back to the file."""
        userconf_path = self._get_userconf_path()

        # Read the template content
        with open(userconf_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update AUTHORS
        import re
        authors_match = re.search(r'AUTHORS\s*=\s*\[([^\]]*)\]', content, re.DOTALL)
        if authors_match:
            authors_list = data['AUTHORS']
            if authors_list:
                authors_str = ',\n    '.join(f'"{author}"' for author in authors_list)
                new_authors = f'AUTHORS = [{authors_str}]'
            else:
                new_authors = 'AUTHORS = []'
            content = content.replace(authors_match.group(0), new_authors)

        # Update CATEGORIES
        cat_list_match = re.search(r'"cat_list"\s*:\s*\[([^\]]*)\]', content, re.DOTALL)
        if cat_list_match:
            cat_list = data['CATEGORIES']['cat_list']
            if cat_list:
                cat_str = ',\n        '.join(f'("{cat[0]}", "{cat[1]}")' for cat in cat_list)
                new_cat_list = f'"cat_list": [\n        {cat_str}\n    ]'
            else:
                new_cat_list = '"cat_list": []'
            content = content.replace(cat_list_match.group(0), new_cat_list)

        # Update DEFAULT_AUTHOR
        default_author_match = re.search(r'DEFAULT_AUTHOR\s*=\s*r?"[^"]*"', content)
        if default_author_match:
            new_default_author = f'DEFAULT_AUTHOR = "{data["DEFAULT_AUTHOR"]}"'
            content = content.replace(default_author_match.group(0), new_default_author)

        # Update AUTHOR_STATUS
        author_status_match = re.search(r'AUTHOR_STATUS\s*=\s*\{([^}]*)\}', content, re.DOTALL)
        if author_status_match:
            status_dict = data['AUTHOR_STATUS']
            if status_dict:
                status_str = ',\n    '.join(f'"{author}": "{status}"' for author, status in status_dict.items())
                new_author_status = f'AUTHOR_STATUS = {{\n    {status_str}\n}}'
            else:
                new_author_status = 'AUTHOR_STATUS = {}'
            content = content.replace(author_status_match.group(0), new_author_status)

        # Update CATEGORIES status
        cat_status_match = re.search(r'"status"\s*:\s*\{([^}]*)\}', content, re.DOTALL)
        if cat_status_match:
            cat_status_dict = data['CATEGORIES']['status']
            if cat_status_dict:
                status_str = ',\n        '.join(f'"{cat_id}": "{status}"' for cat_id, status in cat_status_dict.items())
                new_cat_status = f'"status": {{\n        {status_str}\n    }}'
            else:
                new_cat_status = '"status": {}'
            content = content.replace(cat_status_match.group(0), new_cat_status)

        # Update CATEGORIES default_category
        default_cat_match = re.search(r'"default_category"\s*:\s*r?"[^"]*"', content)
        if default_cat_match:
            new_default_cat = f'"default_category": "{data["CATEGORIES"]["default_category"]}"'
            content = content.replace(default_cat_match.group(0), new_default_cat)

        # Write back to file
        with open(userconf_path, 'w', encoding='utf-8') as f:
            f.write(content)


class index_Handler(TornadoRequestBase):
    def get(self):
        self.render('home/index.html')


