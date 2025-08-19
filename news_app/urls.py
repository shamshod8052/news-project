from django.urls import path

from news_app.views import news_view, news_detail_view, page_404_view, single_page_view, \
    ContactPageView, IndexPageView, LocalNewsView, ForeignNewsView, TechnologyNewsView, SportNewsView, NewsUpdateView, \
    NewsDeleteView, NewsCreateView, admin_page_view, SearchResultsList

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('news/', news_view, name='news'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<slug:news>/', news_detail_view, name='news_detail'),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('pages/contact/', ContactPageView.as_view(), name='contact'),
    path('pages/404-page', page_404_view, name='404-page'),
    path('pages/single-page', single_page_view, name='single-page'),

    path('local-news', LocalNewsView.as_view(), name='local_news_page'),
    path('foreign-news', ForeignNewsView.as_view(), name='foreign_news_page'),
    path('technology-news', TechnologyNewsView.as_view(), name='technology_news_page'),
    path('sport-news', SportNewsView.as_view(), name='sport_news_page'),
    path('admin-page/', admin_page_view, name='admin_page'),
    path('search-result/', SearchResultsList.as_view(), name="search_results")
]
