from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email","id","name","username","is_superuser","is_deleted"]
    exclude = ["password"]
    actions = ['temp_delete','undo_delete']

    def temp_delete(self, request, queryset):
        # Implement your custom action logic here
        queryset.update(is_deleted=True)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects temporarily deleted.')

    def undo_delete(self, request, queryset):
        queryset.update(is_deleted=False)

        selected = queryset.count()
        self.message_user(request, f'{selected} objects undo deleted.')

    temp_delete.short_description = 'Delete temporarily'
    undo_delete.short_description = 'Undo delete'
