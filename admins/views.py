from django.shortcuts import render


def index(request):
    return render(request, 'admins/index.html')


def admin_users(request):
    return render(request, 'admins/admin-users-read.html')


def admin_users_create(request):
    return render(request, 'admins/admin-users-create.html')


def admin_users_update_delete(request):
    return render(request, 'admins/admin-users-update-delete.html')
