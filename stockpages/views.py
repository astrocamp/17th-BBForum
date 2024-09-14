import subprocess

from django.shortcuts import HttpResponse


def stock_data(req, id):
    subprocess.Popen(["python", "stockpages/stockdash.py", str(id)])

    return HttpResponse(f"Dash 已啟動。http://localhost:8050。")
