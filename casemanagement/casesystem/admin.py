from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm

from casemanagement.casesystem.models import UserRole, Case, Task, User


# Register your models here.
class UserChangeForm(ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=("Raw passwords are not stored, so there is no way to see "
                   "this user's password, but you can change the password "
                   "using <a href=\"password/\">this form</a>."))


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name')
    readonly_fields = ('token_secret_key',)
    form = UserChangeForm


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

