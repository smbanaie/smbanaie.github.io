#!/usr/bin/env python3
"""
Test script to debug article counting issue.
"""

import sys
import os
import glob
import re

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def _get_article_counts():
    """Scan content directory and count articles by author and category."""
    import os
    import glob
    import re

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

    print(f"Found {len(blog_files)} total markdown files")

    # Log some file paths for debugging
    meditation_files = [f for f in blog_files if 'Meditation' in f]
    print(f"Found {len(meditation_files)} Meditation files: {meditation_files[:3]}")

    for file_path in blog_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()


            # Extract metadata using regex
            authors_match = re.search(r'^authors:\s*(.+)$', content, re.MULTILINE)
            category_match = re.search(r'^category:\s*(.+)$', content, re.MULTILINE)

            # Debug for Meditation files
            if 'Meditation' in str(file_path):
                print(f"Processing Meditation file: {os.path.basename(file_path)}, category: {category_match.group(1).strip() if category_match else 'NO CATEGORY'}")

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
                        print(f"MEDITATION: Mapped '{category_display}' to '{category_id}' for file {os.path.basename(file_path)}")
                else:
                    print(f"Could not match article category '{category_display}' to any userconf category. Available: {list(category_display_to_id.keys())}")
                    if 'Meditation' in str(file_path):
                        print(f"MEDITATION FILE FAILED: {os.path.basename(file_path)} with category '{category_display}'")

        except Exception as e:
            # Skip files that can't be read or parsed
            print(f"Error processing file {file_path}: {e}")
            continue

    return {
        'authors': author_counts,
        'categories': category_counts
    }

# Get article counts
print("Getting article counts...")
counts = _get_article_counts()

print("\n=== ARTICLE COUNTS ===")
print(f"Authors: {counts['authors']}")
print(f"Categories: {counts['categories']}")

print(f"\nMeditation category count: {counts['categories'].get('Meditation', 0)}")

# Check the content directory
from user_area.smbanaie.smbanaie.userconf import CONTENT_DIR
print(f"\nContent directory: {CONTENT_DIR}")

# List some Meditation files
import glob
blog_pattern = os.path.join(CONTENT_DIR, 'blog', '**', '*.md')
blog_files = glob.glob(blog_pattern, recursive=True)
meditation_files = [f for f in blog_files if 'Meditation' in f]

print(f"\nFound {len(meditation_files)} files containing 'Meditation' in path:")
for f in meditation_files[:5]:  # Show first 5
    print(f"  {f}")

# Check one of the meditation files
if meditation_files:
    test_file = meditation_files[0]
    print(f"\nChecking file: {test_file}")
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print("First 200 chars:")
        print(content[:200])
        print("...")

        # Check category line
        import re
        category_match = re.search(r'^category:\s*(.+)$', content, re.MULTILINE)
        if category_match:
            print(f"Category found: '{category_match.group(1).strip()}'")
        else:
            print("No category line found")

    except Exception as e:
        print(f"Error reading file: {e}")