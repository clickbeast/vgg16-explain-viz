import os
import re

from data_manager import Activation, convert_to_float

filename = 'assets/data/imagenette/1000/1/activations/images/1_685_55_0-7250953_0-2897304_0-2100821.png'
#filename = 'assets/data/imagenette/1000/1/activations/images/1_8158_12_0-05099036_0-001696545_8-650745e23.png'

patternold = (r"(\d+)-(\d+)-(\d+)-([0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)\-([0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)\-(["
              r"0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)\-([0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)\-([0-9]+(?:-[0-9]+)?("
              r"?:e-?[0-9]+)?)\-([0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)\.(?:png|npy)")

pattern = (r"(\d+)_(\d+)_(\d+)_([0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)_([0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)_([0-9]+(?:-["
           r"0-9]+)?(?:e-?[0-9]+)?)\.(?:png|npy)")


def convert_to_float_2(number):
    """Convert number and fraction to a float."""
    return float(number.replace('-', '.', 1))

    #return float(f"{number}.{frac}")


def parse_filename_activation_old(filename):
    """Parse the filename to extract parameters and return the result dictionary."""

    print(f'parsing: {filename}')

    filename = os.path.basename(filename)
    print(filename)

    #pattern = r"(\d+)_(\d+)_(\d+)_([0-9]+)-([0-9]+)_([0-9]+)-([0-9]+)_([0-9]+)-([0-9]+)\.png"
    #pattern = r"(\d+)_(\d+)_(\d+)_([0-9]+)-([0-9]+)_([0-9]+)-([0-9]+)_([0-9]+)-([0-9]+)\.png"

    pattern = (r"(\d+)-(\d+)-(\d+)-([0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)\-([0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)\-(["
               r"0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)\-([0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)\-([0-9]+(?:-[0-9]+)?("
               r"?:e-?[0-9]+)?)\-([0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)\.(?:png|npy)")

    pattern = (r"(\d+)_(\d+)_(\d+)_([0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)_([0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)_([0-9]+(?:-["
               r"0-9]+)?(?:e-?[0-9]+)?)\.(?:png|npy)")

    match = re.match(pattern, filename)

    if not match:
        raise ValueError("Filename does not match the expected structure.")

    param1, param2, param3, number1, number1frac, number2, number2frac, number3, number3frac = match.groups()

    activation_img_dir = os.path.join('assets/data/imagenette/1000', str(1), 'activations', 'images')
    activation_raw_dir = os.path.join('assets/data/imagenette/1000', str(1), 'activations', 'raw_data')

    filename_raw = os.path.splitext(filename)[0] + ".npy"

    result = {
        "layer_idx": int(param1),
        "uid": int(param2),
        "channel": int(param3),
        "entropy": convert_to_float_2(number1, number1frac),
        "magnitude": convert_to_float_2(number2, number2frac),
        "score": convert_to_float_2(number3, number3frac),
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

pattern_bckp = (r"(\d+)_(\d+)_(\d+)_([0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)_([0-9]+(?:-[0-9]+)?(?:e-?[0-9]+)?)_([0-9]+(?:-["
           r"0-9]+)?(?:e-?[0-9]+)?)\.(?:png|npy)")



def parse_filename_activation(filename):
    """Parse the filename to extract parameters and return the result dictionary."""

    print(f'parsing: {filename}')

    filename = os.path.basename(filename)
    print(filename)

    # pattern = r"(\d+)_(\d+)_(\d+)_([0-9]+)-([0-9]+)_([0-9]+)-([0-9]+)_([0-9]+)-([0-9]+)\.png"
    # pattern = r"(\d+)_(\d+)_(\d+)_([0-9]+)-([0-9]+)_([0-9]+)-([0-9]+)_([0-9]+)-([0-9]+)\.png"



    pattern = (
        r"(\d+)_(\d+)_(\d+)_([0-9]+(?:-[0-9]+)?(?:e[+-]?[0-9]+)?)_([0-9]+(?:-[0-9]+)?(?:e[+-]?[0-9]+)?)_([0-9]+(?:-["
        r"0-9]+)?(?:e[+-]?[0-9]+)?)\.(?:png|npy)")

    match = re.match(pattern, filename)

    if not match:
        raise ValueError("Filename does not match the expected structure.")

    param1, param2, param3, number1, number2, number3 = match.groups()

    activation_img_dir = os.path.join('assets/data/imagenette/1000', str(1), 'activations', 'images')
    activation_raw_dir = os.path.join('assets/data/imagenette/1000', str(1), 'activations', 'raw_data')

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


parse_filename_activation(filename)
