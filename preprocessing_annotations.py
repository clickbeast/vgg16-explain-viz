import pandas as pd

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

from torchvision.models import vgg16, VGG16_Weights

#Imagenet weights
weights = VGG16_Weights.DEFAULT

categories = weights.meta['categories']

print(categories)

for idx, category  in enumerate(categories):
    mapping_label_id_to_category[idx] = category
    mapping_label_category_to_id[category] = idx

#todo check wich categrories no match , then fic


#Create dataframe out of it


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



def find_discrepancies(mapping_label_to_category, mapping_category_to_label,
                      mapping_label_id_to_category, mapping_label_category_to_id):
    """
    Find categories that:
    1. Appear in `mapping_label_to_category` but not in `mapping_label_id_to_category`.
       Return their associated labels.
    2. Appear in `mapping_label_id_to_category` but not in `mapping_label_to_category`.
       Return their associated label IDs.

    Args:
    mapping_label_to_category (dict): Maps label (synset ID) to category.
    mapping_category_to_label (dict): Maps category to label (synset ID).
    mapping_label_id_to_category (dict): Maps label ID (class index) to category.
    mapping_label_category_to_id (dict): Maps category to label ID (class index).

    Returns:
    dict: A dictionary containing two keys:
          'in_label_to_category_not_in_label_id_to_category': List of tuples (label, category).
          'in_label_id_to_category_not_in_label_to_category': List of tuples (label_id, category).
    """
    # Categories in `mapping_label_to_category` but not in `mapping_label_id_to_category`
    in_label_to_category_not_in_label_id_to_category = []
    for label, category in mapping_label_to_category.items():
        if category not in mapping_label_category_to_id:
            in_label_to_category_not_in_label_id_to_category.append((label, category))

    # Categories in `mapping_label_id_to_category` but not in `mapping_label_to_category`
    in_label_id_to_category_not_in_label_to_category = []
    for label_id, category in mapping_label_id_to_category.items():
        if category not in mapping_category_to_label:
            in_label_id_to_category_not_in_label_to_category.append((label_id, category))

    # Return discrepancies
    return {
        'in_label_to_category_not_in_label_id_to_category': in_label_to_category_not_in_label_id_to_category,
        'in_label_id_to_category_not_in_label_to_category': in_label_id_to_category_not_in_label_to_category
    }


#these need to be added
#'crane bird': n02012849    -> 'crane bird' -> 'crane'
#'maillot tank suit': n03710721 -> ''

print(find_discrepancies(mapping_label_to_category,
                         mapping_category_to_label,
                         mapping_label_id_to_category,
                         mapping_label_category_to_id ))