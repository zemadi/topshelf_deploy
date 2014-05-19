from django.forms import ModelForm, DateField
from topshelf.models import IngredMaster, UserIngred

__author__ = 'zhila'
# Note: for user auth, you do not need to create a model to store the data.

from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta(object):
        model = User
        fields = ["username","email","password"]
        #Covers typed in password text.
        widgets = {
            "password": forms.PasswordInput
        }

#SignupForm doesn't need to inherit from UserForm-- it can be combined.
class SignupForm(UserForm):
    #requires user to enter password twice to make sure it's not incorrect
    confirm_password = forms.CharField(
        widget= forms.PasswordInput
    )

    def clean(self):
        password = self.cleaned_data.get("password")
        password_conf = self.cleaned_data.get("confirm_password")
        if password is not None and password != password_conf:
            raise forms.ValidationError(
                "Password confirmation does not match password"
            )
        return self.cleaned_data

class LoginForm(forms.Form):
    username =  forms.CharField()
    password = forms.CharField(widget= forms.PasswordInput)

class IngredForm(ModelForm):
    class Meta:
        model = UserIngred

    # def __init__(self, user, *args, **kwargs):
    #     super(IngredForm, self).__init__(*args, **kwargs)
    #     self.fields['ing_master'].queryset = UserIngred.objects.filter(user=user)

# class RecipeForm(ModelForm):
#     select1 = forms.ChoiceField(UserIngred.ing_master)
#     select2 = forms.ChoiceField(UserIngred.ing_master)
#     select3 = forms.ChoiceField(UserIngred.ing_master)
#     diet_choice = forms.ChoiceField(DietMaster.diet)
