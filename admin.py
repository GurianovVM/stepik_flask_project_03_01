from flask_admin.contrib.sqla import ModelView


class AdminClient(ModelView):
    column_exclude_list = ['password']
    column_searchable_list = ['name', 'email']
    can_create = False
    can_edit = False
    can_delete = False


class AdminDish(ModelView):
    column_exclude_list = ['password']
    column_searchable_list = ['title']
    can_create = False
    can_edit = False
    can_delete = False


class AdminCategory(ModelView):
    column_searchable_list = ['name']
    can_create = False
    can_edit = False
    can_delete = False


class AdminOrder(ModelView):
    column_searchable_list = ['name', 'email']
    can_create = False
    can_edit = True
    can_delete = False
