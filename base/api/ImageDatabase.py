import os
import csv
import cv2
import timm
import torch
# import kagglehub
import numpy as np
from PIL import Image
from glob import glob
from pymilvus import MilvusClient

import albumentations as albu
from albumentations.pytorch import ToTensorV2


class CustomModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
    
        self.base_model = timm.create_model(
            "tf_efficientnetv2_l.in21k",
            pretrained=True,
            num_classes=0,
        )
        # self.classifier_head = torch.nn.Linear(1280, n_classes)
        

    def forward(self, x):
        pooled_features = self.base_model(x)
        # output = self.classifier_head(pooled_features)
        # return output
        return pooled_features

    def forward_features(self, x):
        return self.base_model(x)

class ImageDatabase:
    def __init__(self, db_path="vectors.db", model_path = "model.pt", device=None):
        if device is not None:
            self.device = device
        else:
            self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # Feature extractor
        self.feature_extractor = CustomModel()
        if model_path != None:
            model_weights = torch.load(model_path, weights_only=True)
            self.feature_extractor.load_state_dict(model_weights)

        self.feature_extractor.eval()
        self.feature_extractor = self.feature_extractor.to(self.device)

        # Image pre-processor 
        image_size = 480   
        self.transform = albu.Compose([
            albu.Resize(image_size, image_size, interpolation=cv2.INTER_LANCZOS4, always_apply=True),
            ToTensorV2()  # Ensure output is a PyTorch tensor
        ])

        # Vector DB
        self.client = MilvusClient(uri=db_path)
        if not self.client.has_collection(collection_name="image_embeddings"):
            self.client.create_collection(
                collection_name="image_embeddings",
                vector_field_name="vector",
                dimension=1280,
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
        image = np.array(image, dtype=np.float32) / 255
        input = self.transform(image=image)['image']
        input = input.unsqueeze(0).to(self.device)
        with torch.no_grad():
            embedding = self.feature_extractor.forward_features(input).flatten().cpu().numpy()  # -> 1280

        data["vector"] = embedding
        self.client.insert("image_embeddings", data=data)

    def insert_batch(self, image_list, data_list):
        new_image_list = [np.array(image, dtype=np.float32) / 255 for image in image_list]
        input_list = [self.transform(image=image)['image'] for image in new_image_list]
        input_batch = torch.stack(input_list).to(self.device)

        with torch.no_grad():
            embeddings = self.feature_extractor.forward_features(input_batch).cpu().numpy()
        
        for i, data in enumerate(data_list):
            data["vector"] = embeddings[i].flatten()

        self.client.insert("image_embeddings", data=data_list)


    def search(self, image, topk=20):
        image = np.array(image, dtype=np.float32) / 255
        input = self.transform(image=image)['image']
        input = input.unsqueeze(0).to(self.device)
        with torch.no_grad():
            embedding = self.feature_extractor.forward_features(input).flatten().cpu().numpy()

        results = self.client.search(
            "image_embeddings",
            data=[embedding],
            limit=topk,
            output_fields=["*"],
            search_params={"metric_type": "COSINE", "params": {"ef": 32}},
        )

        return results



# if __name__ == "__main__":
#     device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
#     print(f'Running on device: {device}')

#     data_path = kagglehub.dataset_download("nih-chest-xrays/data")
#     print("Path to dataset files:", data_path)


#     # Load image names
#     image_list = []
#     test_list_path = os.path.join(data_path, "test_list.txt")
#     with open(test_list_path, mode ='r') as fin:
#         for image_name in fin:
#             if image_name[-1] == '\n':
#                 image_name = image_name[:-1]
#             image_list.append(image_name)
    

#     # Split images to insert to db and images to evaluate
#     rng = np.random.default_rng(seed=42)
#     shuffled_indices = rng.permutation(len(image_list))
#     half = len(image_list) // 2

#     train_set = set()
#     test_set = set()
#     for i in range(len(image_list)):
#         image_name = image_list[ shuffled_indices[i] ]
#         if i <= half:
#             train_set.add(image_name)
#         else:
#             test_set.add(image_name)


#     # Prepare image paths
#     image_paths = {}
#     img_path_template = os.path.join(data_path, "*/images/*.png")
#     paths = glob(img_path_template)
#     for path in paths:
#         image_name = path.split('/')[-1]
#         image_paths[image_name] = path

#     # Create vector database
#     my_db = ImageDatabase(model_path="/root/code/results6/bestmodel_epoch27_loss0.16240.pt", device=device)

#     # Populate database
#     csv_path = os.path.join(data_path, "Data_Entry_2017.csv")
#     with open(csv_path, mode ='r') as file:
#         csv_file = csv.reader(file)
#         header = True
#         progress = 0


#         image_list = []
#         data_list = []
#         for row in csv_file:
#             if header:
#                 header = False
#                 continue

#             image_name = row[0]
#             if image_name not in train_set:
#                 continue

#             image_path = image_paths[image_name]
#             image = Image.open(image_path).convert("RGB")

#             data = {
#                 "image_filename": image_name,
#                 "labels":row[1],
#                 "patient_id": row[3],
#                 "patient_age": row[4][:-1],
#                 "patient_gender": row[5],
#                 "view_position": row[6]
#             }

#             if len(image_list) < 256:
#                 image_list.append(image)
#                 data_list.append(data)
#             else:
#                 my_db.insert_batch(image_list, data_list)
#                 image_list = []
#                 data_list = []

#             progress += 1
#             print(f"{progress}", end='\r')

#         if len(image_list) > 0:
#             my_db.insert_batch(image_list, data_list)
#             print(f"{progress + 1}")
#         else:
#             print('')