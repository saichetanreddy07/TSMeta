"""Load an existing pandas DataFrame through TSMeta."""

import pandas as pd

import tsmeta

source = pd.DataFrame(
    {
        "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "sales": [100, 125, 130],
    }
)

data = tsmeta.load_data(source)
analysis = tsmeta.analyze(data)

print(analysis.to_dict())
