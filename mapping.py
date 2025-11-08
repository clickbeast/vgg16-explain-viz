layer_idx_to_layer_type = {

    0: ['conv', [224, 224, 64]],
    1: ['relu', [224, 224, 64]],
    2: ['conv', [224, 224, 64]],
    3: ['relu', [224, 224, 64]],

    4: ['max_pool', [112, 112, 128]],
    5: ['conv', [112, 112, 128]],
    6: ['relu', [112, 112, 128]],
    7: ['conv', [112, 112, 128]],
    8: ['relu', [112, 112, 128]],

    9: ['max_pool', [56, 56, 256]],
    10: ['conv', [56, 56, 256]],
    11: ['relu', [56, 56, 256]],
    12: ['conv', [56, 56, 256]],
    13: ['relu', [56, 56, 256]],
    14: ['conv', [56, 56, 256]],
    15: ['relu', [56, 56, 256]],

    16: ['max_pool', [28, 28, 512]],
    17: ['conv', [28, 28, 512]],
    18: ['relu', [28, 28, 512]],
    19: ['conv', [28, 28, 512]],
    20: ['relu', [28, 28, 512]],
    21: ['conv', [28, 28, 512]],
    22: ['relu', [28, 28, 512]],

    23: ['max_pool', [14, 14, 512]],
    24: ['conv', [14, 14, 512]],
    25: ['relu', [14, 14, 512]],
    26: ['conv', [14, 14, 512]],
    27: ['relu', [14, 14, 512]],
    28: ['conv', [14, 14, 512]],
    29: ['relu', [14, 14, 512]],

    30: ['max_pool', [7, 7, 512]],
    31: ['n', [1, 1, 4096]],
    32: ['relu', [1, 1, 4096]],
    33: ['n', [1, 1, 4096]],
    34: ['relu', [1, 1, 4096]],
    35: ['n', [1, 1, 1000]],

    36: ['input', [224, 224, 3]],
    37: ['output', [1, 1, 1000]],
}

layer_idx_to_model_key_name = {
    0: 'features.0',
    1: 'features.1',
    2: 'features.2',
    3: 'features.3',
    4: 'features.4',
    5: 'features.5',
    6: 'features.6',
    7: 'features.7',
    8: 'features.8',
    9: 'features.9',
    10: 'features.10',
    11: 'features.11',
    12: 'features.12',
    13: 'features.13',
    14: 'features.14',
    15: 'features.15',
    16: 'features.16',
    17: 'features.17',
    18: 'features.18',
    19: 'features.19',
    20: 'features.20',
    21: 'features.21',
    22: 'features.22',
    23: 'features.23',
    24: 'features.24',
    25: 'features.25',
    26: 'features.26',
    27: 'features.27',
    28: 'features.28',
    29: 'features.29',
    30: 'features.30',
    31: 'classifier.0',
    32: 'classifier.1',
    33: 'classifier.3',
    34: 'classifier.4',
    35: 'classifier.6',
    36: 'input',
    37: 'output',
}

layer_idx_to_model_layer_idx = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 11,
    12: 12,
    13: 13,
    14: 14,
    15: 15,
    16: 16,
    17: 17,
    18: 18,
    19: 19,
    20: 20,
    21: 21,
    22: 22,
    23: 23,
    24: 24,
    25: 25,
    26: 26,
    27: 27,
    28: 28,
    29: 29,
    30: 30,
    31: 0,
    32: 1,
    33: 3,
    34: 4,
    35: 6,
    36: 36,
    37: 37,
}

dimensionality_reduction_layer_mapping = [
    (1, 0),
    (3, 2),
    (4, -1),
    (6, 5),
    (8, 7),
    (9, -1),
    (11, 10),
    (13, 12),
    (15, 14),
    (16, -1),
    (18, 17),
    (20, 19),
    (22, 21),
    (23, -1),
    (25, 24),
    (27, 26),
    (29, 28),
    (30, -1),
    (32, 31),
    (34, 33),
    (35, -1),
    (36, -1),
    (37, -1),
]


dimensionality_reduction_layer_mapping_reduced = [
    #(1, 0),
    (3, 2),
    (4, -1),
    #(6, 5),
    (8, 7),
    (9, -1),
    #(11, 10),
    #(13, 12),
    (15, 14),
    (16, -1),
    #(18, 17),
    #(20, 19),
    (22, 21),
    (23, -1),
    #(25, 24),
    #(27, 26),
    (29, 28),
    (30, -1),
    (32, 31),
    (34, 33),
    (35, -1),
    (36, -1),
    (37, -1),
]

dimensionality_reduction_layer_mapping_extra_copies = {
    3: (1,0),
    8: (6, 5),
    15: (10, 11, 12, 13),
    22: (17, 18, 19, 20),
    29: (24, 25, 26, 27),
}



debug_dimensionality_reduction_layer_mapping = [
    #(3, 2),
    #(32, 31),
    #(34, 33),
    #(35, -1),
    (36, -1),
    (37, -1),
]


layer_idx_list_full = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,31, 32, 33, 34, 35, 36, 37
]

layer_operation_to_text_description = {
    'conv': 'Convolution',
    'relu': 'RELU',
    'max_pool': 'Max Pool',
    'avg_pool': 'Avg Pool',
    'n': 'fully connected',
    'input': 'input',
    'output': 'output'
}


def get_layer_type_text_description(layer_idx):
    layer_type = layer_idx_to_layer_type[layer_idx]
    multi_dim = '2D ' if (layer_type[1][0] == layer_type[1][1]) and (layer_type[1][0] != 1) else ''
    layer_idx_text = layer_idx
    layer_operation_text = layer_operation_to_text_description[layer_type[0]]
    if layer_idx == 36:
        return 'input layer, 224x224, 3 channels'
    if layer_idx == 37:
        return 'output layer, softmax, 1000 outputs (output probabilities for each class)'
    output_text = (f'layer {layer_idx_text}, {multi_dim}{layer_operation_text}, '
                   f'{layer_type[1][0]}x{layer_type[1][1]}, {layer_type[1][2]} channels')

    return output_text
