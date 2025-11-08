import math

import torch
import torchvision
import torchvision.transforms as transforms
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame
from torchvision.models import VGG16_Weights, vgg16
from torchvision.utils import save_image
import torch
import torchvision
from openTSNE import TSNE
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
import os
import sys
from cam_customized import CamManager
from mapping import layer_idx_to_model_layer_idx, dimensionality_reduction_layer_mapping, layer_idx_to_layer_type, \
    debug_dimensionality_reduction_layer_mapping, dimensionality_reduction_layer_mapping_extra_copies, \
    dimensionality_reduction_layer_mapping_reduced
from process_annotations import DatasetManager
import process_annotations
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import shutil
import os
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
from tqdm import tqdm
import torch.nn.functional as F

#%%


def save_embedding_data(embedding,samples, path):
    # Create data
    x = embedding[:, 0]
    y = embedding[:, 1]
    df = pd.DataFrame(data={
        'uid':samples['uid'],
        'x': x,
        'y': y,
        'label': samples['label'],
        'label_id': samples['label_id'],
        'category': samples['category'],
        'original_img_path': samples['original_img_path'],
        'img_path': samples['img_path'],
        'correct_prediction': samples['correct_prediction'],
    })

    #df = df.sort_values(by=['label'], ascending=True)
    #df["label"] = df["label"].astype(str)

    df.to_csv(path)


def fetch_sample(row, dataset_manager):


    idx, uid, label, label_id, category, original_img_path, img_path, correct_prediction = row

    label = label[0]
    label_id = label_id
    category = category
    uid = uid
    img_path = original_img_path


    image, label, label_id, category, uid, img_path = dataset_manager.fetch_image(label, label_id, category, uid,
                                                                                  img_path)
    image_input = image.unsqueeze(0)

    return image_input



def get_downsample_resolution(layer_idx):
    o_size = layer_idx_to_layer_type[layer_idx][1][0]

    size = int(o_size / 4)

    if o_size == 14:
        size = 4
    if o_size == 7:
        size = 2

    return size

def get_downsample_resolution_strong(layer_idx):
    o_size = layer_idx_to_layer_type[layer_idx][1][0]

    size = int(o_size / 8)

    if o_size == 28:
        size = 7
    if o_size == 14:
        size = 4
    if o_size == 7:
        size = 2

    return size




def spatial_downsample(activation, layer_idx):

    #Step 1 if
    if layer_idx < 31 or layer_idx == 36:
        size = get_downsample_resolution(layer_idx)
        activation = F.adaptive_avg_pool2d(activation, output_size=(size, size))

    return activation

def spatial_downsample_strong(activation, layer_idx):

    #Step 1 if
    if layer_idx < 31 or layer_idx == 36:
        size = get_downsample_resolution_strong(layer_idx)
        activation = F.adaptive_avg_pool2d(activation, output_size=(size, size))

    return activation



#%%


def run_dimensionality_reduction_for_model():


    N_samples = 100



    N_layers = 37
    perplexities = [10, 30, 90]

    data_dir = f'assets/data/imagewoof/{N_samples}'

    dataset_manager = DatasetManager()
    #cam = CamManager()
    #dataiter = process_annotations.get_data_iter_imagenette(1)

    samples_df = pd.read_csv(os.path.join(data_dir, 'samples.csv'))

    #
    # Step 3: load model
    #

    print('Loading VGG16 model')

    weights = VGG16_Weights.DEFAULT
    model = vgg16(weights=weights)
    model.eval()

    activations_hook_storage = {}

    def hook_fn(module, input, output, layer_idx):
        tqdm.write(f"Hook triggered for: {layer_idx}, {module.__class__.__name__}")
        activations_hook_storage[layer_idx] = output

    def register_hook(layer_idx):

        if layer_idx < 31:
            # register conv part
            layer = model.features[layer_idx_to_model_layer_idx[layer_idx]]

            handle = layer.register_forward_hook(
                lambda module, input, output, layer_idx_hook=layer_idx: hook_fn(module, input, output, layer_idx_hook))

        else:
            # register conv part
            layer = model.classifier[layer_idx_to_model_layer_idx[layer_idx]]

            handle = layer.register_forward_hook(
                lambda module, input, output, layer_idx_hook=layer_idx: hook_fn(module, input, output, layer_idx_hook))

        #register part

        return handle


    for layer_idx, layer_idx_copy in tqdm(dimensionality_reduction_layer_mapping, desc="Layer progress", position=0, file=sys.stdout):

        tqdm.write('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
        tqdm.write(f'RUNNING DIMENSIONALITY REDUCTION FOR LAYER: {layer_idx}')

        #
        # Collect activations
        #

        activations = []

        for sample_id, row in enumerate(samples_df.itertuples(index=False, name=None)):
            tqdm.write(str(row))
            idx, uid, label, label_id, category, original_img_path, img_path, correct_prediction = row

            img = fetch_sample(row, dataset_manager)

            if layer_idx == 36:
                #shouold we convert here to grayscale?
                activations.append(spatial_downsample(img, layer_idx).flatten())
                continue

            if layer_idx == 37:
                #shouold we convert here to grayscale?
                #read from the prob
                filename = f'37_{uid}.csv'
                path = os.path.join(data_dir, str(37), 'activations', 'raw_data', filename)
                df = pd.read_csv(path)
                activations.append(df['value'].to_numpy())
                continue

            handle = register_hook(layer_idx)

            with torch.no_grad():
                out = model(img)

            activation = activations_hook_storage[layer_idx]

            activations.append(spatial_downsample(activation, layer_idx).flatten())
            handle.remove()

            pass

        activations = np.array(activations)

        #Pre reduce dimensionality
        tqdm.write('Pre reducing dimensionality')
        pca = PCA(n_components=0.90)
        if layer_idx == 34 or layer_idx == 35 or layer_idx == 36 or layer_idx == 37:
            pca = PCA(n_components=0.96)
        #disable for small datasets

        #if layer_idx == 37:
        #   pca = PCA(n_components=0.99)
        #pca_embedding = pca.fit_transform(activations)
        #activations = pca_embedding

        tqdm.write(f'Performing reduction for layer {layer_idx} with dimensionality {activations.shape}')

        #
        # Perform tsne
        #

        for perplexity in perplexities:

            # run TSNE
            tsne = TSNE(
                perplexity=perplexity,
                metric="euclidean",
                n_jobs=8,
                random_state=42,
                verbose=True,
            )

            embedding_id = f'tsne_{layer_idx}_{perplexity}.csv'
            path = os.path.join(data_dir, str(layer_idx), embedding_id)
            TSNE_embedding = tsne.fit(activations)
            save_embedding_data(TSNE_embedding,samples_df,path)


            if layer_idx_copy != -1:
                #save also for previous layer, same activations
                embedding_id = f'tsne_{layer_idx_copy}_{perplexity}.csv'
                path = os.path.join(data_dir, str(layer_idx_copy), embedding_id)
                save_embedding_data(TSNE_embedding,samples_df,path)



        #
        # Perform pca
        #

        pca = PCA(n_components=2)
        pca_embedding = pca.fit_transform(activations)
        embedding_id = f'pca_{layer_idx}.csv'
        path = os.path.join(data_dir, str(layer_idx), embedding_id)
        save_embedding_data(pca_embedding, samples_df, path)

        if layer_idx_copy != -1:
            # save also for previous layer, same activations
            embedding_id = f'pca_{layer_idx_copy}.csv'
            path = os.path.join(data_dir, str(layer_idx_copy), embedding_id)
            save_embedding_data(pca_embedding, samples_df, path)




    pass





def run_dimensionality_reduction_for_model_reduced():


    N_samples = 7000



    N_layers = 37
    perplexities = [10, 30, 90]

    data_dir = f'assets/data/imagenette/{N_samples}'

    dataset_manager = DatasetManager()
    #cam = CamManager()
    #dataiter = process_annotations.get_data_iter_imagenette(1)

    samples_df = pd.read_csv(os.path.join(data_dir, 'samples.csv'))

    #
    # Step 3: load model
    #

    print('Loading VGG16 model')

    weights = VGG16_Weights.DEFAULT
    model = vgg16(weights=weights)
    model.eval()

    activations_hook_storage = {}

    def hook_fn(module, input, output, layer_idx):
        tqdm.write(f"Hook triggered for: {layer_idx}, {module.__class__.__name__}")
        activations_hook_storage[layer_idx] = output

    def register_hook(layer_idx):

        if layer_idx < 31:
            # register conv part
            layer = model.features[layer_idx_to_model_layer_idx[layer_idx]]

            handle = layer.register_forward_hook(
                lambda module, input, output, layer_idx_hook=layer_idx: hook_fn(module, input, output, layer_idx_hook))

        else:
            # register conv part
            layer = model.classifier[layer_idx_to_model_layer_idx[layer_idx]]

            handle = layer.register_forward_hook(
                lambda module, input, output, layer_idx_hook=layer_idx: hook_fn(module, input, output, layer_idx_hook))

        #register part

        return handle


    for layer_idx, layer_idx_copy in tqdm(dimensionality_reduction_layer_mapping_reduced, desc="Layer progress", position=0, file=sys.stdout):

        tqdm.write('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
        tqdm.write(f'RUNNING DIMENSIONALITY REDUCTION FOR LAYER: {layer_idx}')

        #
        # Collect activations
        #

        activations = []

        for sample_id, row in enumerate(samples_df.itertuples(index=False, name=None)):
            tqdm.write(str(row))
            idx, uid, label, label_id, category, original_img_path, img_path, correct_prediction = row

            img = fetch_sample(row, dataset_manager)

            if layer_idx == 36:
                #shouold we convert here to grayscale?
                activations.append(spatial_downsample_strong(img, layer_idx).flatten())
                continue

            if layer_idx == 37:
                #shouold we convert here to grayscale?
                #read from the prob
                filename = f'37_{uid}.csv'
                path = os.path.join(data_dir, str(37), 'activations', 'raw_data', filename)
                df = pd.read_csv(path)
                activations.append(df['value'].to_numpy())
                continue

            handle = register_hook(layer_idx)

            with torch.no_grad():
                out = model(img)

            activation = activations_hook_storage[layer_idx]

            activations.append(spatial_downsample_strong(activation, layer_idx).flatten())
            handle.remove()

            pass

        activations = np.array(activations)

        #Pre reduce dimensionality
        tqdm.write('Pre reducing dimensionality')
        pca = PCA(n_components=0.90)
        if layer_idx == 34 or layer_idx == 35 or layer_idx == 36 or layer_idx == 37:
            pca = PCA(n_components=0.96)

        #if layer_idx == 37:
        #   pca = PCA(n_components=0.99)
        pca_embedding = pca.fit_transform(activations)
        activations = pca_embedding

        tqdm.write(f'Performing reduction for layer {layer_idx} with dimensionality {activations.shape}')

        #
        # Perform tsne
        #

        # run TSNE
        tsne = TSNE(
            perplexity=47,
            metric="euclidean",
            n_jobs=8,
            random_state=42,
            verbose=True,
        )

        TSNE_embedding = tsne.fit(activations)

        for perplexity in perplexities:

            embedding_id = f'tsne_{layer_idx}_{perplexity}.csv'
            path = os.path.join(data_dir, str(layer_idx), embedding_id)
            save_embedding_data(TSNE_embedding,samples_df,path)


            if layer_idx_copy != -1:
                #save also for previous layer, same activations
                embedding_id = f'tsne_{layer_idx_copy}_{perplexity}.csv'
                path = os.path.join(data_dir, str(layer_idx_copy), embedding_id)
                save_embedding_data(TSNE_embedding,samples_df,path)


            if layer_idx in dimensionality_reduction_layer_mapping_extra_copies:
                # save also for previous layer, same activations
                for layer_id_to_copy in dimensionality_reduction_layer_mapping_extra_copies[layer_idx]:
                    embedding_id = f'tsne_{layer_id_to_copy}_{perplexity}.csv'
                    path = os.path.join(data_dir, str(layer_id_to_copy), embedding_id)
                    save_embedding_data(pca_embedding, samples_df, path)



        #
        # Perform pca
        #

        pca = PCA(n_components=2)
        pca_embedding = pca.fit_transform(activations)
        embedding_id = f'pca_{layer_idx}.csv'
        path = os.path.join(data_dir, str(layer_idx), embedding_id)
        save_embedding_data(pca_embedding, samples_df, path)

        if layer_idx_copy != -1:
            # save also for previous layer, same activations
            embedding_id = f'pca_{layer_idx_copy}.csv'
            path = os.path.join(data_dir, str(layer_idx_copy), embedding_id)
            save_embedding_data(pca_embedding, samples_df, path)

        if layer_idx in dimensionality_reduction_layer_mapping_extra_copies:
            # save also for previous layer, same activations
            for layer_id_to_copy in dimensionality_reduction_layer_mapping_extra_copies[layer_idx]:
                embedding_id = f'pca_{layer_id_to_copy}.csv'
                path = os.path.join(data_dir, str(layer_id_to_copy), embedding_id)
                save_embedding_data(pca_embedding, samples_df, path)

    pass







if __name__ == '__main__':
    #run_dimensionality_reduction_for_model()
    run_dimensionality_reduction_for_model_reduced()

def run_dimensionality_reduction_for_model_heavy():
    N_samples = 1000

    N_layers = 37
    perplexities = [10, 30, 90]

    data_dir = f'assets/data/imagenette/{N_samples}'

    dataset_manager = DatasetManager()
    # cam = CamManager()
    # dataiter = process_annotations.get_data_iter_imagenette(1)

    samples_df = pd.read_csv(os.path.join(data_dir, 'samples.csv'))

    #
    # Step 3: load model
    #

    print('Loading VGG16 model')

    weights = VGG16_Weights.DEFAULT
    model = vgg16(weights=weights)
    model.eval()

    activations_hook_storage = {}

    def hook_fn(module, input, output, layer_idx):
        tqdm.write(f"Hook triggered for: {layer_idx}, {module.__class__.__name__}")
        activations_hook_storage[layer_idx] = output

    def register_hook(layer_idx):
        # register conv part
        layer = model.features[layer_idx_to_model_layer_idx[layer_idx]]
        handle = layer.register_forward_hook(
            lambda module, input, output, layer_idx_hook=layer_idx: hook_fn(module, input, output, layer_idx_hook))
        return handle

    for layer_idx, layer_idx_copy in tqdm(dimensionality_reduction_layer_mapping, desc="Layer progress", position=0,
                                          file=sys.stdout):

        tqdm.write('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
        tqdm.write(f'RUNNING DIMENSIONALITY REDUCTION FOR LAYER: {layer_idx}')

        #
        # Collect activations
        #

        activations = []

        for sample_id, row in enumerate(samples_df.itertuples(index=False, name=None)):
            tqdm.write(str(row))
            idx, uid, label, label_id, category, original_img_path, img_path, correct_prediction = row

            img = fetch_sample(row, dataset_manager)

            if layer_idx == 36:
                # shouold we convert here to grayscale?
                activations.append(img.flatten())
                continue

            if layer_idx == 37:
                # shouold we convert here to grayscale?
                # read from the prob
                filename = f'37_{uid}.csv'
                path = os.path.join(data_dir, str(37), 'activations', 'raw_data', filename)
                df = pd.read_csv(path)
                activations.append(df['value'].to_numpy())
                continue

            handle = register_hook(layer_idx)

            with torch.no_grad():
                out = model(img)

            activation = activations_hook_storage[layer_idx][0].flatten()

            activations.append(activation)
            handle.remove()

            pass

        activations = np.array(activations)

        #
        # Perform tsne
        #

        for perplexity in perplexities:

            # run TSNE
            tsne = TSNE(
                perplexity=perplexity,
                metric="euclidean",
                n_jobs=8,
                random_state=42,
                verbose=False,
            )

            embedding_id = f'tsne_{layer_idx}_{perplexity}.csv'
            path = os.path.join(data_dir, str(layer_idx), embedding_id)
            TSNE_embedding = tsne.fit(activations)
            save_embedding_data(TSNE_embedding, samples_df, path)

            if layer_idx_copy != -1:
                # save also for previous layer, same activations
                embedding_id = f'tsne_{layer_idx_copy}_{perplexity}.csv'
                path = os.path.join(data_dir, str(layer_idx_copy), embedding_id)
                save_embedding_data(TSNE_embedding, samples_df, path)

        #
        # Perform pca
        #

        pca = PCA(n_components=2)
        pca_embedding = pca.fit_transform(activations)
        embedding_id = f'pca_{layer_idx}.csv'
        path = os.path.join(data_dir, str(layer_idx), embedding_id)
        save_embedding_data(pca_embedding, samples_df, path)

        if layer_idx_copy != -1:
            # save also for previous layer, same activations
            embedding_id = f'pca_{layer_idx_copy}.csv'
            path = os.path.join(data_dir, str(layer_idx_copy), embedding_id)
            save_embedding_data(pca_embedding, samples_df, path)

    pass
