from django.shortcuts import render, HttpResponse, redirect
from .models import Article, Category, ArticleCountView, Like, Dislike, Comment
from .forms import LoginForm, RegistrationForm, ArticleForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.models import User


# Create your views here.

# http://127.0.0.1:8000/


class UpdateArticleView(UpdateView):
    template_name = "pages/article_form.html"
    model = Article
    success_url = "/"
    form_class = ArticleForm


class DeleteArticleView(DeleteView):
    template_name = "pages/article_confirm_delete.html"
    success_url = "/"
    model = Article


def index_view(request):
    articles = Article.objects.filter(is_active=True)
    context = {
        "articles": articles
    }
    return render(request, "pages/index.html", context)


def category_articles(request, pk):
    category = Category.objects.get(pk=pk)
    articles = Article.objects.filter(category=category)
    context = {
        "articles": articles
    }
    return render(request, "pages/index.html", context)


def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    comments = article.comments.all()

    try:
        article.likes
    except Exception as e:
        Like.objects.create(article=article)

    try:
        article.dislikes
    except Exception as e:
        Dislike.objects.create(article=article)



    if request.session.session_key:
        request.session.save()
    session_id = request.session.session_key

    if not request.user.is_authenticated:
        views_items = ArticleCountView.objects.filter(session_id=session_id, article=article)
        if not views_items.count() and str(session_id) != "None":
            views = ArticleCountView()
            views.session_id = session_id
            views.article = article
            views.save()

            article.views += 1
            article.save()
    else:
        views_items = ArticleCountView.objects.filter(user=request.user, article=article)
        if not views_items.count():
            views = ArticleCountView()
            views.user = request.user
            views.article = article
            views.save()

            article.views += 1
            article.save()
    comment_likes = {x.pk:x.likes.user.all().count() for x in article.comments.all()}
    comment_dislikes = {x.pk:x.dislikes.user.all().count() for x in article.comments.all()}
    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.article = article
            form.save()
            try:
                form.likes
            except Exception as e:
                Like.objects.create(comment=form)

            try:
                form.dislikes
            except Exception as e:
                Dislike.objects.create(comment=form)
            return redirect("article_detail", article.pk)
    else:
        form = CommentForm() # {{ form }}

    likes = article.likes.user.all().count()
    dislikes = article.dislikes.user.all().count()

    context = {
        "article": article,
        "form": form,
        "comments": comments,
        "likes": likes,
        "dislikes": dislikes,
        "comment_likes": comment_likes,
        "comment_dislikes": comment_dislikes
    }
    return render(request, "pages/article_detail.html", context)


def add_vote(request, obj_type, obj_id, action):
    from django.shortcuts import get_object_or_404

    obj = None
    if obj_type == "article":
        obj = get_object_or_404(Article, pk=obj_id)
    elif obj_type == "comment":
        obj = get_object_or_404(Comment, pk=obj_id)

    try:
        obj.likes
    except Exception as e:
        if obj.__class__ is Article:
            Like.objects.create(article=obj)
        else:
            Like.objects.create(comment=obj)

    try:
        obj.dislikes
    except Exception as e:
        if obj.__class__ is Article:
            Dislike.objects.create(article=obj)
        else:
            Dislike.objects.create(comment=obj)

    if action == "add_like":
        if request.user in obj.likes.user.all():
            obj.likes.user.remove(request.user.pk)
        else:
            obj.likes.user.add(request.user.pk)
            obj.dislikes.user.remove(request.user.pk)
    elif action == "add_dislike":
        if request.user in obj.dislikes.user.all():
            obj.dislikes.user.remove(request.user.pk)
        else:
            obj.dislikes.user.add(request.user.pk)
            obj.likes.user.remove(request.user.pk)
    else:
        return redirect(request.environ["HTTP_REFERER"])
    return redirect(request.environ["HTTP_REFERER"])

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
    else:
        form = LoginForm()
    ctx = {
        "form": form
    }
    return render(request, "pages/login.html", ctx)


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()

    ctx = {
        "form": form
    }
    return render(request, "pages/registration.html", ctx)


def user_logout(request):
    logout(request)
    return redirect("index")


def add_article(request):
    if request.method == "POST":
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect("article_detail", form.pk)
    else:
        form = ArticleForm()

    ctx = {
        "form": form
    }
    return render(request, "pages/article_form.html", ctx)


def profile_view(request, username):
    user = User.objects.get(username=username)
    articles = Article.objects.filter(author=user)
    total_views = sum([article.views for article in articles])
    total_comments = sum([article.comments.all().count() for article in articles])
    context = {
        "user": user,
        "articles": articles,
        "total_views": total_views,
        "total_comments": total_comments
    }

    return render(request, "pages/profile.html", context)