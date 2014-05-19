from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, url, include

from tastypie.api import Api
from topshelf.api.resources import UserIngredResource, UserRecipeResource, MasterIngredientResource

from django.contrib import admin
from topshelf_main import settings

admin.autodiscover()

# Created API's run on Django-Tastypie, for easy access and interaction with Angular. Would like to use this as the basis for a mobile app as well.
v1_api = Api(api_name="v1")
v1_api.register(MasterIngredientResource())
v1_api.register(UserIngredResource())
# v1_api.register(UserRecipeResource())

# Url's for authentication and accounts. Not heavily used right now but these will be once things are cleaned up a bit.
urlpatterns = patterns('',
                       url(r'^$', 'topshelf.views.index', name='index'),
                       url(r'^signup/', 'topshelf.views.signup', name="signup"),
                       url(r'^accounts/login/', 'topshelf.views.login_page', name="login"),
                       url(r'^accounts/password/change/$', auth_views.password_change, name='password_change'),
                       url(r'^accounts/password/change/done/$', auth_views.password_change_done, name='password_change_done'),
                       url(r'^accounts/password/reset/$', auth_views.password_reset,
                           name='password_reset'),
                       url(r'^accounts/password/reset/done/$', auth_views.password_reset_done,
                           name='password_reset_done'),
                       url(r'^accounts/password/reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
                       url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           name='password_reset_confirm'),
                       url(r'accounts/', include('registration.backends.default.urls')),


                       # The recipe data pages are basically just angular data dumps. About and recipe detail pages are currently inactive.
                       # url(r'^about/', 'topshelf.views.about', name='about'),
                       url(r'^(?P<user_id>\w+)/recipe_data/$', 'topshelf.views.recipe', name='recipe_data'),
                       # url(r'^(?P<user_id>\w+)/recipe_detail_data/$', 'topshelf.views.recipe_detail', name='recipe_detail_data'),

                       # For APIs and Angular
                       url(r'^api/', include(v1_api.urls)),
                       url(r'^app/', 'topshelf.views.angular', name="angular"),
                       url(r'api/lecture/doc/',
                           include('tastypie_swagger.urls', namespace='tastypie_swagger'),
                           kwargs={"tastypie_api_module": "v1_api",
                                   "namespace": "lecture_tastypie_swagger"}
                       ),
                       url(r'^admin/', include(admin.site.urls)),

                       )