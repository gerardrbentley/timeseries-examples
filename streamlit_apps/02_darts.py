import streamlit as st

"""
# Streamlit + Darts

Exploring the "Time Series Made Easy in Python" library [Darts](https://unit8co.github.io/darts/).
Adding interactive web elements with [Streamlit](https://streamlit.io)

You can install darts using pip:

`pip install darts`

If that doesn't work you can try with conda:

`conda install -c conda-forge u8darts`
"""

"Create a TimeSeries object from a Pandas DataFrame, and split it in train/validation series:"
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

"Fit an exponential smoothing model, and make a (probabilistic) prediction over the validation series' duration:"

with st.echo():
    from darts.models import ExponentialSmoothing

    model = ExponentialSmoothing()
    model.fit(train)
    prediction = model.predict(len(val), num_samples=1000)

with st.expander("Prediction Time Series"):
    st.write("Type:", type(prediction))
    st.write("First 5 values:", prediction[:5].values())
    st.write("Length:", len(prediction))

"Plot the median, 5th and 95th percentiles:"

with st.echo():
    import matplotlib.pyplot as plt
    fig = plt.figure()
    series.plot()
    prediction.plot(label='forecast', low_quantile=0.05, high_quantile=0.95)
    plt.legend()
    st.pyplot(fig)

"Plot your own Confidence Interval:"


with st.echo():
    custom_fig = plt.figure()
    series.plot()

    low_quantile = st.number_input('Lower Percentile', min_value=0.01, max_value=0.99, value=0.05, help='The quantile to use for the lower bound of the plotted confidence interval.')
    high_quantile = st.number_input('High Percentile', min_value=0.01, max_value=0.99, value=0.95, help='The quantile to use for the upper bound of the plotted confidence interval.')
    prediction.plot(label='forecast', low_quantile=low_quantile, high_quantile=high_quantile)

    plt.legend()
    st.pyplot(custom_fig)