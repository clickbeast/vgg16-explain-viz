import torch
import torchvision
import torchvision.transforms as transforms
import pandas as pd
from torchvision.utils import save_image
import torch
import torchvision
from openTSNE import TSNE
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
import os

from parameters import Parameters

def get_mappings_annotations():
    print('processing annotations')

    # --------------------------------------
    # Process mapping sysnsetid (label) to category
    # --------------------------------------

    mapping_label_to_category = {}
    mapping_category_to_label = {}

    with open('datasets/sysnet_to_category.txt') as f:
        for line in f:
            line_items = line.split(':')
            label = line_items[0]
            # print(line_items)
            category = line_items[1].split(',')[0][1:].strip()

            if label == 'n02012849':
                category = 'crane bird'
            if label == 'n03710721':
                category = 'maillot tank suit'

            mapping_label_to_category[label] = category
            mapping_category_to_label[category] = label

    # --------------------------------------
    # Process mapping label_id (class_index) to category
    # --------------------------------------

    mapping_label_id_to_category = {}
    mapping_label_category_to_id = {}

    from torchvision.models import VGG16_Weights

    # Imagenet weights
    weights = VGG16_Weights.DEFAULT

    categories = weights.meta['categories']

    for idx, category in enumerate(categories):
        mapping_label_id_to_category[idx] = category
        mapping_label_category_to_id[category] = idx

    # todo check wich categrories no match , then fic

    # Create dataframe out of it


    return  mapping_label_to_category, mapping_category_to_label, mapping_label_id_to_category, mapping_label_category_to_id


def get_process_annotation_data():
    mapping_label_to_category, mapping_category_to_label, mapping_label_id_to_category, mapping_label_category_to_id = get_mappings_annotations()

    print('processing annotations')

    # --------------------------------------
    # Create mapping dataframe
    # --------------------------------------


    labels = []
    label_ids = []
    categories = []


    for label, category in mapping_label_to_category.items():
        labels.append(label)
        categories.append(category)
        label_ids.append(mapping_label_category_to_id[category])


    data = {
        'label':  labels,
        'label_id': label_ids,
        'category': categories,
    }

    mapping_data_points_df = pd.DataFrame(data)

    return mapping_data_points_df


def process_annotations(annotations_df):

    mapping_data_points_df = get_process_annotation_data()

    # clean up
    annotations_df = annotations_df.drop(
        columns=['noisy_labels_0', 'noisy_labels_1', 'noisy_labels_5', 'noisy_labels_25', 'noisy_labels_50',
                 'is_valid'])

    # parse true labels from dir
    annotations_df['label'] = annotations_df['path'].str.split('/').str[1]

    # include other mappings
    annotations_df = annotations_df.merge(mapping_data_points_df, left_on='label', right_on='label', how='left')

    # include id
    annotations_df['uid'] = range(0, len(annotations_df))

    return annotations_df




#%%


from torch.utils.data import Dataset
import os
import pandas as pd
from torchvision.io import read_image
from torchvision.transforms import InterpolationMode, ToPILImage
from PIL import Image
import numpy

# Define the transformation pipeline
transform = transforms.Compose([
    # Resize the image to 256x256 using bilinear interpolation
    transforms.Resize(256, interpolation=InterpolationMode.BILINEAR),

    # Central crop to 224x224
    transforms.CenterCrop(224),

    # Convert the image to a Tensor and rescale to [0.0, 1.0]
    transforms.ToTensor(),

    # Normalize the image with the given mean and std
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


class CustomImageDataset(Dataset):
    def __init__(self, dataset_dir, annotations_df, transform=None, target_transform=None):
        self.annotations_df = annotations_df
        self.dataset_dir = dataset_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.annotations_df)

    def __getitem__(self, idx):
        img_path = os.path.join(self.dataset_dir, self.annotations_df.iloc[idx]['path'])
        image_tensor = read_image(img_path)

        # Convert tensor to PIL Image before applying transformations
        # image = ToPILImage()(image_tensor)

        image = Image.open(img_path)

        # Ensure the image is in RGB mode (3 channels)
        if image.mode != 'RGB':
            image = image.convert('RGB')



        label = self.annotations_df.iloc[idx]['label']
        label_id = self.annotations_df.iloc[idx]['label_id']
        category = self.annotations_df.iloc[idx]['category']
        uid = self.annotations_df.iloc[idx]['uid']

        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)

        return image, label, label_id, category, uid, img_path


class DatasetManager:



    def __init__(self):
        mapping_label_to_category, mapping_category_to_label, mapping_label_id_to_category, mapping_label_category_to_id = get_mappings_annotations()
        self.mapping_label_id_to_category = mapping_label_to_category
        self.mapping_category_to_label = mapping_category_to_label
        self.mapping_label_id_to_category = mapping_label_id_to_category
        self.mapping_label_category_to_id = mapping_label_category_to_id
        pass

    def fetch_image(self, label, label_id, category, uid, img_path):
        image = Image.open(img_path)
        # Ensure the image is in RGB mode (3 channels)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        image = transform(image)
        return image, label, label_id, category, uid, img_path



def get_data_iter_imagenette(batch_size):
    print('Loading dataset')
    annotations_imagenette_df = pd.read_csv(Parameters.ANNOTATIONS_IMAGENETTE)
    annotations_imagenette_df = process_annotations(annotations_imagenette_df)
    imagenette_data_set = CustomImageDataset(Parameters.DIR_IMAGENETTE, annotations_imagenette_df, transform=transform)
    trainloader = torch.utils.data.DataLoader(imagenette_data_set, batch_size=batch_size,
                                              shuffle=True)

    dataiter = iter(trainloader)
    print('Done loading datset')

    return dataiter


def get_data_iter_imagewoof(batch_size):

    print('Loading dataset')


    annotations_imagewoof_df = pd.read_csv(Parameters.ANNOTATIONS_IMAGEWOOF)
    annotations_imagewoof_df = process_annotations(annotations_imagewoof_df)
    imagenette_data_set = CustomImageDataset(Parameters.DIR_IMAGEWOOF, annotations_imagewoof_df, transform=transform)
    trainloader = torch.utils.data.DataLoader(imagenette_data_set, batch_size=batch_size,
                                              shuffle=True)

    dataiter = iter(trainloader)

    print('Done loading datset')




    return dataiter

# print(image)
# print(category)







