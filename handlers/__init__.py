__author__ = 'mojtaba.banaie'

# Import all handlers for backward compatibility
from handlers.admin.dashboard import admin_Handler
from handlers.admin.categories import categories_Handler, category_consistency_Handler
from handlers.admin.posts import add_new_post_Handler, admin_add_post_Handler, posts_list_Handler, edit_post_Handler
from handlers.admin.users import users_Handler
from handlers.admin.settings import settings_Handler

# Re-export for easy importing
__all__ = [
    'admin_Handler',
    'categories_Handler',
    'category_consistency_Handler',
    'add_new_post_Handler',
    'admin_add_post_Handler',
    'posts_list_Handler',
    'edit_post_Handler',
    'users_Handler',
    'settings_Handler'
]