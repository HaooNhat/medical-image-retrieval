from django.http import JsonResponse

from .ImageDatabase import ImageDatabase
from PIL import Image

# from .const import results
from .utils import find_image_from_cloudinary, calculate_probs, generate_custom_id, transform_text, upload_single_image


def getRoutes(request):
    routes = [
        "GET /api/",
        "POST /api/query",
    ]
    return JsonResponse(routes, safe=False)


def query(request):
    if request.method == "POST":
        query_image = request.FILES["query_image"]

        image = Image.open(query_image).convert("RGB")

        my_db = ImageDatabase(db_path="sample_vectors.db", model_path="models/model.pt")
        results = my_db.search(image)
        res = []
        # real version
        for result in results[0]:
            a = result["entity"]
            a.pop("vector")
            res.append(a)
            image_url = find_image_from_cloudinary(a["image_filename"])
            res[-1]["image_url"] = image_url
            # print(f"Server: {a}")
        
        # test version:
        # for result in results:
        #     image_url = find_image_from_cloudinary(result["image_filename"])
        #     res.append(result)
        #     res[-1]["image_url"] = image_url
            # print(res[-1])
            
        probs = calculate_probs(res)

        return JsonResponse(
            {
                "results": res,
                "probs": probs,
            }
        )


def upload(request):
    if request.method == "POST":
        upload_image = request.FILES['image_file']
        
        image_url = find_image_from_cloudinary(upload_image.name)

        if image_url:
            return JsonResponse({
                "message": "Image already exist"
            })
        
        data = {
            "image_filename": upload_image.name,
            "labels": transform_text(request.POST['labels']),
            "patient_id": request.POST['patient_id'],
            "patient_age": request.POST['patient_age'],
            "patient_gender": request.POST['patient_gender'],
            "view_position": request.POST['view_position'],
            "id": generate_custom_id(),
        }
        
        try:
            print("Outer check 1")
            my_db = ImageDatabase(db_path="sample_vectors.db", model_path="models/model.pt")
            print("Outer check 2")
            my_db.insert(upload_image, data)
            print("Outer check 3")
            upload_single_image(upload_image)
        
            print("Outer check 4")
            return JsonResponse(
                {
                    "message": "Upload successfully",
                }
            )
        except:
            return JsonResponse({
                "message": "Error insert image data"
            })