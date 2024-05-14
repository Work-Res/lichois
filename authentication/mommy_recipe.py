# recipes.py
from model_mommy.recipe import Recipe, seq
from django.contrib.auth import get_user_model

user_recipe = Recipe(get_user_model(),
                     username='test',
                     password='test@123',
                     email='test@example.com',
                     )
