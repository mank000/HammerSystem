from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import RegistrationForm, UserUpdateForm, VerificationForm
from .models import HammerSystemUser
from .utils import generate_invite_code, generate_verifircation_code

User = get_user_model()


class IndexView(FormView):
    template_name = 'index.html'
    form_class = UserUpdateForm

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        if user.is_authenticated:
            initial['invite_code'] = user.invite_code
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.is_authenticated:
            return context
        invite_code = user.invite_code
        users_with_same_code = HammerSystemUser.objects.filter(
            invite_code=invite_code).exclude(id=user.id)
        context['users_with_same_code'] = users_with_same_code
        return context


class LoginView(FormView):
    template_name = "login.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('phone:auth_code')

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone']
        user = HammerSystemUser.objects.filter(phone=phone_number).first()

        if user:
            user.auth_code = generate_verifircation_code()
            user.save()
        else:
            user = HammerSystemUser.objects.create(
                phone=form.cleaned_data['phone'])
            user.invite_code = generate_invite_code()
            user.auth_code = generate_verifircation_code()
            user.save()

        self.request.session['phone'] = str(user.phone)

        return redirect(self.success_url)


class LogoutView(View):
    template_name = "logout.html"

    def get(self, request):
        self.request.session['phone'] = ''
        logout(request)
        return redirect('phone:index')


class VerifyView(FormView):
    template_name = 'auth_code.html'
    form_class = VerificationForm
    success_url = reverse_lazy('phone:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['code'] = HammerSystemUser.objects.get(
            phone=self.request.session['phone']).auth_code
        return context

    def form_valid(self, form):
        phone_number = self.request.session.get('phone')
        auth_code = form.cleaned_data.get('auth_code')

        try:
            user = get_object_or_404(HammerSystemUser,
                                     phone=phone_number,
                                     auth_code=auth_code)
        except Http404:
            form.add_error('auth_code', 'Неверный код подтверждения')
            return self.form_invalid(form)

        user.auth_code = None
        login(self.request, user)
        user.save()
        return super().form_valid(form)


@login_required
def update_user(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.invite_code_changed = True
            user.invite_code = form.cleaned_data['invite_code']
            user.save()
            return redirect('phone:index')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'index.html', {'form': form})
