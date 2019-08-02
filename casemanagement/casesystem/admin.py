from django.contrib import admin
from casemanagement.casesystem.models import UserRole, Case, Task, User


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name')


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')


class TasksInlineAdmin(admin.StackedInline):
    model = Task
    raw_id_fields = ("role",)
    extra = 1


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'case_name', 'case_status', 'role')
    inlines = (TasksInlineAdmin, )
    raw_id_fields = ("role",)

