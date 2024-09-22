from django.shortcuts import get_object_or_404, render

from userprofiles.models import Profile


def popular_stocks(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        user_img = profile.user_img
    else:
        user_img = None

    return render(
        request,
        "popular_pages/popular_stocks/popular_stocks.html",
        {"user_img": user_img},
    )


def popular_students(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        user_img = profile.user_img
    else:
        user_img = None
    return render(
        request,
        "popular_pages/popular_students/popular_students.html",
        {"user_img": user_img},
    )


def popular_answers(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        user_img = profile.user_img
    else:
        user_img = None
    return render(
        request,
        "popular_pages/popular_answers/popular_answers.html",
        {"user_img": user_img},
    )


def base(request):
    return render(request, "base.html")
