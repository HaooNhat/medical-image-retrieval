from django.http import JsonResponse
from .ImageDatabase import example_search
import json


def getRoutes(request):
    routes = [
        "GET /api/",
        "POST /api/query",
    ]
    return JsonResponse(routes, safe=False)


def query(request):
    res = example_search()
    return JsonResponse(
        {
            "result": "oke",
        }
    )
