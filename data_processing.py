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

from cam_customized import CamManager
from mapping import layer_idx_to_model_layer_idx
from process_annotations import DatasetManager
import process_annotations
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import shutil
import os
from tqdm import tqdm
import sys


#%%


def create_directory_structure(data_dir):
    print('Creating directory structure')
    images_dir = os.path.join(data_dir, 'images')
    create_directory(images_dir)

    # create a directory for every layer , 36 & 37, are input and output
    for layer_idx in range(38):

        layer_dir = os.path.join(data_dir, str(layer_idx))
        create_directory(layer_dir)

        if layer_idx == 37:
            top10_dir = os.path.join(layer_dir, 'top10')
            create_directory(top10_dir)
        if layer_idx == 36:
            images_dir = os.path.join(layer_dir, 'images')
            create_directory(images_dir)

        activations_dir = os.path.join(layer_dir, 'activations')
        create_directory(activations_dir)

        activations_images = os.path.join(activations_dir, 'images')
        create_directory(activations_images)

        activations_raw_data = os.path.join(activations_dir, 'raw_data')
        create_directory(activations_raw_data)

        activations_dir = os.path.join(layer_dir, 'explainability')
        create_directory(activations_dir)



# via chatgpt
def create_directory(path):
    # Specify the directory name
    directory_name = path

    # Create the directory
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists")
    except Exception as e:
        print(f"Error: {e}")

    pass


#create_directory_structure('assets/data/imagenette/700')



#%%

def float_to_str_with_dash(value, n_significant):
    # Format the float to n significant digits
    formatted = f"{value:.{n_significant}g}"  # 'g' ensures significant digits

    # Replace the decimal point with a dash
    formatted_with_dash = formatted.replace('.', '-')
    return formatted_with_dash

def calculate_score(data_2D):
    # calculate the entropy
    entropy = calculate_binned_entropy(data_2D)

    # calculate the magnitude, overall mean:
    #check if abs needed
    magnitude = abs(np.mean(data_2D))

    score = entropy * magnitude

    #convert the score



    return float_to_str_with_dash(entropy, 7), float_to_str_with_dash(magnitude,7), float_to_str_with_dash(score,7)





def calculate_scoring(data):
    scoring = []
    for channel in range(len(data)):
        data_2D = np.array(data[channel])
        scoring.append(calculate_score(data_2D))
    return scoring


# via chatgpt
def min_max_normalization_o(array):
    """Normalize a 2D array to the range [0, 1] using Min-Max scaling."""
    return (array - np.min(array)) / (np.max(array) - np.min(array))


# via chatgpt
def calculate_binned_entropy_o(data, bins=10):
    """
    Calculate the entropy of a 2D array using Min-Max normalization and binning.

    Parameters:
        data (numpy array): 2D array of activations.
        bins (int): Number of bins for discretization.

    Returns:
        float: Entropy value.
    """
    # Step 1: Normalize the data to [0, 1]
    normalized_data = min_max_normalization_o(data)

    # Step 2: Flatten the array for entropy calculation
    flattened = normalized_data.flatten()

    # Step 3: Create histogram bins and count occurrences
    hist, bin_edges = np.histogram(flattened, bins=bins, density=True)

    # Step 4: Normalize histogram to get probabilities
    probabilities = hist / hist.sum()

    # Step 5: Compute entropy using the Shannon formula
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-12))  # Avoid log(0) by adding a small value

    return entropy




def min_max_normalization(array):
    """Normalize a 2D array to the range [0, 1] using Min-Max scaling."""
    min_val = np.min(array)
    max_val = np.max(array)
    # Avoid division by zero when all values are identical
    if min_val == max_val:
        return np.zeros_like(array)  # Return a normalized array of all zeros
    return (array - min_val) / (max_val - min_val)


def calculate_binned_entropy(data, bins=10):
    """
    Calculate the entropy of a 2D array using Min-Max normalization and binning.

    Parameters:
        data (numpy array): 2D array of activations.
        bins (int): Number of bins for discretization.

    Returns:
        float: Entropy value.
    """
    # Step 1: Normalize the data to [0, 1]
    normalized_data = min_max_normalization(data)

    # Step 2: Flatten the array for entropy calculation
    flattened = normalized_data.flatten()

    # Step 3: Create histogram bins and count occurrences
    hist, bin_edges = np.histogram(flattened, bins=bins, density=True)

    # Step 4: Normalize histogram to get probabilities
    probabilities = hist / hist.sum()

    # Step 5: Handle degenerate cases (e.g., all data in one bin)
    if np.all(probabilities == 0) or np.count_nonzero(probabilities) == 1:
        return 0.0  # Entropy is zero when there's no uncertainty

    # Step 6: Compute entropy using the Shannon formula
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-12))  # Avoid log(0) by adding a small value

    return entropy



#via chatgpt
def float_to_int_limited_digits(value, max_digits):
    # Ensure value is positive (handle separately if negatives are needed)
    abs_value = abs(value)

    if abs_value == 0:
        return 0

    # Find the magnitude of the number (order of 10)
    magnitude = int(math.floor(math.log10(abs_value)))

    # Scale the value to bring the most significant digits into the integer part
    scaled_value = abs_value / (10**magnitude)  # Normalize to [1, 10)

    # Retain only the most significant digits
    result = scaled_value * (10**(max_digits - 1))  # Scale to max_digits
    result_int = int(round(result))  # Round to nearest integer

    # Return the result
    return result_int




def save_activation_to_image(data, data_dir, layer_idx, uid, scoring):
    for channel in range(len(data)):
        entropy = scoring[channel][0]
        magnitude = scoring[channel][1]
        score = scoring[channel][2]

        activation = data[channel]

        activation_np = np.array(activation)


        denominator = np.max(activation_np) - np.min(activation_np)
        if denominator == 0:
            #print(f'BONJOUUR: {channel} ,  {layer_idx}')
            normalized_activation_np = np.zeros_like(activation_np)
        else:
            normalized_activation_np = 1 * (activation_np - np.min(activation_np)) / denominator
        #normalized_activation_np = normalized_activation_np.astype(np.uint8)

        cmap = plt.cm.plasma  # You can choose other colormaps like 'plasma', 'inferno', etc.
        rgb_image = cmap(normalized_activation_np)

        denominator = (np.max(rgb_image) - np.min(rgb_image))
        if denominator == 0:
            normalized_rgb_image = np.zeros_like(rgb_image)
        else:
            normalized_rgb_image = 255 * (rgb_image - np.min(rgb_image)) / denominator

        normalized_rgb_image = normalized_rgb_image.astype(np.uint8)
        normalized_rgb_image = normalized_rgb_image[:, :, :3]

        # The result is an RGBA image (last channel is alpha), so remove the alpha channel
        # rgb_image = (normalized_array[:, :, :3]).astype(np.uint8)
        #plt.imsave(path, normalized_activation_np, cmap='plasma', interpolation='bilinear')

        # Save the image using Pillow
        image = Image.fromarray(normalized_rgb_image)
        path = os.path.join(data_dir,
                            f'{layer_idx}/activations/images/{layer_idx}_{uid}_{channel}_{entropy}_{magnitude}_{score}.png')
        image.save(path)
        print(f'    saved: {path}')

    pass


def save_activation_to_array(data, data_dir, layer_idx, uid, scoring):
    for channel in range(len(data)):
        entropy = scoring[channel][0]
        magnitude = scoring[channel][1]
        score = scoring[channel][2]

        activation = data[channel]
        path = os.path.join(data_dir,
                            f'{layer_idx}/activations/raw_data/{layer_idx}_{uid}_{channel}_{entropy}_{magnitude}_{score}.npy')
        np.save(path, activation)
        #print(f'    saved: {path}')
    pass



def save_image_raw_array(img, path):
    np.save(path, img)


#%%

def process_data():


    N_SAMPLES = 100


    data_dir = f'assets/data/imagewoof/{N_SAMPLES}'
    create_directory_structure(data_dir)

    dataset_manager = DatasetManager()
    cam = CamManager()

    uids = []
    labels = []
    label_ids = []
    categories = []
    original_img_paths = []
    img_paths = []
    correct_predictions = []

    #use for testing

    save_activations = False
    use_test_sample = False
    t_uid = 5259
    t_label = 'n03888257'
    t_label_id = 701
    t_category = 'parachute'
    t_img_path = 'datasets/imagenette2-320/train/n03888257/n03888257_22484.JPEG'

    dataiter = process_annotations.get_data_iter_imagenette(1)
    #dataiter = process_annotations.get_data_iter_imagewoof(1)





    print('Loading VGG16 model')

    weights = VGG16_Weights.DEFAULT
    model = vgg16(weights=weights)
    model.eval()



    for sample_id in tqdm(range(0, N_SAMPLES), desc="Sample progress", position=0, file=sys.stdout):

        #
        # Step 1: Initialize the sample
        #
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')
        print(f'Fetching next sample: {sample_id}/{N_SAMPLES}')

        image, label, label_id, category, uid, img_path = next(dataiter)

        # extract to correct format
        image_input = image[0].unsqueeze(0)
        label = label[0]
        label_id = label_id[0].item()
        category = category[0]
        uid = uid[0].item()
        img_path = img_path[0]


        if use_test_sample:
            label, label_id, category, uid, img_path = t_label, t_label_id, t_category, t_uid, t_img_path
            image, label, label_id, category, uid, img_path = dataset_manager.fetch_image(label, label_id, category, uid, img_path)

            image_input = image.unsqueeze(0)
            image = image.unsqueeze(0)
            #save_image_raw_array(image, os.path.join(data_dir, 'test_image.npy'))


        #track sample
        uids.append(uid)
        labels.append(label)
        label_ids.append(label_id)
        categories.append(category)
        original_img_paths.append(img_path)
        img_paths.append(os.path.join(data_dir, 'images', f'{uid}.png'))



        tqdm.write(str(img_path))
        tqdm.write(f'Sample {uid} fetched')
        # sample_dir = os.path.join(data_dir, str(uid))

        # tqdm.write(label_id)
        # tqdm.write(image_input)


        #
        # Step 2: save input layer data
        #
        tqdm.write('Computing input layer data')
        # save orginal image
        shutil.copy2(img_path, os.path.join(data_dir, f'images/{uid}.png'))

        # save full image, normalized passed into the network
        image_path = os.path.join(data_dir, f'36/images/{uid}.png')
        save_image(image, image_path)

        # calculate score, for each channel
        scoring = calculate_scoring(image[0])

        # save activations rgb
        save_activation_to_image(image[0], data_dir, 36, uid, scoring)
        # save activation raw data
        save_activation_to_array(image[0], data_dir, 36, uid, scoring)

        tqdm.write('Done computing input layer data')


        #
        # Step 3: load model
        #

        #tqdm.write('Loading VGG16 model')


        #weights = VGG16_Weights.DEFAULT
        #model = vgg16(weights=weights)
        #model.eval()

        # tqdm.write(dict(model.named_modules()))

        # Initialize the inference transforms
        #preprocess = weights.transforms()


        #
        # Step 4: Register hooks
        #

        tqdm.write('Registering hooks for VGG16 model')


        activations = {}
        hooks = []

        def hook_fn(module, input, output, layer_idx):
            tqdm.write(f"Hook triggered for: {layer_idx}, {module.__class__.__name__}")
            activations[layer_idx] = output

        if save_activations:
            # register conv part
            for layer_idx in range(31):
                layer = model.features[layer_idx_to_model_layer_idx[layer_idx]]
                layer.register_forward_hook(
                    lambda module, input, output, layer_idx_hook=layer_idx: hook_fn(module, input, output, layer_idx_hook))

        # register neuron part
        for layer_idx in range(31, 36):
            layer = model.classifier[layer_idx_to_model_layer_idx[layer_idx]]
            hook = layer.register_forward_hook(
                lambda module, input, output, layer_idx_hook=layer_idx: hook_fn(module, input, output, layer_idx_hook))
            hooks.append(hook)


        #
        # Step 5 run inference for current image
        #

        tqdm.write(f'Running inference for sample {uid}')

        with torch.no_grad():
            out = model(image_input)

        #
        # Step 6 classify image, save top 10, save target 37
        #
        tqdm.write(f'Classifying image, top10, output activation {uid}')

        output_top10_dir = os.path.join(data_dir, str(37) + '/top10')
        probabilities = torch.nn.functional.softmax(out[0], dim=0)
        top10_prob, top10_catid = torch.topk(probabilities, 10)
        top10_categories = [dataset_manager.mapping_label_id_to_category[cat_id.item()] for cat_id in top10_catid]
        top10_labels = [dataset_manager.mapping_category_to_label[category] for category in top10_categories]
        top10 = {
            'uid': [uid] * 10,
            'gt_label_id': [label_id] * 10,
            'label_id': top10_catid,
            'category': top10_categories,
            'label': top10_labels,
            'prob': top10_prob
        }

        tqdm.write(str(top10))

        top10_path = os.path.join(output_top10_dir, f'top10_{uid}.csv')
        top10_df = pd.DataFrame(data=top10)
        top10_df.to_csv(top10_path)


        #Save correct prediction
        correct_prediction = label_id == top10_catid[0].item()
        correct_predictions.append(correct_prediction)

        # Save the output activation raw values

        raw_activation = {
            'uid': [uid] * 1000,
            'idx': list(range(1000)),
            'value': probabilities
        }

        output_raw_activation_path = os.path.join(data_dir, str(37) + f'/activations/raw_data/37_{uid}.csv')
        raw_activation_df = pd.DataFrame(data=raw_activation)
        raw_activation_df.to_csv(output_raw_activation_path)


        if save_activations:

            #
            # Step 7 save  activation conv data
            #


            tqdm.write(f'Computing 2D Conv activations')


            for layer_idx in range(0, 31):

                #calcualte the score for the activation

                activation = activations[layer_idx][0]

                # calculate score, for each channel
                scoring = calculate_scoring(activation)


                # save activations rgb
                save_activation_to_image(activation, data_dir, layer_idx, uid, scoring)
                # save activation raw data
                save_activation_to_array(activation, data_dir, layer_idx, uid, scoring)

        #
        # Step 8 save activation classification data
        #

        tqdm.write(f'Computing neuron activations')


        for layer_idx in range(31, 36):
            activation = activations[layer_idx][0]
            raw_activation = {
                'uid': [uid] * len(activation),
                'idx': list(range(len(activation))),
                'value': activation
            }

            neuron_layer_activation_path = os.path.join(data_dir, f'{layer_idx}/activations/raw_data/{layer_idx}_{uid}.csv')
            raw_activation_df = pd.DataFrame(data=raw_activation)
            raw_activation_df.to_csv(neuron_layer_activation_path)



        #
        # Step 9 save explainability
        #

        tqdm.write(f'Computing grad-cam and gb for conv 29')

        for layer_idx in range(0, 1):
            layer_idx = 29
            cam_dir = os.path.join(data_dir, str(layer_idx), 'explainability')
            cam.run_cam(img_path, cam_dir, layer_idx, uid)
            tqdm.write(f'    done layer {layer_idx}')
            pass

        # Remove all hooks
        for hook in hooks:
            hook.remove()





    #
    # Step 10 save sample in index
    #

    data = {
        'uid': uids,
        'label': labels,
        'label_id': label_ids,
        'category': categories,
        'original_img_path': original_img_paths,
        'img_path': img_paths,
        'correct_prediction': correct_predictions
    }

    samples_df = pd.DataFrame(data=data)
    samples_df.to_csv(os.path.join(data_dir, 'samples.csv'))



if __name__ == '__main__':
    process_data()


