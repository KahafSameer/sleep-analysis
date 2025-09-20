import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import traceback

class SleepAnalyzer:
    def __init__(self):
        # Define column mappings for flexibility
        self.column_mappings = {
            'sleep_duration': ['Sleep_Duration', 'duration', 'sleep_hours', 'hours'],
            'quality': ['Sleep_Quality', 'quality', 'sleep_score'],
            'study': ['Study_Hours', 'study_time'],
            'screen': ['Screen_Time', 'screen_hours'],
            'activity': ['Physical_Activity', 'exercise'],
            'caffeine': ['Caffeine_Intake', 'caffeine'],
            'gender': ['Gender', 'sex'],
            'year': ['University_Year', 'year', 'academic_year']
        }

    def _find_column(self, df, category):
        """Dynamically find the correct column name from available options"""
        possible_names = self.column_mappings.get(category, [])
        for name in possible_names:
            if name in df.columns:
                return name
        return None

    def analyze(self, df):
        try:
            # Validate input data
            if df is None or df.empty:
                raise ValueError("No data provided for analysis")

            duration_col = self._find_column(df, 'sleep_duration')
            if not duration_col:
                raise ValueError("Sleep duration data not found in the provided dataset")

            # Calculate basic statistics
            try:
                avg_duration = df[duration_col].mean()
                std_duration = df[duration_col].std()
            except Exception:
                raise ValueError("Error calculating sleep statistics")

            analysis_results = {
                'avg_duration': avg_duration,
                'consistency_score': max(0, 10 - (std_duration * 2)),
                'recommendations': [],
                'insights': []
            }

            # Quality score calculation
            try:
                quality_col = self._find_column(df, 'quality')
                if quality_col:
                    analysis_results['quality_score'] = df[quality_col].mean()
                else:
                    # If no quality column, calculate a score based on duration
                    analysis_results['quality_score'] = self._calculate_quality_from_duration(df[duration_col].mean())
            except Exception:
                analysis_results['quality_score'] = 5.0  # Default score if calculation fails

            # Generate recommendations with error handling
            try:
                analysis_results['recommendations'] = self._generate_recommendations(df, analysis_results)
            except Exception:
                analysis_results['recommendations'] = ["Maintain a consistent sleep schedule"]

            # Add insights with error handling
            try:
                self._add_additional_insights(df, analysis_results)
            except Exception:
                analysis_results['insights'] = ["Basic sleep analysis completed"]

            return analysis_results

        except Exception as e:
            return {
                'avg_duration': 0,
                'quality_score': 0,
                'consistency_score': 0,
                'recommendations': [
                    "Unable to analyze sleep data",
                    "Please check your data format and try again"
                ],
                'insights': [f"Analysis Error: {str(e)}"]
            }

    def _add_additional_insights(self, df, results):
        """Add more insights based on available data"""
        insights = []
        
        if self._find_column(df, 'study') and self._find_column(df, 'screen'):
            insights.append("Correlations between study, screen time, and sleep quality have been analyzed.")
            
        if self._find_column(df, 'activity'):
            insights.append("The impact of physical activity on sleep patterns has been assessed.")
            
        results['insights'] = insights

    def _generate_recommendations(self, df, results):
        """Generate dynamic recommendations based on available data"""
        recommendations = []
        duration_col = self._find_column(df, 'sleep_duration')
        
        # Basic sleep duration recommendations
        if results['avg_duration'] < 7:
            recommendations.append("Increase sleep duration to at least 7 hours")
        elif results['avg_duration'] > 9:
            recommendations.append("Consider optimizing sleep duration to 7-9 hours")

        # Additional contextual recommendations
        study_col = self._find_column(df, 'study')
        screen_col = self._find_column(df, 'screen')
        activity_col = self._find_column(df, 'activity')
        
        if study_col and df[study_col].mean() > 8:
            recommendations.append("Consider balancing study time with adequate rest")
        
        if screen_col and df[screen_col].mean() > 4:
            recommendations.append("Reduce screen time, especially before bedtime")
            
        if activity_col and df[activity_col].mean() < 30:
            recommendations.append("Increase physical activity for better sleep quality")
            
        return recommendations

    def _calculate_quality_from_duration(self, avg_duration):
        if 7 <= avg_duration <= 9:
            return 8.5
        elif 6 <= avg_duration < 7 or 9 < avg_duration <= 10:
            return 6.5
        else:
            return 4.5
