from  handlers import admin_handler, index_handler
# from Handlers.category__handler import CategoryHandler,CategoryEditHandler,CategoryDeleteHandler,CategoryNewHandler

urlList  = [
    (r'/admin', admin_handler.admin_Handler),
    (r'/', index_handler.index_Handler),
    (r'/posts/add', admin_handler.add_new_post_Handler),

]