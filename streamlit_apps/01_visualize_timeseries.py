import streamlit as st
"## Import Necessary Libraries"
import pandas as pd
import plotly.express as px

from pathlib import Path

"""## Data Source

United States Prime Supplier of Sales Volumes

via US Energy Information Administration [online](https://www.eia.gov/petroleum/data.php)

Monthly release date: February 18, 2022

Sales of petroleum products by 

- refiners
- gas plant operators
- importers
- large inter-state distributors 

into the final local markets of consumption by U.S.

"""


"## Get path to file"
data_folder = Path('data')
files = list(data_folder.glob('sales_oil*'))
files

"## Load in the excel data to a pandas Dataframe"
excel_path = files[0]
excel_data = pd.read_excel(excel_path, sheet_name='Data 1', header=2)
"Show some example rows"
excel_data.iloc[:5]

"We'll simplify our data a bit to just the Month and Total Sales"
excel_data['Month'] = excel_data['Date']
excel_data['Sales'] = excel_data['U.S. Total Gasoline All Sales/Deliveries by Prime Supplier (Thousand Gallons per Day)']
excel_data = excel_data[['Month', 'Sales']]

"And just take the past 10 years"
excel_data = excel_data.iloc[-120:]

"## Check out the types and names of the data we have"
for column in excel_data:
    column
    non_null_count = excel_data[column].count()
    non_null_count
    excel_data[column].dtype


"## Show a Line Chart"
line_chart = px.line(excel_data, x='Month', y='Sales')
st.plotly_chart(line_chart)

"## Use Pandas Dataframe index with a timeseries"
monthly_sales = excel_data.set_index('Month', drop=False)
monthly_sales

"## Pandas dt functions"
"[See More in the docs](https://pandas.pydata.org/docs/user_guide/timeseries.html#time-date-components)"

monthly_sales['year'] = monthly_sales['Month'].dt.year
monthly_sales['quarter'] = monthly_sales['Month'].dt.quarter
monthly_sales.iloc[:5]

"## Line Plot highlighting the year"

monthly_sales.year.dtype
yearly_plot = px.line(monthly_sales, x='Month', y='Sales', color='year')
st.plotly_chart(yearly_plot)

"## Area Plot"
area_sales = px.area(monthly_sales, x='Month', y='Sales')
st.plotly_chart(area_sales)

"## Area Plot highlighting the quarter"

area_quarterly_sales = px.area(monthly_sales, x='Month', y='Sales', color='quarter')
st.plotly_chart(area_quarterly_sales)

"## Yearly sales"
"by summing after resampling with [frequency string](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects) for End of Year"

yearly_sales = monthly_sales['Sales'].resample('A').sum()
yearly_sales

"## Bar Plot"
"Plotly express lets us use Dataframe index with attribute ([see docs](https://plotly.com/python/px-arguments/#using-the-index-of-a-dataframe))"

yearly_sale_plot = px.bar(yearly_sales, x=yearly_sales.index, y='Sales', color=yearly_sales.index.year.values.astype('str'))
st.plotly_chart(yearly_sale_plot)

"## Quarterly Sales"

"Can be done with resampling"
quarterly_sales = monthly_sales[['Sales']].resample('Q').sum()
quarterly_sales['quarter'] = quarterly_sales.index.quarter.values.astype('str')
quarterly_sales['year'] = quarterly_sales.index.year.values
quarterly_sales

"Or similarly with groupby year and quarter since we have that already"
group_quarter = monthly_sales[['Sales','year','quarter']].groupby(by=['year','quarter']).sum()
group_quarter

"## Stacked Bar Plot"
quarterly_bar = px.bar(quarterly_sales, x='year', y='Sales', color='quarter')
st.plotly_chart(quarterly_bar)

"## Side by Side Group Bar Plot"

quarterly_bar_group = px.bar(quarterly_sales, x='year', y='Sales', color='quarter', barmode='group')
st.plotly_chart(quarterly_bar_group)

"## Stacked Area"

quarterly_area = px.area(quarterly_sales, x='year', y='Sales', color='quarter')
st.plotly_chart(quarterly_area)

"## Overlapping Area"

import plotly.graph_objects as go

quarterly_overlaid = go.Figure()
for quarter in quarterly_sales.quarter.unique():
    sub_df = quarterly_sales[quarterly_sales.quarter == quarter]
    quarterly_overlaid.add_trace(go.Scatter(x=sub_df.year, y=sub_df.Sales, fill='tonexty'))
st.plotly_chart(quarterly_overlaid)


"Or just use a line chart..."
quarterly_line = px.line(quarterly_sales, x='year', y='Sales', color='quarter')
st.plotly_chart(quarterly_line)

"## Heatmap"
heatmap = px.imshow(quarterly_sales.pivot(index='year', values='Sales', columns='quarter'))
st.plotly_chart(heatmap)