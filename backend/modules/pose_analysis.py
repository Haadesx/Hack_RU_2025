# modules/pose_analysis.py - Posture and body tension analysis
import numpy as np
from typing import Dict, List, Any

def analyze_pose_keypoints(keypoints: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze pose keypoints for posture alignment and tension indicators
    
    Args:
        keypoints: Dictionary containing pose landmarks from MediaPipe or TensorFlow.js
        
    Returns:
        dict: Posture analysis with alignment, tension flags, and recommendations
    """
    try:
        # Check if keypoints are in MediaPipe format or TensorFlow.js format
        # MediaPipe: {landmarks: [{x, y, z, visibility}]}
        # TensorFlow.js PoseNet: {keypoints: [{position: {x, y}, score}]}
        
        if not keypoints:
            return {"error": "No keypoints provided", "ok": False}
        
        # Extract landmarks - handle different formats
        landmarks = keypoints.get('landmarks', keypoints.get('keypoints', []))
        
        if not landmarks or len(landmarks) == 0:
            return {
                "ok": False,
                "error": "No valid landmarks detected",
                "recommendation": "Please ensure full body is visible in camera"
            }
        
        # Convert to numpy array for easier computation
        # Assuming format: [{x, y, ...}] or [{position: {x, y}}]
        points = []
        for lm in landmarks:
            if 'position' in lm:  # TensorFlow.js format
                points.append([lm['position']['x'], lm['position']['y']])
            elif 'x' in lm and 'y' in lm:  # MediaPipe format
                points.append([lm['x'], lm['y']])
        
        if len(points) < 8:  # Need at least key upper body points
            return {
                "ok": False,
                "error": "Insufficient landmarks for analysis",
                "recommendation": "Please adjust camera angle"
            }
        
        points = np.array(points)
        
        # Key point indices (MediaPipe Pose landmark indices)
        # Adjust if using different pose detection library
        NOSE = 0
        LEFT_SHOULDER = 11 if len(points) > 11 else 5
        RIGHT_SHOULDER = 12 if len(points) > 12 else 6
        LEFT_HIP = 23 if len(points) > 23 else 11
        RIGHT_HIP = 24 if len(points) > 24 else 12
        LEFT_EAR = 7 if len(points) > 7 else 3
        RIGHT_EAR = 8 if len(points) > 8 else 4
        
        # Calculate posture metrics
        results = {
            "ok": True,
            "tension_indicators": [],
            "alignment_score": 0.0,
            "recommendations": []
        }
        
        # 1) Forward head posture check
        if len(points) > LEFT_EAR and len(points) > LEFT_SHOULDER:
            ear = points[LEFT_EAR]
            shoulder = points[LEFT_SHOULDER]
            
            # Calculate horizontal distance between ear and shoulder
            forward_lean = abs(ear[0] - shoulder[0])
            
            if forward_lean > 0.08:  # Threshold for forward head (normalized coords)
                results["tension_indicators"].append("forward_head_posture")
                results["recommendations"].append("Your head is forward - try chin tucks to realign")
                results["forward_head_score"] = float(min(1.0, forward_lean * 10))
            else:
                results["forward_head_score"] = 0.0
        
        # 2) Shoulder alignment check
        if len(points) > RIGHT_SHOULDER and len(points) > LEFT_SHOULDER:
            left_shoulder = points[LEFT_SHOULDER]
            right_shoulder = points[RIGHT_SHOULDER]
            
            # Check if shoulders are level
            shoulder_slope = abs(left_shoulder[1] - right_shoulder[1])
            
            if shoulder_slope > 0.05:
                results["tension_indicators"].append("uneven_shoulders")
                results["recommendations"].append("Shoulders appear uneven - consider stretching tight side")
                results["shoulder_imbalance"] = float(shoulder_slope * 10)
            else:
                results["shoulder_imbalance"] = 0.0
        
        # 3) Upper body tilt (slouching indicator)
        if len(points) > LEFT_SHOULDER and len(points) > LEFT_HIP:
            shoulder = points[LEFT_SHOULDER]
            hip = points[LEFT_HIP]
            
            # Calculate angle of torso from vertical
            torso_vec = shoulder - hip
            angle = np.degrees(np.arctan2(torso_vec[0], torso_vec[1]))
            
            results["torso_angle"] = float(angle)
            
            if abs(angle) > 15:
                results["tension_indicators"].append("slouching")
                results["recommendations"].append("Sit up taller - engage your core")
                results["slouch_score"] = float(min(1.0, abs(angle) / 30))
            else:
                results["slouch_score"] = 0.0
        
        # 4) Calculate overall alignment score
        tension_count = len(results["tension_indicators"])
        results["alignment_score"] = float(max(0.0, 1.0 - (tension_count * 0.25)))
        
        # 5) Overall posture assessment
        if results["alignment_score"] > 0.75:
            results["posture_status"] = "good"
            results["summary"] = "Posture looks well-aligned"
        elif results["alignment_score"] > 0.5:
            results["posture_status"] = "fair"
            results["summary"] = "Minor posture adjustments recommended"
        else:
            results["posture_status"] = "needs_attention"
            results["summary"] = "Several posture issues detected - consider ergonomic adjustments"
        
        # 6) Add general recommendation if none specific
        if not results["recommendations"]:
            results["recommendations"].append("Maintain current posture - looking good!")
        
        return results
        
    except Exception as e:
        return {
            "ok": False,
            "error": f"Pose analysis failed: {str(e)}",
            "recommendation": "Please try capturing pose again"
        }

def simulate_pose_analysis():
    """
    Generate simulated pose analysis for testing without camera
    """
    return {
        "ok": True,
        "tension_indicators": ["forward_head_posture"],
        "alignment_score": 0.65,
        "posture_status": "fair",
        "summary": "Minor forward head posture detected",
        "recommendations": [
            "Try chin tucks to realign head position",
            "Take breaks every 30 minutes to reset posture"
        ],
        "forward_head_score": 0.4,
        "shoulder_imbalance": 0.1,
        "slouch_score": 0.2,
        "torso_angle": 8.5,
        "note": "Simulated data for demo purposes"
    }
