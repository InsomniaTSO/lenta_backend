from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from users.models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма создания пользователя в панели администратора."""
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',)


class CustomUserChangeForm(UserChangeForm):
    """Форма изменения пользователя в панели администратора."""
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',)


@register(User)
class UserAdmin(BaseUserAdmin):
    """
    Класс для панели администратора пользователей. Исползуются
    кастомные формы создания и редактирования пользователя.
    """
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = (
        'email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active'
    )
    list_filter = (
        'email', 'username',
    )
    fieldsets = (
        (None, {'fields': (
            'email', 'username', 'first_name', 'last_name', 'password',
        )}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name', 'password1',
                'password2', 'is_staff', 'is_active',
            )
        }),
    )
    search_fields = ('email', 'username',)
    ordering = ('email', 'username',)
