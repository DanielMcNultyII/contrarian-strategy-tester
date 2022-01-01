'''
Daniel McNulty II

Functions needed for the contrarian strategy tester.
'''

# Import necessary libraries and functions.
import pandas as pd
import numpy as np
import yfinance as yf
from dash.dash_table import DataTable, FormatTemplate
import plotly.graph_objs as go

# Function that takes in a dataframe and outputs it as a dash DataTable with a specific format.
def generic_tbl_fmt(df):
    # Return a DataTable
    return DataTable(
            # Create a column in the DataTable for each column in the input dataframe.
            columns=[{'name': i, 'id': i, 'type': 'numeric', 'format': FormatTemplate.percentage(4)} for i in
                     df.columns],
            # Set the data of the DataTable to the data in the df.
            data=df.to_dict('records'),
            # Set cell formatting to use center aligned text, a gray background, and white font color.
            style_cell={
                'textAlign': 'center',
                'whiteSpace': 'normal',
                'height': 'auto',
                'color': 'white',
                'backgroundColor': '#696969',
            },
            # Make the DataTable header background black.
            style_header={'backgroundColor': '#000000'},
            # Style conditional that makes the background of any cell clicked on in the DataTable purple to
            # differentiate it from the gray background of other cells.
            style_data_conditional=[
                {
                    'if': {
                        'state': 'active'  # 'active' | 'selected'
                    },
                    'backgroundColor': '#8140CF'
                }
            ],
            # Style the DataTable like a list view, not putting borders between columns.
            style_as_list_view=True,
            # Show 20 rows of the DataTable at a time.
            page_size=20,
            # Allow for the DataTable to be exported to a csv file.
            export_format='csv',
            # Provide an X-axis scrollbar for desktop browsers if the content in a DataTable overflows.
            style_table={'overflowX': 'auto'}
    )

# Function that takes in a dataframe and outputs it as a dash DataTable with a specific format designed for the daily
# weights, collateral, and strategy returns table.
def contrarian_portfolio_tbl_fmt(df):
    # Return a DataTable
    return DataTable(
            # Create a column in the DataTable for each column in the input dataframe.
            columns=[{'name': i, 'id': i, 'type': 'numeric', 'format': FormatTemplate.percentage(4)} for i in
                     df.columns],
            # Set the data of the DataTable to the data in the df.
            data=df.to_dict('records'),
            # Set cell formatting to use center aligned text, a gray background, and white font color.
            style_cell={
                'textAlign': 'center',
                'whiteSpace': 'normal',
                'height': 'auto',
                'color': 'white',
                'backgroundColor': '#696969',
            },
            # Make the DataTable header background black.
            style_header={'backgroundColor': '#000000'},
            # Style conditionals
            style_data_conditional=[
                {
                    # If the strategy daily return is positive, make the DataTable row green.
                    'if': {
                        'filter_query': '{{Strategy Daily Return}} < {}'.format(0.00),
                    },
                    'backgroundColor': '#FF4136',
                },
                {
                    # If the strategy daily return is negative, make the DataTable row red.
                    'if': {
                        'filter_query': '{{Strategy Daily Return}} > {}'.format(0.00),
                    },
                    'backgroundColor': '#3cb371',
                },
                {
                    # Style conditional that makes the background of any cell clicked on in the DataTable grey to
                    # differentiate it from the red and green backgrounds of other cells.
                    'if': {
                        'state': 'active'  # 'active' | 'selected'
                    },
                    'backgroundColor': '#696969',
                    'border': '#ffffff',
                }
            ],
            # Style the DataTable like a list view, not putting borders between columns.
            style_as_list_view=True,
            # Show 20 rows of the DataTable at a time.
            page_size=20,
            # Allow for the DataTable to be exported to a csv file.
            export_format='csv',
            # Provide an X-axis scrollbar for desktop browsers if the content in a DataTable overflows.
            style_table={'overflowX': 'auto'}
    )

# Function that takes in a dataframe and outputs it as a dash DataTable with a specific format designed for the summary
# statistics table.
def sum_stat_tbl_fmt(df):
    # Return a DataTable
    return DataTable(
        # Create a column in the DataTable for each column in the input dataframe.
        columns=[{'name': i, 'id': i, 'type': 'numeric', 'format': FormatTemplate.percentage(4)} for i in
                 df.columns],
        # Set the data of the DataTable to the data in the df.
        data=df.to_dict('records'),
        # Set cell formatting to use center aligned text, a gray background, and white font color.
        style_cell={
            'textAlign': 'center',
            'whiteSpace': 'normal',
            'height': 'auto',
            'color': 'white',
            'backgroundColor': '#696969',
        },
        # Make the DataTable header background black.
        style_header={'backgroundColor': '#000000'},
        style_data_conditional=[
            {
                # If the annualized Sharpe ratio is positive, make the DataTable row green.
                'if': {
                    'filter_query': '{{Annualized Sharpe Ratio}} < {}'.format(0.00),
                },
                'backgroundColor': '#FF4136',
            },
            {
                # If the annualized Sharpe ratio is negative, make the DataTable row red.
                'if': {
                    'filter_query': '{{Annualized Sharpe Ratio}} > {}'.format(0.00),
                },
                'backgroundColor': '#3cb371',
            },
            {
                # Style conditional that makes the background of any cell clicked on in the DataTable grey to
                # differentiate it from the red or green backgrounds of other cells.
                'if': {
                    'state': 'active'  # 'active' | 'selected'
                },
                'backgroundColor': '#696969',
                'border': '#ffffff',
            }
        ],
        # Style the DataTable like a list view, not putting borders between columns.
        style_as_list_view=True,
    )

# Function that takes in a dataframe and outputs it as a dash DataTable with a specific format designed for the yearly
# summary statistics table.
def yrly_sum_stat_tbl_fmt(df):
    return DataTable(
        # Define the columns needed for the table. Here, the columns consist of year, average daily return, standard
        # deviation of daily returns, annualized average daily return, annualized standard deviation of daily returns,
        # and and annualized Sharpe ratio.
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
        # Set the data of the DataTable to the data in the df.
        data=df.to_dict('records'),
        # Set cell formatting to use center aligned text, a gray background, and white font color.
        style_cell={
            'textAlign': 'center',
            'whiteSpace': 'normal',
            'height': 'auto',
            'color': 'white',
            'backgroundColor': '#696969',
        },
        # Make the DataTable header background black.
        style_header={'backgroundColor': '#000000'},
        style_data_conditional=[
            {
                # If the annualized Sharpe ratio is positive, make the DataTable row green.
                'if': {
                    'filter_query': '{{Annualized Sharpe Ratio}} < {}'.format(0.00),
                },
                'backgroundColor': '#FF4136',
            },
            {
                # If the annualized Sharpe ratio is negative, make the DataTable row red.
                'if': {
                    'filter_query': '{{Annualized Sharpe Ratio}} > {}'.format(0.00),
                },
                'backgroundColor': '#3cb371',
            },
            {
                # Style conditional that makes the background of any cell clicked on in the DataTable grey to
                # differentiate it from the red or green backgrounds of other cells.
                'if': {
                    'state': 'active'  # 'active' | 'selected'
                },
                'backgroundColor': '#696969',
                'border': '#ffffff',
            }
        ],
        # Style the DataTable like a list view, not putting borders between columns.
        style_as_list_view=True,
        # Show 20 rows of the DataTable at a time.
        page_size=20,
        # Allow for the DataTable to be exported to a csv file.
        export_format='csv',
        # Provide an X-axis scrollbar for desktop browsers if the content in a DataTable overflows.
        style_table={'overflowX': 'auto'}
    )

# Function that takes an input list of tickers, a start date, and an end date. It collects the historical closing price
# data for each ticker from the start date to the end date from Yahoo Finance and then calculates the daily returns for
# each ticker from these closing prices.
def daily_return(tickers, start_date, end_date):
    # Create a Ticker object for each ticker in the input tickers list.
    sel = [yf.Ticker(i) for i in tickers]

    # Collect the closing prices for each ticker from the input start date to the input end date from Yahoo Finance and
    # store each in a list. Then use this list to create a DataFrame containing all the tickers closing prices.
    hist_list = [i.history(start=start_date, end=end_date)['Close'] for i in sel]
    hist_df = pd.DataFrame(hist_list).transpose()
    hist_df.columns = tickers

    # Calculate the daily returns for each ticker.
    daily_ret = hist_df.pct_change(1).iloc[1:]

    # Return the daily returns for each ticker.
    return daily_ret

# Function that takes daily returns of tickers in as input and runs the contrarian strategy on it. It returns the daily
# returns input, the daily excess returns for each ticker, and the a table containing the calculated weights for each
# ticker, collateral collateral needed, and contrarian strategy daily return for each day in the input daily returns
# DataFrame.
def contrarian_portfolio_ret(daily_ret):
    # Calculate the daily excess returns over the average return for each day (row) in the input daily return DataFrame.
    excess_ret = daily_ret.sub(daily_ret.mean(axis=1), axis=0)
    er_dimensions = excess_ret.shape

    # Calculate the weight to put on each ticker for each day (row)
    weights = excess_ret.apply(lambda x: -x / er_dimensions[1], axis=1).shift(1).iloc[1:]
    # Calculate the collateral needed for each day (row)
    collateral = abs(weights).apply(sum, axis=1) / 2

    # Calculate the contrarian strategy return for each day (row)
    strat_ret = [daily_ret.iloc[i + 1].dot(weights.iloc[i]) / collateral.iloc[i] if collateral.iloc[i] != 0.0
                 else 0.0 for i in range(0, er_dimensions[0] - 1)]

    # Create the results_df, which will contain the calculated weights for each ticker, collateral collateral needed,
    # and contrarian strategy daily return for each day.
    results_df = weights
    results_df['Collateral Needed'] = collateral
    results_df['Strategy Daily Return'] = strat_ret

    # Reformat the daily_ret DataFrame such that it has Date as a column and not an index
    daily_ret = daily_ret.reset_index()
    daily_ret['Date'] = daily_ret['Date'].dt.date

    # Reformat the excess_ret DataFrame such that it has Date as a column and not an index
    excess_ret = excess_ret.reset_index()
    excess_ret['Date'] = excess_ret['Date'].dt.date

    # Reformat the results_df DataFrame such that it has Date as a column and not an index
    results_df = results_df.reset_index()
    results_df['Date'] = results_df['Date'].dt.date

    # Return the daily_ret, excess_ret, and results_df DataFrames
    return daily_ret, excess_ret, results_df

# Function that returns a line plot figure object from an input DataFrame. The input DataFrame must have a Strategy
# Daily Return column, as that is the y value for this line plot.
def lin_plt(sel_hist):
    # Create a line plot where date is the X axis, Strategy Daily Return is the Y axis, the line color is blue, and a
    # legend is shown for the Daily Strategy Return line.
    lin_cht = go.Figure(data=[go.Scatter(x=sel_hist.Date, y=sel_hist['Strategy Daily Return'],
                                         name='Daily Strategy Return', line={'color': 'blue'}, showlegend=True)])

    # Put a horizontal black line at y=0 for reference (ie. Make it easier to see when Daily Strategy Return is
    # positive or negative.).
    lin_cht.add_hline(y=0, line={'color': 'black'})

    # Update the figure layout
    lin_cht.update_layout(
        # Add an X axis 'Date' label
        xaxis_title='Date',
        # Enable hover interaction, providing the return and date closest to where the mouse cursor is hovering over the
        # line plot.
        hovermode='x',
        # Format the Y axis.
        yaxis={'tickformat': ',.0%'},
        # Set margins.
        margin=go.layout.Margin(
            l=0,  # left margin
            r=0,  # right margin
            b=50,  # bottom margin
            t=50,  # top margin
        ),
    )

    # Provide a rangeslider for the X axis (Dates), so users can zoom in on periods they are most interested in.
    lin_cht.update_xaxes(rangeslider_visible=True)

    # Return the figure object.
    return lin_cht

# Function that returns a figure object with a line plot for 'Annualized Standard Deviation of Daily Returns' and a bar
# plot for 'Annualized Average Daily Returns' from an input DataFrame. The input DataFrame must have a Annualized
# Standard Deviation of Daily Returns column and a 'Annualized Average Daily Return' column, as these are the y values
# for the line plot and bar plot respectively.
def ann_plt(sel_sum):
    # Create a line plot where date is the X axis, Annualized Standard Deviation of Daily Return is the Y axis, the line
    # color is red, and a legend is shown for the Annualized Standard Deviation of Daily Return line.
    fig = go.Figure(data=[go.Scatter(x=sel_sum.Date, y=sel_sum['Annualized Standard Deviation of Daily Returns'],
                                     name='Annualized Standard Deviation of Daily Strategy Return', line={'color': 'red'},
                                     showlegend=True)])

    # Create a bar plot where date is the X axis, Annualized Average Daily Return is the Y axis, the bar color is blue,
    # and a legend is shown for the Annualized Average Daily Return line.
    fig.add_bar(x=sel_sum.Date, y=sel_sum['Annualized Average Daily Return'], name='Annualized Average Daily Strategy Return',
                marker={'color': 'blue'}, showlegend=True)

    # Put a horizontal black line at y=0 for reference (ie. Make it easier to see when values are positive or
    # negative.).
    fig.add_hline(y=0, line={'color': 'black'})

    # Update the figure layout
    fig.update_layout(
        # Add an X axis 'Year' label
        xaxis_title='Year',
        # Enable hover interaction, providing the y and x values closest to where the mouse cursor is hovering over the
        # line plot.
        hovermode='x',
        # Format the x and y axes
        xaxis={'tickformat': 'd'},
        yaxis={'tickformat': ',.0%'},
        # Set margins.
        margin=go.layout.Margin(
            l=0,  # left margin
            r=0,  # right margin
            b=50,  # bottom margin
            t=50,  # top margin
        ),
    )

    # Return the figure object.
    return fig

# Function that calculates the summary statistics for an input DataFrame (sel_hist) and number of trading days per year
# (trading_days). Summary statistics include the Average Daily Return, Standard Deviation of Daily Returns, Annualized
# Average Daily Return, Annualized Standard Deviation of Daily Returns, and Annualized Sharpe Ratio for the 'Strategy
# Daily Return' column of the input DataFrame. As such, the input DataFrame must have a 'Strategy Daily Return' column.
def summary_stats(sel_hist, trading_days):
    # Convert input trading_days to a float to prevent any possible truncation later.
    trading_days = float(trading_days)

    # Calculate the Average Daily Return from the 'Strategy Daily Return' column using the average function from numpy.
    # Likewise, calculate the Standard Deviation of Daily Return from the 'Strategy Daily Return' column using the
    # std function from numpy.
    avg_daily_ret = np.average(sel_hist['Strategy Daily Return'])
    std_dev_daily_ret = np.std(sel_hist['Strategy Daily Return'], ddof=1)

    # Create a DataFrame named sum_stats which holds:
    #       - Average Daily Return: Calculated above.
    #       - Standard Deviation of Daily Returns: Calculated above.
    #       - Annualized Average Daily Return: Calculated by taking the Average Daily Return and multiplying it by the
    #                                          trading days per year.
    #       - Annualized Standard Deviation of Daily Returns: Calculated by taking the Standard Deviation of Daily
    #                                                         Returns and multiplying it by the square root of the
    #                                                         trading days per year.
    #       - Annualized Sharpe Ratio: Calculated by dividing the Average Daily Return by the Standard Deviation of
    #                                  Daily Returns and multiplying the quotient by the square root of the trading days
    #                                  per year.
    sum_stats = pd.DataFrame({'Average Daily Return': [avg_daily_ret],
                              'Standard Deviation of Daily Returns': [std_dev_daily_ret],
                              'Annualized Average Daily Return': [avg_daily_ret * trading_days],
                              'Annualized Standard Deviation of Daily Returns': [std_dev_daily_ret*np.sqrt(trading_days)],
                              'Annualized Sharpe Ratio': [(avg_daily_ret/std_dev_daily_ret)*np.sqrt(trading_days)]})

    # Return the sum_stats DataFrame.
    return sum_stats

# Function that calculates the yearly summary statistics for an input DataFrame (sel_hist) and number of trading days
# per year (trading_days). Summary statistics include the Average Daily Return, Standard Deviation of Daily Returns,
# Annualized Average Daily Return, Annualized Standard Deviation of Daily Returns, and Annualized Sharpe Ratio for the
# 'Strategy Daily Return' column of the input DataFrame. As such, the input DataFrame must have a 'Strategy Daily
# Return' column.
def yearly_summaries(sel_hist, trading_days):
    # Convert input trading_days to a float to prevent any possible truncation later.
    trading_days = float(trading_days)

    # Make sure the dates in sel_hist['Date'] are of type datetime. Then, group the sel_hist Strategy Daily Returns by
    # year.
    sel_hist['Date'] = pd.to_datetime(sel_hist['Date'])
    yr_groups = sel_hist['Strategy Daily Return'].groupby(sel_hist['Date'].dt.year)

    # Create a sum_stats DataFrame. Initially, have it contain:
    #       - Date: A column which holds the years.
    #       - Average Daily Return: A column which holds the Average Daily Return for each year. Calculated using
    #                               mean() for each year group.
    #       - Standard Deviation of Daily Returns: A column which holds the Average Daily Return for each year.
    #                                              Calculated using std() for each year group.
    sum_stats = pd.DataFrame({'Date': yr_groups.mean().index,
                              'Average Daily Return': yr_groups.mean(),
                              'Standard Deviation of Daily Returns': yr_groups.std(ddof=1)})

    # Add 3 more columns to sum_stats:
    #       - Annualized Average Daily Return: Calculated by multiplying the Average Daily Return column by the number
    #                                          of trading days.
    #       - Annualized Standard Deviation of Daily Returns: Calculated by multiplying the Standard Deviation of Daily
    #                                                         Returns column by the square root of the number of trading
    #                                                         days.
    #       - Annualized Sharpe Ratio: Calculated by dividing the Average Daily Return column values by their
    #                                  corresponding Standard Deviation of Daily Returns column values, then multiplying
    #                                  the quotients by the square root of the number of trading days.
    sum_stats['Annualized Average Daily Return'] = sum_stats['Average Daily Return'] * trading_days
    sum_stats['Annualized Standard Deviation of Daily Returns'] = sum_stats['Standard Deviation of Daily Returns'] * np.sqrt(trading_days)
    sum_stats['Annualized Sharpe Ratio'] = sum_stats['Average Daily Return'].divide(sum_stats['Standard Deviation of Daily Returns'])*np.sqrt(trading_days)

    # Return the sum_stats DataFrame.
    return sum_stats
