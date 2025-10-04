# modules/hrv_analysis.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

def analyze_hrv_data(csv_path: str) -> Dict:
    """
    Analyze HRV data from wearable CSV file
    Expected columns: timestamp, heart_rate, rr_intervals (optional), sleep_stage (optional)
    """
    try:
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Validate required columns
        required_cols = ['timestamp', 'heart_rate']
        if not all(col in df.columns for col in required_cols):
            return {
                "ok": False,
                "error": f"Missing required columns. Expected: {required_cols}, Found: {list(df.columns)}"
            }
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Basic heart rate analysis
        hr_data = df['heart_rate'].dropna()
        avg_hr = float(hr_data.mean())
        hr_std = float(hr_data.std())
        hr_min = float(hr_data.min())
        hr_max = float(hr_data.max())
        
        # HRV Analysis (if RR intervals available)
        hrv_metrics = {}
        if 'rr_intervals' in df.columns:
            rr_intervals = df['rr_intervals'].dropna()
            if len(rr_intervals) > 10:  # Need sufficient data
                hrv_metrics = calculate_hrv_metrics(rr_intervals)
        
        # Sleep analysis (if sleep stage data available)
        sleep_metrics = {}
        if 'sleep_stage' in df.columns:
            sleep_metrics = analyze_sleep_patterns(df)
        
        # Circadian rhythm analysis
        circadian_metrics = analyze_circadian_patterns(df)
        
        # Stress indicators
        stress_indicators = {
            "high_hr_variability": hr_std > avg_hr * 0.2,
            "elevated_resting_hr": avg_hr > 80,
            "low_hrv": hrv_metrics.get('rmssd', 0) < 20 if hrv_metrics else True,
            "irregular_patterns": hr_std > avg_hr * 0.3
        }
        
        # Wellness score (0-1, higher is better)
        wellness_components = [
            max(0, 1 - (avg_hr - 60) / 40),  # Heart rate component
            max(0, 1 - hr_std / (avg_hr * 0.3)),  # Variability component
            hrv_metrics.get('wellness_score', 0.5) if hrv_metrics else 0.5,  # HRV component
            sleep_metrics.get('sleep_quality_score', 0.5) if sleep_metrics else 0.5  # Sleep component
        ]
        wellness_score = float(np.mean(wellness_components))
        
        # Recommendations
        recommendations = generate_hrv_recommendations(
            avg_hr, hr_std, hrv_metrics, sleep_metrics, stress_indicators
        )
        
        return {
            "ok": True,
            "heart_rate": {
                "average": avg_hr,
                "std": hr_std,
                "min": hr_min,
                "max": hr_max,
                "resting_hr": float(hr_data.quantile(0.1))  # Bottom 10% as resting HR
            },
            "hrv_metrics": hrv_metrics,
            "sleep_metrics": sleep_metrics,
            "circadian_metrics": circadian_metrics,
            "stress_indicators": stress_indicators,
            "wellness_score": wellness_score,
            "recommendations": recommendations,
            "data_period": {
                "start": df['timestamp'].min().isoformat(),
                "end": df['timestamp'].max().isoformat(),
                "duration_hours": (df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 3600
            }
        }
        
    except Exception as e:
        return {
            "ok": False,
            "error": f"HRV analysis failed: {str(e)}",
            "heart_rate": {"average": 70, "std": 5, "min": 60, "max": 80, "resting_hr": 65},
            "hrv_metrics": {},
            "sleep_metrics": {},
            "circadian_metrics": {},
            "stress_indicators": {},
            "wellness_score": 0.5,
            "recommendations": ["Unable to analyze wearable data at this time"]
        }

def calculate_hrv_metrics(rr_intervals: pd.Series) -> Dict:
    """Calculate HRV metrics from RR intervals"""
    try:
        # Convert to milliseconds
        rr_ms = rr_intervals * 1000
        
        # Time domain metrics
        rmssd = float(np.sqrt(np.mean(np.diff(rr_ms) ** 2)))  # Root mean square of successive differences
        sdnn = float(np.std(rr_ms))  # Standard deviation of NN intervals
        pnn50 = float(np.sum(np.abs(np.diff(rr_ms)) > 50) / len(rr_ms) * 100)  # Percentage of differences > 50ms
        
        # Frequency domain metrics (simplified)
        # Use Welch's method for power spectral density
        from scipy import signal
        fs = 1000 / np.mean(rr_ms)  # Sampling frequency
        f, psd = signal.welch(rr_ms, fs=fs, nperseg=min(len(rr_ms)//4, 256))
        
        # Define frequency bands
        vlf_band = (0.003, 0.04)  # Very low frequency
        lf_band = (0.04, 0.15)    # Low frequency  
        hf_band = (0.15, 0.4)     # High frequency
        
        vlf_power = np.trapz(psd[(f >= vlf_band[0]) & (f <= vlf_band[1])], f[(f >= vlf_band[0]) & (f <= vlf_band[1])])
        lf_power = np.trapz(psd[(f >= lf_band[0]) & (f <= lf_band[1])], f[(f >= lf_band[0]) & (f <= lf_band[1])])
        hf_power = np.trapz(psd[(f >= hf_band[0]) & (f <= hf_band[1])], f[(f >= hf_band[0]) & (f <= hf_band[1])])
        
        lf_hf_ratio = lf_power / hf_power if hf_power > 0 else 0
        
        # HRV wellness score (0-1)
        wellness_score = min(1.0, max(0.0, (rmssd - 10) / 50))  # Normalize RMSSD
        
        return {
            "rmssd": rmssd,
            "sdnn": sdnn,
            "pnn50": pnn50,
            "vlf_power": float(vlf_power),
            "lf_power": float(lf_power),
            "hf_power": float(hf_power),
            "lf_hf_ratio": float(lf_hf_ratio),
            "wellness_score": wellness_score
        }
        
    except Exception as e:
        return {"error": f"HRV calculation failed: {str(e)}"}

def analyze_sleep_patterns(df: pd.DataFrame) -> Dict:
    """Analyze sleep patterns from sleep stage data"""
    try:
        sleep_df = df[df['sleep_stage'].notna()].copy()
        
        if len(sleep_df) == 0:
            return {"error": "No sleep data available"}
        
        # Sleep stage distribution
        stage_counts = sleep_df['sleep_stage'].value_counts()
        total_sleep_time = len(sleep_df) * 0.5  # Assuming 30-second epochs
        
        # Calculate sleep efficiency (simplified)
        deep_sleep_time = stage_counts.get('deep', 0) * 0.5
        rem_sleep_time = stage_counts.get('rem', 0) * 0.5
        light_sleep_time = stage_counts.get('light', 0) * 0.5
        
        sleep_efficiency = (deep_sleep_time + rem_sleep_time + light_sleep_time) / total_sleep_time if total_sleep_time > 0 else 0
        
        # Sleep quality score
        quality_components = [
            min(1.0, deep_sleep_time / 2),  # Deep sleep component
            min(1.0, rem_sleep_time / 2),   # REM sleep component
            sleep_efficiency                 # Efficiency component
        ]
        sleep_quality_score = float(np.mean(quality_components))
        
        return {
            "total_sleep_hours": total_sleep_time,
            "deep_sleep_hours": deep_sleep_time,
            "rem_sleep_hours": rem_sleep_time,
            "light_sleep_hours": light_sleep_time,
            "sleep_efficiency": sleep_efficiency,
            "sleep_quality_score": sleep_quality_score,
            "stage_distribution": stage_counts.to_dict()
        }
        
    except Exception as e:
        return {"error": f"Sleep analysis failed: {str(e)}"}

def analyze_circadian_patterns(df: pd.DataFrame) -> Dict:
    """Analyze circadian rhythm patterns"""
    try:
        # Extract hour from timestamp
        df['hour'] = df['timestamp'].dt.hour
        
        # Calculate hourly heart rate patterns
        hourly_hr = df.groupby('hour')['heart_rate'].mean()
        
        # Find peak and trough times
        peak_hour = hourly_hr.idxmax()
        trough_hour = hourly_hr.idxmin()
        
        # Calculate circadian amplitude (peak - trough)
        circadian_amplitude = hourly_hr.max() - hourly_hr.min()
        
        # Assess circadian health
        circadian_health_score = min(1.0, circadian_amplitude / 20)  # Normalize amplitude
        
        return {
            "peak_hour": int(peak_hour),
            "trough_hour": int(trough_hour),
            "circadian_amplitude": float(circadian_amplitude),
            "circadian_health_score": circadian_health_score,
            "hourly_pattern": hourly_hr.to_dict()
        }
        
    except Exception as e:
        return {"error": f"Circadian analysis failed: {str(e)}"}

def generate_hrv_recommendations(avg_hr: float, hr_std: float, hrv_metrics: Dict, 
                               sleep_metrics: Dict, stress_indicators: Dict) -> List[str]:
    """Generate personalized recommendations based on HRV analysis"""
    recommendations = []
    
    # Heart rate recommendations
    if avg_hr > 80:
        recommendations.append("Consider stress reduction techniques - your resting heart rate is elevated")
    elif avg_hr < 60:
        recommendations.append("Excellent cardiovascular fitness! Maintain your current routine")
    
    # HRV recommendations
    if hrv_metrics.get('rmssd', 0) < 20:
        recommendations.append("Try daily meditation or breathing exercises to improve heart rate variability")
    elif hrv_metrics.get('rmssd', 0) > 50:
        recommendations.append("Great HRV! Your autonomic nervous system is well-balanced")
    
    # Sleep recommendations
    if sleep_metrics.get('sleep_quality_score', 0) < 0.6:
        recommendations.append("Focus on sleep hygiene - aim for 7-9 hours of quality sleep")
    
    # Stress recommendations
    if stress_indicators.get('high_hr_variability', False):
        recommendations.append("Consider reducing caffeine and practicing relaxation techniques")
    
    if not recommendations:
        recommendations.append("Your biometrics look great! Keep maintaining your healthy lifestyle")
    
    return recommendations