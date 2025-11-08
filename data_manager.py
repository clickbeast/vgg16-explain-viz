from dataclasses import dataclass
import math

import torch
import torchvision
import torchvision.transforms as transforms
import pandas as pd
from joblib.externals.cloudpickle import instance
from pandas.core.interchange.dataframe_protocol import DataFrame
from scipy.interpolate import insert
from torchvision.models import VGG16_Weights, vgg16
from torchvision.utils import save_image
import torch
import torchvision
from openTSNE import TSNE
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
import os
import re

from cam_customized import CamManager
from data_processing import calculate_scoring, save_activation_to_image, save_activation_to_array
from dimensionality_reduction import fetch_sample
from mapping import layer_idx_to_model_layer_idx, layer_idx_list_full
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
from glob import glob
from typing import Optional


#%%


@dataclass
class Instance:
    dataset: str
    n_samples: int
    layer_idx: int
    perplexity: int
    method: str
    number_of_samples_list = [100, 1000, 7000]
    perplexities_list = [10, 30, 90]
    dataset_list = ['imagenette', 'imagewoof']
    layer_idx_list = layer_idx_list_full
    n_layers = 37

    def get_data_dir(self):

        # Default the 7000 samples to 1000 for imagewoof
        if self.dataset == 'imagewoof' and self.n_samples == 7000:
            return os.path.join('assets', 'data', self.dataset, str(1000))

        return os.path.join('assets', 'data', self.dataset, str(self.n_samples))


    def get_data_dir_from_argument(self, argument, n_samples):

        # Default the 7000 samples to 1000 for imagewoof
        if argument == 'imagewoof' and n_samples == 7000:
            return os.path.join('assets', 'data', argument, str(1000))

        return os.path.join('assets', 'data', argument, str(n_samples))


        pass

    def __hash__(self):
        # Return a tuple-based hash that uses the fields we want to compare

        if self.method == 'pca':
            return hash((self.dataset, self.n_samples, self.layer_idx, self.method))


        return hash((self.dataset, self.n_samples, self.layer_idx, self.perplexity, self.method))

    def __eq__(self, other):
        if isinstance(other, Instance):

            # When the dataset is 'pca', ignore perplexity for comparison
            if self.method == 'pca' and other.method == 'pca':
                return (self.dataset, self.n_samples, self.layer_idx, self.method) == (
                    other.dataset, other.n_samples, other.layer_idx, other.method)

            # Compare only the fields we care about for equality
            return (self.dataset, self.n_samples, self.layer_idx, self.perplexity, self.method) == (
                other.dataset, other.n_samples, other.layer_idx, other.perplexity, other.method)
        return False


@dataclass
class Sample:
    idx: int
    uid: int
    label_id: int
    label: str
    category: str
    img_path: str
    correct_prediction: bool


@dataclass
class Activation:
    layer_idx: int
    uid: int
    channel: int
    entropy: float
    magnitude: float
    score: float
    filename_img: str
    filepath_img: str
    filename_raw: str
    filepath_raw: str
    norm_score: Optional[int]


#%%

#
#  Loading of the dimensionality reduction data
#


# Preload all the data, normally you have enought RAM for this.
def load_dataframe_from_csv(filename):
    # read csv from file
    df = pd.read_csv(filename)
    df.sort_values(by='category')
    #df["label"] = df["label"].astype(str)
    df.rename(columns={'Unnamed: 0': 'original_key'}, inplace=True)

    return df


def load_dimensionality_reduction_dataframes(instance: Instance):
    data_frames_out = {}
    for dataset in instance.dataset_list:
        for number_of_samples in instance.number_of_samples_list:
            for layer_idx in instance.layer_idx_list:
                # load tsne dataframes
                for perplexity in instance.perplexities_list:
                    # read csv from file

                    tsne_filename = f'tsne_{layer_idx}_{perplexity}.csv'
                    tsne_path = os.path.join(instance.get_data_dir_from_argument(dataset, number_of_samples), str(layer_idx), tsne_filename)
                    df = load_dataframe_from_csv(tsne_path)
                    key_instance_tsne = Instance(
                        dataset,
                        number_of_samples,
                        layer_idx,
                        perplexity,
                        'tsne'
                    )

                    data_frames_out[key_instance_tsne] = df

                pca_filename = f'pca_{layer_idx}.csv'
                pca_path = os.path.join(instance.get_data_dir_from_argument(dataset, number_of_samples), str(layer_idx), pca_filename)

                key_instance_pca = Instance(
                    dataset,
                    number_of_samples,
                    layer_idx,
                    -1,
                    'pca'
                )

                df = load_dataframe_from_csv(pca_path)
                data_frames_out[key_instance_pca] = df

    return data_frames_out


#%%

#via chatgpt
def find_files_with_params(directory, param1, param2):
    print(f'finding files: {param1}, {param2}')

    """
    Looks for a file in the specified directory that matches the pattern
    'param1_param2_anything.png'.

    Parameters:
        directory (str): The directory to search in.
        param1 (str): The first parameter in the filename.
        param2 (str): The second parameter in the filename.

    Returns:
        tuple: (bool, str) - (True, filename) if the file exists, otherwise (False, None).
    """
    # Create the search pattern
    pattern = os.path.join(directory, f"{param1}_{param2}_*.png")

    # Find all matching files
    matches = glob(pattern)

    if matches:
        # Return True with the first matching file
        return True, matches
    else:
        # No match found
        return False, []


def find_files_with_three_params(directory, param1, param2, param3):
    print(f'finding files: {param1}, {param2}, {param3}')

    """
    Looks for a file in the specified directory that matches the pattern
    'param1_param2_anything.png'.

    Parameters:
        directory (str): The directory to search in.
        param1 (str): The first parameter in the filename.
        param2 (str): The second parameter in the filename.

    Returns:
        tuple: (bool, str) - (True, filename) if the file exists, otherwise (False, None).
    """
    # Create the search pattern
    pattern = os.path.join(directory, f"{param1}_{param2}_{param3}_*.npy")

    # Find all matching files
    matches = glob(pattern)

    if matches:
        # Return True with the first matching file
        return True, matches
    else:
        # No match found
        return False, []


def compute_activations(sample: Sample, instance: Instance):
    print('computing activations')

    layer_idx = instance.layer_idx
    data_dir = instance.get_data_dir()

    dataset_manager = DatasetManager()

    print('loading VGG16')
    weights = VGG16_Weights.DEFAULT
    model = vgg16(weights=weights)
    model.eval()

    activations_hook_storage = {}
    print('done')


    def hook_fn(module, input, output, layer_idx):
        print(f"Hook triggered for: {layer_idx}, {module.__class__.__name__}")
        activations_hook_storage[layer_idx] = output

    def register_hook(layer_idx):
        # register conv part
        layer = model.features[layer_idx_to_model_layer_idx[layer_idx]]
        handle = layer.register_forward_hook(
            lambda module, input, output, layer_idx_hook=layer_idx: hook_fn(module, input, output, layer_idx_hook))
        return handle

    img = fetch_model_img(sample, dataset_manager)

    handle = register_hook(layer_idx)

    with torch.no_grad():
        out = model(img)

    activation = activations_hook_storage[layer_idx][0]

    handle.remove()

    print('saving activation')

    # calculate score, for each channel
    scoring = calculate_scoring(activation)

    # save activations rgb
    save_activation_to_image(activation, data_dir, layer_idx, sample.uid, scoring)
    save_activation_to_array(activation, data_dir, layer_idx, sample.uid, scoring)



    pass


def fetch_model_img(sample: Sample, dataset_manager):
    image, label, label_id, category, uid, img_path = dataset_manager.fetch_image(sample.label,
                                                                                  sample.label_id,
                                                                                  sample.category,
                                                                                  sample.uid,
                                                                                  sample.img_path)
    image_input = image.unsqueeze(0)


    return image_input

def get_activations(instance: Instance, sample: Sample, sort='id') -> [Activation]:
    print('getting activations')
    activation_dir = os.path.join(instance.get_data_dir(), str(instance.layer_idx), 'activations', 'images')
    found, activation_file_names = find_files_with_params(activation_dir, str(instance.layer_idx), str(sample.uid))
    activations = []

    for filename in activation_file_names:
        activation = parse_filename_activation(filename, instance, sample)
        activations.append(activation)
    activations = compute_norm_score(activations)

    if sort == 'id':
        activations.sort(key=lambda x: x.channel)
    else:
        activations.sort(key=lambda x: x.norm_score)


    return activations


def padded_2D_array(flat_array, n_elements_per_row):
    flat_array = flat_array.astype(float)

    # Compute the total number of rows needed
    num_rows = int(np.ceil(len(flat_array) / n_elements_per_row))

    # Create a padded array to make the size divisible by n_elements_per_row
    padded_size = num_rows * n_elements_per_row
    padded_z_flat = np.pad(flat_array, (0, padded_size - len(flat_array)), constant_values=np.nan)

    # Reshape the padded array into a 2D array
    z_2d = padded_z_flat.reshape(num_rows, n_elements_per_row)

    return z_2d


def get_neuron_activations(instance: Instance, sample: Sample):
    print('getting neuron activation')
    file_name = f'{instance.layer_idx}_{sample.uid}.csv'
    file_path = os.path.join(instance.get_data_dir(), str(instance.layer_idx), 'activations', 'raw_data', file_name)

    df = pd.read_csv(file_path)
    value_array = df["value"].to_numpy()

    return value_array


def is_activation_available(instance: Instance, sample: Sample):
    #base case
    if instance.layer_idx > 30:
        return True

    activation_dir = os.path.join(instance.get_data_dir(), str(instance.layer_idx), 'activations', 'images')
    found, filenames = find_files_with_params(activation_dir, str(instance.layer_idx), str(sample.uid))

    #check if the png are there
    return found


def is_neuron_activation(instance: Instance):
    if instance.layer_idx > 30 and instance.layer_idx != 36:
        return True


def get_activation(instance: Instance, sample: Sample, channel) -> Activation:

    print('getting individual activation')
    print(instance)
    print(sample)

    activation_dir = os.path.join(instance.get_data_dir(), str(instance.layer_idx), 'activations', 'raw_data')
    found, filenames = find_files_with_three_params(activation_dir, instance.layer_idx, sample.uid, channel)
    print(found)
    print(filenames)

    activation = parse_filename_activation(filenames[0], instance, sample)

    return activation


def get_activation_detail(instance: Instance, sample: Sample, channel):
    loaded_array = np.load(get_activation(instance, sample, channel).filepath_raw)
    return loaded_array


#%%


def convert_to_float(number, frac):
    """Convert number and fraction to a float."""
    return float(f"{number}.{frac}")

def convert_to_float_2(number):
    """Convert number and fraction to a float."""
    return float(number.replace('-', '.', 1))


def parse_filename_activation(filename, instance: Instance, sample: Sample):
    """Parse the filename to extract parameters and return the result dictionary."""

    print(f'parsing: {filename}')

    filename = os.path.basename(filename)


    #pattern = r"(\d+)_(\d+)_(\d+)_([0-9]+)-([0-9]+)_([0-9]+)-([0-9]+)_([0-9]+)-([0-9]+)\.(?:png|npy)"

    pattern = (
        r"(\d+)_(\d+)_(\d+)_([0-9]+(?:-[0-9]+)?(?:e[+-]?[0-9]+)?)_([0-9]+(?:-[0-9]+)?(?:e[+-]?[0-9]+)?)_([0-9]+(?:-["
        r"0-9]+)?(?:e[+-]?[0-9]+)?)\.(?:png|npy)")

    match = re.match(pattern, filename)

    if not match:
        raise ValueError("Filename does not match the expected structure.")

    param1, param2, param3, number1, number2, number3 = match.groups()

    activation_img_dir = os.path.join(instance.get_data_dir(), str(instance.layer_idx), 'activations', 'images')
    activation_raw_dir = os.path.join(instance.get_data_dir(), str(instance.layer_idx), 'activations', 'raw_data')

    filename_raw = os.path.splitext(filename)[0] + ".npy"

    result = {
        "layer_idx": int(param1),
        "uid": int(param2),
        "channel": int(param3),
        "entropy": convert_to_float_2(number1),
        "magnitude": convert_to_float_2(number2),
        "score": convert_to_float_2(number3),
        'filename_img': filename,
        'filepath_img': os.path.join(activation_img_dir, filename),
        'filename_raw': filename_raw,
        'filepath_raw': os.path.join(activation_raw_dir, filename),
        "norm_score": None,  # Optional, may be None if not available
    }

    # Create an instance of Activation using the values from the result dictionary
    activation_object = Activation(
        layer_idx=result['layer_idx'],
        uid=result['uid'],
        channel=result['channel'],
        entropy=result['entropy'],
        magnitude=result['magnitude'],
        score=result['score'],
        filename_img=result['filename_img'],
        filepath_img=result['filepath_img'],
        filename_raw=result['filename_raw'],
        filepath_raw=result['filepath_raw'],
        norm_score=result.get('norm_score')  # Get the norm_score if available, otherwise None
    )

    print(activation_object)

    return activation_object


def compute_norm_score(activations: list[Activation]) -> list[Activation]:
    if not activations:
        return activations

    min_score = min(a.score for a in activations)
    max_score = max(a.score for a in activations)

    if max_score == min_score:
        for a in activations:
            a.norm_score = 50
        return activations

    scale = 99 / (max_score - min_score)
    for a in activations:
        a.norm_score = int(1 + (a.score - min_score) * scale)

    return activations


def is_instance_changed_via_input(trigger):
    if trigger == 'dataset-selection' or trigger == 'number-of-samples' or trigger == 'dimensionality-method' or trigger == 'perplexity' or trigger == 'result':
        return True
    return False

#if the activations take up to much space, we could do subsampling techniqus where we conly take a general idea
#SOLUTUON FIRST DO DIMENSIONALITY REDUCTION ON THE LAYER ACTVIATION REDUCE TIS
