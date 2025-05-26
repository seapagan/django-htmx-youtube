from django.urls import path

from films import views

urlpatterns = [
    path("index/", views.IndexView.as_view(), name="index"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.CustomLogout.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("films/", views.FilmList.as_view(), name="film-list"),
]

htmx_urlpatterns = [
    path("check-username/", views.check_username, name="check-username"),
    path("add-film/", views.add_film, name="add-film"),
    path("delete-film/<int:pk>/", views.delete_film, name="delete-film"),
    path("search-film/", views.search_film, name="search-film"),
    path("clear/", views.clear_messages, name="clear"),
    path("sort/", views.sort, name="sort"),
]

urlpatterns += htmx_urlpatterns
