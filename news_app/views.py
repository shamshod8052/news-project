from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from config.custom_permission import OnlyLoggedSuperUser
from news_app.forms import ContactForm, CommentForm
from news_app.models import New, Category


# def index_view(request):
#     categories_list = Category.objects.all()
#     news_list = New.objects.all().order_by('-publish_time')[:5]
#     local_news = New.objects.filter(category__name='Mahalliy').all()[:5]
#
#     context = {
#         'news_list': news_list,
#         'categories_list': categories_list,
#         'local_news': local_news,
#     }
#
#     return render(request, 'index.html', context=context)


class IndexPageView(ListView):
    model = New
    template_name = 'index.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        context['news_list'] = New.objects.all().order_by('-publish_time')[:5]
        context['local_news'] = New.objects.filter(category__name='Mahalliy').all()[:5]
        context['xorij_news'] = New.objects.filter(category__name='Xorij').all()[:5]
        context['sport_news'] = New.objects.filter(category__name='Sport').all()[:5]
        context['texnologiya_news'] = New.objects.filter(category__name='Texnologiya').all()[:5]

        return context


def news_view(request):
    news_list = New.objects.all()
    context = {
        'news_list': news_list,
    }

    return render(request, 'news.html', context=context)

def news_detail_view(request, news):
    new = New.objects.get(slug=news, status=New.Status.PUBLISHED)
    context = {}
    # hitcount_logic
    hitcount = get_hitcount_model().objects.get_for_object(new)
    hits = hitcount.hits
    hitcontext = context['hitcount'] = {'pk': hitcount.pk}
    hit_count_response = HitCountMixin.hit_count(request, hitcount)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.new = new
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    comments = new.comments.filter(active=True)
    comments_count = comments.count()
    context = {
        'new': new,
        'user': request.user,
        'comments': comments,
        'comment_form': comment_form,
        'new_comment': new_comment,
        'comments_count': comments_count,
    }

    return render(request, 'news_detail.html', context=context)

# def contact_page_view(request):
#     form = ContactForm(request.POST)
#     if form.is_valid():
#         form.save()
#         return HttpResponse("<b>Your message has been sent. Thank you!</b>")
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'pages/contact.html', context=context)

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form,
        }
        return render(request, 'pages/contact.html', context=context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<b>Your message has been sent. Thank you!</b>")
        context = {
            'form': form
        }

        return render(request, 'pages/contact.html', context=context)

def page_404_view(request):
    context = {

    }

    return render(request, 'pages/404.html', context=context)

def single_page_view(request):
    context = {

    }

    return render(request, 'pages/single_page.html', context=context)


class LocalNewsView(ListView):
    model = New
    template_name = 'pages/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.filter(category__name='Mahalliy')

        return news


class ForeignNewsView(ListView):
    model = New
    template_name = 'pages/xorij.html'
    context_object_name = 'xorij_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.filter(category__name='Xorij')

        return news


class TechnologyNewsView(ListView):
    model = New
    template_name = 'pages/texnologiya.html'
    context_object_name = 'texnologik_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.filter(category__name='Texnologiya')

        return news


class SportNewsView(ListView):
    model = New
    template_name = 'pages/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.filter(category__name='Sport')

        return news


class NewsUpdateView(UpdateView):
    model = New
    fields = ['title', 'body', 'image', 'category']
    template_name = 'crud/news_edit.html'


class NewsDeleteView(DeleteView):
    model = New
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('index')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = New
    template_name = 'crud/news_create.html'
    fields = [
        "title", "title_uz", "title_en", "title_ru", "slug", "body",
        "body_uz", "body_en", "body_ru", "image", "category", "status"
    ]


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users,
    }

    return render(request, 'pages/admin_page.html', context)


class SearchResultsList(ListView):
    model = New
    template_name = "search_result.html"
    context_object_name = 'search_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        result = New.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query)
        )

        return result
