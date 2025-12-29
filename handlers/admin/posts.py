#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib
import datetime
import codecs
from urllib.parse import quote_plus
from handlers.index_handler import TornadoRequestBase
from user_area.smbanaie.smbanaie.userconf import USER_DIR, CATEGORIES, AUTHORS
from utils.logger_setup import logger


class add_new_post_Handler(TornadoRequestBase):
    """Handler for adding new posts."""

    def get(self, *args, **kwargs):
        """Display new post form."""
        catList = {}
        authors = []
        for clist in CATEGORIES["cat_list"]:
            catList[clist[0]] = clist[1]
        for user in AUTHORS:
            authors.append(user)
        date = str(__import__('jdatetime').datetime.now())
        fa_date_components = date[:10].split("-")
        month = fa_date_components[1]
        if month[0] == "0":
            month = month[1]
        self.render('admin/posts/add.html',
                   catlist=catList,
                   authors=authors,
                   year=fa_date_components[0],
                   month=month)

    def post(self, *args, **kwargs):
        """Create a new post."""
        date = str(__import__('jdatetime').datetime.now())
        fa_date_components = date[:10].split("-")
        d = datetime.datetime.now()
        en_date_components = "%d-%d-%d" % (d.year, d.month, d.day)

        try:
            logger.debug("Received new post request: title=%s slug=%s",
                        self.get_argument('title'), self.get_argument('slug'))
        except Exception:
            logger.debug("Received new post request (could not read title/slug yet)")

        article_path = USER_DIR + os.path.sep + "content" + os.path.sep + "blog" + os.path.sep + "fa"
        article_path += os.path.sep + self.get_argument("category") + os.path.sep
        article_path += fa_date_components[0] + os.path.sep
        if fa_date_components[1][0] == "0":
            article_path += fa_date_components[1][1]
        else:
            article_path += fa_date_components[1]

        pathlib.Path(article_path).mkdir(parents=True, exist_ok=True)

        filepath = article_path + os.path.sep + self.get_argument("slug") + ".md"
        with codecs.open(filepath, "w", encoding="utf-8") as f:
            f.write("title:" + self.get_argument('title') + "\r\n")
            f.write("date:" + en_date_components + "\r\n")
            f.write("modified:" + en_date_components + "\r\n")
            f.write("icon:icon-link2\r\n")
            f.write("lang:fa\r\n")
            f.write("category:" + self.get_argument('cat_name') + "\r\n")
            f.write("tags:" + self.get_argument('tagsvalues') + "\r\n")
            f.write("Slug:" + self.get_argument('slug') + "\r\n")
            f.write("authors:" + self.get_argument('authors') + "\r\n")
            f.write("summary:" + self.get_argument('summary') + "\r\n")
            f.write("image: " + self.get_argument("img_adr") + self.get_argument("image") + "\r\n\r\n")
            f.write("![" + self.get_argument("img_desc") + " <>](/images" +
                   self.get_argument("img_adr") + self.get_argument("image") + ")\r\n\r\n")
            f.write(self.get_argument('article'))

        logger.info("Wrote new post: %s", filepath)
        try:
            self.finish("\n" + article_path)
        except Exception:
            # If Tornado has trouble finishing (e.g. connection closed), still log
            logger.debug("Finished response for post creation (connection may be closed)")


class posts_list_Handler(TornadoRequestBase):
    """Handler for listing posts with pagination."""

    def get(self, *args, **kwargs):
        """Scan USER_DIR/content/blog/fa for Markdown posts and render a paginated list.

        Query params:
        - page: 1-based page number (default 1)
        - page_size: items per page (default 20)
        """
        try:
            base = pathlib.Path(USER_DIR) / 'content' / 'blog' / 'fa'
        except Exception:
            base = pathlib.Path('')

        posts = []
        if base.exists():
            for filepath in base.rglob('*.md'):
                try:
                    meta = {}
                    with filepath.open('r', encoding='utf-8') as fh:
                        for line in fh:
                            line = line.strip()
                            if line == '':
                                break
                            if ':' in line:
                                k, v = line.split(':', 1)
                                meta[k.strip().lower()] = v.strip()
                    mtime = filepath.stat().st_mtime
                    slug = filepath.stem
                    posts.append({
                        'title': meta.get('title', slug),
                        'slug': slug,
                        'date': meta.get('date', ''),
                        'category': meta.get('category', ''),
                        'path': str(filepath),
                        'edit_url': '/admin/posts/edit?file=' + quote_plus(str(filepath)),
                        'mtime': mtime,
                    })
                except Exception as e:
                    logger.debug('Skipping file %s due to parse error: %s', filepath, e)

        # sort by mtime desc
        posts.sort(key=lambda p: p['mtime'], reverse=True)

        # Pagination
        try:
            page = int(self.get_argument('page', '1'))
        except Exception:
            page = 1
        try:
            page_size = int(self.get_argument('page_size', '20'))
        except Exception:
            page_size = 20
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 20

        total = len(posts)
        total_pages = (total + page_size - 1) // page_size if total else 1
        if page > total_pages:
            page = total_pages

        start = (page - 1) * page_size
        end = start + page_size
        page_items = posts[start:end]

        pages = list(range(1, total_pages + 1))

        self.render('admin/posts/list.html', posts=page_items, page=page, page_size=page_size,
                    total=total, total_pages=total_pages, pages=pages)


class edit_post_Handler(TornadoRequestBase):
    """Handler for editing existing posts."""

    def get(self, *args, **kwargs):
        """Display post edit form."""
        file_path = self.get_argument('file', '')
        if not file_path:
            self.write("No file specified")
            self.set_status(400)
            return

        # Security check - ensure file is within content directory
        content_dir = os.path.join(USER_DIR, 'content')
        if not os.path.abspath(file_path).startswith(os.path.abspath(content_dir)):
            self.write("Invalid file path")
            self.set_status(403)
            return

        if not os.path.exists(file_path):
            self.write("File not found")
            self.set_status(404)
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse front matter
            front_matter = {}
            body_start = 0
            lines = content.split('\n')
            in_front_matter = False

            for i, line in enumerate(lines):
                line = line.strip()
                if line == '---':
                    if not in_front_matter:
                        in_front_matter = True
                    else:
                        body_start = i + 1
                        break
                elif in_front_matter and ':' in line:
                    key, value = line.split(':', 1)
                    front_matter[key.strip().lower()] = value.strip()

            body = '\n'.join(lines[body_start:]) if body_start > 0 else content

            # Prepare category list
            catList = {}
            for clist in CATEGORIES["cat_list"]:
                catList[clist[0]] = clist[1]

            # Prepare authors list
            authors = list(AUTHORS)

            self.render('admin/posts/edit.html',
                       post_content=body,
                       front_matter=front_matter,
                       catlist=catList,
                       authors=authors,
                       file_path=file_path)

        except Exception as e:
            logger.error(f"Error loading post for editing: {e}")
            self.write(f"Error loading post: {str(e)}")
            self.set_status(500)

    def post(self, *args, **kwargs):
        """Update an existing post."""
        file_path = self.get_argument('file_path', '')
        if not file_path:
            self.write("No file specified")
            self.set_status(400)
            return

        # Security check - ensure file is within content directory
        content_dir = os.path.join(USER_DIR, 'content')
        if not os.path.abspath(file_path).startswith(os.path.abspath(content_dir)):
            self.write("Invalid file path")
            self.set_status(403)
            return

        try:
            # Reconstruct front matter
            front_matter = {
                'title': self.get_argument('title', ''),
                'date': self.get_argument('date', ''),
                'modified': datetime.datetime.now().strftime('%Y-%m-%d'),
                'icon': 'icon-link2',
                'lang': 'fa',
                'category': self.get_argument('cat_name', ''),
                'tags': self.get_argument('tagsvalues', ''),
                'slug': self.get_argument('slug', ''),
                'authors': self.get_argument('authors', ''),
                'summary': self.get_argument('summary', ''),
                'image': self.get_argument('img_adr', '') + self.get_argument('image', '')
            }

            # Build content
            content_lines = ['---']
            for key, value in front_matter.items():
                if value:  # Only include non-empty values
                    content_lines.append(f'{key}:{value}')
            content_lines.append('---')
            content_lines.append('')
            content_lines.append(self.get_argument('article', ''))

            content = '\n'.join(content_lines)

            # Write to file
            with codecs.open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info("Updated post: %s", file_path)
            self.write('Post updated successfully')

        except Exception as e:
            logger.error(f"Error updating post {file_path}: {e}")
            self.write(f"Error updating post: {str(e)}")
            self.set_status(500)
