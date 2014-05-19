import urllib2
import requests
from bs4 import BeautifulSoup
import django.utils.encoding

__author__ = 'zhila'
from django.http import request
from django.core.management.base import BaseCommand
from topshelf.models import IngredMaster_test

#Second ingredient import. This one had clean data (after I scraped and formatted it) but not as many ingredients. This one has about 1k compared to 15k. It is still a good starting point for a search and may be useful in creating dictionaries for the ingredients list. The best way to normalize the data might be to use these as a generic key for all values stored in the larger ingredients list.

class Command(BaseCommand):
    def handle(self, *args, **options):
        # This site had a nice list of lots of ingredients, so I scraped it.
        data = urllib2.urlopen('http://www.food.com/library/all.zsp')
        food_data = BeautifulSoup(data, from_encoding='utf-8')
        data.close()

        ingredients = []
        for a in food_data.find_all('a'):
            ingredients.append(a.encode_contents())

        # Pushes data to data table.
        for item in ingredients:
            IngredMaster_test.objects.create(ing_test = item)