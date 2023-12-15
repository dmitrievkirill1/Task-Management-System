from django.urls import path
from web.views import index, register_view, login_view, logout_view, project_detail, add_project, add_task, \
    edit_project, delete_project, edit_task, delete_task, add_comment

urlpatterns = [
    path('', index, name="main"),
    path('register/', register_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('projects/<int:project_id>/', project_detail, name='project_detail'),
    path('projects/add/', add_project, name='add_project'),
    path('projects/<int:project_id>/add_task/', add_task, name='add_task'),
    path('projects/<int:project_id>/edit/', edit_project, name='edit_project'),
    path('projects/<int:project_id>/delete/', delete_project, name='delete_project'),
    path('projects/<int:project_id>/tasks/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('projects/<int:project_id>/tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('projects/<int:project_id>/tasks/<int:task_id>/add_comment/', add_comment, name='add_comment'),

]
