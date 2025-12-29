#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib
from handlers.index_handler import TornadoRequestBase
from user_area.smbanaie.smbanaie.userconf import USER_DIR
from utils.logger_setup import logger


class categories_Handler(TornadoRequestBase):
    """Handler for category management."""

    def get(self, *args, **kwargs):
        """Display category management interface."""
        # Get current categories from userconf
        from user_area.smbanaie.smbanaie.userconf import CATEGORIES

        # Get article counts
        article_counts = self._get_article_counts()

        # Prepare category data (keep original tuple format for backward compatibility)
        categories_data = []
        for cat_id, cat_name in CATEGORIES.get('cat_list', []):
            categories_data.append((cat_id, cat_name))

        self.render('admin/categories/index.html',
                   categories=categories_data,
                   category_counts=article_counts['categories'],
                   category_status=CATEGORIES.get('status', {}),
                   default_category=CATEGORIES.get('default_category', ''))

    def post(self, *args, **kwargs):
        """Handle category creation, editing, or deletion."""
        action = self.get_argument('action', '')
        logger.info(f"Categories POST action: {action}")

        success = False
        if action == 'add':
            logger.info("Calling add_category")
            success = self.add_category()
        elif action == 'edit':
            success = self.edit_category()
        elif action == 'delete':
            success = self.delete_category()

        if success:
            self.redirect('/admin/categories')

    def _is_english_name(self, name):
        """Check if name contains only English characters, numbers, and underscores."""
        import re
        return bool(re.match(r'^[a-zA-Z0-9_]+$', name))

    def add_category(self):
        """Add a new category."""
        name = self.get_argument('name', '').strip()
        display_name = self.get_argument('display_name', '').strip()
        status = self.get_argument('status', 'active')
        is_default = self.get_argument('is_default', '0') == '1'
        logger.info(f"Adding category: name='{name}', display_name='{display_name}', status='{status}', default={is_default}")

        if not name or not display_name:
            logger.warning("Category name or display name missing")
            self.set_status(400)
            self.write('Error: Name and display name are required')
            return

        # Validate that technical name is in English
        if not self._is_english_name(name):
            logger.warning(f"Category name contains non-English characters: '{name}'")
            self.set_status(400)
            self.write('Error: نام فنی دسته‌بندی باید فقط شامل حروف انگلیسی، اعداد و زیرخط (_) باشد')
            return

        try:
            # Read current data
            data = self._read_userconf_data()

            # Check if category already exists (by name)
            existing_names = [cat[0] for cat in data['CATEGORIES']['cat_list']]
            if name in existing_names:
                self.set_status(400)
                self.write(f'Error: Category "{name}" already exists')
                return

            # Add new category to the cat_list
            data['CATEGORIES']['cat_list'].append((name, display_name))

            # Set category status
            data['CATEGORIES']['status'][name] = status

            # Handle default category
            if is_default:
                # Ensure the default category is active
                if status == 'active':
                    data['CATEGORIES']['default_category'] = name
                else:
                    self.set_status(400)
                    self.write('Error: Cannot set an inactive category as default')
                    return
            elif data['CATEGORIES'].get('default_category', '') == '' and len(data['CATEGORIES']['cat_list']) == 1:
                # If this is the first category, make it default
                data['CATEGORIES']['default_category'] = name

            # Write back the updated data to file
            self._write_userconf_data(data)

            logger.info(f"Added new category: {name} ({display_name}, status: {status}, default: {is_default})")
            return True

        except Exception as e:
            logger.error(f"Error adding category {name}: {e}")
            self.set_status(500)
            self.write(f'Error adding category: {str(e)}')

    def edit_category(self):
        """Edit an existing category."""
        old_name = self.get_argument('old_name', '')
        new_name = self.get_argument('new_name', '').strip()
        new_display_name = self.get_argument('new_display_name', '').strip()
        status = self.get_argument('status', 'active')
        is_default = self.get_argument('is_default', '0') == '1'

        if not old_name or not new_name or not new_display_name:
            self.set_status(400)
            self.write('Error: All fields are required')
            return

        # Validate that technical name is in English
        if not self._is_english_name(new_name):
            logger.warning(f"Category name contains non-English characters: '{new_name}'")
            self.set_status(400)
            self.write('Error: نام فنی دسته‌بندی باید فقط شامل حروف انگلیسی، اعداد و زیرخط (_) باشد')
            return

        try:
            # Read current data
            data = self._read_userconf_data()

            # Find the category by old_name
            cat_list = data['CATEGORIES']['cat_list']
            category_index = None
            for i, (name, display) in enumerate(cat_list):
                if name == old_name:
                    category_index = i
                    break

            if category_index is None:
                self.set_status(404)
                self.write(f'Error: Category "{old_name}" not found')
                return

            # Check if new name already exists (and it's not the same category)
            existing_names = [cat[0] for cat in cat_list]
            if new_name in existing_names and new_name != old_name:
                self.set_status(400)
                self.write(f'Error: Category "{new_name}" already exists')
                return

            # Update the category
            cat_list[category_index] = (new_name, new_display_name)

            # Update status
            if old_name in data['CATEGORIES']['status']:
                del data['CATEGORIES']['status'][old_name]
            data['CATEGORIES']['status'][new_name] = status

            # Handle default category
            if is_default:
                # Ensure the default category is active
                if status == 'active':
                    data['CATEGORIES']['default_category'] = new_name
                else:
                    self.set_status(400)
                    self.write('Error: Cannot set an inactive category as default')
                    return
            elif data['CATEGORIES']['default_category'] == old_name:
                # If we were the default, and we're not setting a new default, clear it
                data['CATEGORIES']['default_category'] = ''

            # Write back the updated data to file
            self._write_userconf_data(data)

            logger.info(f"Updated category: {old_name} -> {new_name} ({new_display_name}, status: {status}, default: {is_default})")
            return True

        except Exception as e:
            logger.error(f"Error editing category {old_name}: {e}")
            self.set_status(500)
            self.write(f'Error editing category: {str(e)}')

    def delete_category(self):
        """Delete a category."""
        name = self.get_argument('name', '')
        migration_option = self.get_argument('migration_option', 'keep')

        if not name:
            self.set_status(400)
            self.write('Name is required')
            return

        try:
            # Read current data
            data = self._read_userconf_data()

            # Find the category
            cat_list = data['CATEGORIES']['cat_list']
            category_index = None
            category_display = None
            for i, (cat_name, cat_display) in enumerate(cat_list):
                if cat_name == name:
                    category_index = i
                    category_display = cat_display
                    break

            if category_index is None:
                self.set_status(404)
                self.write(f'Error: Category "{name}" not found')
                return

            # Get article count for this category
            article_counts = self._get_article_counts()
            article_count = article_counts['categories'].get(name, 0)

            # Prevent deletion of default category if there are other categories
            if data['CATEGORIES']['default_category'] == name:
                other_categories = [cat for cat in cat_list if cat[0] != name]
                if other_categories:
                    self.set_status(400)
                    self.write(f'Error: Cannot delete default category "{category_display}". Please set another category as default first.')
                    return

            # Handle migration of articles
            if article_count > 0:
                if migration_option == 'default':
                    # Move articles to default category
                    default_cat = data['CATEGORIES']['default_category']
                    if default_cat and default_cat != name:
                        self._migrate_articles_to_category(name, default_cat)
                        logger.info(f"Migrated {article_count} articles from {name} to default category {default_cat}")
                    else:
                        self.set_status(400)
                        self.write('Error: No valid default category for migration')
                        return
                elif migration_option == 'replace':
                    # Move articles to replacement category
                    replacement_category = self.get_argument('replacement_category', '')
                    if replacement_category and replacement_category != name:
                        self._migrate_articles_to_category(name, replacement_category)
                        logger.info(f"Migrated {article_count} articles from {name} to {replacement_category}")
                    else:
                        self.set_status(400)
                        self.write('Error: Invalid replacement category')
                        return
                # For 'keep', we just leave the articles as-is

            # Remove the category
            cat_list.pop(category_index)

            # Remove from status dict
            if name in data['CATEGORIES']['status']:
                del data['CATEGORIES']['status'][name]

            # Clear default category if it was this one
            if data['CATEGORIES']['default_category'] == name:
                data['CATEGORIES']['default_category'] = ''

            # Write back the updated data to file
            self._write_userconf_data(data)

            logger.info(f"Deleted category: {name} ({category_display}) - {article_count} articles migrated with option '{migration_option}'")
            return True

        except Exception as e:
            logger.error(f"Error deleting category {name}: {e}")
            self.set_status(500)
            self.write(f'Error deleting category: {str(e)}')

    def _migrate_articles_to_category(self, old_category, new_category):
        """Migrate articles from one category to another."""
        try:
            base = pathlib.Path(USER_DIR) / 'content' / 'blog' / 'fa'
            if not base.exists():
                return

            migrated_count = 0
            for filepath in base.rglob('*.md'):
                try:
                    with filepath.open('r', encoding='utf-8') as f:
                        content = f.read()

                    # Check if this file belongs to the old category
                    if f'category:{old_category}' in content:
                        # Replace the category
                        new_content = content.replace(f'category:{old_category}', f'category:{new_category}')
                        with filepath.open('w', encoding='utf-8') as f:
                            f.write(new_content)
                        migrated_count += 1
                except Exception as e:
                    logger.error(f"Error migrating file {filepath}: {e}")

            logger.info(f"Migrated {migrated_count} articles from {old_category} to {new_category}")
            return migrated_count

        except Exception as e:
            logger.error(f"Error migrating articles: {e}")
            return 0


class category_consistency_Handler(TornadoRequestBase):
    """Handler for category consistency checking."""

    def get(self, *args, **kwargs):
        """Display category consistency interface."""
        try:
            # Analyze category consistency
            consistency_data = self._analyze_category_inconsistencies()

            self.render('admin/category_consistency.html',
                       consistency_data=consistency_data)

        except Exception as e:
            logger.error(f"Error loading category consistency page: {e}")
            self.set_status(500)
            self.write(f"خطا در بارگذاری صفحه: {str(e)}")

    def _analyze_category_inconsistencies(self, file_categories=None, folder_categories=None, userconf_categories=None):
        """Analyze inconsistencies between file categories, folder categories, and userconf categories."""
        inconsistencies = {
            'missing_in_userconf': [],  # Categories used in files but not in userconf
            'missing_in_files': [],     # Categories in userconf but not used in files
            'orphaned_folders': [],     # Category folders that exist but category not in userconf
            'summary': {
                'total_file_categories': 0,
                'total_folder_categories': 0,
                'total_userconf_categories': 0,
                'issues_count': 0
            }
        }

        try:
            # Get categories from files
            if file_categories is None:
                file_categories = self._get_categories_from_files()
            inconsistencies['summary']['total_file_categories'] = len(file_categories)

            # Get categories from folder structure
            if folder_categories is None:
                folder_categories = self._get_categories_from_folders()
            inconsistencies['summary']['total_folder_categories'] = len(folder_categories)

            # Get categories from userconf
            if userconf_categories is None:
                from user_area.smbanaie.smbanaie.userconf import CATEGORIES
                userconf_categories = set(cat[0] for cat in CATEGORIES.get('cat_list', []))
            inconsistencies['summary']['total_userconf_categories'] = len(userconf_categories)

            # Find categories used in files but not in userconf
            inconsistencies['missing_in_userconf'] = list(file_categories - userconf_categories)

            # Find categories in userconf but not used in files
            inconsistencies['missing_in_files'] = list(userconf_categories - file_categories)

            # Find orphaned folders (folders exist but no corresponding category in userconf)
            inconsistencies['orphaned_folders'] = list(folder_categories - userconf_categories)

            # Calculate total issues
            inconsistencies['summary']['issues_count'] = (
                len(inconsistencies['missing_in_userconf']) +
                len(inconsistencies['missing_in_files']) +
                len(inconsistencies['orphaned_folders'])
            )

        except Exception as e:
            logger.error(f"Error analyzing category consistency: {e}")
            inconsistencies['summary']['error'] = str(e)

        return inconsistencies

    def _get_categories_from_files(self):
        """Extract categories used in Markdown files."""
        categories = set()
        try:
            base = pathlib.Path(USER_DIR) / 'content' / 'blog' / 'fa'
            if base.exists():
                for filepath in base.rglob('*.md'):
                    try:
                        with filepath.open('r', encoding='utf-8') as fh:
                            for line in fh:
                                line = line.strip()
                                if line.startswith('category:'):
                                    category = line.split(':', 1)[1].strip()
                                    if category:
                                        categories.add(category)
                                elif line == '':  # Stop at end of front matter
                                    break
                    except Exception as e:
                        logger.debug(f'Skipping file {filepath} due to read error: {e}')
        except Exception as e:
            logger.error(f"Error getting categories from files: {e}")

        return categories

    def _get_categories_from_folders(self):
        """Extract categories from folder structure."""
        categories = set()
        try:
            base = pathlib.Path(USER_DIR) / 'content' / 'blog' / 'fa'
            if base.exists():
                for item in base.iterdir():
                    if item.is_dir() and not item.name.startswith('.') and item.name != '__pycache__':
                        categories.add(item.name)
        except Exception as e:
            logger.error(f"Error getting categories from folders: {e}")

        return categories

    def _read_userconf_data(self):
        """Read current userconf data."""
        try:
            from user_area.smbanaie.smbanaie.userconf import AUTHORS, AUTHOR_STATUS, DEFAULT_AUTHOR, CATEGORIES

            return {
                'AUTHORS': list(AUTHORS),  # Convert to list to make it mutable
                'AUTHOR_STATUS': dict(AUTHOR_STATUS),  # Convert to dict to make it mutable
                'DEFAULT_AUTHOR': DEFAULT_AUTHOR,
                'CATEGORIES': dict(CATEGORIES)  # Include categories for completeness
            }
        except Exception as e:
            logger.error(f"Error reading userconf data: {e}")
            raise

    def _write_userconf_data(self, data):
        """Write updated userconf data back to file."""
        try:
            userconf_path = os.path.join(USER_DIR, 'userconf.py')

            # Read the current file content
            with open(userconf_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update the data structures
            # CATEGORIES
            categories_start = content.find('CATEGORIES = {')
            if categories_start != -1:
                categories_end = content.find('}', categories_start) + 1
                if categories_end > categories_start:
                    categories_str = 'CATEGORIES = ' + str(data['CATEGORIES'])
                    content = content[:categories_start] + categories_str + content[categories_end:]

            # Write back to file
            with open(userconf_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Updated userconf.py with new data")

        except Exception as e:
            logger.error(f"Error writing userconf data: {e}")
            raise
