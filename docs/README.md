# Pelican Documentation

## Quick Start

1. **Navigate to project directory**:
   ```bash
   cd user_area/smbanaie/smbanaie
   ```

2. **Build and serve locally**:
   ```bash
   invoke build && invoke serve
   # Visit http://localhost:8000
   ```

3. **Deploy to production**:
   ```bash
   invoke ghpages
   # Site published to https://smbanaie.github.io
   ```

## 📖 Complete Guide (Recommended)
**Start here**: **[pelican-complete-guide.md](pelican-complete-guide.md)** - Everything you need in one comprehensive file

## Additional Reference Files

- **[pelican-commands-table.md](pelican-commands-table.md)** - Quick command reference table
- **[configuration-examples.md](configuration-examples.md)** - Configuration examples
- **[github-deployment-guide.md](github-deployment-guide.md)** - GitHub Pages deployment details

## User Management
- **Enhanced Interface**: `/admin/users` provides advanced user management with improved modal messages
- **Features**: Post count display, default author warnings, success/error modals

## Project Overview

This Pelican project generates a Persian/Farsi blog with:
- **737 articles** across multiple categories
- **Multi-language support** (Persian primary, English secondary)
- **Responsive theme** (pelican-fh5co-marble)
- **Search functionality** (Tipue Search)
- **RSS/Atom feeds**
- **XML sitemap**
- **Google Analytics integration**

## Key Features

### Content Management
- Markdown-based articles with Persian date support
- Categorized content (Culture, Diary, Meditation, etc.)
- Static pages (About, Contact)
- Image management

### Development Workflow
- Auto-regeneration on file changes
- Local development server
- Production-ready builds

### Deployment
- One-command GitHub Pages deployment
- Custom domain support
- CDN delivery via GitHub

## Directory Structure

```
user_area/smbanaie/smbanaie/
├── content/           # Source Markdown files
├── themes/           # Pelican themes
├── plugins/          # Pelican plugins
├── public/           # Generated HTML (after build)
├── pelicanconf.py    # Development config
├── publishconf.py    # Production config
└── tasks.py          # Invoke automation tasks
```

## Essential Commands

| Task | Command | Description |
|------|---------|-------------|
| **Develop** | `invoke build` | Build for local testing |
| **Test** | `invoke serve` | View site at localhost:8000 |
| **Auto-dev** | `invoke regenerate` | Auto-rebuild on changes |
| **Deploy** | `invoke ghpages` | Publish to GitHub Pages |

## Configuration Quick Reference

### Local Development
```python
# pelicanconf.py
SITEURL = ''  # Empty for relative URLs
```

### Production
```python
# publishconf.py
SITEURL = 'http://banaie.ir'  # Your domain
```

## Getting Help

### Common Issues
- **Plugin errors**: Run `pip install beautifulsoup4 pytz`
- **Translation warnings**: Safe to ignore (non-critical)
- **Feed warnings**: Use `invoke preview` for production feeds

### Debug Commands
```bash
# Show all settings
pelican -s pelicanconf.py --print-settings

# Verbose build
invoke build -v
```

## Contributing

### Content Creation
1. Create Markdown files in `content/blog/fa/Category/YYYY/MM/`
2. Add front matter (Title, Date, Category, etc.)
3. Use `invoke build && invoke serve` to test

### Theme Customization
1. Edit templates in `themes/pelican-fh5co-marble/templates/`
2. Modify styles in `themes/pelican-fh5co-marble/static/css/`
3. Use `invoke regenerate` for live preview

## Repository

- **Source**: https://github.com/smbanaie/smbanaie.github.io
- **Live Site**: https://smbanaie.github.io
- **Theme**: pelican-fh5co-marble (Persian-optimized)

---

**Need help?** Check the detailed guides above or run `invoke --list` for available commands.
