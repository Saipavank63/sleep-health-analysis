"""
Data transformation module for sleep health data.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Optional, Tuple

class SleepDataTransformer:
    """Handles transformation and feature engineering for sleep data."""
    
    def __init__(self, data: pd.DataFrame):
        """Initialize transformer with input data."""
        self.data = data.copy()
        self.quality_checks = {}
        self.scaler = StandardScaler()
    
    def clean_data(self) -> 'SleepDataTransformer':
        """Clean the data by removing invalid entries and handling missing values."""
        # Remove negative values
        self.data = self.data[self.data.select_dtypes(include=[np.number]) >= 0]
        
        # Remove duplicates
        self.data = self.data.drop_duplicates()
        
        # Sort by date
        self.data = self.data.sort_values('date')
        
        return self
    
    def engineer_features(self) -> 'SleepDataTransformer':
        """Create new features from existing data."""
        # Convert bedtime and wake time to datetime
        self.data['bedtime_datetime'] = pd.to_datetime(self.data['date'].dt.date) + \
                                      pd.to_timedelta(self.data['bedtime'], unit='h')
        self.data['wake_time_datetime'] = pd.to_datetime(self.data['date'].dt.date) + \
                                        pd.to_timedelta(self.data['wake_time'], unit='h')
        
        # Calculate sleep efficiency
        self.data['sleep_efficiency'] = (self.data['deep_sleep_pct'] + 
                                       0.5 * self.data['rem_sleep_pct']) / 100
        
        # Calculate sleep regularity
        self.data['bedtime_shift'] = self.data['bedtime'].diff().abs()
        
        # Calculate sleep debt
        self.data['sleep_debt'] = 8 - self.data['sleep_duration']
        
        # Add day of week
        self.data['day_of_week'] = self.data['date'].dt.dayofweek
        
        return self
    
    def normalize_features(self, columns: Optional[List[str]] = None) -> 'SleepDataTransformer':
        """Normalize specified numerical features."""
        if columns is None:
            columns = ['sleep_duration', 'quality_score', 'activity_level', 
                      'stress_level', 'heart_rate']
        
        self.data[columns] = self.scaler.fit_transform(self.data[columns])
        return self
    
    def perform_quality_checks(self) -> 'SleepDataTransformer':
        """Perform data quality checks and store results."""
        # Check for missing values
        self.quality_checks['missing_values'] = self.data.isnull().sum()
        
        # Check value ranges
        self.quality_checks['value_ranges'] = {
            col: {'min': self.data[col].min(), 
                 'max': self.data[col].max()}
            for col in self.data.select_dtypes(include=[np.number]).columns
        }
        
        # Check data completeness
        self.quality_checks['record_count'] = len(self.data)
        
        # Check data types
        self.quality_checks['data_types'] = self.data.dtypes.to_dict()
        
        return self
    
    def get_transformed_data(self) -> pd.DataFrame:
        """Return the transformed data."""
        return self.data
    
    def get_quality_report(self) -> Dict:
        """Return the quality check results."""
        return self.quality_checks

if __name__ == "__main__":
    # Example usage
    from data_loader import SleepDataGenerator
    
    # Generate sample data
    generator = SleepDataGenerator(n_samples=100)
    raw_data = generator.generate_data()
    
    # Transform data
    transformer = SleepDataTransformer(raw_data)
    transformed_data = (transformer
                       .clean_data()
                       .engineer_features()
                       .normalize_features()
                       .perform_quality_checks()
                       .get_transformed_data())
    
    print("Transformed data shape:", transformed_data.shape)
    print("\nQuality report:")
    print(transformer.get_quality_report())
