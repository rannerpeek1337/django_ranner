from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),  # http://127.0.0.1:8000/
    path("categories/<int:pk>/", views.category_articles, name="category_articles"),
    path("articles/<int:pk>/", views.article_detail, name="article_detail"),
    path("login/", views.login_view, name="login"),
    path("registration/", views.registration_view, name="registration"),
    path("logout/", views.user_logout, name="logout"),
    path("articles/add", views.add_article, name="add_article"),
    path("articles/update/<int:pk>/", views.UpdateArticleView.as_view(), name="update"),
    path("articles/delete/<int:pk>/", views.DeleteArticleView.as_view(), name="delete"),
    path("profile/<str:username>/", views.profile_view, name="profile"),
    path("<str:obj_type>/<int:obj_id>/<str:action>/", views.add_vote, name="add_vote")
]