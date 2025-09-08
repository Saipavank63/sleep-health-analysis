"""
Visualization module for sleep health data.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional

class SleepDataVisualizer:
    """Creates visualizations for sleep health data."""
    
    def __init__(self, data: pd.DataFrame):
        """Initialize visualizer with transformed data."""
        self.data = data
        # Set default style
        plt.style.use('seaborn')
    
    def plot_sleep_duration_distribution(self, save_path: Optional[str] = None) -> None:
        """Plot distribution of sleep duration."""
        plt.figure(figsize=(10, 6))
        sns.histplot(data=self.data, x='sleep_duration', bins=30)
        plt.title('Distribution of Sleep Duration')
        plt.xlabel('Hours of Sleep')
        plt.ylabel('Count')
        
        if save_path:
            plt.savefig(save_path)
        plt.close()
    
    def plot_quality_vs_duration(self, save_path: Optional[str] = None) -> None:
        """Create scatter plot of sleep quality vs duration."""
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=self.data, x='sleep_duration', y='quality_score',
                       hue='stress_level', size='activity_level',
                       sizes=(20, 200), alpha=0.6)
        plt.title('Sleep Quality vs Duration')
        plt.xlabel('Sleep Duration (hours)')
        plt.ylabel('Quality Score')
        
        if save_path:
            plt.savefig(save_path)
        plt.close()
    
    def plot_sleep_stages(self, save_path: Optional[str] = None) -> None:
        """Plot average distribution of sleep stages."""
        stages = ['deep_sleep_pct', 'rem_sleep_pct', 'light_sleep_pct']
        values = [self.data[stage].mean() for stage in stages]
        labels = ['Deep Sleep', 'REM Sleep', 'Light Sleep']
        
        plt.figure(figsize=(10, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', 
                colors=sns.color_palette('pastel'))
        plt.title('Average Sleep Stages Distribution')
        
        if save_path:
            plt.savefig(save_path)
        plt.close()
    
    def create_interactive_dashboard(self) -> Dict[str, go.Figure]:
        """Create interactive plotly visualizations."""
        dashboard = {}
        
        # Time series of sleep metrics
        fig_time_series = px.line(self.data, x='date',
                                y=['sleep_duration', 'quality_score'],
                                title='Sleep Metrics Over Time')
        dashboard['time_series'] = fig_time_series
        
        # Weekly patterns
        weekly_avg = self.data.groupby('day_of_week')[
            ['sleep_duration', 'quality_score']].mean().reset_index()
        fig_weekly = px.bar(weekly_avg, x='day_of_week',
                          y=['sleep_duration', 'quality_score'],
                          title='Weekly Sleep Patterns',
                          barmode='group')
        dashboard['weekly_patterns'] = fig_weekly
        
        # Correlation heatmap
        corr_cols = ['sleep_duration', 'quality_score', 'activity_level',
                    'stress_level', 'heart_rate', 'deep_sleep_pct']
        corr_matrix = self.data[corr_cols].corr()
        fig_corr = px.imshow(corr_matrix,
                            title='Correlation Matrix of Sleep Metrics')
        dashboard['correlation'] = fig_corr
        
        return dashboard
    
    def generate_summary_dashboard(self, save_path: Optional[str] = None) -> None:
        """Generate a comprehensive dashboard with multiple plots."""
        fig, axes = plt.subplots(2, 2, figsize=(20, 15))
        
        # Sleep duration distribution
        sns.histplot(data=self.data, x='sleep_duration', bins=30, ax=axes[0, 0])
        axes[0, 0].set_title('Sleep Duration Distribution')
        
        # Quality vs Duration
        sns.scatterplot(data=self.data, x='sleep_duration', y='quality_score',
                       hue='stress_level', size='activity_level',
                       sizes=(20, 200), alpha=0.6, ax=axes[0, 1])
        axes[0, 1].set_title('Sleep Quality vs Duration')
        
        # Sleep stages
        stages = ['deep_sleep_pct', 'rem_sleep_pct', 'light_sleep_pct']
        values = [self.data[stage].mean() for stage in stages]
        axes[1, 0].pie(values, labels=['Deep', 'REM', 'Light'],
                      autopct='%1.1f%%', colors=sns.color_palette('pastel'))
        axes[1, 0].set_title('Sleep Stages Distribution')
        
        # Weekly patterns
        weekly_avg = self.data.groupby('day_of_week')['quality_score'].mean()
        sns.barplot(x=weekly_avg.index, y=weekly_avg.values, ax=axes[1, 1])
        axes[1, 1].set_title('Quality Score by Day of Week')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
        plt.close()

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
    
    # Create visualizations
    visualizer = SleepDataVisualizer(transformed_data)
    visualizer.generate_summary_dashboard('summary_dashboard.png')
    
    # Create interactive dashboard
    interactive_dashboard = visualizer.create_interactive_dashboard()
    for name, fig in interactive_dashboard.items():
        fig.show()
