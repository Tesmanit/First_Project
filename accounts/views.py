from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.views import LoginView, LogoutView


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegisterForm()

    ctx = {
        'form': form,
        'title': 'Регистрация',
        'button_content': 'Создать аккаунт'
    }
    return render(request, 'accounts/register.html', ctx)


class Login(LoginView):
    template_name = 'accounts/register.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_content'] = 'Войти'
        return context

class Logout(LogoutView):
    template_name = 'accounts/register.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = 'Войти заново'
        return context
