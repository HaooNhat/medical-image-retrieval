from django.http import JsonResponse

from .ImageDatabase import ImageDatabase
from PIL import Image

from .const import results
from .utils import find_image_from_cloudinary


def getRoutes(request):
    routes = [
        "GET /api/",
        "POST /api/query",
    ]
    return JsonResponse(routes, safe=False)


def query(request):
    if request.method == "POST":
        query_image = request.FILES["query_image"]

        # image = Image.open(query_image).convert("RGB")

        # my_db = ImageDatabase(model_path="models/model.pt")
        # results = my_db.search(image)
        res = []
        # real version
        # for result in results[0]:
        #     a = result["entity"]
        #     a.pop("vector")
        #     res.append(a)
        #     image_url = find_image_from_cloudinary(a["image_filename"])
        #     res[-1]["image_url"] = image_url
        #     print(f"Server: {a}")
        
        # test version:
        for result in results:
            image_url = find_image_from_cloudinary(result["image_filename"])
            res.append(result)
            res[-1]["image_url"] = image_url
            # print(res[-1])

        return JsonResponse(
            {
                "results": res,
            }
        )
