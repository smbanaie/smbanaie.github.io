#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from handlers.index_handler import TornadoRequestBase
from user_area.smbanaie.smbanaie.userconf import USER_DIR
from utils.logger_setup import logger


class users_Handler(TornadoRequestBase):
    """User management handler."""

    def get(self, *args, **kwargs):
        """Display user management interface."""
        try:
            # Get user data from userconf
            from user_area.smbanaie.smbanaie.userconf import AUTHORS, AUTHOR_STATUS, DEFAULT_AUTHOR

            # Get article counts for each user
            user_counts = {}
            for author in AUTHORS:
                user_counts[author] = self._count_articles_by_author(author)

            # Get user status data
            user_status = AUTHOR_STATUS

            # Get default author
            default_author = DEFAULT_AUTHOR

            # Prepare user data for template
            users_data = []
            for author in AUTHORS:
                users_data.append(author)  # Keep original format for backward compatibility

            self.render('admin/users/index.html',
                       users=users_data,
                       user_status=user_status,
                       user_counts=user_counts,
                       default_author=default_author)

        except Exception as e:
            logger.error(f"Error loading users page: {e}")
            self.set_status(500)
            self.write(f"خطا در بارگذاری صفحه کاربران: {str(e)}")

    def post(self, *args, **kwargs):
        """Handle user management actions."""
        action = self.get_argument('action', '')

        if action == 'add':
            self.add_user()
        elif action == 'edit':
            self.edit_user()
        elif action == 'delete':
            self.delete_user()
        else:
            self.write("Invalid action")

    def _count_articles_by_author(self, author_name):
        """Count articles by a specific author."""
        try:
            content_dir = Path(USER_DIR) / "content" / "blog" / "fa"
            count = 0

            if content_dir.exists():
                for category_dir in content_dir.iterdir():
                    if category_dir.is_dir():
                        for year_dir in category_dir.iterdir():
                            if year_dir.is_dir() and year_dir.name.isdigit():
                                for month_dir in year_dir.iterdir():
                                    if month_dir.is_dir() and month_dir.name.isdigit():
                                        for md_file in month_dir.glob("*.md"):
                                            try:
                                                with open(md_file, 'r', encoding='utf-8') as f:
                                                    content = f.read()
                                                    # Check if author is in the front matter
                                                    author_patterns = [
                                                        f"authors: {author_name}",
                                                        f"Authors: {author_name}",
                                                        f"Author: {author_name}",
                                                        f"author: {author_name}"
                                                    ]
                                                    for pattern in author_patterns:
                                                        if pattern in content:
                                                            count += 1
                                                            break
                                            except Exception as e:
                                                logger.error(f"Error reading file {md_file}: {e}")

            return count

        except Exception as e:
            logger.error(f"Error counting articles for author {author_name}: {e}")
            return 0

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
            # AUTHORS
            authors_start = content.find('AUTHORS = [')
            if authors_start != -1:
                authors_end = content.find(']', authors_start) + 1
                authors_str = 'AUTHORS = ' + str(data['AUTHORS'])
                content = content[:authors_start] + authors_str + content[authors_end:]

            # AUTHOR_STATUS
            status_start = content.find('AUTHOR_STATUS = {')
            if status_start != -1:
                status_end = content.find('}', status_start) + 1
                status_str = 'AUTHOR_STATUS = ' + str(data['AUTHOR_STATUS'])
                content = content[:status_start] + status_str + content[status_end:]

            # DEFAULT_AUTHOR
            default_start = content.find('DEFAULT_AUTHOR = "')
            if default_start != -1:
                default_end = content.find('"', default_start + len('DEFAULT_AUTHOR = "')) + 1
                default_str = f'DEFAULT_AUTHOR = "{data["DEFAULT_AUTHOR"]}"'
                content = content[:default_start] + default_str + content[default_end:]

            # Write back to file
            with open(userconf_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Updated userconf.py with new data")

        except Exception as e:
            logger.error(f"Error writing userconf data: {e}")
            raise

    def add_user(self):
        """Add a new user."""
        try:
            username = self.get_argument('username', '').strip()

            if not username:
                self.write("نام کاربری نمی‌تواند خالی باشد")
                return

            # Get current userconf data
            data = self._read_userconf_data()

            # Check if user already exists
            if username in data['AUTHORS']:
                self.write("این نام کاربری از قبل وجود دارد")
                return

            # Add user to authors list
            data['AUTHORS'].append(username)

            # Add user to status dict with active status
            data['AUTHOR_STATUS'][username] = 'active'

            # If this is the first user, set as default
            if not data['DEFAULT_AUTHOR']:
                data['DEFAULT_AUTHOR'] = username

            # Write back the updated data to file
            self._write_userconf_data(data)

            logger.info(f"Added new user: {username}")
            self.redirect('/admin/users')

        except Exception as e:
            logger.error(f"Error adding user {username}: {e}")
            self.set_status(500)
            self.write(f'Error adding user: {str(e)}')

    def edit_user(self):
        """Edit an existing user."""
        try:
            old_username = self.get_argument('old_username', '').strip()
            new_username = self.get_argument('new_username', '').strip()
            status = self.get_argument('status', 'active')
            is_default = self.get_argument('is_default', '0') == '1'

            if not old_username or not new_username:
                self.write("نام کاربری نمی‌تواند خالی باشد")
                return

            # Get current userconf data
            data = self._read_userconf_data()

            # Check if old user exists
            if old_username not in data['AUTHORS']:
                self.write("کاربر مورد نظر یافت نشد")
                return

            # Check if new username already exists (if different from old)
            if new_username != old_username and new_username in data['AUTHORS']:
                self.write("این نام کاربری از قبل وجود دارد")
                return

            # Update username if changed
            if new_username != old_username:
                # Update in authors list
                idx = data['AUTHORS'].index(old_username)
                data['AUTHORS'][idx] = new_username

                # Update in status dict
                if old_username in data['AUTHOR_STATUS']:
                    data['AUTHOR_STATUS'][new_username] = data['AUTHOR_STATUS'].pop(old_username)

                # Update default author if needed
                if data['DEFAULT_AUTHOR'] == old_username:
                    data['DEFAULT_AUTHOR'] = new_username

                username = new_username
            else:
                username = old_username

            # Update status
            data['AUTHOR_STATUS'][username] = status

            # Update default author
            if is_default:
                data['DEFAULT_AUTHOR'] = username
            elif data['DEFAULT_AUTHOR'] == username and not is_default:
                # If we're removing default status, we need another default
                # Find another active user to be default
                for author in data['AUTHORS']:
                    if author != username and data['AUTHOR_STATUS'].get(author, 'active') == 'active':
                        data['DEFAULT_AUTHOR'] = author
                        break

            # Write back the updated data to file
            self._write_userconf_data(data)

            logger.info(f"Updated user: {old_username} -> {username}")
            self.redirect('/admin/users')

        except Exception as e:
            logger.error(f"Error editing user {old_username}: {e}")
            self.set_status(500)
            self.write(f'Error editing user: {str(e)}')

    def delete_user(self):
        """Delete a user."""
        try:
            username = self.get_argument('username', '').strip()

            if not username:
                self.write("نام کاربری نمی‌تواند خالی باشد")
                return

            # Get current userconf data
            data = self._read_userconf_data()

            # Check if user exists
            if username not in data['AUTHORS']:
                self.write("کاربر مورد نظر یافت نشد")
                return

            # Check if this is the default author
            if data['DEFAULT_AUTHOR'] == username:
                # Find another active user to be the new default
                new_default = None
                for author in data['AUTHORS']:
                    if author != username and data['AUTHOR_STATUS'].get(author, 'active') == 'active':
                        new_default = author
                        break

                if new_default:
                    data['DEFAULT_AUTHOR'] = new_default
                else:
                    self.write(f'Error: Cannot delete default author "{username}". Please set another active author as default first, then try deleting.')
                    return

            # Check if this is the last active user
            active_users = [author for author in data['AUTHORS'] if data['AUTHOR_STATUS'].get(author, 'active') == 'active']
            if len(active_users) == 1 and active_users[0] == username:
                self.write(f'Error: Cannot delete default author "{username}". This is the only active author. Please add another active author and set it as default before deleting.')
                return

            # Remove the user
            data['AUTHORS'].remove(username)

            # Remove from status dict
            if username in data['AUTHOR_STATUS']:
                del data['AUTHOR_STATUS'][username]

            # If we had no default author and this was the last user, set a new default
            if not data['DEFAULT_AUTHOR'] and data['AUTHORS']:
                data['DEFAULT_AUTHOR'] = data['AUTHORS'][0]

            # Write back the updated data to file
            self._write_userconf_data(data)

            logger.info(f"Deleted user: {username}")
            self.redirect('/admin/users')

        except Exception as e:
            logger.error(f"Error deleting user {username}: {e}")
            self.set_status(500)
            self.write(f'Error deleting user: {str(e)}')

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
            # AUTHORS
            authors_start = content.find('AUTHORS = [')
            if authors_start != -1:
                authors_end = content.find(']', authors_start) + 1
                authors_str = 'AUTHORS = ' + str(data['AUTHORS'])
                content = content[:authors_start] + authors_str + content[authors_end:]

            # AUTHOR_STATUS
            status_start = content.find('AUTHOR_STATUS = {')
            if status_start != -1:
                status_end = content.find('}', status_start) + 1
                status_str = 'AUTHOR_STATUS = ' + str(data['AUTHOR_STATUS'])
                content = content[:status_start] + status_str + content[status_end:]

            # DEFAULT_AUTHOR
            default_start = content.find('DEFAULT_AUTHOR = "')
            if default_start != -1:
                default_end = content.find('"', default_start + len('DEFAULT_AUTHOR = "')) + 1
                default_str = f'DEFAULT_AUTHOR = "{data["DEFAULT_AUTHOR"]}"'
                content = content[:default_start] + default_str + content[default_end:]

            # Write back to file
            with open(userconf_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Updated userconf.py with new data")

        except Exception as e:
            logger.error(f"Error writing userconf data: {e}")
            raise
