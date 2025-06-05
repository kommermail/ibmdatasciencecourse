# Dashboard Project for Car Sales at XYZ Automotive
# 
# Analyze the historical trends in automobile sales during recession periods,
# as I did in the previous part. The goal is to provide insights into how the
# sales of XYZAutomotives, a company specializing in automotive sales, were affected
# during times of recession.
#
# The dataset includes the following variables:
#     Date: The date of the observation.
#     Recession: A binary variable indicating recession perion; 1 means it was recession, 
#       0 means it was normal.
#     Automobile_Sales: The number of vehicles sold during the period.
#     GDP: The per capita GDP value in USD.
#     unemployment_rate: The monthly unemployment rate.
#     Consumer_Confidence: A synthetic index representing consumer confidence, which can 
#       impact consumer spending and automobile purchases.
#     Seasonality_Weight: The weight representing the seasonality effect on automobile sales during the period.
#     Price: The average vehicle price during the period.
#     Advertising_Expenditure: The advertising expenditure of the company.
#     Vehicle_Type: The type of vehicles sold; Supperminicar, Smallfamiliycar, 
#       Mediumfamilycar, Executivecar, Sports.
#     Competition: The measure of competition in the market, such as the number 
#       of competitors or market share of major manufacturers.
#     Month: Month of the observation extracted from Date.
#     Year: Year of the observation extracted from Date.
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Sales Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout =html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1(children='XYZ Automotive Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
    #TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[{'label':'Yearly Statistics','value':'Yearly Statistics'},
                    {'label':'Recession Period Statistics','value':'Recession Period Statistics'}],
            style={'width':280, 'padding': '3px', 'fontSize': 20, 'textAlignLast': 'center'},
            value=None,
            placeholder='Select a report type'
        )
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=None,
            placeholder='Select-year'
        )),
    html.Div([#TASK 2.3: Add a division for output display
    html.Div(id='output-container', className='chart-grid', style={'display':'flex'})])])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year',
     component_property='value')])

def update_output_container(selected_statistics, year):
    graphs = []
    recession_data = data.loc[data['Recession'] == 1]
    if not selected_statistics:
        return html.Div("Please select a report type.")
    if selected_statistics == 'Yearly Statistics' and not year:
        return html.Div("Please select a year.")


    if selected_statistics == 'Recession Period Statistics':

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].sum().reset_index()
        graphs.append(dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', 
                            title="Average Automobile Sales fluctuation over Recession Period")))
        # #graph2 vehicles sold by type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index()               
        graphs.append(dcc.Graph(figure=px.bar(average_sales,
                                x='Vehicle_Type',
                                y='Automobile_Sales',
                                title="Average Automobiles Sold by Vehicle Type")))
        # #graph3 expenditure share by vehicle type
        exp_rec= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        graphs.append(dcc.Graph(figure=px.pie(exp_rec,
                                values='Advertising_Expenditure',
                                names='Vehicle_Type',
                                title='Total Expenditure Share by Vehicle Type During Recession Periods')))
        # #graph4 unemployment effect on sales
        unemp_data = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].sum().reset_index()
        graphs.append(dcc.Graph(figure=px.bar(unemp_data,
                                x='Vehicle_Type',
                                y='Automobile_Sales',
                                labels={'unemployment_rate': 'unemployment rate', 'Automobile_Sales': 'Average Automobile Sales'},
                                title='Effect of Unemployment Rate on Vehicle Type and Sales')))
        return html.Div(graphs, style={'display': 'grid', 'grid-template-columns': 'repeat(2, 1fr)', 'gap': '20px'})

    if selected_statistics == 'Yearly Statistics' and year:
        yearly_data = data[data['Year'] == year]
        
        #graph1 yearly sales
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        graphs.append(dcc.Graph(figure=px.line(yas,
                                        x='Year',
                                        y='Automobile_Sales',
                                        title="Yearly Automobile Sales Over Time")))
        #graph2 monthly automobile sales
        mas=yearly_data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        graphs.append(dcc.Graph(figure=px.line(mas,
                                x='Month',
                                y='Automobile_Sales',
                                title='Total Monthly Automobile Sales')))
        #graph3 avg vehicles sold
        avr_vdata=yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        graphs.append(dcc.Graph(figure=px.bar(avr_vdata,
                                        x='Vehicle_Type',
                                        y='Automobile_Sales',
                                        title='Average Vehicles Sold in the year {}'.format(year))))
        #graph4 expenditure by vehicle type
        exp_data=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        graphs.append(dcc.Graph(figure=px.pie(exp_data,
                                        values='Advertising_Expenditure',
                                        names='Vehicle_Type',
                                            title='Advertisement Expenditure for Each Vehicle in {}'.format(year))))
        
        return html.Div(graphs, style={'display': 'grid', 'grid-template-columns': 'repeat(2, 1fr)', 'gap':'20px'})
    else:return html.Div("Select valid statistics option and year to display graphs.")

    # Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)