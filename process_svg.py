import re

from mapping import layer_idx_to_layer_type

N_GROUPS = 38

layer_idx_map = {
    0: 14,
    1: 15,
    2: 33,
    3: 34,
    4: 'input',
    5: 16,
    6: 9,
    7: 0,
    8: 1,
    9: 17,
    10: 18,
    11: 21,
    12: 22,
    13: 2,
    14: 4,
    15: 7,
    16: 8,
    17: 'output',
    18: 35,
    19: 31,
    20: 23,
    21: 30,
    22: 24,
    23: 19,
    24: 10,
    25: 5,
    26: 25,
    27: 6,
    28: 20,
    29: 3,
    30: 11,
    31: 12,
    32: 13,
    33: 26,
    34: 27,
    35: 28,
    36: 29,
    37: 32,
}

#change the input, and output to layer 38 (input) and layer 39 (output)

layer_idx_map[4] = 36
layer_idx_map[17] = 37

#Change the colors to match the theme
color_map = {

    # Blue fill
    '#DAE8FC': '#313C4B',
    # Blue stroke
    '#6C8EBF': '#6580A8',

    # Orange fill
    '#FFE6CC': '#36210A',
    # Orange stroke
    '#D79B00': '#885A00',

    # Red fill
    '#F8CECC': '#61403E',
    # Red stroke
    '#B85450': '#9B5B58',

    # Green fill
    '#D5E8D4': '#344333',
    # Green stroke
    '#82B366': '#46702E',

    # purple pink fill
    '#F3D1FF': '#543B5E',
    # purple pink stroke
    '#000033': '#BDA1C8',

    # purple blue fill
    '#C5C6E8': '#50516D',
    # purple blue stroke
    '#0012B3': '#A3B0D7',
}

#Change the colors to match the theme
color_map_layer_type_to_color = {
    'conv': {
        # Blue fill
        'fill': '#313C4B',
        # Blue stroke
        'stroke': '#6580A8',
    },

    'relu': {
        # Orange fill
        'fill': '#36210A',
        # Orange stroke
        'stroke': '#885A00',
    },

    'max_pool': {
        # Red fill
        'fill': '#61403E',
        # Red stroke
        'stroke': '#9B5B58',
    },

    'n': {
        # Green fill
        'fill': '#344333',
        # Green stroke
        'stroke': '#46702E',
    },

    'input': {
        # purple pink fill
        'fill': '#543B5E',
        # purple pink stroke
        'stroke': '#BDA1C8',
    },

    'output': {
        # purple blue fill
        'fill': '#50516D',
        # purple blue stroke
        'stroke': '#A3B0D7',
    }
}


# Change group - traverse in opposite direction

# From chatgpt via: "replace occururences of a word ,
# word by word each time replacing the word by another word from
# an array, I am replacing these occurences in a file, so i want to also
# read in the file line by line and then save it again to another file"

# Heavy Modifications done to make it work.


def replace_word_in_file(input_file, output_file, target_word, replacements):
    """
    Replace occurrences of `target_word` in `input_file` with words from `replacements` array,
    and save the modified content to `output_file`.
    """
    replacement_index = 0  # Index to track the current replacement word

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if 'Group' in line:
                on_click_part = f' onClick={{() => handleLayerClick({str(replacements[replacement_index])})}}'
                out_line = line.replace('id="Group"', f'id="layer_{str(replacements[replacement_index])}"' +
                                        on_click_part)
                outfile.write(out_line)
                replacement_index += 1
            else:
                outfile.write(line)


# Example usage
input_file = "input.svg"
output_file = "output.svg"
output_2_file = "vgg16_model_visualization.svg"
target_word = "group"
replacements = list(layer_idx_map.values())[::-1]


def replace_colors(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            for key in color_map.keys():
                if key in line:
                    line = line.replace(key, color_map[key])
            outfile.write(line)
    pass


def replace_colors_method_2(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        layer_type = ''
        layer_group_line_count = 0
        for line_idx, line in enumerate(infile):
            #skip first line
            if line_idx == 0:
                continue
            # skip third line (title)
            if line_idx == 2:
                continue



            if layer_group_line_count == 0:
                layer_group_id_pattern = re.compile(r'id="layer_(\d+)"')
                match = layer_group_id_pattern.search(line)

                if match:
                    #get the layer id
                    layer_id = int(match.group(1))
                    #get the layer type based on the id
                    layer_type = layer_idx_to_layer_type[layer_id][0]

                    #increase the counter to start color replace procedure
                    layer_group_line_count += 1

                    #just write the line
                    outfile.write(line)

                else:
                    outfile.write(line)



            elif layer_group_line_count > 0:
                if layer_group_line_count == 1:
                    #replace the fill and the stroke with the correct one
                    fill_color = color_map_layer_type_to_color[layer_type]['fill']
                    stroke_color = color_map_layer_type_to_color[layer_type]['stroke']

                    out_line = re.sub(r'fill="([^"]+)"', f'fill="{fill_color}"', line)
                    out_line = re.sub(r'stroke="([^"]+)"', f'stroke="{stroke_color}"', out_line)

                    outfile.write(out_line)

                    layer_group_line_count += 1


                elif layer_group_line_count == 10:

                    stroke_color = color_map_layer_type_to_color[layer_type]['stroke']

                    out_line = re.sub(r'stroke="([^"]+)"', f'stroke="{stroke_color}"', line)

                    outfile.write(out_line)

                    layer_group_line_count += 1


                elif layer_group_line_count == 4:
                    stroke_color = color_map_layer_type_to_color[layer_type]['stroke']

                    out_line = re.sub(r'stroke="([^"]+)"', f'stroke="{stroke_color}"', line)

                    outfile.write(out_line)

                    #reset the counter!!!
                    layer_group_line_count = 0
                else:
                    #just copy the line
                    outfile.write(line)
                    layer_group_line_count += 1


    pass


#change layer ids to correct ones
replace_word_in_file(input_file, output_file, target_word, replacements)
#change colors to correct ones.
#replace_colors(output_file, output_2_file)
replace_colors_method_2(output_file, output_2_file)
