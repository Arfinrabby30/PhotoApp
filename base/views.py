from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.



def gallery(request):
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name__contains=category)

    categories = Category.objects.all()
    # photos = Photo.objects.all()

    context = {'categories': categories, 'photos': photos}
    return render(request, 'base/gallery.html', context)



def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    context = {'photo': photo}
    return render(request, 'base/photo.html', context)



def addPhoto(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                name=data['category_new'])
        else:
            category = None

        photo = Photo.objects.create(
            category=category,
            description=data['description'],
            image=image,
        )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'base/add.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists:
            messages.info(request, "Invalid username.")
            return redirect('login')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid password!")
            return redirect('login')

        else:
            login(request, user)
            return redirect('gallery')
    return render(request, 'base/login.html')


def logout_page(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username already taken.")
            return redirect('register_page')

        user = User.objects.create(
            username=username,
        )

        user.set_password(password)
        user.save()
        messages.info(request, "Account has been created!.")
        return redirect('login')

    return render(request, 'base/register.html')
