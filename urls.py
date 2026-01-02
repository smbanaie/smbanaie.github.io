import os.path
import tornado
import tornado.web
from handlers import (
    admin_Handler,
    categories_Handler,
    category_consistency_Handler,
    add_new_post_Handler,
    admin_add_post_Handler,
    posts_list_Handler,
    edit_post_Handler,
    users_Handler,
    settings_Handler,
    index_handler
)

urlList  = [
    (r'/admin/posts', posts_list_Handler),
    (r'/admin/posts/add', admin_add_post_Handler),
    (r'/admin/posts/edit', edit_post_Handler),
    (r'/admin/categories', categories_Handler),
    (r'/admin/category-consistency', category_consistency_Handler),
    (r'/admin/users', users_Handler),
    (r'/admin/settings', settings_Handler),
    (r'/admin', admin_Handler),
    (r'/admin/', admin_Handler),
    (r'/', index_handler.index_Handler),
    (r'/posts/add', add_new_post_Handler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "static")}),
    (r'/images/(.*)', tornado.web.StaticFileHandler, {'path': r'e:\Projects\pelicanwebsitebuilder\user_area\smbanaie\smbanaie\content\images'}),

]