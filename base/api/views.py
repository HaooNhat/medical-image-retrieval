from django.http import JsonResponse
from .ImageDatabase import example_search


def getRoutes(request):
    routes = [
        "GET /api/",
        "POST /api/query",
    ]
    return JsonResponse(routes, safe=False)


def query(request):
    example_search()
    pass
