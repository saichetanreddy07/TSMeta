"""Use timestamp insertion and interpolation during cleaning."""

import pandas as pd

import tsmeta

data = pd.DataFrame(
    {
        "date": pd.to_datetime(["2024-01-01", "2024-01-03", "2024-01-04"]),
        "sales": [10.0, 14.0, 16.0],
    }
)

cleaning = tsmeta.clean_data(
    data,
    insert_missing_timestamps=True,
    interpolation_method="linear",
)

print(cleaning.data)
print(cleaning.summary())
