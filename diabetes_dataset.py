# Class to handle loading and preprocessing of
# the diabetes dataset

import pandas as pd


class DiabetesDataset:
    # loops and holds the diabetes dataset

    def __init__(self, filepath):
        self.filepath = filepath
        self.df = pd.read_csv(filepath)

    def get_record_count(self):
        return len(self.df)

    def get_feature_count(self):
        return len(self.df.columns)

    def get_data_quality(self):
        missing = self.df.isnull().sum().sum()
        total = len(self.df) * len(self.df.columns)
        quality = (1 - missing / total) * 100
        return round(quality, 1)

    def get_preview(self, rows=10):
        return self.df.head(rows)

    def get_summary(self):
        return self.df.describe()
