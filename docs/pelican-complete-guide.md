# Pelican Complete Guide for Persian Blog

## Overview
This is a complete guide for working with your Pelican-powered Persian/Farsi blog. The site contains 737 articles and uses a custom Persian-optimized theme.

## Project Structure
```
user_area/smbanaie/smbanaie/
├── content/              # Source Markdown files
│   ├── blog/fa/         # Persian articles by category
│   ├── pages/fa/        # Static pages
│   ├── images/          # Media files
│   └── extra/           # Static files (robots.txt, etc.)
├── themes/pelican-fh5co-marble/  # Persian theme
├── plugins/             # Pelican plugins
├── public/              # Generated HTML (after build)
├── pelicanconf.py       # Development config
├── publishconf.py       # Production config
└── tasks.py             # Invoke automation tasks
```

## Quick Start (3 Commands)

```bash
# 1. Navigate to project
cd user_area/smbanaie/smbanaie

# 2. Build and test locally
invoke build && invoke serve
# Visit: http://localhost:8000

# 3. Deploy to production
invoke ghpages
# Live at: https://smbanaie.github.io
```

## Essential Commands Table

| Command | Purpose | Config Used | Output | Use When |
|---------|---------|-------------|--------|----------|
| `invoke build` | Local development build | `pelicanconf.py` | `public/` | Testing changes |
| `invoke serve` | Start local server | N/A | Serves `public/` | Viewing site |
| `invoke regenerate` | Auto-rebuild on changes | `pelicanconf.py` | `public/` | Development |
| `invoke preview` | Production build | `publishconf.py` | `public/` | Pre-deployment |
| `invoke ghpages` | Deploy to GitHub Pages | `publishconf.py` | GitHub | Publishing |
| `invoke clean` | Remove generated files | N/A | Deletes `public/` | Clean rebuild |

## SITEURL Configuration (Critical)

### For Local Development
```python
# pelicanconf.py
SITEURL = ''  # Empty string - REQUIRED for local testing
```

### For Production
```python
# publishconf.py
SITEURL = 'http://banaie.ir'  # Your live domain
```

**NEVER** set SITEURL in development config - it breaks local links!

## Configuration Files

### pelicanconf.py (Development)
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

AUTHOR = 'سید مجتبی بنائی'
SITENAME = 'سایت شخصی سید مجتبی بنائی'
SITEDESCRIPTION = 'روزنوشت‌ها و مطالب شخصی سید مجتبی بنائی'
SITEURL = ''  # CRITICAL: Empty for local development

# Content
PATH = 'content'
ARTICLE_PATHS = ['blog/fa']
PAGE_PATHS = ['pages/fa']
OUTPUT_PATH = 'public'

# Theme
THEME = 'themes/pelican-fh5co-marble'
I18N_GETTEXT_LOCALEDIR = 'themes/pelican-fh5co-marble/locale/'
I18N_GETTEXT_DOMAIN = 'messages'

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'i18n_subsites',
    'tipue_search',
    'sitemap',
    'pelican_persian_date',
    'ga_page_view'
]

# Language
DEFAULT_LANG = 'fa'
LOCALE = 'fa_IR'
I18N_TEMPLATES_LANG = 'fa_IR'

# Persian date format
DEFAULT_DATE_FORMAT = {'fa': '%A %d %B %Y'}
DATE_FORMATS = {'fa': '%A %d %B %Y'}

# Multi-language
I18N_SUBSITES = {
    'en': {
        'PAGE_PATHS': ['pages/en'],
        'ARTICLE_PATHS': ['blog/en'],
        'LOCALE': 'en_US'
    }
}

# Navigation
DISPLAY_PAGES_ON_MENU = True
MENUITEMS = [
    ('Archive', 'archives.html'),
    ('Contact', 'contact.html')
]

# URLs
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{slug}.html'

# Static files
STATIC_PATHS = ['images', 'extra/CNAME', 'extra/favicon.ico', 'extra/robots.txt']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/CNAME': {'path': 'CNAME'},
}

# Logo and social
LOGO = '/images/logo.jpg'
SOCIAL = (
    ('Github', 'https://github.com/smbanaie'),
    ('Facebook', 'https://facebook.com/smbanaie'),
    ('Twitter', 'https://twitter.com/smbanaie'),
    ('Linkedin', 'https://linkedin.com/in/smbanaie'),
)
```

### publishconf.py (Production)
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pelicanconf import *

# Production overrides
SITEURL = 'http://banaie.ir'  # CRITICAL: Set your domain here
RELATIVE_URLS = False
DELETE_OUTPUT_DIRECTORY = True

# Feeds (production only)
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

# Analytics
GOOGLE_TRACKING_ID = "UA-13075446-1"

# Sitemap
SITEMAP = {
    'format': 'xml',
    'priorities': {'articles': 0.5, 'indexes': 0.5, 'pages': 0.5},
    'changefreqs': {'articles': 'monthly', 'indexes': 'daily', 'pages': 'monthly'}
}
```

## Content Creation

### Article Structure
Create files in: `content/blog/fa/Category/YYYY/MM/filename.md`

**Example article** (`content/blog/fa/Diary/1402/01/test-article.md`):
```markdown
Title: عنوان مقاله آزمایشی
Date: 1402-01-15
Modified: 1402-01-15
Category: Diary
Tags: test, article
Slug: test-article
Authors: سید مجتبی بنائی
Summary: خلاصه مقاله آزمایشی

این یک مقاله آزمایشی است که نشان می‌دهد چگونه یک مقاله جدید ایجاد کنیم.

## بخش اول

محتوای مقاله در اینجا قرار می‌گیرد.

## بخش دوم

می‌توانید از تمام ویژگی‌های Markdown استفاده کنید:
- لیست‌ها
- **بولد**
- *ایتالیک*
- [لینک‌ها](https://example.com)

### زیربخش

و همچنین تصاویر:
![توضیح تصویر]({static}/images/example.jpg)
```

### Categories Available
- `Culture` - فرهنگ و جامعه
- `Diary` - روزنوشت
- `Meditation` - بر بلندای شعر و عرفان
- `Self-Contemplation` - پرواز اندیشه
- `Misc` - از گوشه و کنار
- `Tech` - فناوری

### Pages
Create static pages in: `content/pages/fa/page-name.md`

**Example page** (`content/pages/fa/about.md`):
```markdown
Title: درباره من
Date: 1402-01-01
Modified: 1402-01-01
Slug: about-me

# درباره سید مجتبی بنائی

این صفحه درباره من است...
```

## Development Workflow

### Daily Development Cycle
```bash
# 1. Navigate to project
cd user_area/smbanaie/smbanaie

# 2. Start auto-regeneration (recommended for development)
invoke regenerate

# In another terminal:
# 3. Serve locally
invoke serve
# Visit: http://localhost:8000

# 4. Edit files in content/ directory
# 5. See changes automatically at localhost:8000
```

### One-time Build and Test
```bash
# Build once
invoke build

# Serve to test
invoke serve
# Visit: http://localhost:8000
```

### Production Deployment
```bash
# Build for production
invoke preview

# Test production build locally (optional)
invoke serve

# Deploy to GitHub Pages
invoke ghpages
```

## GitHub Pages Deployment

### Repository Setup
- **Repository**: `https://github.com/smbanaie/smbanaie.github.io`
- **Branch**: `master`
- **URL**: `https://smbanaie.github.io`

### One-Command Deployment
```bash
invoke ghpages
```

This runs:
1. `invoke preview` (production build)
2. `ghp-import -b master -m "Publish site on YYYY-MM-DD" public -p -f`

### Manual Deployment (Alternative)
```bash
# Build for production
invoke preview

# Deploy manually
cd public
git add .
git commit -m "Deploy site"
git push origin master
```

### Custom Domain Setup
1. Create `content/extra/CNAME`:
   ```
   banaie.ir
   ```

2. Update `publishconf.py`:
   ```python
   SITEURL = 'https://banaie.ir'
   ```

3. Add to `STATIC_PATHS` and `EXTRA_PATH_METADATA` (already configured)

4. Deploy: `invoke ghpages`

5. Configure DNS: Point `banaie.ir` to `smbanaie.github.io`

## Theme Customization

### Current Theme: pelican-fh5co-marble
- **Location**: `themes/pelican-fh5co-marble/`
- **Features**: Persian RTL support, responsive design

### Modifying Templates
Edit HTML templates in: `themes/pelican-fh5co-marble/templates/`

**Example**: Change footer in `base.html`:
```html
<footer>
    <p>&copy; {{ SITENAME }} - Custom Footer Text</p>
</footer>
```

### Modifying Styles
Edit CSS in: `themes/pelican-fh5co-marble/static/css/style.css`

**Example**: Change header color:
```css
header {
    background-color: #your-color;
}
```

### Adding Custom CSS
Create `themes/pelican-fh5co-marble/static/css/custom.css` and include it in templates.

## Plugins Configuration

### Enabled Plugins
```python
PLUGINS = [
    'i18n_subsites',        # Multi-language support
    'tipue_search',         # Search functionality
    'sitemap',              # XML sitemap generation
    'pelican_persian_date', # Persian date formatting
    'ga_page_view'          # Google Analytics page views
]
```

### Plugin Dependencies
Install required packages:
```bash
pip install beautifulsoup4 pytz jdatetime
```

### Plugin-Specific Settings

**Google Analytics Page Views**:
```python
GOOGLE_SERVICE_ACCOUNT = 'your-service-account@project.iam.gserviceaccount.com'
GOOGLE_KEY_FILE = 'service-account-key.json'
GA_START_DATE = '2018-07-20'
GA_END_DATE = 'today'
GA_METRIC = 'ga:pageviews'
```

## Troubleshooting

### Build Errors

#### "Cannot load plugin" errors
**Symptoms**: `No module named 'bs4'` or `No module named 'pytz'`
**Solution**:
```bash
pip install beautifulsoup4 pytz
```

#### Translation warnings
**Symptoms**: `Cannot find translations for language 'fa'`
**Impact**: Non-critical, safe to ignore
**Cause**: Missing translation files (doesn't break functionality)

#### SITEURL feed warnings
**Symptoms**: `Feeds generated without SITEURL set properly`
**Solution**: Use `invoke preview` for production builds with feeds

### Link/URL Issues

#### Broken links in local development
**Cause**: SITEURL set in `pelicanconf.py`
**Solution**: Keep `SITEURL = ''` in development config

#### Broken links in production
**Cause**: SITEURL not set in `publishconf.py`
**Solution**: Set `SITEURL = 'https://yourdomain.com'` in production

### Content Issues

#### Articles not appearing
**Check**:
- File in correct path: `content/blog/fa/Category/YYYY/MM/filename.md`
- Front matter complete (Title, Date, etc.)
- File extension is `.md`

#### Images not loading
**Check**:
- Images in `content/images/` directory
- Correct path in Markdown: `{static}/images/filename.jpg`
- File permissions and case sensitivity

### Deployment Issues

#### GitHub Pages not updating
**Check**:
1. Repository exists: `https://github.com/smbanaie/smbanaie.github.io`
2. Have push permissions
3. GitHub Pages enabled in repository settings
4. Correct branch (`master`) selected

#### Custom domain not working
**Check**:
1. CNAME file exists: `content/extra/CNAME`
2. DNS configured correctly
3. HTTPS enabled in GitHub Pages settings

## Performance Optimization

### Development Settings
```python
# pelicanconf.py - faster builds during development
DELETE_OUTPUT_DIRECTORY = False  # Don't clean each time
CACHE_CONTENT = True            # Use cache
LOAD_CONTENT_CACHE = True       # Load from cache
```

### Production Settings
```python
# publishconf.py - optimized for deployment
DELETE_OUTPUT_DIRECTORY = True  # Clean builds
CACHE_CONTENT = False           # No cache for production
LOAD_CONTENT_CACHE = False      # Fresh builds
```

### Build Speed Tips
- Use `invoke regenerate` only when actively developing
- Use `invoke build` for one-time checks
- Keep content organized in proper directory structure
- Use relative paths for assets

## Backup and Recovery

### Content Backup
```bash
# Daily backup
cp -r content/ backup/content-$(date +%Y%m%d)/

# Full project backup
tar -czf backup-$(date +%Y%m%d).tar.gz user_area/smbanaie/
```

### Site Recovery
```bash
# If build breaks, clean and rebuild
invoke clean
invoke build
```

### Git-based Recovery
```bash
# Rollback deployment
cd public
git reset --hard HEAD~1  # Go back one commit
git push --force origin master
```

## Advanced Usage

### Custom Invoke Tasks
Edit `tasks.py` to add custom automation:

```python
@task
def backup(c):
    """Backup content directory"""
    import shutil
    from datetime import datetime
    backup_dir = f"backup-{datetime.now().strftime('%Y%m%d')}"
    shutil.copytree('content', backup_dir)
    print(f"Content backed up to {backup_dir}")
```

### Environment Variables
```python
# In pelicanconf.py
import os
if os.environ.get('PELICAN_ENV') == 'production':
    SITEURL = 'https://banaie.ir'
else:
    SITEURL = ''
```

### CI/CD with GitHub Actions
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Pelican Site
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with: python-version: '3.9'
    - run: |
        cd user_area/smbanaie/smbanaie
        pip install -r requirements.txt
        invoke preview
        pip install ghp-import
        ghp-import -b master public -p -f
```

## File Organization Standards

### Content Structure
```
content/
├── blog/fa/
│   ├── Culture/
│   │   └── 1402/
│   │       └── 01/
│   │           └── article-title.md
│   ├── Diary/
│   └── ...
├── pages/fa/
│   ├── about-me.md
│   └── contact.md
├── images/
│   ├── 1402/
│   │   └── 01/
│   │       └── article-image.jpg
│   └── static/
│       └── logo.jpg
└── extra/
    ├── CNAME
    ├── robots.txt
    └── favicon.ico
```

### Naming Conventions
- **Articles**: `YYYY-MM-DD-article-slug.md`
- **Images**: `descriptive-name.jpg`
- **Categories**: Persian names as used in theme
- **Directories**: `YYYY/MM/` format for dates

## Maintenance Tasks

### Monthly Tasks
- Check for Pelican/plugin updates: `pip list --outdated`
- Review and clean old backup files
- Check Google Analytics integration
- Test all major links

### Weekly Tasks
- Run full production build test: `invoke preview`
- Check for broken internal links
- Review recent articles formatting

### Daily Tasks (Development)
- Use `invoke regenerate` for live development
- Test changes at `http://localhost:8000`
- Commit meaningful changes regularly

## Reference

### Repository URLs
- **Source**: https://github.com/smbanaie/smbanaie.github.io
- **Live Site**: https://smbanaie.github.io
- **Theme**: pelican-fh5co-marble (Persian-optimized)

### Key Statistics
- **Articles**: 737
- **Categories**: 6 (Culture, Diary, Meditation, Self-Contemplation, Misc, Tech)
- **Languages**: Persian (primary), English (secondary)
- **Theme**: Responsive, RTL-support, Search-enabled

### Support Resources
- Pelican Documentation: https://docs.getpelican.com/
- Theme Documentation: https://github.com/smbanaie/pelican-fh5co-marble
- Markdown Guide: https://www.markdownguide.org/

---

## Quick Commands Reference
```bash
# Development
invoke build && invoke serve    # Build and test locally
invoke regenerate              # Auto-rebuild on changes

# Production
invoke preview                 # Build for production
invoke ghpages                 # Deploy to GitHub Pages

# Maintenance
invoke clean                   # Clean generated files
pelican --help                 # Show all Pelican options
```

**Remember**: Always use `SITEURL = ''` for local development and set your domain in production config!
