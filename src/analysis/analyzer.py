"""
Sleep data analysis module.
"""
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple

class SleepAnalyzer:
    """Analyzes sleep patterns and generates insights."""
    
    def __init__(self, data: pd.DataFrame):
        """Initialize analyzer with transformed data."""
        self.data = data
        
    def calculate_basic_stats(self) -> Dict[str, Dict[str, float]]:
        """Calculate basic statistics for key metrics."""
        metrics = ['sleep_duration', 'quality_score', 'deep_sleep_pct', 
                  'rem_sleep_pct', 'light_sleep_pct']
        
        stats_dict = {}
        for metric in metrics:
            stats_dict[metric] = {
                'mean': self.data[metric].mean(),
                'median': self.data[metric].median(),
                'std': self.data[metric].std(),
                'min': self.data[metric].min(),
                'max': self.data[metric].max()
            }
        
        return stats_dict
    
    def analyze_weekly_patterns(self) -> pd.DataFrame:
        """Analyze sleep patterns by day of week."""
        return self.data.groupby('day_of_week').agg({
            'sleep_duration': 'mean',
            'quality_score': 'mean',
            'deep_sleep_pct': 'mean',
            'bedtime': 'mean',
            'wake_time': 'mean'
        }).round(2)
    
    def analyze_correlations(self) -> pd.DataFrame:
        """Calculate correlations between different metrics."""
        correlation_cols = ['sleep_duration', 'quality_score', 'activity_level',
                          'stress_level', 'heart_rate', 'deep_sleep_pct',
                          'rem_sleep_pct', 'light_sleep_pct']
        
        return self.data[correlation_cols].corr()
    
    def detect_anomalies(self, column: str, threshold: float = 2.0) -> pd.DataFrame:
        """Detect anomalies in specified metric using z-score."""
        z_scores = np.abs(stats.zscore(self.data[column]))
        return self.data[z_scores > threshold].copy()
    
    def calculate_sleep_trends(self, window: int = 7) -> pd.DataFrame:
        """Calculate moving averages for key metrics."""
        metrics = ['sleep_duration', 'quality_score', 'deep_sleep_pct']
        trend_data = pd.DataFrame()
        
        for metric in metrics:
            trend_data[f'{metric}_ma'] = self.data[metric].rolling(window=window).mean()
        
        return trend_data
    
    def generate_sleep_report(self) -> Dict:
        """Generate a comprehensive sleep analysis report."""
        report = {
            'basic_stats': self.calculate_basic_stats(),
            'weekly_patterns': self.analyze_weekly_patterns().to_dict(),
            'correlations': self.analyze_correlations().to_dict(),
            'trends': self.calculate_sleep_trends().tail().to_dict()
        }
        
        # Add key insights
        report['insights'] = {
            'avg_sleep_duration': self.data['sleep_duration'].mean(),
            'best_quality_day': self.analyze_weekly_patterns()['quality_score'].idxmax(),
            'worst_quality_day': self.analyze_weekly_patterns()['quality_score'].idxmin(),
            'sleep_quality_trend': 'improving' if self.data['quality_score'].tail().is_monotonic_increasing else 'varying'
        }
        
        return report

if __name__ == "__main__":
    # Example usage
    from data_loader import SleepDataGenerator
    from transformer import SleepDataTransformer
    
    # Generate and transform data
    generator = SleepDataGenerator(n_samples=100)
    raw_data = generator.generate_data()
    
    transformer = SleepDataTransformer(raw_data)
    transformed_data = (transformer
                       .clean_data()
                       .engineer_features()
                       .get_transformed_data())
    
    # Analyze data
    analyzer = SleepAnalyzer(transformed_data)
    report = analyzer.generate_sleep_report()
    
    print("Sleep Analysis Report:")
    print(report)
