''# Daniel McNulty II


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from datetime import datetime
from dateutil.relativedelta import relativedelta
from functions import daily_return, contrarian_portfolio_ret, contrarian_portfolio_tbl_fmt, lin_plt, summary_stats, \
                      sum_stat_tbl_fmt, generic_tbl_fmt, yearly_summaries, yrly_sum_stat_tbl_fmt, ann_plt


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, prevent_initial_callbacks=True, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
             html.Div(className='header', children=[
                 html.H1('Contrarian Strategy Tester', style={'margin': '0%'})]
             ),
             html.Div(className='column1', children=[
                 html.H3('Settings'),
                 html.H5('Ticker List'),
                 dcc.Textarea(
                        id='ticker_list',
                        placeholder='Input stock tickers separated by a comma (ie. AAPL,TSLA,AMZN)',
                        style={'width': '100%', 'display': 'block'}
                 ),
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
                 html.H5('Trading Days per Year'),
                 dcc.Input(id='trading_days', style={'display': 'block'}),
                 dbc.Button("Run Contrarian Strategy", id='run', outline=True, block=True),
             ]
             ),
             html.Div(className='column2', children=[
                 html.H3('Summary Statistics'),
                 dcc.Loading(id='load-stats', children=[html.Div(id='summary-stats')], type='circle'
                 ),
                 html.H3('Historic Portfolio Returns'),
                 dcc.Loading(id='load-graph', children=[
                         dcc.Tabs([
                             dcc.Tab(label='Daily Stock Returns', children=[dcc.Graph(id='dret_graph')]),
                             dcc.Tab(label='Annualized Daily Stock Returns and Standard Deviations of Daily Stock Returns',
                                     children=[dcc.Graph(id='ann_graph')]),
                     ])], type='circle'),
                 html.H3('Historical Data'),
                 dcc.Loading(id='load-res', children=[
                     dcc.Tabs([
                         dcc.Tab(label='Daily Stock Returns', id='dret'),
                         dcc.Tab(label='Pearson Correlations of Daily Stock Returns', id='retcorr'),
                         dcc.Tab(label='Daily Weights, Collateral, and Portfolio Returns', id='dwcr'),
                         dcc.Tab(label='Summary Statistics by Year', id='ssby')
                     ])
                 ], type='circle')],
                 )
             ])


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
    dr = daily_return(str(ticker_list).replace(' ', '').split(','), start_date, end_date)
    res_wts_ret = contrarian_portfolio_ret(dr)
    sum_stats = summary_stats(res_wts_ret[2], trading_days)
    yrly_sum_stats = yearly_summaries(res_wts_ret[2], trading_days)

    res_wts_ret[2]['Date'] = res_wts_ret[2]['Date'].dt.date

    dcorr = dr.corr(method = 'pearson', min_periods = 1).reset_index()
    dcorr = dcorr.rename(columns = {'index': ''})

    return [sum_stat_tbl_fmt(sum_stats)], lin_plt(res_wts_ret[2]), ann_plt(yrly_sum_stats), \
           [generic_tbl_fmt(res_wts_ret[0])], [generic_tbl_fmt(dcorr)], \
           [contrarian_portfolio_tbl_fmt(res_wts_ret[2])], [yrly_sum_stat_tbl_fmt(yrly_sum_stats)]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)
