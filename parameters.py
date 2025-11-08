
# --------------------------------------
# PARAMETERS
# --------------------------------------

class Parameters:
    NUMBER_OF_SAMPLES_LIST = [700, 3000, 12000]
    PERPLEXITIES = [10, 30, 50, 80, 100]
    DATASET = ['imagenette', 'imagewoof']
    DIMENSIONALITY_REDUCTION_METHODS = ['tsne', 'pca']
    LAYER_IDX_LIST = []
    ACTIVATIONS = []
    ANNOTATIONS_IMAGENETTE = 'datasets/imagenette2-320/noisy_imagenette.csv'
    ANNOTATIONS_IMAGEWOOF = 'datasets/imagewoof2-320/noisy_imagewoof.csv'
    DIR_IMAGENETTE = 'datasets/imagenette2-320'
    DIR_IMAGEWOOF = 'datasets/imagewoof2-320'
    BATCH_SIZE = 32
    NUMBER_OF_SAMPLES = 10
    N_LAYERS = 38

