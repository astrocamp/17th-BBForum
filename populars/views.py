from django.shortcuts import render


def popular_stocks(request):
    return render(request, "popular_pages/popular_stocks/popular_stocks.html")


def popular_students(request):
    return render(request, "popular_pages/popular_students/popular_students.html")


def popular_answers(request):
    return render(request, "popular_pages/popular_answers/popular_answers.html")


def base(request):
    return render(request, "base.html")
