from .views import CreateGroupView, CreateUserView, DeleteGroupView, DeleteUserView, ListGroupView, ListUserView, UpdateGroupView, UpdateUserView
from django.urls import path, include

usuarios_patterns = ([
    path('crear',CreateUserView.as_view(),name='crear'),
    path('',ListUserView.as_view(),name='lista'),
    path('actualizar/<int:pk>',UpdateUserView.as_view(),name='editar'),
    path('eliminar/<int:pk>',DeleteUserView.as_view(),name='eliminar')
],'usuario')

grupos_patterns = ([
    path('',ListGroupView.as_view(),name='lista'),
    path('crear',CreateGroupView.as_view(),name='crear'),
    path('actualizar/<int:pk>',UpdateGroupView.as_view(),name='editar'),
    path('eliminar/<int:pk>',DeleteGroupView.as_view(),name='eliminar')
],'grupo')