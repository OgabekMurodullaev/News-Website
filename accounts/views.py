from django.contrib.auth.decorators import login_required, user_passes_test
from newsproject.custom_user_passes import CustomUserPassesMixin
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


def userlogin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    return HttpResponse("Siz muvaqqiyatli login qildingiz")
                else:
                    return HttpResponse("Akkauntingiz aktiv holatda emas.")
            else:
                return HttpResponse("Login yoki Parolda xatolik")
    form = LoginForm()
    context = {
        "form": form
    }

    return render(request, 'accounts/login.html', context)


@login_required
def userprofile_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {
        "user": user,
        "profile": profile
    }
    return render(request, 'pages/user-profile.html', context)


def user_registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                "new_user": new_user
            }
            return render(request, 'account/register_done.html', context)
    else:
        form = UserRegistrationForm()
        context = {
            "form": form
        }
        return render(request, 'account/register.html', context)


# class UserRegisterView(CreateView):
#     form_class = UserRegistrationForm
#     success_url = reverse_lazy('login')
#     template_name = 'account/register.html'


@login_required
def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile,)
        if 'remove_image' in request.POST:
            # Agar checkbox belgilangani bo'lsa, rasmni olib tashlash
            request.user.profile.image = None
            request.user.profile.save()
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/profile_edit.html', {"user_form": user_form, "profile_form": profile_form})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_page(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        "admin_users": admin_users
    }
    return render(request, 'pages/admin_page.html', context)

class AdminPageView(CustomUserPassesMixin, View):
    def get(self, request):
        admin_users = User.objects.filter(is_superuser=True)
        context = {
            "admin_users": admin_users
        }
        return render(request, 'pages/admin_page.html', context)


