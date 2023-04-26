from django.contrib import admin
from reviews.models import (
    Categories,
    Comment,
    Genres,
    Review,
    Title,
    TitleGenre,
    User,
)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')


admin.site.register(Title, TitleAdmin)
admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(TitleGenre)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(User)
