from flask_user import current_user
from flask import url_for, redirect, request, abort
from flask_admin.contrib import sqla


class AdminModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('Admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('user.login', next=request.url))

class UserView(AdminModelView):
    column_list = ['user_id', 'first_name', 'last_name', 'email', 'date_created', 'admin', 'deleted']
    form_columns = ('first_name', 'last_name', 'email', 'admin', 'deleted')
    column_searchable_list = ('user_id', 'first_name', 'last_name', 'email', 'date_created', 'admin', 'deleted')
    column_editable_list = ('email', 'admin', 'deleted')
    page_size = 20

class DockingJobsView(AdminModelView):
    column_list = ['docking_job_id', 'user_id', 'job_status_id', 'last_updated', 'job_type_id', 'memo', 'marked_favorite', 'deleted']
    form_columns = ('docking_job_id', 'user_id', 'job_status_id', 'last_updated', 'job_type_id', 'memo', 'marked_favorite', 'deleted')
    column_searchable_list = ('docking_job_id', 'user_id', 'job_status_id', 'last_updated', 'job_type_id', 'memo', 'marked_favorite', 'deleted')
    column_editable_list = ('docking_job_id', 'user_id', 'job_status_id', 'last_updated', 'job_type_id', 'memo', 'marked_favorite', 'deleted')
    page_size = 20

class JobTypesView(AdminModelView):
    column_list = ['job_type_id', 'short_name', 'long_name']
    form_columns = ('job_type_id', 'short_name', 'long_name')
    column_searchable_list = ('job_type_id', 'short_name', 'long_name')
    column_editable_list = ('job_type_id', 'short_name', 'long_name')
    page_size = 20

class JobStatusesView(AdminModelView):
    column_list = ['job_status_id', 'job_status_name']
    form_columns = ('job_status_id', 'job_status_name')
    column_searchable_list = ('job_status_id', 'job_status_name')
    column_editable_list = ('job_status_id', 'job_status_name')
    page_size = 20