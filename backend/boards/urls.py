from django.urls import path

from . import views

urlpatterns = [
    path("list-boards/", views.ListBoards),
    path("new-board/", views.CreateBoard),
    path("lists/<int:pk>/", views.get_lists),
    path("<int:pk>/rename-board/", views.RenameBoard),
    path("<int:pk>/board-status-update/", views.BoardStatusUpdate),
    path("<int:pk>/new-list/", views.CreateList),
    path("<int:pk>/board-lists/", views.get_lists),
    path("<int:pk>/rename-list/", views.RenameList),
    path("<int:pk>/list-status-update/", views.ListStatusUpdate),
    path("list/<int:pk>/new-card/", views.CreateCards),
    path("card/<int:pk>/change-order/", views.ChangeCardOrder)
]