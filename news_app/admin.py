from django.contrib import admin

from news_app.models import Category, New, Contact, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')

@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'publish_time')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_time'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'created_time', 'active')
    list_filter = ('active', 'created_time')
    search_fields = ('user__first_name', 'body')
    actions = ('disable_comments', 'activate_comments')

    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def activate_comments(self, request, queryset):
        queryset.update(active=True)
