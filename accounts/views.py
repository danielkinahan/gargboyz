from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView



class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        # Set is_active to False by default
        form.instance.is_active = False
        return super().form_valid(form)

class LoginView(LoginView):
    template_name = 'accounts/login.html'