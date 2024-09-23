import os
import subprocess
from datetime import datetime

from django.shortcuts import get_object_or_404, render

from articles.models import Article, IndustryTag
from userprofiles.models import Profile

from .stockdash import get_stock_data


def stock_data_twii(req):
    latest_price, percent_change = get_stock_data("^TWII")
    current_time = datetime.now().strftime("%m/%d %H:%M")

    if req.user.is_authenticated:
        profile = get_object_or_404(Profile, user=req.user)
        user_img = profile.user_img
    else:
        user_img = None

    return render(
        req,
        "pages/market_index/market_index.html",
        {
            "stock": "加權指數",
            "security_code": "TWA00",
            "latest_price": latest_price,
            "percent_change": percent_change,
            "current_time": current_time,
            "twii": True,
            "user_img": user_img,
        },
    )


def stock_data(req, id):
    if os.name == "nt":  # Windows
        python_executable = r".venv\Scripts\python.exe"
    else:  # macOS/Linux
        python_executable = ".venv/bin/python"

    subprocess.Popen([python_executable, "stockpages/stockdash.py", str(id)])

    stock = get_object_or_404(IndustryTag, security_code=id)
    articles = Article.objects.filter(stock=id).order_by("-id")

    # Get stock price and percentage change
    latest_price, percent_change = get_stock_data(id)
    current_time = datetime.now().strftime("%m/%d %H:%M")

    print(articles)
    if req.user.is_authenticated:
        profile = get_object_or_404(Profile, user=req.user)
        user_img = profile.user_img
    else:
        user_img = None

    return render(
        req,
        "pages/market_index/market_index.html",
        {
            "stock": stock,
            "articles": articles,
            "latest_price": latest_price,
            "percent_change": percent_change,
            "current_time": current_time,
            "user_img": user_img,
        },
    )
