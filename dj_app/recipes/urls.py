from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'recipes.views',
    url(r'^/?$', 'home'),
)
