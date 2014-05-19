from django.contrib.auth.models import User
from django.db import models
# the names Ing and Ingred are used for ingredients. Typing ingredients constantly is just tiring.

# IngredMaster is a model with a ton of inconsistent data from the Yummly API. It is unused with the current version of the app but will be cleaned up and used later.
class IngredMaster(models.Model):
    ing = models.CharField(max_length=100)

    def __unicode__(self):
        return self.ing

# List of ingredients in the database, for users to select from. These were test models that ended up working out, so I kept the variable names. These will be cleaned up after bootcamp.

#NOTE: I would never normally make the max length 10k characters, but the data can only be cleaned up manually. So, it has to be re-uploaded and then cleaned in django admin. Not efficient but I couldn't get loaddata to work with JSON.
class IngredMaster_test(models.Model):
    ing_test = models.CharField(max_length=10000)

    def __unicode__(self):
        return self.ing_test

# Table that records user ingredients. Quantity, date, and count are not currently being used but will be added on as input features later. I hope to optimize the recipe search by calculing expiration dates for food, and prioritizing those items in a recipe search.
class UserIngred(models.Model):
    ing_master = models.ForeignKey(IngredMaster_test)
    # May need to add quantity, purchasedate, to intermediary table
    quantity = models.FloatField(null=True, blank=True)
    #Date that a user purchased an item.
    purch_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User)
    #Counts how many times that user has used the ingredient.
    count = models.IntegerField(default=1)

    def __unicode__(self):
        return self.ing_master.ing_test

# A table for a user's favorite recipes. This is currently unused but will be added on later. I just didn't have time to implement it before demo day.
class UserRecipe(models.Model):
    recipe_name = models.CharField(max_length=100)
    user = models.ForeignKey(User)

# #TO ADD LATER, AFTER BOOTCAMP: Add space for people to upload their own .
# class PersonalRecipes(models.Model):
#     recipe_name = models.CharField(max_length=100)
#     personalrecipe_ing = models.ForeignKey(ing_user)
