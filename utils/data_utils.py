import json
import pandas as pd



class ConfigReader:
    def __init__(self, config_path):
        with open(config_path) as f:
            self.config = json.load(f)
        self.env = self.config.get("environment", "dev")
        self.env_config = self.config.get("environments", {}).get(self.env, {})

    def get_env_value(self, key, default=None):
        return self.env_config.get(key, default)

    def get(self, key, default=None):
        return self.config.get(key, default)

class TestCaseDataReader:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        try:
            self.df = pd.read_csv(csv_path)
        except Exception as e:
            raise FileNotFoundError(f"Could not read CSV file: {csv_path}. Error: {e}")

    def get_test_case_data(self, test_case_id, id_column='test_case_id'):
        if id_column not in self.df.columns:
            raise ValueError(f"ID column '{id_column}' not found in CSV file.")
        row = self.df[self.df[id_column] == test_case_id]
        if row.empty:
            raise ValueError(f"Test case ID '{test_case_id}' not found in CSV file '{self.csv_path}'.")
        return row.iloc[0].to_dict()