import os.path

from dash import Dash, html, dcc, State, ctx, MATCH, ALL
import dash
import numpy as np
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
from dash_svg import Svg, G, Path, Circle
import ssp_matrix
import time
from data_manager import load_dimensionality_reduction_dataframes, Instance, Sample, is_neuron_activation, \
    is_activation_available, Activation, is_instance_changed_via_input, compute_activations, get_activations, \
    get_neuron_activations, padded_2D_array, get_activation_detail
from mapping import get_layer_type_text_description
import json


# --------------------------------------
# Preload data
# --------------------------------------


default_key = 'imagenette_tsne_3000_40_1'

start_instance = Instance(
    'imagenette',  #dataset
    1000,  #n_samples
    1,  #selected layer
    30,  #perplexity
    'tsne'
)

#read all the dimensionaliy reductions done, might take a while
dim_red_dataframes = load_dimensionality_reduction_dataframes(start_instance)

#default
df_default = dim_red_dataframes[start_instance]
fig_scatter = px.scatter(data_frame=df_default, x='x', y='y', color='label')

# --------------------------------------
# Dash app started from this point.
# --------------------------------------


app = Dash(title='Imagenet Data Insights with VGG16')

about_dashboard_text = html.P('Welcome to the Imagenet Data Insights with VGG16 Dashboard.'
                              ' This dashboard enables you to get insights into imagenet data'
                              ' by leveraging the power of a neural net that has been trained'
                              ' to perform classification on the imagenet dataset. By exploring'
                              ' representations of our data beyond simple rgb images the hope is'
                              ' that this dashboard enables you to get new insights in imagenet data.'
                              ' For example the discovery of interesting properties inherent to the data'
                              ' such as distrinict clusters based on uniqueqly shared features between groups'
                              ' of pictures.'
                              )
about_dataset_text = html.Ul([
    html.Li([
        html.Span('Dataset: '),
        '2 subsets of Imagenet'
    ]),
    html.Li([html.Span('Description: '),
             'The first subset is imagenette contains 13394 samples. The second Imagewoof 12954 samples'
             ]),
    html.Li([
        html.Span('Data Source used in implementation: '),
        html.A(
            href='https://github.com/fastai/imagenette/tree/master',
            target='_blank',
            children='Imagenette & Imagewoof',
        )
    ]),
    # html.Li([
    #     html.Span('Orginal Creator: '),
    #     html.A(
    #         href='https://yann.lecun.com/exdb/mnist/',
    #         target='_blank',
    #         children='MNIST Database by Yan LeCun Et al.',
    #     )
    # ]),
])

# Layout of the scatter plot
# (via chatgpt, with customization)
layout = {
    'plot_bgcolor': '#100F12',  # Dark background for the plot
    'paper_bgcolor': '#100F12',  # Dark background for the paper (entire plot area)
    'font': {
        'color': '#FFFFFF'  # White text for better contrast
    },
    'xaxis': {
        'showgrid': True,
        'gridcolor': '#444444',  # Dark gray gridlines
        'title': 'Dimension 1',
        'titlefont': {'color': '#FFFFFF'},
        'zeroline': False,
    },
    'yaxis': {
        'showgrid': True,
        'gridcolor': '#444444',  # Dark gray gridlines
        'title': 'Dimension 2',
        'titlefont': {'color': '#FFFFFF'},
        'zeroline': False,

    },
    'title': 'TSNE with perplexity 40',
    'titlefont': {'color': '#FFFFFF'}
}

fig_scatter.update_layout(layout)
fig = fig_scatter


def render_outputs():
    n_activations = 512

    activation_image_elements = []
    for i in range(n_activations):
        element = html.Div(id={"type": "activation-channel", "index": i}, className='activationImageContainer',
                           children=[
                               html.Img(className='activationImage', src='assets/output_1.png'),
                               html.Div(className='activationChannelInfo', children=[
                                   html.Div(className='channel', children=[str(i)]),
                                   html.Div(className='score', children=['10'])
                               ])
                           ])
        activation_image_elements.append(element)

    activations = html.Div(className='activationsViewContainer', children=[
        html.Div(className='activationsGridContainer', children=activation_image_elements)
    ])

    return activations



model_container_children = [
    html.H2('MODEL VISUALIZATION'),
    html.H4(id="model-visualization-text", children=['Layer 1 selected.']),
    html.Div(className='modelSubContainer', children=[
        html.Div(className='modelViewer', children=[
            ssp_matrix.Matrix(id="result", selectedLayer=1, hoverColor='white', selectedColor='white'),
            html.Div(className='vggLegendContainer', children=[
                html.Img(className='vggLegend', src='assets/vgg16_legend.svg')
            ]),

        ]),
    ]),
]


def get_h4_with_info(id, title, info):
    return html.Div(className='titleContainer', children=[
        html.H4(title),
        html.Div(className='tooltip', title=info, children=[
            html.Img(id='tooltip-button', className='infoButton', src='assets/info-icon.svg'),
            html.Div(id='tooltip-content', className='', children=[

            ]),
            dcc.Store(id="tooltip-state", data=False),
        ]),
    ])


def get_layer_selection_options():
    return list(range(0, 38))


html.H4('Select perplexity')

control_container_children = [
    html.H2('CONFIGURE'),
    get_h4_with_info('info-subset', 'Select subset of imagenet you want',
                     'Imagenette is a subset of imagenet with a variety of 10 '
                     'classes that are quite different from each other. (tench, '
                     'English springer, cassette player, chain saw, church, '
                     'French horn, garbage truck, gas pump, golf ball, '
                     'parachute).\n\nImagewoof is a subset of imagenet that only '
                     'contains dog breeds. There are 10 different breeds. ('
                     'Australian terrier, Border terrier, Samoyed, Beagle, '
                     'Shih-Tzu, English foxhound, Rhodesian ridgeback, Dingo, '
                     'Golden retriever, Old English sheepdog)'),
    html.Div(className='dropdownContainer', children=[
        html.Div(className='dropdownB', children=[
            dcc.Dropdown(
                options=['Imagenette', 'ImageWoof'],
                value='Imagenette',
                id='dataset-selection',
                className='dropdown',
            ),
        ]),
    ]),
    html.H4('Select subset of data you want to use'),
    dcc.Slider(
        min=10,
        max=7000,
        value=1000,
        step=None,
        id="number-of-samples",
        marks={
            100: '100',
            1000: '1000',
            7000: '7000'
        },
        tooltip={"placement": "bottom", "always_visible": True},
    ),
    # html.H4('Select VGG16 layer to inspect'),
    #     html.Div(className='dropdownContainer', children=[
    #         html.Div(className='dropdownB', children=[
    #             dcc.Dropdown(
    #                 options=get_layer_selection_options(),
    #                 value=0,
    #                 id='layer-selection',
    #                 className='dropdown',
    #             ),
    #         ]),
    #     ]),

    html.H4('Select dimensionality reduction method'),
    html.Div(className='dropdownContainer', children=[
        html.Div(className='dropdownB', children=[
            dcc.Dropdown(
                options=['TSNE', 'PCA'],
                value='TSNE',
                id='dimensionality-method',
                className='dropdown',
                style={'color': 'white'}
            ),
        ]),
    ]),
    html.Div(id='method-control-container', className='methodControlContainer', children=[
        html.H4('Select perplexity'),
        dcc.Slider(
            min=10,
            max=90,
            value=30,
            step=None,
            id="perplexity",
            marks={
                10: '10',
                30: '30',
                90: '90'
            },
            tooltip={"placement": "bottom", "always_visible": True},
        ),
    ])
]

graph_container_children = [
    html.H2('DIMENSIONALITY REDUCTION CHART'),
    html.Div(className='figContainer', children=[
        dcc.Graph(id='chart', figure=fig)
    ]),
]

data_container_children = [
    html.Div(className='layerOutputsTitleContainer', children=[
        html.H2('ACTIVATIONS'),
        # html.Div(id='legend-activation', className='legendActivationContainer', children=[
        #             html.Div(className='colorBar', children=['']),
        #             html.Div(className='legend', children=[html.Div('0'),html.Div('Legend'),html.Div('1')]),
        #         ]),
        html.Div(className='layerOutputSortContainer', children=[
            html.H4('Sort on:'),
            html.Div(className='layerOutputSortSelection', children=[
                dcc.Dropdown(
                    options=['Channel Index', 'Score'],
                    value='Channel Index',
                    id='sort-method',
                    className='dropdown',
                    style={'color': 'white'}
                ),
            ])

        ])
    ]),

    html.Div(id='layer-outputs', children=[
        html.Div(id='layer-outputs-placeholder', className='layerOutputsNoSelectionContainer', children=[
            html.H5('Select a datapoint, to see the outputs for the selected layer.'),
            html.H5(''),
        ]),
    ]),

    #render_outputs(),


    # html.Div(className='layerOutputsNoComputationContainer', children=[
    #     html.H5('Activations for this sample have not been computed yet. Press below to compute.'),
    #     html.Div(id='compute-button', className='buttonB', children=['Compute activations'])
    # ], style={'display': 'none'}),

    html.Div(id='compute-button-view', className='layerOutputsNoComputationContainer', children=[
        html.H5('Activations for this sample have not been computed yet. Press below to compute.'),
        html.Div(className='computeButtonContainer', children=[
            html.Div(id='compute-button', className='buttonB', children=['Compute activations'])
        ]),
    ], style={'display': 'none'}),




    dcc.Loading(
        id='loading-indicator',
        type='circle',
        children=[
            html.Div(id='layer-outputs-data', children=['']),
    ]),

    html.Div(className='abc', children=[
        html.Div(id='legend-activation', className='legendActivationContainer', children=[
            html.Div(className='colorBar', children=['']),
            html.Div(className='legend', children=[html.Div('0'),html.Div('Legend'),html.Div('1')]),
        ]),
    ])
]

inspector_container_children = [

    html.Div(className='inspectorContainerTitleContainer', children=[
        html.H2('INSPECTOR'),
        html.Div(id='selected-sample', title='-1'),
        html.Div(id='compute-sample', title='-1'),
        html.Div(id='instance', **{'data-instance': '-1'}),

        html.Div(id='cancel-button-view', className='cancelButtonContainer', children=[
            html.Div(id='cancel-button', className='buttonA', children=['Cancel selection'])
        ])
    ]),

    html.Div(id='inspector',className='', children=[
        html.H5('Hover over or select a datapoint to see:'),
        html.H5('The corresponding image'),
        html.H5('The top 10 output probabilities, and explainability for the top label.'),
    ])
]

info_container_children = [
    html.H2('ABOUT'),
    html.Div(className='infoContentContainer', children=[
        html.Div(className='aboutDashboardContainer', children=[
            html.Div(className='aboutDashboardContent', children=[
                about_dashboard_text
            ]),
        ]),
        html.Div(className='aboutDatasetContainer', children=[
            html.Div(className='aboutDatasetContent', children=[
                about_dataset_text,
            ]),
        ]),

    ]),
]

app.layout = [

    html.Div(id='container', className='container', children=[

    # The memory store reverts to the default on every page refresh
    #dcc.Store(id={'type': 'storage', 'index': 'instance'}),


        html.Div(id='modal-overlay', className='modalOverlay', children=[
            html.Div(id='modal-cancel', className='modalCancelBox', children=[
            ]),
            html.Div(id='modal-content', className='modalContent', children=[
                'bonjour'
            ])
        ]),
        html.Div(id='', className='headerContainer', children=[
            html.H1('Imagenet Data Insights with VGG16')
        ]),

        html.Div(id='', className='modelContainer', children=model_container_children),
        html.Div(id='', className='controlContainer', children=control_container_children),
        html.Div(id='', className='graphContainer', children=graph_container_children),
        html.Div(id='', className='dataContainer', children=data_container_children),
        html.Div(id='', className='inspectorContainer', children=inspector_container_children),
        html.Div(id='', className='infoContainer', children=info_container_children),

    ]),
    html.H5('Created by Simon Vermeir'),

]


# --------------------------------------
# Callbacks
# --------------------------------------

@app.callback(
    Output('model-visualization-text', 'children'),
    Input('result', 'selectedLayer'),
)
def update_selected_layer_text(selectedLayer):
    return ['Selected ' + get_layer_type_text_description(selectedLayer)]


@app.callback(
    Output('modal-overlay', 'style'),
    Output('modal-content', 'children'),
    #Input({"type": "activation-channel", "index": ALL}, 'id'),
    Input({"type": "activation-channel", "index": ALL}, 'n_clicks'),
    Input('modal-cancel', 'n_clicks'),


    #states
    State('dataset-selection', 'value'),
    State('number-of-samples', 'value'),
    State('dimensionality-method', 'value'),
    State('perplexity', 'value'),
    State('result', 'selectedLayer'),

    State('selected-sample', 'title'),
    State('compute-sample', 'title'),

    prevent_initial_call=True,
)
def show_activation_detail_container(
        n_clicks,
        n_clicks_cancel,

        dataset,
        number_samples,
        dim_method,
        perplexity,
        layer_idx,


        selected_sample,
        compute_sample
):
    #print(n_clicks)
    #print(c_id)
    print('hiere')
    print(n_clicks)
    print(dash.callback_context.triggered_prop_ids)

    check = False
    for idx in range(len(n_clicks)):
        if n_clicks[idx] is not None:
            if n_clicks[idx] > 0:
                check = True

    if check:

        triggered_id = dash.callback_context.triggered_prop_ids
        if triggered_id:
            triggered_id = list(triggered_id.values())[0]
            if str(triggered_id) == 'modal-cancel':
                return [{"display": "none"}, 'bonsoir hello']

            triggered_id = triggered_id['index']
            print(triggered_id)

            #Colect instance
            dataset_selected = dataset.lower()
            n_samples_selected = int(number_samples)
            method_selected = dim_method.lower()
            perplexity_selected = int(perplexity)
            layer_idx_selected = int(layer_idx)
            uid = int(selected_sample)
            compute_sample = int(compute_sample)

            instance = Instance(
                dataset_selected,  # dataset
                n_samples_selected,  # n_samples
                layer_idx_selected,  # selected layer
                perplexity_selected,  # perplexity
                method_selected,
            )

            df = dim_red_dataframes[instance]
            sample = df.loc[(df['uid'] == uid)]

            # extract sample object
            sample = Sample(
                sample.index[0],
                sample['uid'].values[0],
                sample['label_id'].values[0],
                sample['label'].values[0],
                sample['category'].values[0],
                sample['img_path'].values[0],
                sample['correct_prediction'].values[0]
            )

            result = render_activation_detail(instance, sample, triggered_id)
            return [{"display": "block"}, result]

    else:
        return [{"display": "none"}, 'bonsoir hello']


def render_activation_detail(instance: Instance , sample: Sample, channel):
    img_rgb = get_activation_detail(instance, sample, channel)
    fig = px.imshow(img_rgb)

    fig.update_layout(width=500, height=500)

    result = html.Div(className='activationDetailContainer', children=[
        dcc.Graph(id='neuron-activation-chart', className='detailChart', figure=fig)
    ])

    return result

#clickData, HoverData, coloredState


@app.callback(
    Output('chart', 'figure'),
    Output('method-control-container', 'style'),
    Input('dataset-selection', 'value'),
    Input('number-of-samples', 'value'),
    Input('dimensionality-method', 'value'),
    Input('perplexity', 'value'),
    Input('result', 'selectedLayer')
)
def update_chart(dataset, number_of_samples, dimensionality_method, perplexity, layer_idx):
    #print('bonjour')

    dataset_selected = dataset.lower()
    n_samples_selected = int(number_of_samples)
    method_selected = dimensionality_method.lower()
    perplexity_selected = int(perplexity)
    layer_idx_selected = int(layer_idx)

    key = default_key
    title = 'TSNE with perplexity 40'
    style = {}

    if method_selected == 'tsne':

        key = Instance(
            dataset_selected,  # dataset
            n_samples_selected,  # n_samples
            layer_idx_selected,  # selected layer
            perplexity_selected,  # perplexity
            'tsne'
        )

        title = f'{dimensionality_method} with perplexity {perplexity}'
        style = {}
    else:

        key = Instance(
            dataset_selected,  # dataset
            n_samples_selected,  # n_samples
            layer_idx_selected,  # selected layer
            perplexity_selected,  # perplexity
            'pca'
        )

        title = f'{dimensionality_method}'
        style = {'display': 'none'}

    df = dim_red_dataframes[key]
    df['prediction'] = df['correct_prediction'].apply(lambda x: 'circle' if x else 'x')

    fig = px.scatter(data_frame=df, x='x', y='y', color='category')

    fig.update_layout(layout)
    fig.update_layout(title=title)
    fig.update_layout(transition_duration=1000)

    #extract uid and select correct point if needed.
    #based on trigger from updating the children of the activation

    return [fig, style]


@app.callback(
    Output('inspector', 'children'),


    Input('chart', 'hoverData'),
    Input('chart', 'clickData'),
    Input('cancel-button', 'n_clicks'),

    State('dataset-selection', 'value'),
    State('number-of-samples', 'value'),
    State('dimensionality-method', 'value'),
    State('perplexity', 'value'),
    State('result', 'selectedLayer'),

    State('instance', 'data-instance'),



    State('chart', 'clickData'),
    State('selected-sample', 'title'),
)
def display_inspector(hoverData,
                      clickData,
                      n_clicks,

                      dataset,
                      number_of_samples,
                      dimensionality_method,
                      perplexity,
                      layer_idx,

                      data_instance,

                      prev_clickData,
                      selected_sample):
    result = [html.H5('Hover over or select a datapoint to see:'),
    html.H5('The corresponding image'),
    html.H5('The top 10 output probabilities, and explainability for the top label.'),]

    dataset_selected = dataset.lower()
    n_samples_selected = int(number_of_samples)
    method_selected = dimensionality_method.lower()
    perplexity_selected = int(perplexity)
    layer_idx_selected = int(layer_idx)
    selected_sample = int(selected_sample)
    hover_allowed = False


    instance_selected = {
        'dataset_selected': dataset_selected,
        'n_samples_selected': n_samples_selected,
        'method_selected': method_selected,
        'perplexity_selected': perplexity_selected,
        'layer_idx_selected': layer_idx_selected,
    }

    instance_selected_old = json.loads(data_instance)


    #if is_instance_changed(instance_selected, instance_selected_old):
    #    print('keikeboe')
    #    return result


    if selected_sample == -1:
        hover_allowed = True

    instance_key = Instance(
        dataset_selected,  # dataset
        n_samples_selected,  # n_samples
        layer_idx_selected,  # selected layer
        perplexity_selected,  # perplexity
        method_selected,
    )

    if hover_allowed:
        if isinstance(hoverData, dict):
            #print(hoverData)
            x = hoverData['points'][0]['x']
            y = hoverData['points'][0]['y']

            return render_inspector(instance_key, x, y)

    if isinstance(clickData, dict):
        x = clickData['points'][0]['x']
        y = clickData['points'][0]['y']

        return render_inspector(instance_key, x, y)

    return result



@app.callback(
    Output('layer-outputs', 'children'),
    Output('selected-sample', 'title'),
    Output('compute-sample', 'title'),
    Output('compute-button-view', 'style'),

    Output("instance", "data-instance"),


    Input('chart', 'clickData'),
    Input('cancel-button', 'n_clicks'),
    Input('compute-button', 'n_clicks'),


    Input('dataset-selection', 'value'),
    Input('number-of-samples', 'value'),
    Input('dimensionality-method', 'value'),
    Input('perplexity', 'value'),
    Input('result', 'selectedLayer'),



    State('dataset-selection', 'value'),
    State('number-of-samples', 'value'),
    State('dimensionality-method', 'value'),
    State('perplexity', 'value'),
    State('result', 'selectedLayer'),

    State('selected-sample', 'title'),
    State('compute-sample', 'title'),
    State('chart', 'clickData'),
    State('cancel-button', 'n_clicks'),
    State('compute-button', 'n_clicks'),

    prevent_initial_call=True,

)
def display_activation(clickData,
                       cancel_n_clicks,
                       compute_n_clicks,

                       a,
                       b,
                       c,
                       d,
                       e,

                       dataset,
                       number_of_samples,
                       dimensionality_method,
                       perplexity,
                       layer_idx,

                       selected_sample,
                       compute_sample,
                       prev_clickData,
                       prev_cancel_n_clicks,
                       prev_compute_n_clicks):

    result_no_selection = html.Div(id='layer-outputs-placeholder', className='layerOutputsPlaceHolderContainer', children=[
        html.H5('Select a datapoint, to see the outputs for the selected layer.'),
        html.H5('Tip: to see activations select a RELU layer.'),
    ]),

    #Move this to seprate div render if needed...
    result_compute = html.Div(className='layerOutputsNoComputationContainer', children=[
        html.H5('Activations for this sample have not been computed yet. Press below to compute.'),
        html.Div(className='computeButtonContainer', children=[
            html.Div(id='compute-button', className='buttonB', children=['Compute activations'])
        ]),
    ])

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]


    compute_button_view_inactive = {'display': 'none'}
    compute_button_view_active = {"display": "block"}

    #extract data

    dataset_selected = dataset.lower()
    n_samples_selected = int(number_of_samples)
    method_selected = dimensionality_method.lower()
    perplexity_selected = int(perplexity)
    layer_idx_selected = int(layer_idx)
    current_uid = int(selected_sample)

    instance_selected = {
        'dataset_selected' : dataset_selected,
        'n_samples_selected' : n_samples_selected,
        'method_selected' : method_selected,
        'perplexity_selected' : perplexity_selected,
        'layer_idx_selected' : layer_idx_selected,
    }

    instance_selected = json.dumps(instance_selected)

    #channel_index , score

    instance = Instance(
        dataset_selected,  # dataset
        n_samples_selected,  # n_samples
        layer_idx_selected,  # selected layer
        perplexity_selected,  # perplexity
        method_selected,
    )

    #If instance changed, revert to default

    instance_changed = False

    if is_instance_changed_via_input(triggered_id):
        print('instance changed , via change of input')
        return [result_no_selection, str(-1), str(-1), compute_button_view_inactive, instance_selected]


    if cancel_n_clicks:
        #deterimine if the cancel button was clicked
        if cancel_n_clicks != prev_cancel_n_clicks:
            print('cancel clicked and approved.')
            print(f'WEHEE : {cancel_n_clicks, clickData}')
            return [result_no_selection, str(-1), str(-1), compute_button_view_inactive, instance_selected]



    print('gooday')

    #selectionn happened
    if isinstance(clickData, dict):

        x = clickData['points'][0]['x']
        y = clickData['points'][0]['y']

        df = dim_red_dataframes[instance]
        sample = df.loc[(df['x'] == x) & (df['y'] == y)]


        # extract sample object
        sample = Sample(
            sample.index[0],
            sample['uid'].values[0],
            sample['label_id'].values[0],
            sample['label'].values[0],
            sample['category'].values[0],
            sample['img_path'].values[0],
            sample['correct_prediction'].values[0]
        )

        if triggered_id == 'compute-button':
                print('compute pressed')
                # time.sleep(3)

                return ['', str(sample.uid), str(1), compute_button_view_inactive, instance_selected]




        #sample has been clicked again unselect.
        if sample.uid == current_uid:
            print('sample has been clicked again')
            return [result_no_selection, str(-1),  str(-1), compute_button_view_inactive, instance_selected]
        else:

            #Check what type of activation
            if is_neuron_activation(instance):
                return ['', str(sample.uid), str(2), compute_button_view_inactive, instance_selected]

            else:

                if is_activation_available(instance, sample):

                    return ['', str(sample.uid),  str(2), compute_button_view_inactive, instance_selected]
                else:
                    #Show the button
                    return ['', str(sample.uid),  str(-1), compute_button_view_active, instance_selected]

    print(f'gooday: {clickData}')

    return [result_no_selection, str(-1), str(-1), compute_button_view_inactive, instance_selected]


# @app.callback(
#     Output('layer-outputs-data', 'children'),
#     Output('compute-sample', 'title'),
#
#     Input('compute-button', 'clickData'),
#     prevent_initial_call=True,
# )
# def handle_compute_button_press(clickData):





@app.callback(
    Output('layer-outputs-data', 'children'),
    Output('legend-activation', 'style'),

    Input('selected-sample', 'title'),
    Input('compute-sample', 'title'),
    #Input('compute-button', 'n_clicks'),
    Input('sort-method', 'value'),


    State('dataset-selection', 'value'),
    State('number-of-samples', 'value'),
    State('dimensionality-method', 'value'),
    State('perplexity', 'value'),
    State('result', 'selectedLayer'),
    State('sort-method', 'value'),
)
def display_activation_data(selected_sample,
                            compute_sample,
                            #compute_button_clicks,
                            sort_method_trigger,

                            dataset,
                            number_of_samples,
                            dimensionality_method,
                            perplexity,
                            layer_idx,
                            sort_method):
    #return render_neuron_activation(instance, sample)

    print('CALLED display activation')

    show_legend = {'display': 'block'}
    hide_legend = {'display': 'none'}

    dataset_selected = dataset.lower()
    n_samples_selected = int(number_of_samples)
    method_selected = dimensionality_method.lower()
    perplexity_selected = int(perplexity)
    layer_idx_selected = int(layer_idx)
    sort_method = sort_method.lower()



    if sort_method_trigger:
        sort_method = sort_method_trigger.lower()

    if sort_method == 'channel index':
        sort_method = 'id'

    current_uid = int(selected_sample)
    compute_sample = int(compute_sample)

    print(f'compute: {compute_sample}, sample: {current_uid}')

    if current_uid == -1:
        return [f'', hide_legend]


    compute_allowed = False
    activation_available = False



    if compute_sample == -1:
        activation_available = False
        compute_allowed = False
    elif compute_sample == 1:
        compute_allowed = True
        activation_available = False
    elif compute_sample == 2:
        activation_available = True
        compute_allowed = False


    #
    #
    #


    instance = Instance(
        dataset_selected,  # dataset
        n_samples_selected,  # n_samples
        layer_idx_selected,  # selected layer
        perplexity_selected,  # perplexity
        method_selected,
    )

    df = dim_red_dataframes[instance]
    sample = df.loc[(df['uid'] == current_uid)]

    # extract sample object
    sample = Sample(
        sample.index[0],
        sample['uid'].values[0],
        sample['label_id'].values[0],
        sample['label'].values[0],
        sample['category'].values[0],
        sample['img_path'].values[0],
        sample['correct_prediction'].values[0]
    )

    #
    #
    #


    #Compute triggerd
    if compute_allowed:
        time.sleep(5)
        #done computing
        compute_activations(sample, instance)
        activation_available = True

    #Display the activation
    if activation_available:
        #return f'ACTIVATION AVAILABLE'

        if is_neuron_activation(instance):
            return [render_neuron_activation(instance, sample), hide_legend]
        else:
            return [render_activations(instance, sample, sort_method), show_legend]


    return [f'', hide_legend]


def render_neuron_activation(instance: Instance, sample: Sample):
    #return html.Div(children=['RENDERED NEURON ACTIVATIONS'])
    print('render neuuron activation')

    data = get_neuron_activations(instance, sample)
    img_rgb = padded_2D_array(data, 100)
    custom_data_neuron_idx = padded_2D_array(np.arange(len(data)), 100)

    fig = px.imshow(img_rgb, text_auto=True)

    # Update hovertemplate to show value and index
    fig.update_traces(
        hovertemplate="Value: %{z:.2f}<br>Neuron index: %{customdata}<extra></extra>",
        customdata=(custom_data_neuron_idx)
    )

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Translucent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        title_font=dict(color='white'),  # Title color for dark mode
        font=dict(color='white'),  # Font color for labels and ticks
        xaxis=dict(
            tickfont=dict(color='white'),  # X-axis tick labels in white
            showgrid=False  # Hide the grid lines (optional)
        ),
        yaxis=dict(
            tickfont=dict(color='white'),  # Y-axis tick labels in white
            showgrid=False  # Hide the grid lines (optional)
        ),
        bargap=0.2,  # Adjust the space between bars
        template="plotly_dark"  # Use Plotly dark mode template
    )


    result = html.Div(className='neuronActivationContainer', children=[
        dcc.Graph(id='neuron-activation-chart', figure=fig, style={'width': '100%', 'height': '100%'}
)
    ])

    return result



def render_activations(instance: Instance,  sample: Sample, sort='id'):
    #Depending on the layer
    print('render activation')

    #return html.Div(children=['RENDERED ACTIVATIONS'])

    activation_image_elements = []

    for activation in get_activations(instance, sample, sort):
        element = html.Div(id={"type": "activation-channel", "index": activation.channel}, className='activationImageContainer',
                           children=[
                               html.Img(className='activationImage', src=activation.filepath_img),
                               html.Div(className='activationChannelInfo', children=[
                                   html.Div(className='channel', children=[str(activation.channel)]),
                                   html.Div(className='score', children=[str(activation.norm_score)])
                               ])
                           ])

        activation_image_elements.append(element)

    activations = html.Div(className='activationsViewContainer', children=[
        html.Div(className='activationsGridContainer', children=activation_image_elements)
    ])

    return activations








#instance same but the x and y valyues changed because czncel happned now on another layer// antoher instance -> solve
def render_inspector(instance: Instance, x, y):
    df = dim_red_dataframes[instance]

    sample = df.loc[(df['x'] == x) & (df['y'] == y)]

    # extract sample object

    sample = Sample(
        sample.index[0],
        sample['uid'].values[0],
        sample['label_id'].values[0],
        sample['label'].values[0],
        sample['category'].values[0],
        sample['img_path'].values[0],
        sample['correct_prediction'].values[0]
    )

    print(sample)

    #get top 10
    top10_filename = f'top10_{sample.uid}.csv'
    top10_df = pd.read_csv(os.path.join(instance.get_data_dir(), str(37), 'top10', top10_filename))

    # Step 1: Extract the category from the first row
    predicted_category = top10_df['category'].iloc[0]

    # Step 2: Sort the dataframe by 'prob' column in descending order
    top10_df_sorted = top10_df.sort_values(by='prob', ascending=True)

    # Step 3: Create a horizontal bar chart using Plotly
    top10_fig = px.bar(
        top10_df_sorted,
        x='prob',
        y='category',
        orientation='h',  # Horizontal bars
        labels={'prob': 'Probability', 'category': 'Category'},
        text='prob'  # Display probabilities on the bars
    )

    top10_fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Translucent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        title_font=dict(color='white'),  # Title color for dark mode
        font=dict(color='white'),  # Font color for labels and ticks
        xaxis=dict(
            tickfont=dict(color='white'),  # X-axis tick labels in white
            showgrid=False  # Hide the grid lines (optional)
        ),
        yaxis=dict(
            tickfont=dict(color='white'),  # Y-axis tick labels in white
            showgrid=False  # Hide the grid lines (optional)
        ),
        bargap=0.2,  # Adjust the space between bars
        template="plotly_dark"  # Use Plotly dark mode template
    )


    cam_path = os.path.join(instance.get_data_dir(), str(29), 'explainability', f'29_{sample.uid}_gradcam_cam.jpg')
    gb_path  = os.path.join(instance.get_data_dir(), str(29), 'explainability', f'29_{sample.uid}_gradcam_gb.jpg')
    cam_gb_path =  os.path.join(instance.get_data_dir(), str(29), 'explainability', f'29_{sample.uid}_gradcam_cam_gb.jpg')

    result = [

        html.H3('General'),
        html.Div(className='inspectorGeneralContainer', children=[
            html.H5(f'Inspecting uid: {sample.uid}', title=f'{sample.uid}'),
            html.Div(className='imageContainer', children=[
                html.Img(id='image', className='image', src=f'{sample.img_path}'),
            ]),
            html.H5(id='image-label', className='labelTitle', children=[f'True label: {sample.category}']),
            html.H5(id='image-label', className='', children=[f'Predicted label: {predicted_category}']),

            html.H3('Top 10 prediction'),

            html.Div(className='chartTop10', children=[
                dcc.Graph(id='chart-top10', figure=top10_fig)
            ]),
        ]),


        # scrollable container
        html.Div(className='explainabilityContainer', children=[
            html.H3('Explainability (via layer 29)'),

            html.H4('Class Activation Map'),
            html.Div(className='imageContainer', children=[
                html.Img(id='image', className='image', src=cam_path),
                ]),
            html.H4('Guided Back Propagation'),
            html.Div(className='imageContainer', children=[
                html.Img(id='image', className='image', src=gb_path),
                ]),
            html.H4('CAM + GBP'),
            html.Div(className='imageContainer', children=[
                html.Img(id='image', className='image', src=cam_gb_path),
                ]),
            # figure top 10
        ])
    ]

    return result






if __name__ == '__main__':
    app.run(debug=False)
