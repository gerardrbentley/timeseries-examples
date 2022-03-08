import streamlit as st

"""
# Streamlit + Darts

Exploring the "Time Series Made Easy in Python" library [Darts](https://unit8co.github.io/darts/).
Adding interactive web elements with [Streamlit](https://streamlit.io)

## Install 

You can install darts using pip or conda

```sh
# pip
pip install darts
# conda (recommended for dependencies)
conda install -c conda-forge -c pytorch u8darts-all
```
"""
with st.expander("If that doesn't work..."):
    """\
You can try with conda:

`conda install -c conda-forge u8darts`

Or install it without all of the models with pip (from [docs](https://unit8co.github.io/darts/#id3)):
```sh
# Install core only (without neural networks, Prophet or AutoARIMA): 
pip install u8darts

# Install core + neural networks (PyTorch): pip install 
u8darts[torch]

# Install core + Facebook Prophet: pip install 
u8darts[prophet]

# Install core + AutoARIMA: pip install 
u8darts[pmdarima]


# Install darts with all available models (recommended): 
conda install -c conda-forge -c pytorch u8darts-all

# Install core + neural networks (PyTorch): 
conda install -c conda-forge -c pytorch u8darts-torch

# Install core only (without neural networks, Prophet or AutoARIMA): 
conda install -c conda-forge u8darts
```
"""

"## Create a TimeSeries object from a Pandas DataFrame, and split it in train/validation series:"
with st.echo():
    import pandas as pd
    from darts import TimeSeries

    # Read a pandas DataFrame
    df = pd.read_csv('data/air_passengers.csv', delimiter=",")

    # Create a TimeSeries, specifying the time and value columns
    series = TimeSeries.from_dataframe(df, 'Month', '#Passengers')

    # Set aside the last 36 months as a validation series
    train, val = series[:-36], series[-36:]

with st.expander("Train Time Series"):
    st.write("Type:", type(train))
    st.write("First 5 values:", train[:5].values())
    st.write("Length:", len(train))
    attributes = [x for x in dir(train) if not x.startswith("_")]
    st.write("Non-private Attributes:", attributes)

with st.expander("Xarray View"):
    st.markdown(train, unsafe_allow_html=True)

"## Fit an exponential smoothing model, and make a (probabilistic) prediction over the validation series' duration:"

with st.echo():
    from darts.models import ExponentialSmoothing

    model = ExponentialSmoothing()
    model.fit(train)
    prediction = model.predict(len(val), num_samples=1000)

with st.expander("Prediction Time Series"):
    st.write("Type:", type(prediction))
    st.write("First 5 values:", prediction[:5].values())
    st.write("Length:", len(prediction))

"## Plot the median, 5th and 95th percentiles:"

with st.echo():
    import matplotlib.pyplot as plt
    fig = plt.figure()
    series.plot()
    prediction.plot(label='forecast', low_quantile=0.05, high_quantile=0.95)
    plt.legend()
    st.pyplot(fig)

"## Interact with Training and Plotting:"


with st.echo('below'):
    interactive_fig = plt.figure()
    series.plot()

    st.subheader("Training Controls")
    num_periods = st.number_input("Number of validation months", min_value=0, max_value=len(series), value=36, help='How many months worth of datapoints to exclude from training')
    num_samples = st.number_input("Number of prediction samples", min_value=1, max_value=10000, value=1000, help="Number of times a prediction is sampled for a probabilistic model")
    st.subheader("Plotting Controls")
    low_quantile = st.number_input('Lower Percentile', min_value=0.01, max_value=0.99, value=0.05, help='The quantile to use for the lower bound of the plotted confidence interval.')
    high_quantile = st.number_input('High Percentile', min_value=0.01, max_value=0.99, value=0.95, help='The quantile to use for the upper bound of the plotted confidence interval.')
    
    train, val = series[:-num_periods], series[-num_periods:]
    model = ExponentialSmoothing()
    model.fit(train)
    prediction = model.predict(len(val), num_samples=num_samples)
    prediction.plot(label='forecast', low_quantile=low_quantile, high_quantile=high_quantile)

    plt.legend()
    st.pyplot(interactive_fig)

pandas_options = pd.read_csv('pandas_frequencies.csv')
pandas_options = pandas_options.set_index('Date Offset')
options = {'Weekly': ('W', 52), 'Monthly': ('M', 12), 'Yearly': ('A', 1)}
"""## Go Wild!\

Use your own csv data that has a well formed time series and plot some forecasts!

(Limited to ExponentialSmoothing. For now...)
"""
with st.echo('below'):
    data = st.file_uploader("New Timeseries csv")
    delimiter = st.text_input("CSV Delimiter", value=',', max_chars=1, help='How your CSV values are separated')
    if data is not None:
        custom_df = pd.read_csv(data, sep=delimiter)
        with st.expander("Show Raw Data"):
            st.dataframe(custom_df)

        columns = list(custom_df.columns)
        with st.expander("Show all columns"):
            st.write(' | '.join(columns))

        time_col = st.selectbox("Time Column", columns, help="Name of the column in your csv with time period data")
        value_cols = st.multiselect("Values Column(s)", columns, columns[1], help="Name of column(s) with values to sample and forecast")
        sampling_period = st.selectbox("Time Series Period", options, help='How to define samples. Pandas will sum entries between periods to create a well-formed Time Series')

        custom_df[time_col] = pd.to_datetime(custom_df[time_col])
        freq_string, periods_per_year = options[sampling_period]
        custom_df = custom_df.set_index(time_col).resample(freq_string).sum()
        with st.expander("Show Resampled Data"):
            st.write("Number of samples:", len(custom_df))
            st.dataframe(custom_df)

        custom_series = TimeSeries.from_dataframe(custom_df, value_cols=value_cols)

        st.subheader("Custom Training Controls")
        max_periods = len(custom_df) - (2 * periods_per_year)
        num_periods = st.number_input("Number of validation periods", key='cust_period', min_value=2, max_value=max_periods, value=max_periods, help='How many periods worth of datapoints to exclude from training')
        num_samples = st.number_input("Number of prediction samples", key='cust_sample', min_value=1, max_value=10000, value=1000, help="Number of times a prediction is sampled for a probabilistic model")
        
        st.subheader("Custom Plotting Controls")
        low_quantile = st.number_input('Lower Percentile', key='cust_low', min_value=0.01, max_value=0.99, value=0.05, help='The quantile to use for the lower bound of the plotted confidence interval.')
        high_quantile = st.number_input('High Percentile', key='cust_high', min_value=0.01, max_value=0.99, value=0.95, help='The quantile to use for the upper bound of the plotted confidence interval.')

        train, val = custom_series[:-num_periods], custom_series[-num_periods:]
        model = ExponentialSmoothing()
        model.fit(train)
        prediction = model.predict(len(val), num_samples=num_samples)

        custom_fig = plt.figure()
        custom_series.plot()

        prediction.plot(label='forecast', low_quantile=low_quantile, high_quantile=high_quantile)

        plt.legend()
        st.pyplot(custom_fig)