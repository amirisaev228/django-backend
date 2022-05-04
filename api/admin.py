from django.contrib import admin
from api.models import Genre, Book, Order, User

admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(User)