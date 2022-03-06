# Timeseries

## Timeseries Data Overview

We live in an age of data that we don't know how to sort through [LINK: explosion of data].
It comes in many forms, from pictures to purchases to all the searches we make in google.

The focus of this will be on "timeseries" data;
any data that is ordered by the passage of time.

Some real-world Timeseries data examples:

- Weather history
- Stock price history
- Purchase / Sale history
- Field sensor signals (ex. seismic detectors)
- Credit spending habits

Mathematically speaking, we have example "observations" at each "period" of time.
This can be represented like a list of values going back in time:

`y_t`, `y_t-1`, `y_t-2`, ... `y_0`

But before getting too deep into Timeseries, what isn't a Timeseries?

### Non-Timeseries Data

When developers think of "data", many will rightfully jump to "databases."
Often used are the flavors of relational SQL such as Postgres and MySQL.
There are also many flavors of unstructured and columnar Non-SQL databases.

#### Relational Data

Relational data fits many normal business use cases, like keeping track of your employee / user / student data.
Here's some relational data with 3 columns that holds some information about our users:

| id      | name | favorite_food
| ----------- | ----------- | ----- |
| 1      | Alice       | Spam |
| 2   | Bob        | Eggs |

#### Non-Relational Data

Unstructured data fits many user-created use cases, like representing a blog post or user's settings.

VS Code handles non-default user preferences by adding to a JSON document.
Here are some of mine:

```json
{
    "python.testing.pytestEnabled": true,
    "python.sortImports.path": "isort",
    "python.sortImports.args": [
        "--profile black"
    ],
    "window.zoomLevel": 1,
}
```

### Timeseries Forecasting

One of the powers of Timeseries data is the ability to predict the future.
It's not possible in all cases of course, but that is the goal of Timeseries "forecasting."

By analyzing the history and patterns of the data, a prediction can be made for one or more periods in the future.

This is incredibly powerful and used every day in real business scenarios.
For example, using a businesses' historical sales to predict if they'll make enough to payback a bigger loan.

Mathematically this is represented as the result of a function on the present and previous time periods.
"Y Hat" is the predicted value of the next period.

`y_hat_t+1` = `g(t`, `y_t`, `y_t-1`, `y_t-2`, ... `y_0)`

In python we might write a function like the following:

`prediction = get_prediction(period, observations)`

#### Unique Features

- Trend:
  - Long term general direction
  - Affects how we think about the data over longer periods
- Cyclicality
  - Long horizon patterns of high-low-high movement
  - Longer than years, which can usually fit in seasonality 
- Seasonality
  - Shorter periods of rising and falling movement
  - Usually in sync with times of year
- Irregularity
  - Random changes that don't fit the trend and cycle

#### Unforecastable Data

These concepts just don't exist in Relational and Unstructured data.
You couldn't predict anything about the future of our users' favorite foods just by looking at the table above.

(*Note:* If we also kept track of when each person's preference changed, then we would be able to create some Timeseries data from that!)

