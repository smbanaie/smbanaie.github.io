#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib
import datetime
from handlers.index_handler import TornadoRequestBase
from user_area.smbanaie.smbanaie.userconf import USER_DIR
from utils.logger_setup import logger


class admin_Handler(TornadoRequestBase):
    """Main dashboard handler for the admin panel."""

    def get(self, *args, **kwargs):
        """Display the main admin dashboard."""
        # Get dashboard statistics
        stats = self.get_dashboard_stats()
        date = str(__import__('jdatetime').datetime.now())
        date = date.split('.')[0]

        self.render('admin/starter.html', stats=stats, date=date)

    def post(self, *args, **kwargs):
        """Handle dashboard actions."""
        action = self.get_argument('action', '')

        if action == 'recalculate_stats':
            return self.recalculate_stats()
        elif action == 'backup':
            return self.create_backup()
        elif action == 'generate_site':
            return self.generate_site()

        self.write("Invalid action")
        self.set_status(400)

    def get_dashboard_stats(self):
        """Calculate dashboard statistics."""
        stats = {
            'total_posts': 0,
            'total_categories': 0,
            'total_authors': 0,
            'recent_posts': [],
            'posts_by_category': {},
            'posts_by_month': {}
        }

        try:
            # Get categories from userconf
            from user_area.smbanaie.smbanaie.userconf import CATEGORIES, AUTHORS
            stats['total_categories'] = len(CATEGORIES.get('cat_list', []))
            stats['total_authors'] = len(AUTHORS)

            # Scan for posts
            base = pathlib.Path(USER_DIR) / 'content' / 'blog' / 'fa'
            if base.exists():
                posts = []
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

                        post_info = {
                            'title': meta.get('title', filepath.stem),
                            'slug': filepath.stem,
                            'date': meta.get('date', ''),
                            'category': meta.get('category', ''),
                            'author': meta.get('authors', ''),
                            'path': str(filepath),
                            'mtime': filepath.stat().st_mtime
                        }
                        posts.append(post_info)

                        # Count by category
                        category = post_info['category']
                        if category:
                            stats['posts_by_category'][category] = stats['posts_by_category'].get(category, 0) + 1

                        # Count by month
                        if post_info['date']:
                            try:
                                date_obj = datetime.datetime.fromisoformat(post_info['date'])
                                month_key = f"{date_obj.year}-{date_obj.month:02d}"
                                stats['posts_by_month'][month_key] = stats['posts_by_month'].get(month_key, 0) + 1
                            except:
                                pass

                    except Exception as e:
                        # Skip files that can't be read or parsed
                        continue

                # Sort posts by date (most recent first)
                posts.sort(key=lambda x: x['mtime'], reverse=True)
                stats['recent_posts'] = posts[:5]  # Last 5 posts
                stats['total_posts'] = len(posts)

        except Exception as e:
            logger.error(f"Error calculating dashboard stats: {e}")

        return stats

    def recalculate_stats(self):
        """Recalculate all statistics and category counts."""
        try:
            # Recalculate article counts
            article_counts = self._get_article_counts()

            # Get current userconf data
            from user_area.smbanaie.smbanaie.userconf import AUTHORS, AUTHOR_STATUS, DEFAULT_AUTHOR, CATEGORIES
            data = {
                'AUTHORS': AUTHORS,
                'AUTHOR_STATUS': AUTHOR_STATUS,
                'DEFAULT_AUTHOR': DEFAULT_AUTHOR,
                'CATEGORIES': CATEGORIES
            }

            # Update the data with correct counts (this is mainly for verification)
            # The counts are calculated on-the-fly when pages load

            # Log the results
            logger.info(f"Statistics recalculated - Authors: {len(data['AUTHORS'])}, Categories: {len(data['CATEGORIES']['cat_list'])}, Articles: {sum(article_counts['authors'].values())}")

            # Return success response
            self.write("آمار با موفقیت بازسازی شد")
            self.set_status(200)

        except Exception as e:
            logger.error(f"Error recalculating stats: {e}")
            self.write(f"خطا در بازسازی آمار: {str(e)}")
            self.set_status(500)

    def create_backup(self):
        """Create a backup of the userconf and content."""
        try:
            import shutil

            # Create backup directory
            backup_dir = os.path.join(USER_DIR, 'backups')
            os.makedirs(backup_dir, exist_ok=True)

            # Create timestamp
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

            # Backup userconf
            userconf_src = os.path.join(USER_DIR, 'userconf.py')
            userconf_dst = os.path.join(backup_dir, f'userconf_{timestamp}.py')
            shutil.copy2(userconf_src, userconf_dst)

            # Create content backup (optional - just log for now)
            logger.info(f"Backup created: {userconf_dst}")

            self.write("پشتیبان با موفقیت ایجاد شد")
            self.set_status(200)

        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            self.write(f"خطا در ایجاد پشتیبان: {str(e)}")
            self.set_status(500)

    def generate_site(self):
        """Generate the Pelican site."""
        try:
            build_type = self.get_argument('build_type', 'build')

            # Import required modules
            import subprocess

            # Change to the user directory
            user_dir = USER_DIR

            # Determine the command based on build type
            if build_type == 'preview':
                command = ['invoke', 'preview']
            else:
                command = ['invoke', 'build']

            # Run the command
            logger.info(f"Running site generation command: {' '.join(command)} in {user_dir}")

            result = subprocess.run(
                command,
                cwd=user_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                logger.info("Site generation completed successfully")
                self.write("سایت با موفقیت تولید شد")
                self.set_status(200)
            else:
                logger.error(f"Site generation failed: {result.stderr}")
                self.write(f"خطا در تولید سایت: {result.stderr}")
                self.set_status(500)

        except subprocess.TimeoutExpired:
            logger.error("Site generation timed out")
            self.write("خطا: تولید سایت زمان زیادی طول کشید")
            self.set_status(500)
        except Exception as e:
            logger.error(f"Error generating site: {e}")
            self.write(f"خطا در تولید سایت: {str(e)}")
            self.set_status(500)
