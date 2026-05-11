from django.shortcuts import get_object_or_404, render
from django.views import View

from apps.hub.forms import ContactForm
from apps.hub.models import News, Service, TeamMember


class HomeView(View):
    def get(self, request):
        context = {
            "services": Service.objects.filter(is_active=True)[:6],
            "team": TeamMember.objects.filter(is_active=True)[:4],
            "news": News.objects.filter(published=True)[:3],
        }
        return render(request, "hub/home.html", context)


class AboutView(View):
    def get(self, request):
        return render(
            request, "hub/about.html", {"team": TeamMember.objects.filter(is_active=True)}
        )


class ServicesView(View):
    def get(self, request):
        return render(
            request, "hub/services.html", {"services": Service.objects.filter(is_active=True)}
        )


class NewsListView(View):
    def get(self, request):
        return render(request, "hub/news.html", {"news_list": News.objects.filter(published=True)})


class NewsDetailView(View):
    def get(self, request, slug):
        article = get_object_or_404(News, slug=slug, published=True)
        return render(request, "hub/news_detail.html", {"article": article})


class TeamView(View):
    def get(self, request):
        return render(request, "hub/team.html", {"team": TeamMember.objects.filter(is_active=True)})


class ContactView(View):
    def get(self, request):
        return render(request, "hub/contact.html", {"form": ContactForm()})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()
            return render(request, "hub/contact.html", {"form": ContactForm(), "sent": True})
        return render(request, "hub/contact.html", {"form": form})
