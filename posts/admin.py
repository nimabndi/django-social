from django.contrib import admin
from .models import Post, Comment,Vote

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Vote)
