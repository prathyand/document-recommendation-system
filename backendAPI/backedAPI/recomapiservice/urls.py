from django.urls import path

from .views import recomviews
from .views import searchview
from .views import similardocview
from .views import userinteractionsview

urlpatterns = [
    path('feed/', recomviews.RecomListView.as_view()),
    path('feed/<keyid>/', recomviews.RecomListView.as_view()),
    path('rediscover/<keyid>/', recomviews.RediscoverView.as_view()),
    path('rediscover/', recomviews.RediscoverView.as_view()),
    path('search/<searchquery>/',searchview.SearchListView.as_view()),
    path('similardoc/<docid>/',similardocview.SimilardocListView.as_view()),
    path('createInteraction/',userinteractionsview.UserInteractionsView.as_view())
    ]