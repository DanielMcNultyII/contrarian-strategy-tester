# Daniel McNulty II


import pandas as pd
import numpy as np
import yfinance as yf
from dash_table import DataTable, FormatTemplate
import plotly.graph_objs as go


def generic_tbl_fmt(df):
    return DataTable(
            columns=[{'name': i, 'id': i, 'type': 'numeric', 'format': FormatTemplate.percentage(4)} for i in
                     df.columns],
            data=df.to_dict('records'),
            style_cell={
                'textAlign': 'center',
                'whiteSpace': 'normal',
                'height': 'auto',
                'color': 'white',
                'backgroundColor': '#696969',
            },
            style_header={'backgroundColor': '#000000'},
            style_data_conditional=[
                {
                    'if': {
                        'state': 'active'  # 'active' | 'selected'
                    },
                    'backgroundColor': '#8140CF'
                }
            ],
            style_as_list_view=True,
            page_size=20,
            export_format='csv',
            style_table={'overflowX': 'auto'}
    )


def contrarian_portfolio_tbl_fmt(df):
    return DataTable(
            columns=[{'name': i, 'id': i, 'type': 'numeric', 'format': FormatTemplate.percentage(4)} for i in
                     df.columns],
            data=df.to_dict('records'),
            style_cell={
                'textAlign': 'center',
                'whiteSpace': 'normal',
                'height': 'auto',
                'color': 'white',
                'backgroundColor': '#696969',
            },
            style_header={'backgroundColor': '#000000'},
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{{Portfolio Daily Return}} < {}'.format(0.00),
                    },
                    'backgroundColor': '#FF4136',
                },
                {
                    'if': {
                        'filter_query': '{{Portfolio Daily Return}} > {}'.format(0.00),
                    },
                    'backgroundColor': '#3cb371',
                },
                {
                    'if': {
                        'state': 'active'  # 'active' | 'selected'
                    },
                    'backgroundColor': '#696969',
                    'border': '#ffffff',
                }
            ],
            style_as_list_view=True,
            page_size=20,
            export_format='csv',
            style_table={'overflowX': 'auto'}
    )


def sum_stat_tbl_fmt(df):
    return DataTable(
        columns=[{'name': i, 'id': i, 'type': 'numeric', 'format': FormatTemplate.percentage(4)} for i in
                 df.columns],
        data=df.to_dict('records'),
        style_cell={
            'textAlign': 'center',
            'whiteSpace': 'normal',
            'height': 'auto',
            'color': 'white',
            'backgroundColor': '#696969',
        },
        style_header={'backgroundColor': '#000000'},
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{{Annualized Sharpe Ratio}} < {}'.format(0.00),
                },
                'backgroundColor': '#FF4136',
            },
            {
                'if': {
                    'filter_query': '{{Annualized Sharpe Ratio}} > {}'.format(0.00),
                },
                'backgroundColor': '#3cb371',
            },
            {
                'if': {
                    'state': 'active'  # 'active' | 'selected'
                },
                'backgroundColor': '#696969',
                'border': '#ffffff',
            }
        ],
        style_as_list_view=True,
    )


def yrly_sum_stat_tbl_fmt(df):
    return DataTable(
        columns=[{'name': 'Year', 'id': 'Date'},
                 {'name': 'Average Daily Return', 'id': 'Average Daily Return', 'type': 'numeric',
                  'format': FormatTemplate.percentage(4)},
                 {'name': 'Standard Deviation of Daily Returns', 'id': 'Standard Deviation of Daily Returns',
                  'type': 'numeric', 'format': FormatTemplate.percentage(4)},
                 {'name': 'Annualized Average Daily Return', 'id': 'Annualized Average Daily Return',
                  'type': 'numeric', 'format': FormatTemplate.percentage(4)},
                 {'name': 'Annualized Standard Deviation of Daily Returns',
                  'id': 'Annualized Standard Deviation of Daily Returns',
                  'type': 'numeric', 'format': FormatTemplate.percentage(4)},
                 {'name': 'Annualized Sharpe Ratio',
                  'id': 'Annualized Sharpe Ratio',
                  'type': 'numeric', 'format': FormatTemplate.percentage(4)}
                 ],
        data=df.to_dict('records'),
        style_cell={
            'textAlign': 'center',
            'whiteSpace': 'normal',
            'height': 'auto',
            'color': 'white',
            'backgroundColor': '#696969',
        },
        style_header={'backgroundColor': '#000000'},
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{{Annualized Sharpe Ratio}} < {}'.format(0.00),
                },
                'backgroundColor': '#FF4136',
            },
            {
                'if': {
                    'filter_query': '{{Annualized Sharpe Ratio}} > {}'.format(0.00),
                },
                'backgroundColor': '#3cb371',
            },
            {
                'if': {
                    'state': 'active'  # 'active' | 'selected'
                },
                'backgroundColor': '#696969',
                'border': '#ffffff',
            }
        ],
        style_as_list_view=True,
        export_format='csv',
    )


def daily_return(tickers, start_date, end_date):
    sel = [yf.Ticker(i) for i in tickers]

    hist_list = [i.history(start=start_date, end=end_date)['Close'] for i in sel]
    hist_df = pd.DataFrame(hist_list).transpose()
    hist_df.columns = tickers

    daily_ret = hist_df.pct_change(1).iloc[1:]

    return daily_ret


def contrarian_portfolio_ret(daily_ret):
    excess_ret = daily_ret.sub(daily_ret.mean(axis=1), axis=0)
    er_dimensions = excess_ret.shape

    weights = excess_ret.apply(lambda x: -x / er_dimensions[1], axis=1).shift(1).iloc[1:]
    collateral = abs(weights).apply(sum, axis=1) / 2

    strat_ret = [daily_ret.iloc[i + 1].dot(weights.iloc[i]) / collateral.iloc[i] if collateral.iloc[i] != 0.0
                 else 0.0 for i in range(0, er_dimensions[0] - 1)]

    results_df = weights
    results_df['Collateral Needed'] = collateral
    results_df['Portfolio Daily Return'] = strat_ret

    daily_ret = daily_ret.reset_index()
    daily_ret['Date'] = daily_ret['Date'].dt.date

    excess_ret = excess_ret.reset_index()
    excess_ret['Date'] = excess_ret['Date'].dt.date

    results_df = results_df.reset_index()
    results_df['Date'] = results_df['Date'].dt.date

    return daily_ret, excess_ret, results_df


def lin_plt(sel_hist):
    lin_cht = go.Figure(data=[go.Scatter(x=sel_hist.Date, y=sel_hist['Portfolio Daily Return'],
                                         name='Portfolio Daily Return', line={'color': 'blue'}, showlegend=True)])

    lin_cht.add_hline(y=0, line={'color': 'black'})

    lin_cht.update_layout(
        xaxis_title='Date',
        hovermode='x',
        yaxis={'tickformat': ',.0%'},
        margin=go.layout.Margin(
            l=0,  # left margin
            r=0,  # right margin
            b=50,  # bottom margin
            t=50,  # top margin
        ),
    )

    lin_cht.update_xaxes(rangeslider_visible=True)

    return lin_cht


def ann_plt(sel_sum):
    fig = go.Figure(data=[go.Scatter(x=sel_sum.Date, y=sel_sum['Annualized Standard Deviation of Daily Returns'],
                                     name='Annualized Standard Deviation of Daily Returns', line={'color': 'red'},
                                     showlegend=True)])

    fig.add_bar(x=sel_sum.Date, y=sel_sum['Annualized Average Daily Return'], name='Annualized Average Daily Return',
                marker={'color': 'blue'}, showlegend=True)

    fig.add_hline(y=0, line={'color': 'black'})

    fig.update_layout(
        xaxis_title='Year',
        hovermode='x',
        xaxis={'tickformat': 'd'},
        yaxis={'tickformat': ',.0%'},
        margin=go.layout.Margin(
            l=0,  # left margin
            r=0,  # right margin
            b=50,  # bottom margin
            t=50,  # top margin
        ),
    )

    return fig


def summary_stats(sel_hist, trading_days):
    trading_days = float(trading_days)
    avg_daily_ret = np.average(sel_hist['Portfolio Daily Return'])
    std_dev_daily_ret = np.std(sel_hist['Portfolio Daily Return'], ddof=1)

    sum_stats = pd.DataFrame({'Average Daily Return': [avg_daily_ret],
                              'Standard Deviation of Daily Returns': [std_dev_daily_ret],
                              'Annualized Average Daily Return': [avg_daily_ret * trading_days],
                              'Annualized Standard Deviation of Daily Returns': [std_dev_daily_ret*np.sqrt(trading_days)],
                              'Annualized Sharpe Ratio': [(avg_daily_ret/std_dev_daily_ret)*np.sqrt(trading_days)]})

    return sum_stats


def yearly_summaries(sel_hist, trading_days):
    trading_days = float(trading_days)
    sel_hist['Date'] = pd.to_datetime(sel_hist['Date'])
    yr_groups = sel_hist['Portfolio Daily Return'].groupby(sel_hist['Date'].dt.year)
    sum_stats = pd.DataFrame({'Date': yr_groups.mean().index,
                              'Average Daily Return': yr_groups.mean(),
                              'Standard Deviation of Daily Returns': yr_groups.std(ddof=1)})

    sum_stats['Annualized Average Daily Return'] = sum_stats['Average Daily Return'] * trading_days
    sum_stats['Annualized Standard Deviation of Daily Returns'] = sum_stats['Standard Deviation of Daily Returns'] * np.sqrt(trading_days)
    sum_stats['Annualized Sharpe Ratio'] = sum_stats['Average Daily Return'].divide(sum_stats['Standard Deviation of Daily Returns'])*np.sqrt(trading_days)

    return sum_stats
