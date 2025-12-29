#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from handlers.index_handler import TornadoRequestBase
from user_area.smbanaie.smbanaie.userconf import USER_DIR, CONTENT_DIR, AUTHORS, CATEGORIES, SITE_REPO, DEFAULT_IMAGE_PATH
from utils.logger_setup import logger


class settings_Handler(TornadoRequestBase):
    """Handler for settings management."""

    def get(self, *args, **kwargs):
        """Display settings management interface."""
        settings = {
            'user_dir': USER_DIR,
            'content_dir': CONTENT_DIR,
            'authors': AUTHORS,
            'categories': CATEGORIES.get('cat_list', []),
            'site_repo': SITE_REPO,
            'default_image_path': DEFAULT_IMAGE_PATH
        }

        self.render('admin/settings/index.html', settings=settings)

    def post(self, *args, **kwargs):
        """Handle settings updates."""
        action = self.get_argument('action', '')

        if action == 'update_site':
            self.update_site_settings()
        elif action == 'update_paths':
            self.update_path_settings()

        self.redirect('/admin/settings')

    def update_site_settings(self):
        """Update site-related settings."""
        site_repo = self.get_argument('site_repo', '').strip()

        # Read current userconf
        userconf_path = USER_DIR + os.path.sep + 'userconf.py'
        with open(userconf_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update SITE_REPO
        pattern = r'SITE_REPO\s*=\s*"[^"]*"'
        replacement = f'SITE_REPO = "{site_repo}"'
        updated_content = re.sub(pattern, replacement, content)

        # Write back to file
        with open(userconf_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        logger.info(f"Updated site repo: {site_repo}")

    def update_path_settings(self):
        """Update path-related settings."""
        user_dir = self.get_argument('user_dir', '').strip()
        default_image_path = self.get_argument('default_image_path', '').strip()

        # Read current userconf
        userconf_path = USER_DIR + os.path.sep + 'userconf.py'
        with open(userconf_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update paths
        content = re.sub(r'USER_DIR\s*=\s*r"[^"]*"', f'USER_DIR = r"{user_dir}"', content)
        content = re.sub(r'DEFAULT_IMAGE_PATH\s*=\s*str\(Path\([^)]*\)',
                        f'DEFAULT_IMAGE_PATH = str(Path("{default_image_path}"))', content)

        # Write back to file
        with open(userconf_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Updated paths: USER_DIR={user_dir}, DEFAULT_IMAGE_PATH={default_image_path}")
