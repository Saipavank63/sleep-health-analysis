"""
Data loader module for sleep health data.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List

class SleepDataGenerator:
    """Generates synthetic sleep health data for demonstration."""
    
    def __init__(self, n_samples: int = 1000):
        self.n_samples = n_samples
        np.random.seed(42)
    
    def generate_data(self) -> pd.DataFrame:
        """Generate synthetic sleep data."""
        # Generate dates
        start_date = datetime(2025, 1, 1)
        dates = [start_date + timedelta(days=x) for x in range(self.n_samples)]
        
        # Generate sleep metrics
        data = {
            'date': dates,
            'sleep_duration': np.random.normal(7.5, 1.5, self.n_samples),
            'quality_score': np.random.normal(75, 15, self.n_samples),
            'bedtime': np.random.normal(23, 1.5, self.n_samples),
            'wake_time': None,  # Will be calculated
            'activity_level': np.random.normal(45, 20, self.n_samples),
            'stress_level': np.random.normal(5, 2, self.n_samples),
            'heart_rate': np.random.normal(65, 5, self.n_samples),
            'deep_sleep_pct': np.random.normal(20, 5, self.n_samples),
            'rem_sleep_pct': np.random.normal(25, 5, self.n_samples),
            'light_sleep_pct': None  # Will be calculated
        }
        
        df = pd.DataFrame(data)
        
        # Calculate wake time based on sleep duration
        df['wake_time'] = np.mod(df['bedtime'] + df['sleep_duration'], 24)
        
        # Calculate light sleep percentage
        df['light_sleep_pct'] = 100 - df['deep_sleep_pct'] - df['rem_sleep_pct']
        
        return self._apply_constraints(df)
    
    def _apply_constraints(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply realistic constraints to the data."""
        # Clip values to realistic ranges
        df['sleep_duration'] = np.clip(df['sleep_duration'], 4, 12)
        df['quality_score'] = np.clip(df['quality_score'], 0, 100)
        df['activity_level'] = np.clip(df['activity_level'], 0, 120)
        df['stress_level'] = np.clip(df['stress_level'], 0, 10)
        df['heart_rate'] = np.clip(df['heart_rate'], 45, 85)
        
        return df

class SleepDataLoader:
    """Handles loading and basic preprocessing of sleep data."""
    
    @staticmethod
    def load_from_csv(filepath: str) -> pd.DataFrame:
        """Load sleep data from CSV file."""
        try:
            return pd.read_csv(filepath, parse_dates=['date'])
        except Exception as e:
            raise Exception(f"Error loading data from {filepath}: {str(e)}")
    
    @staticmethod
    def load_from_database(connection_string: str, query: str) -> pd.DataFrame:
        """Load sleep data from database."""
        try:
            return pd.read_sql(query, connection_string)
        except Exception as e:
            raise Exception(f"Error loading data from database: {str(e)}")

if __name__ == "__main__":
    # Example usage
    generator = SleepDataGenerator(n_samples=100)
    data = generator.generate_data()
    print(data.head())
    print("\nData shape:", data.shape)
    print("\nData info:")
    print(data.info())
