import pandas as pd
import os
from urllib.request import urlretrieve


class DataLoader:
    def __init__(self, filepath="data/auto-mpg.data"):
        self.filepath = filepath
        self.columns = ["mpg", "cylinders", "displacement", "horsepower",
                        "weight", "acceleration", "model_year", "origin", "name"]

        # Create data directory if missing
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

    def load_data(self):
        """Smart loader that downloads data if missing"""
        if not os.path.exists(self.filepath):
            print("Downloading dataset...")
            url = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
            urlretrieve(url, self.filepath)

        return pd.read_csv(self.filepath, sep=r'\s+', names=self.columns)