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
str_path_data = "sKor_data_tot_v02.csv"
df_raw = pd.read_csv(str_path_data)
df_raw.drop(columns=["Unnamed: 0"], inplace= True)
lst_var_labels = list(df_raw.columns)
lst_var_labels.pop(lst_var_labels.index("id_hh"))
lst_var_labels.pop(lst_var_labels.index("id_hs"))

# Column name lists for numerical and categorical variables.
lst_labels_num = [l for l in lst_var_labels if l.split("_")[0] == "num"]
lst_labels_cat = [l for l in lst_var_labels if l.split("_")[0] == "cat"]


# Application Set-Up.
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Empty Figure. 
fig_empty = go.Figure(
    layout_template = "plotly_dark",
    layout_paper_bgcolor = "#222222",
    layout_plot_bgcolor = "#222222", 
)

# BootStrap Components. CARDS
card_1 = dbc.Card(
    [        
        dbc.CardBody(
            [
                html.H4(
                    "1. Welcome!",
                    className= "card-title",
                ),
                html.P(
                    "Welcome to this web application! "
                    "This application will help you to exploer the data set used for the EDA (Energy Data Analysis) coursework! "
                    "EDA is a core module for the MSc. Energy Systems and Data Analytics at UCL. ",
                    className= "card-text",
                ),
                html.H4(
                    "2. Who we are...",
                    className= "card-title",
                ),
                html.P(
                    "We are \"One Team\" Group 8 for the EDA coursework (ESDA 21-22 cohort). "
                    "We are just three. But, our capability is far beyond four!", 
                    className= "card-text",
                ),
                html.H4(
                    "3. What data?",
                    className= "card-title",
                ),
                html.P(
                    "For the coursework, household energy consumption data from South Korea has been used. "
                    "This data encompasses various household characteristics for annual energy consumption as heat unit. ",
                    className= "card-text",
                ),
                html.P(                    
                    "You may not familiar with variable names in the data set. Please, refer to \"Table of Variables\" on the right hand side.",
                    className= "card-text",
                ),                                                  
            ],
        ),
    ],
    style= {"height": "100vh"},
    id= "card_1",
)

card_2 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4(
                    "4. This Application ...",
                    className= "card-title",
                ),
                html.P(
                    "This application consists of three tabs. "
                    "First one is what you are currently looking at for an introduction. "
                    "Second one is dedicated to provide you the scatter plot for numerical variables. "
                    "The last one is dedicated to provide you the box plot for categorical variables. "
                    "It is not difficult for you to understand how this application works. "
                    "But, please read \"5. How to use\" before you go to next tabs. ", 
                    className= "card-text",
                ),
                html.H4(
                    "5. How to use",
                    className= "card-title",
                ),
                html.P(
                    "For each tab for graphs, you will need to select several options in the left panel. "
                    "You need to select a variable to be shown as x-axis. "
                    "Then, you need to select a variable to be shown as y-axis. "
                    "After that, you need to select, at least one, hovering labels which will be shown when you hover your mouse on the data points. "
                    "At last, you finally need to push \"Plot with selections\" button to apply your selections. ", 
                    className= "card-text",
                ),                
            ],
        ),
    ],
    style= {"height": "100vh"},
    id= "card_2",
)

card_3 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4(
                    "UCL ESDA",
                    className= "card-title",
                ),                
                html.P(""),
                html.P(""),
                dbc.CardImg(src="./static/images/esda_banner.png"),
                html.P(""),
                html.P(""),
                dbc.CardImg(src="./static/images/esda_who.png"),
                html.P(""),
                html.P(""),
                dbc.CardImg(src="./static/images/esda_built.png"),
                html.P(""),
                html.P(""),
                dbc.CardImg(src="./static/images/esda_phil.png"),                       
            ],            
        ),
    ],
    style= {"height": "100vh"},
    id= "card_3",
)

card_4 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4(
                    "Table of variables",
                    className= "card-title",
                ),
                html.P(""),
                html.P(""),
                dbc.CardImg(src="./static/images/var_table.png"),                  
            ],            
        ),
    ],
    style= {"height": "100vh"},
    id= "card_4",
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
                            placeholder= "Choose Label X",
                            options=[{'label': i, 'value': i} for i in lst_labels_num],
                        ),
                        dcc.Dropdown(
                            id = "tab1_dd2_label_y",
                            className= "tab1_dropDowns",
                            placeholder= "Choose Label Y",
                            options=[{'label': i, 'value': i} for i in lst_labels_num],
                        ),
                        dcc.Dropdown(
                            id = "tab1_dd3_hoverLabel",
                            className= "tab1_dropDowns",
                            placeholder= "Choose hovering Labels",
                            options=[{'label': i, 'value': i} for i in lst_var_labels],
                            multi= True,
                        ),
                        dbc.Button(
                            "Plot with seletions",
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
# BootStrap Components. TAB2.
tab2_content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id = "tab2_dd1_label_x",
                            className= "tab2_dropDowns",
                            placeholder= "Choose Label X",
                            options=[{'label': i, 'value': i} for i in lst_labels_cat],
                        ),
                        dcc.Dropdown(
                            id = "tab2_dd2_label_y",
                            className= "tab2_dropDowns",
                            placeholder= "Choose Label Y",
                            options=[{'label': i, 'value': i} for i in lst_labels_num],
                        ),
                        dcc.Dropdown(
                            id = "tab2_dd3_hoverLabel",
                            className= "tab2_dropDowns",
                            placeholder= "Choose hovering Labels",
                            options=[{'label': i, 'value': i} for i in lst_var_labels],
                            multi= True,
                        ),
                        dbc.Button(
                            "Plot with seletions",
                            id = "button_tab2_plt",
                            className= "tab2_buttons",
                            color= "warning",                            
                            disabled= True,
                        ),
                    ],
                    width = {"size" : 2},
                    id = "tab2_row1_col1"
                ),
                dbc.Col(
                    [
                        dbc.Spinner(children= [dcc.Graph(id = "mainBox", figure= fig_empty)],),                                                
                    ],
                    width = {"size" : 5},
                    id = "tab2_row1_col2",
                    align = "center"
                ),                
                dbc.Col(
                    [
                        dbc.Spinner(children= [dcc.Graph(id = "tab2_dist_x", figure= fig_empty)],),
                        dbc.Spinner(children= [dcc.Graph(id = "tab2_dist_y", figure= fig_empty)],),
                    ],
                    width = {"size" : 5},
                    id = "tab2_row1_col3",
                    align = "center",
                ),
            ],
            id = "tab2_row1"
        ),
    ]
)

# BoostStrap Components. TAB_INTRO.
tab_intro = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(                    
                    width= 1,
                ),
                dbc.Col(
                    card_3,
                    width= 2,
                ),                          
                dbc.Col(
                    card_1,
                    width= 2,
                ),
                dbc.Col(
                    card_2,
                    width= 2,
                ),
                dbc.Col(
                    card_4,
                    width= 4,
                ),                
            ],
            style= {"padding":"15px"},
        ),
    ],
)

# Application Set-Up.
app.layout = html.Div(
    [        
        dbc.Tabs(
            [
                dbc.Tab(tab_intro, label = "INTRODUCTION"),
                dbc.Tab(tab1_content, label = "SCATTER_EXPLORER"),
                dbc.Tab(tab2_content, label = "BOX_EXPLORER"),
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

# Function to have simple dist plotting.
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

# Function to have simple box plotting.
def plt_mainBox (in_label_x, in_label_y, in_hover, in_df, in_lst_cat):
    
    import pandas as pd
    import plotly.express as px
    
    in_df[in_lst_cat] = in_df[in_lst_cat].astype("category")
    
    # Hover data setting.        
    if in_hover:
        hoverLabel = { str(i):":.5g" for i in in_hover}
    else:
        hoverLabel = {}    
    
    fig = px.box(
        in_df,
        x= in_label_x,
        y= in_label_y,
        color= in_label_x,
        hover_name= "id_hs",
        hover_data= hoverLabel,
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
    
@app.callback(
    Output("button_tab2_plt", "disabled"),
    [
        Input("tab2_dd1_label_x", "value"),
        Input("tab2_dd2_label_y", "value"),
        Input("tab2_dd3_hoverLabel", "value"),
    ],        
)
def tab2_activate_plot_button (in_label_x, in_label_y, in_hover):
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
    
@app.callback(
    Output("mainBox", "figure"),
    Output("tab2_dist_x", "figure"),
    Output("tab2_dist_y", "figure"),
    Input("button_tab2_plt","n_clicks"),    
    [
        State("tab2_dd1_label_x", "value"),
        State("tab2_dd2_label_y", "value"),
        State("tab2_dd3_hoverLabel", "value"),
    ],        
)
def tab1_trig_ploting (in_nClicks_plt, in_label_x, in_label_y, in_hover):
    if in_nClicks_plt:
        fig_mainBox = plt_mainBox(in_label_x, in_label_y, in_hover, df_raw, lst_labels_cat)
        fig_tab2_dist_x = plt_dist_aux(in_label_x, df_raw)
        fig_tab2_dixt_y = plt_dist_aux(in_label_y, df_raw)
        return fig_mainBox, fig_tab2_dist_x, fig_tab2_dixt_y
    else:
        return [dash.no_update]*3


if __name__ == '__main__':
    app.run_server(debug=True)