from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, TemplateView
from django.views.generic.list import ListView

from films.forms import RegisterForm
from films.models import Film


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"


class Login(LoginView):
    template_name = "registration/login.html"


class CustomLogout(LogoutView):
    """Custom logout to re-enable GET."""

    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        print("in custom logout")
        return self.post(request, *args, **kwargs)


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)


class FilmList(LoginRequiredMixin, ListView):
    template_name = "films.html"
    model = Film
    context_object_name = "films"

    def get_queryset(self):
        user = self.request.user
        return user.films.all()


def check_username(request):
    username = request.POST.get("username")
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse(
            "<div id='username-error' class='error'>This username already exists</div>"
        )
    else:
        return HttpResponse(
            "<div id='username-error' class='success'>This username is available</div>"
        )


@login_required
def add_film(request):
    name = request.POST.get("filmname")

    film = Film.objects.get_or_create(name=name)[0]

    # add the film to the user's list
    request.user.films.add(film)

    # return template with all of the user's films
    films = request.user.films.all()
    messages.success(request, f"Added {name} to list of films")
    return render(request, "partials/film-list.html", context={"films": films})


@login_required
@require_http_methods(["DELETE"])
def delete_film(request, pk):
    # remove the film from the user's list
    request.user.films.remove(pk)

    # return template with all of the user's remaining films
    films = request.user.films.all()
    return render(request, "partials/film-list.html", context={"films": films})


@login_required
def search_film(request):
    search_text = request.POST.get("search")

    userfilms = request.user.films.all()
    results = Film.objects.filter(name__icontains=search_text).exclude(
        name__in=userfilms.values_list("name", flat=True)
    )
    context = {"results": results}

    return render(request, "partials/search-results.html", context=context)


def clear_messages(request):
    return HttpResponse("")
