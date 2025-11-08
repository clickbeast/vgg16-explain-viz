import torch
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


#%%


class ModelDataCollector:

    def __init__(self):
        super().__init__()







def save_activation():
    pass

def save_activation_values():
    pass
def save_activation_image():
    for channel in range(len(activations['features.1'][0])):
        activation_channel_0 = activations['features.1'][0][channel]

        activation_np = np.array(activation_channel_0, dtype=np.uint8)

        normalized_activation_np = 1000 * (activation_np - np.min(activation_np)) / (
                np.max(activation_np) - np.min(activation_np))
        normalized_activation_np = normalized_activation_np.astype(np.uint8)

        cmap = plt.cm.plasma  # You can choose other colormaps like 'plasma', 'inferno', etc.
        rgb_image = cmap(normalized_activation_np)

        normalized_rgb_image = 255 * (rgb_image - np.min(rgb_image)) / (np.max(rgb_image) - np.min(rgb_image))
        normalized_rgb_image = normalized_rgb_image.astype(np.uint8)
        normalized_rgb_image = normalized_rgb_image[:, :, :3]

        # The result is an RGBA image (last channel is alpha), so remove the alpha channel
        # rgb_image = (normalized_array[:, :, :3]).astype(np.uint8)

        # Save the image using Pillow
        image = Image.fromarray(normalized_rgb_image)
        image.save(f'data/testing/output_1_{channel}.png')
        print(f'saved: data/testing/output_1_{channel}.png')


#%%



# Step 1: Initialize model with the best available weights
weights = VGG16_Weights.DEFAULT
model = vgg16(weights=weights)
model.eval()

# Step 2: Initialize the inference transforms
preprocess = weights.transforms()


with torch.no_grad():
    model(image_test_input)
