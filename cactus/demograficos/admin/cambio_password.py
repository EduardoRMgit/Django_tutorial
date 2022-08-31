from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm, UsernameField
from django.contrib.auth.views import PasswordResetCompleteView
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _


# ------------------------------------------------------
# Cambio de password
# ------------------------------------------------------

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[
                self._meta.model.USERNAME_FIELD
            ].widget.attrs.update({'autofocus': ''})

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_unusable_password()
        return user


class ResetUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(ResetUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['password'].help_text = _(
            'Por seguridad no es posible mostrar la contraseña. '
            'Pero puedes cambiarla usando el link de la parte superior.')


class AdminResetCompleteView(PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        context = super(AdminResetCompleteView,
                        self).get_context_data(**kwargs)
        context['login_url'] = reverse('admin:login')
        return context


class PasswordResetUserAdmin(UserAdmin):
    add_form = UserCreationForm
    add_form_template = 'demograficos/admin/add_user_form.html'
    fieldsets = (
        (None, {'fields': ('username',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
        }),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username',)}),
    )
    form = ResetUserChangeForm
    change_form_template = 'demograficos/admin/change_user.html'

    def get_urls(self):
        return [
            url('^(?P<id>[^/.]+)/password_reset_url/$',
                self.admin_site.admin_view(self.password_reset_url),
                name='password_reset_url'),
            url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/'
                r'(?P<token>[0-9A-Za-z]+-[0-9A-Za-z]+)/$',
                PasswordResetConfirmView.as_view(
                    success_url=reverse_lazy('admin:password_reset_complete')),
                name='password_reset_confirm'),
            url(r'^password_reset_complete/done/$',
                AdminResetCompleteView.as_view(),
                name='password_reset_complete')
        ] + super(PasswordResetUserAdmin, self).get_urls()

    @never_cache
    def password_reset_url(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied

        # user = self.get_object(request, unquote(id))
        # if user is None:
        #     raise Http404(_('No existe el usuario.'))

        user = User.objects.filter(pk=id)
        if user.count() != 1:
            raise Http404(_('No existe el usuario.'))
        user = user.first()

        token_generator = PasswordResetTokenGenerator()
        url = request.build_absolute_uri(
            reverse(
                'admin:password_reset_confirm',
                kwargs={
                    'uidb64': force_text(
                        urlsafe_base64_encode(force_bytes(user.pk))),
                    'token': token_generator.make_token(user)}))
        return TemplateResponse(
            request,
            'demograficos/admin/password_reset_url.html',
            context={
                'user': user,
                'url_cactus': url,
                'title': _('Cambiar contraseña.'),
                'timeout_days': settings.PASSWORD_RESET_TIMEOUT_DAYS})
