from django.conf import settings
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.fields import ToManyField, CharField, ToOneField
from tastypie.resources import ModelResource, Resource
from topshelf.api.authorization import UserObjectsOnlyAuthorization
from topshelf.models import IngredMaster, UserIngred, UserRecipe, IngredMaster_test


# # Limit post, delete, etc to only the admin?
# class MasterIngredientResource(ModelResource):
#     class Meta:
#         max_limit = None
#         queryset = IngredMaster.objects.all()
#         resource_name = "all_ingredients"
#         authorization = Authorization()
#         authentication = BasicAuthentication()

# Limit post, delete, etc to only the admin?
class MasterIngredientResource(ModelResource):
    class Meta:
        max_limit = None
        queryset = IngredMaster_test.objects.all()
        resource_name = "all_ingredients"
        authorization = Authorization()
        authentication = BasicAuthentication()


class UserIngredResource(ModelResource):
    ing_master= ToOneField(MasterIngredientResource, "ing_master", full=True)

    class Meta:
        queryset = UserIngred.objects.all().order_by('ing_master')
        resource_name = "pantry"
        authorization = UserObjectsOnlyAuthorization()
        authentication = BasicAuthentication()


class UserRecipeResource(ModelResource):
    ingred = ToManyField(MasterIngredientResource, "ingred", full=True, null=True)

    class Meta:
        queryset = UserRecipe.objects.all()
        resource_name = "user_favorites"
        authorization = UserObjectsOnlyAuthorization()
        authentication = BasicAuthentication()




######################
# Non-Model Resource #
######################

class Version(object):
    def __init__(self, identifier=None):
        self.identifier = identifier


class VersionResource(Resource):
    identifier = CharField(attribute='identifier')

    class Meta:
        resource_name = 'version'
        allowed_methods = ['get']
        object_class = Version
        include_resource_uri = False

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.identifier
        else:
            kwargs['pk'] = bundle_or_obj['identifier']

        return kwargs

    def get_object_list(self, bundle, **kwargs):
        return [Version(identifier=settings.VERSION)]

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle, **kwargs)