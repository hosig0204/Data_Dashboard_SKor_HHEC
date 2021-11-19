# Import necessary modules
import os
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Some modules for graping.
import plotly.graph_objects as go

# Module for DataFrame.
import pandas as pd

# Import DataFrame.
str_path_data = "C:/PythonProject/EDA-Project/data/sKor_data_v01.csv"
df_raw = pd.read_csv(str_path_data)
df_raw.drop(columns=["Unnamed: 0"], inplace= True)
lst_var_labels = list(df_raw.columns)
lst_var_labels.pop(lst_var_labels.index("id_hh"))
lst_var_labels.pop(lst_var_labels.index("id_hs"))

# Application Set-Up.
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Empty Figure. 
fig_empty = go.Figure(
    layout_template = "plotly_dark",
    layout_paper_bgcolor = "#222222",
    layout_plot_bgcolor = "#222222", 
)

# BootStrap Components. TAB1.
tab1_content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id = "tab1_dd1_label_x",
                            className= "tab1_dropDowns",
                            placeholder= "Choose Label.",
                            options=[{'label': i, 'value': i} for i in lst_var_labels],
                        ),
                        dcc.Dropdown(
                            id = "tab1_dd2_label_y",
                            className= "tab1_dropDowns",
                            placeholder= "Choose Label.",
                            options=[{'label': i, 'value': i} for i in lst_var_labels],
                        ),
                        dcc.Dropdown(
                            id = "tab1_dd3_hoverLabel",
                            className= "tab1_dropDowns",
                            placeholder= "Choose hovering Labels.",
                            options=[{'label': i, 'value': i} for i in lst_var_labels],
                            multi= True,
                        ),
                        dbc.Button(
                            "Load to Plotting",
                            id = "button_tab1_plt",
                            className= "tab1_buttons",
                            color= "warning",                            
                            disabled= True,
                        ),
                    ],
                    width = {"size" : 2},
                    id = "tab1_row1_col1"
                ),
                dbc.Col(
                    [
                        dbc.Spinner(children= [dcc.Graph(id = "mainScatter", figure= fig_empty)],),                                                
                    ],
                    width = {"size" : 5},
                    id = "tab1_row1_col2",
                    align = "center"
                ),                
                dbc.Col(
                    [
                        dbc.Spinner(children= [dcc.Graph(id = "dist_x", figure= fig_empty)],),
                        dbc.Spinner(children= [dcc.Graph(id = "dist_y", figure= fig_empty)],),
                    ],
                    width = {"size" : 5},
                    id = "tab1_row1_col3",
                    align = "center",
                ),
            ],
            id = "tab1_row1"
        ),
    ]
)

# Application Set-Up.
app.layout = html.Div(
    [        
        dbc.Tabs(
            [
                dbc.Tab(tab1_content, label = "SCATTER_EXPLORER"),
                # dbc.Tab(tab2_content, label = "TBD_02"),
                # dbc.Tab(tab3_content, label = "TBD_03"),                
            ],
        ),        
    ],
    id = "mainContainer",
)

# Function to have simple scatter plotting.
def plt_mainScatter(in_label_x, in_label_y, in_hover, in_df):
    
    import pandas as pd
    import plotly.express as px
    
    # Hover data setting.
        
    if in_hover:
        hoverLabel = { str(i):":.5g" for i in in_hover}
    else:
        hoverLabel = {}
    
    # Create figure.
    
    fig = px.scatter(
        in_df,
        x = in_label_x,
        y= in_label_y,
        hover_name= "id_hs",
        hover_data= hoverLabel,
    )

    fig.update_layout(
        template = "plotly_dark",
        paper_bgcolor = "#222222",
        plot_bgcolor = "#222222",
    )
    
    return fig

# Function to have simple 
def plt_dist_aux(in_label, in_df):
    
    import pandas as pd
    import plotly.express as px    
    
    fig = px.histogram(
        in_df,
        x= in_label,
        title= in_label,
    )
    
    fig.update_layout(
        template = "plotly_dark",
        paper_bgcolor = "#222222",
        plot_bgcolor = "#222222",
    )
    
    return fig
    
# Call-back to activate plotting button.
@app.callback(
    Output("button_tab1_plt", "disabled"),
    [
        Input("tab1_dd1_label_x", "value"),
        Input("tab1_dd2_label_y", "value"),
        Input("tab1_dd3_hoverLabel", "value"),
    ],        
)
def tab1_activate_plot_button (in_label_x, in_label_y, in_hover):
    if in_hover:        
        if (
            in_label_x == None or
            in_label_y == None or
            in_label_x == "None" or
            in_label_y == "None" 
            ):
            return True
        else:
            return False
    else:
        return True
    
# Call-back to trigger plotting.
@app.callback(
    Output("mainScatter", "figure"),
    Output("dist_x", "figure"),
    Output("dist_y", "figure"),
    Input("button_tab1_plt","n_clicks"),    
    [
        State("tab1_dd1_label_x", "value"),
        State("tab1_dd2_label_y", "value"),
        State("tab1_dd3_hoverLabel", "value"),
    ],        
)
def tab1_trig_ploting (in_nClicks_plt, in_label_x, in_label_y, in_hover):
    if in_nClicks_plt:
        fig_mainScatter = plt_mainScatter(in_label_x, in_label_y, in_hover, df_raw)
        fig_dist_x = plt_dist_aux(in_label_x, df_raw)
        fig_dixt_y =plt_dist_aux(in_label_y, df_raw)
        return fig_mainScatter, fig_dist_x, fig_dixt_y
    else:
        return [dash.no_update]*3


if __name__ == '__main__':
    app.run_server(debug=True)