import argparse
import os
import cv2
import numpy as np
import torch
from torchvision import models
from pytorch_grad_cam import (
    GradCAM, HiResCAM, ScoreCAM, GradCAMPlusPlus,
    AblationCAM, XGradCAM, EigenCAM, EigenGradCAM,
    LayerCAM, FullGrad, GradCAMElementWise, KPCA_CAM
)
from pytorch_grad_cam import GuidedBackpropReLUModel
from pytorch_grad_cam.utils.image import (
    show_cam_on_image, deprocess_image, preprocess_image
)
from PIL import Image
from torchvision.transforms import InterpolationMode, ToPILImage
import torchvision.transforms as transforms



from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget




def crop_image(img):

    img = Image.fromarray(img)

    # Define the transformation pipeline
    transform = transforms.Compose([
        # Resize the image to 256x256 using bilinear interpolation
        transforms.Resize(256, interpolation=InterpolationMode.BILINEAR),

        # Central crop to 224x224
        transforms.CenterCrop(224),

    ])

    transform(img)

    # Convert PIL image to a NumPy array
    img = np.asarray(img, dtype=np.float32)



    return img




class CamManager:

    def __init__(self):
        super().__init__()
        self.device = 'cpu'
        print('loading model for cam')
        self.model = models.vgg16(pretrained=True).to(torch.device(self.device)).eval()
        print('done loading for cam')

    def get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--device', type=str, default='cpu',
                            help='Torch device to use')
        parser.add_argument(
            '--image-path',
            type=str,
            default='./examples/both.png',
            help='Input image path')
        parser.add_argument('--aug-smooth', action='store_true',
                            help='Apply test time augmentation to smooth the CAM')
        parser.add_argument(
            '--eigen-smooth',
            action='store_true',
            help='Reduce noise by taking the first principle component'
                 'of cam_weights*activations')
        parser.add_argument('--method', type=str, default='gradcam',
                            choices=[
                                'gradcam', 'hirescam', 'gradcam++',
                                'scorecam', 'xgradcam', 'ablationcam',
                                'eigencam', 'eigengradcam', 'layercam',
                                'fullgrad', 'gradcamelementwise', 'kpcacam'
                            ],
                            help='CAM method')

        parser.add_argument('--output-dir', type=str, default='output',
                            help='Output directory to save the images')
        args = parser.parse_args()

        if args.device:
            print(f'Using device "{args.device}" for acceleration')
        else:
            print('Using CPU for computation')

        return args



    def run_cam(self, img_path, output_dir, layer_idx, uid, model=None):

        args = self.get_args()

        methods = {
            "gradcam": GradCAM,
            "hirescam": HiResCAM,
            "scorecam": ScoreCAM,
            "gradcam++": GradCAMPlusPlus,
            "ablationcam": AblationCAM,
            "xgradcam": XGradCAM,
            "eigencam": EigenCAM,
            "eigengradcam": EigenGradCAM,
            "layercam": LayerCAM,
            "fullgrad": FullGrad,
            "gradcamelementwise": GradCAMElementWise,
            'kpcacam': KPCA_CAM
        }

        if args.device == 'hpu':
            import habana_frameworks.torch.core as htcore

        self.model = models.vgg16(pretrained=True).to(torch.device(args.device)).eval()

        # Choose the target layer you want to compute the visualization for.
        # Usually this will be the last convolutional layer in the model.
        # Some common choices can be:
        # Resnet18 and 50: model.layer4
        # VGG, densenet161: model.features[-1]
        # mnasnet1_0: model.layers[-1]
        # You can print the model to help chose the layer
        # You can pass a list with several target layers,
        # in that case the CAMs will be computed per layer and then aggregated.
        # You can also try selecting all layers of a certain type, with e.g:
        # from pytorch_grad_cam.utils.find_layers import find_layer_types_recursive
        # find_layer_types_recursive(model, [torch.nn.ReLU])

        target_layers = [self.model.features[layer_idx]]

        rgb_img = cv2.imread(img_path, 1)[:, :, ::-1]
        rgb_img = crop_image(rgb_img)
        rgb_img = np.float32(rgb_img) / 255
        input_tensor = preprocess_image(rgb_img,
                                        mean=[0.485, 0.456, 0.406],
                                        std=[0.229, 0.224, 0.225]).to()

        input_tensor = input_tensor

        # We have to specify the target we want to generate
        # the Class Activation Maps for.
        # If targets is None, the highest scoring category (for every member in the batch) will be used.
        # You can target specific categories by
        # targets = [ClassifierOutputTarget(281)]
        # targets = [ClassifierOutputTarget(281)]
        targets = None

        # Using the with statement ensures the context is freed, and you can
        # recreate different CAM objects in a loop.
        cam_algorithm = methods[args.method]
        with cam_algorithm(model=self.model,
                           target_layers=target_layers) as cam:
            # AblationCAM and ScoreCAM have batched implementations.
            # You can override the internal batch size for faster computation.
            cam.batch_size = 32
            grayscale_cam = cam(input_tensor=input_tensor,
                                targets=targets,
                                aug_smooth=args.aug_smooth,
                                eigen_smooth=args.eigen_smooth)

            grayscale_cam = grayscale_cam[0, :]

            cam_image = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
            cam_image = cv2.cvtColor(cam_image, cv2.COLOR_RGB2BGR)

        gb_model = GuidedBackpropReLUModel(model=self.model, device=args.device)
        gb = gb_model(input_tensor, target_category=None)

        cam_mask = cv2.merge([grayscale_cam, grayscale_cam, grayscale_cam])
        cam_gb = deprocess_image(cam_mask * gb)
        gb = deprocess_image(gb)

        os.makedirs(args.output_dir, exist_ok=True)

        cam_output_path = os.path.join(output_dir, f'{layer_idx}_{uid}_{args.method}_cam.jpg')
        gb_output_path = os.path.join(output_dir, f'{layer_idx}_{uid}_{args.method}_gb.jpg')
        cam_gb_output_path = os.path.join(output_dir, f'{layer_idx}_{uid}_{args.method}_cam_gb.jpg')
        cv2.imwrite(cam_output_path, cam_image)
        cv2.imwrite(gb_output_path, gb)
        cv2.imwrite(cam_gb_output_path, cam_gb)


if __name__ == '__main__':
    """ python cam.py -image-path <path_to_image>
        Example usage of loading an image and computing:
            1. CAM
            2. Guided Back Propagation
            3. Combining both
        """


    data_dir = 'assets/data/imagenette/700'
    img = np.load(os.path.join(data_dir,'test_image.npy'))
    t_uid = 5259
    t_label = 'n03888257'
    t_label_id = 701
    t_category = 'parachute'
    t_img_path = 'datasets/imagenette2-320/train/n03888257/n03888257_22484.JPEG'
    output_dir = os.path.join(data_dir, 'testing', 'explainability')
    print(output_dir)


    cam = CamManager()
    cam.run_cam(t_img_path, output_dir, 29, t_uid)
