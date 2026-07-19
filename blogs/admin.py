from django.contrib import admin
# Importing Blog & Comment models
from .models import Blog, Comment, Profile

# Registers models
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Profile)

