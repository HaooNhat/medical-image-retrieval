from django.http import JsonResponse
from .ImageDatabase import ImageDatabase, example_search
from django.core.files.storage import FileSystemStorage
from PIL import Image


def getRoutes(request):
    routes = [
        "GET /api/",
        "POST /api/query",
    ]
    return JsonResponse(routes, safe=False)


def query(request):
    # res = example_search()
    # return JsonResponse(
    #     {
    #         "results": res,
    #     }
    # )

    if request.method == "POST":
        query_image = request.FILES["query_image"]

        # fs = FileSystemStorage()
        # saved_image = fs.save(query_image.name, query_image)
        # print(f"Image path: {saved_image}")
        # query_image_path = f"media/{saved_image}"

        # image = Image.open(query_image_path).convert("RGB")
        image = Image.open(query_image).convert("RGB")

        my_db = ImageDatabase()
        results = my_db.search(image)
        res = []
        for result in results[0]:
            a = result["entity"]
            a.pop("vector")
            print(f"Server: {a}")
            res.append(a)

        fs.delete(query_image_path)

        return JsonResponse(
            {
                "results": res,
            }
        )
