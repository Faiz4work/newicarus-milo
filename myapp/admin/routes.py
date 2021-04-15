from myapp import admin, db
from flask_admin.contrib.sqla import ModelView
from myapp.models import Users, Jobs
from flask import redirect, url_for, flash
from flask_login import current_user
from flask_admin.menu import MenuLink

class MyView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True
        else:
            return False
    def inaccessible_callback(self, name, **kwargs):
        flash('You are not authorized for this view', 'danger')
        return redirect(url_for("main.home"))


admin.add_view(MyView(Users, db.session))
admin.add_link(MenuLink(name='Search', url='/'))
admin.add_link(MenuLink('Logout', url='/logout'))


admin.add_view(ModelView(Jobs, db.session))
