"""
Test configuration and shared fixtures for Pelican Website Builder tests.
"""

import pytest
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture
def temp_user_dir():
    """Create a temporary user directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_userconf_data():
    """Mock userconf data for testing."""
    return {
        'AUTHORS': ['testuser', 'smbanaie', 'مجتبی بنائی'],
        'CATEGORIES': {
            'cat_list': [
                ('Culture', 'فرهنگ و جامعه'),
                ('Diary', 'روزنوشت'),
                ('Meditation', 'بر بلندای شعر و عرفان'),
                ('Tech', 'فناوری')
            ],
            'default_category': 'Diary',
            'status': {
                'Culture': 'active',
                'Diary': 'active',
                'Meditation': 'active',
                'Tech': 'active'
            }
        },
        'DEFAULT_AUTHOR': 'smbanaie',
        'AUTHOR_STATUS': {
            'testuser': 'active',
            'smbanaie': 'active',
            'مجتبی بنائی': 'active'
        }
    }

@pytest.fixture
def sample_article_content():
    """Sample article content for testing."""
    return """title: Test Article
date: 2024-01-01
modified: 2024-01-01
icon: icon-link2
lang: fa
category: فناوری
tags: test, article
authors: testuser
slug: test-article

This is a test article content.
"""

@pytest.fixture
def sample_meditation_article():
    """Sample meditation article content."""
    return """title: مدیتیشن مقاله
date: 2024-01-01
modified: 2024-01-01
icon: icon-link2
lang: fa
category: بر بلندای شعر و عرفان
tags: meditation, poetry
authors: smbanaie
slug: meditation-article

این یک مقاله درباره مدیتیشن است.
"""
