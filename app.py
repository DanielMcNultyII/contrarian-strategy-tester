'''
Daniel McNulty II

User interface code for the contrarian strategy tester.
'''

# Import necessary libraries and functions.
import os
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from datetime import datetime
from dateutil.relativedelta import relativedelta
from functions import daily_return, contrarian_portfolio_ret, contrarian_portfolio_tbl_fmt, lin_plt, summary_stats, \
                      sum_stat_tbl_fmt, generic_tbl_fmt, yearly_summaries, yrly_sum_stat_tbl_fmt, ann_plt
import math

# Set the external stylesheet reference.
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Initialize the app, not calling the callbacks upon initialization.
app = dash.Dash(__name__, prevent_initial_callbacks=True, external_stylesheets=external_stylesheets)
server = app.server

# Define the app layout.
app.layout = html.Div(children=[
             # Header with "Contrarian Strategy Tester" header.
             html.Div(className='header', children=[
                 html.H1('Contrarian Strategy Tester', style={'margin': '0%'})]
             ),
             # The first (left-most) column where users will enter inputs and where the run strategy button to run the
             # callback is placed.
             html.Div(className='column1', children=[
                 html.H3('Settings'),
                 # Ticker input
                 html.H5('Ticker List'),
                 dcc.Textarea(
                        id='ticker_list',
                        placeholder='Input stock tickers separated by a comma (ie. AAPL,TSLA,AMZN)',
                        style={'width': '100%', 'display': 'block'}
                 ),
                 # Date range input.
                 html.H5('Date Range'),
                 dcc.DatePickerRange(
                        id='date_range',
                        max_date_allowed=datetime.now() - relativedelta(days=1),
                        initial_visible_month=datetime.now() - relativedelta(days=1000),
                        start_date=(datetime.now() - relativedelta(days=1000)).date(),
                        end_date=(datetime.now() - relativedelta(days=1)).date(),
                        updatemode='singledate',
                        style={'display': 'block'}
                 ),
                 # Trading days per year input.
                 html.H5('Trading Days per Year'),
                 dcc.Input(id='trading_days', style={'display': 'block'}),
                 # Button to press in order to initiate callback.
                 dbc.Button("Run Contrarian Strategy", id='run', outline=True)
             ]
             ),
             # The first (right-most) column where output from the callback will be displayed.
             html.Div(className='column2', children=[
                 # Summary statistics display. Displays a loading circle while callback is running.
                 html.H3('Summary Statistics'),
                 dcc.Loading(id='load-stats', children=[html.Div(id='summary-stats')], type='circle'
                 ),
                 # Historic strategy return plots display. Displays a loading circle while callback is running.
                 html.H3('Historic Strategy Returns'),
                 dcc.Loading(id='load-graph', children=[
                         dcc.Tabs([
                             dcc.Tab(label='Daily Strategy Returns', children=[dcc.Graph(id='dret_graph')]),
                             dcc.Tab(label='Annualized Daily Strategy Returns and Standard Deviations of Daily Strategy Returns',
                                     children=[dcc.Graph(id='ann_graph')]),
                     ])], type='circle'),
                 # Historical data tables display. Displays a loading circle while callback is running.
                 html.H3('Historical Data'),
                 dcc.Loading(id='load-res', children=[
                     dcc.Tabs([
                         dcc.Tab(label='Daily Stock Returns', id='dret'),
                         dcc.Tab(label='Pearson Correlations of Daily Stock Returns', id='retcorr'),
                         dcc.Tab(label='Daily Weights, Collateral, and Strategy Returns', id='dwcr'),
                         dcc.Tab(label='Summary Statistics by Year', id='ssby')
                     ])
                 ], type='circle')],
                 )
             ])
'''
Callback which calls function update dashboard that takes user input tickers, date range, and trading days per year and 
outputs the results of using a contrarian strategy with said inputs to the dash app. Results include:
    - A summary statistics table with average daily return, standard deviation of daily returns, annualized daily 
      returns, annualized standard deviation of daily returns, and sharpe ratio of the strategy
    - A line plot of the strategy's daily returns
    - A line plot of the strategy's annualized standard deviation of the strategy's daily returns overlaid on a bar plot
      of the strategy's annualized average daily returns for each year of the selected date range.
    - Exportable tables with 
            > The chosen stocks' daily returns
            > The Pearson correlations of the chosen stocks' daily returns
            > The daily calculated weights for each stock, required collateral, and strategy return
            > The summary statistics from before by year. 
      These tables export in csv format. The rows of the daily calculated weights for each stock, required collateral, 
      and strategy return and the summary statistics from before by year tables are highlighted red when there is a loss
      that day and green when there is a gain that day.
'''
@app.callback(
    [Output(component_id='summary-stats', component_property='children'),
     Output(component_id='dret_graph', component_property='figure'),
     Output(component_id='ann_graph', component_property='figure'),
     Output(component_id='dret', component_property='children'),
     Output(component_id='retcorr', component_property='children'),
     Output(component_id='dwcr', component_property='children'),
     Output(component_id='ssby', component_property='children')],
    [Input(component_id='run', component_property='n_clicks')],
    [State(component_id='ticker_list', component_property='value'),
     State(component_id='date_range', component_property='start_date'),
     State(component_id='date_range', component_property='end_date'),
     State(component_id='trading_days', component_property='value')]
)
def update_dashboard(click, ticker_list, start_date, end_date, trading_days):
    # Establish error handling with try/except block.
    try:
        # Take user-entered string of tickers and convert it to a list. If the resulting list only has a length of 1,
        # raise an exception.
        ticks = str(ticker_list).replace(' ', '').split(',')
        if len(ticks) <= 1:
            raise Exception('ERROR - More than 1 ticker must be used')

        # Call function daily_return to collect the return data for all input tickers. Then test whether there are any
        # NaN values in the return data collected. If there are, raise an exception and let the user know which tickers
        # have missing or incomplete data (Have NaNs or blanks in their returns).
        dr = daily_return(ticks, start_date, end_date)
        ret_test = {l: any(math.isnan(i) for i in dr[l]) for l in ticks}
        if True in ret_test.values():
            ticks_missing_data = [i for i in ret_test if ret_test[i] is True]
            raise ValueError('ERROR - Missing or incomplete data found for the following tickers: ' + \
                             str(ticks_missing_data).replace('[', '').replace(']', '').replace("'",'') + \
                             '. Please confirm the ticker existed for all dates in the date range specified and try again.')

        # Run the contrarian strategy using the daily returns collected and stored into dr.
        res_wts_ret = contrarian_portfolio_ret(dr)
        # Take the returns of the contrarian strategy and calculate the overall summary statistics. These include
        # average daily return, standard deviation of daily returns, annualized daily returns, annualized standard
        # deviation of daily returns, and annualized sharpe ratio of the strategy.
        sum_stats = summary_stats(res_wts_ret[2], trading_days)
        # Take the returns of the contrarian strategy and calculate the summary statistics for each year. These include
        # average daily return, standard deviation of daily returns, annualized daily returns, annualized standard
        # deviation of daily returns, and annualized sharpe ratio of the strategy.
        yrly_sum_stats = yearly_summaries(res_wts_ret[2], trading_days)

        # Determine the Pearson correlation between the returns of each ticker.
        res_wts_ret[2]['Date'] = res_wts_ret[2]['Date'].dt.date
        dcorr = dr.corr(method = 'pearson', min_periods = 1).reset_index()
        dcorr = dcorr.rename(columns = {'index': ''})

        # Return the summary statistics table, contrarian strategy daily return line plot, contrarian strategy
        # annualized daily returns and annualized standard deviations of the contrarian strategy daily returns plot,
        # the tickers' daily stock returns table, the Pearson correlations table, the daily weights, collateral, and
        # contrarian strategy returns table, and the summary statistics by year table.
        return [sum_stat_tbl_fmt(sum_stats)], lin_plt(res_wts_ret[2]), ann_plt(yrly_sum_stats), \
               [generic_tbl_fmt(res_wts_ret[0])], [generic_tbl_fmt(dcorr)], \
               [contrarian_portfolio_tbl_fmt(res_wts_ret[2])], [yrly_sum_stat_tbl_fmt(yrly_sum_stats)]

    # If an exception is raised, print the exception message to the dash app and leave the plot elements blank.
    except Exception as e:
        return [str(e)], {}, {}, \
               [str(e)], \
               [str(e)], \
               [str(e)], \
               [str(e)]


# Run the app.
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
