from django.contrib import admin
from .models import Blog,Comment,Commentreply,Content,Contact

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Commentreply)
admin.site.register(Content)
admin.site.register(Contact)
