import os
import timm
import torch
import numpy as np
from PIL import Image
from pymilvus import MilvusClient


class ImageDatabase:
    # rel_path = "vectors.db"
    # abs_path = os.path.abspath(rel_path)
    # full_path = os.path.join(abs_path, "vectors.db")

    def __init__(self, db_path="vectors.db", device=None):
        if device is not None:
            self.device = device
        else:
            self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # Feature extractor
        self.feature_extractor = timm.create_model(
            "maxvit_base_tf_384.in21k_ft_in1k",
            pretrained=True,
            num_classes=0,
        )
        self.feature_extractor.eval()
        self.feature_extractor = self.feature_extractor.to(self.device)

        # Image pre-processor
        data_config = timm.data.resolve_model_data_config(self.feature_extractor)
        self.transforms = timm.data.create_transform(**data_config, is_training=False)

        # Vector DB
        self.client = MilvusClient(uri=db_path)
        # self.client = MilvusClient(uri=self.abs_path)
        if not self.client.has_collection(collection_name="image_embeddings"):
            self.client.create_collection(
                collection_name="image_embeddings",
                vector_field_name="vector",
                dimension=768,
                auto_id=True,
                enable_dynamic_field=True,
                metric_type="COSINE",
            )

            # Indexing
            index_params = MilvusClient.prepare_index_params()
            index_params.add_index(
                field_name="vector",
                metric_type="COSINE",
                index_type="HNSW",
                index_name="HNSW_index",
                params={"M": 64, "efConstruction": 128},
            )
            self.client.create_index(
                collection_name="image_embeddings",
                index_params=index_params,
                sync=True,  # Whether to wait for index creation to complete before returning. Defaults to True.
            )

    def insert(self, image, data):
        input = self.transforms(image).unsqueeze(0).to(self.device)
        embedding = self.feature_extractor(input).flatten()  # 1, 768 -> 768

        data["vector"] = embedding.numpy()
        self.client.insert("image_embeddings", data=data)

    def search(self, image, topk=20):
        input = self.transforms(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            embedding = self.feature_extractor(input).flatten().numpy()

        results = self.client.search(
            "image_embeddings",
            data=[embedding],
            limit=topk,
            output_fields=["*"],
            search_params={"metric_type": "COSINE", "params": {"ef": 32}},
        )

        return results


def example_search():
    image_path = "images/00000017_001.png"
    image = Image.open(image_path).convert("RGB")

    my_db = ImageDatabase(db_path="vectors.db")
    # my_db = ImageDatabase()
    results = my_db.search(image)
    res = {}
    for result in results[0]:
        a = result["entity"]
        a.pop("vector")
        return a
        print(f"Server: {a}")
        res[f"result_{len(res) + 1}"] = a

    return res


# def populate_db():
#     with open('/kaggle/input/sample/sample_labels.csv', mode ='r') as file:
#         csv_file = csv.reader(file)
#         header = True
#         cnt = 0
#         for cols in csv_file:
#             if header:
#                 header = False
#                 continue
#             image_path = os.path.join("/kaggle/input/sample/sample/sample/images", cols[0])
#             image = Image.open(image_path).convert("RGB")
#             data = {
#                 "image_filename": cols[0],
#                 "labels":cols[1],
#                 "patient_id": cols[3],
#                 "patient_age": int(cols[4][:-1]),
#                 "patient_gender": cols[5],
#                 "view_position": cols[6]
#             }
#             my_db.insert(image, data)
#             cnt += 1
#             print(f"{cnt}/5606", end='\r')
#         print('')
