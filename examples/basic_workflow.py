"""Basic TSMeta workflow using the public API."""

import pandas as pd

import tsmeta

data = pd.DataFrame(
    {
        "date": pd.date_range("2024-01-01", periods=4, freq="D"),
        "sales": [10.0, 12.0, None, 18.0],
        "region": ["north", "north", "north", "north"],
    }
)

validation = tsmeta.validate_data(data)
print(validation.summary())

cleaning = tsmeta.clean_data(data)
cleaned_data = cleaning.data
print(cleaning.summary())

analysis = tsmeta.analyze(cleaned_data)
print(analysis.summary())
