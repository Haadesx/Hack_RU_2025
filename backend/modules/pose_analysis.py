# modules/pose_analysis.py
import numpy as np
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

# MediaPipe pose landmark indices
POSE_LANDMARKS = {
    "NOSE": 0,
    "LEFT_EYE_INNER": 1,
    "LEFT_EYE": 2,
    "LEFT_EYE_OUTER": 3,
    "RIGHT_EYE_INNER": 4,
    "RIGHT_EYE": 5,
    "RIGHT_EYE_OUTER": 6,
    "LEFT_EAR": 7,
    "RIGHT_EAR": 8,
    "MOUTH_LEFT": 9,
    "MOUTH_RIGHT": 10,
    "LEFT_SHOULDER": 11,
    "RIGHT_SHOULDER": 12,
    "LEFT_ELBOW": 13,
    "RIGHT_ELBOW": 14,
    "LEFT_WRIST": 15,
    "RIGHT_WRIST": 16,
    "LEFT_PINKY": 17,
    "RIGHT_PINKY": 18,
    "LEFT_INDEX": 19,
    "RIGHT_INDEX": 20,
    "LEFT_THUMB": 21,
    "RIGHT_THUMB": 22,
    "LEFT_HIP": 23,
    "RIGHT_HIP": 24,
    "LEFT_KNEE": 25,
    "RIGHT_KNEE": 26,
    "LEFT_ANKLE": 27,
    "RIGHT_ANKLE": 28,
    "LEFT_HEEL": 29,
    "RIGHT_HEEL": 30,
    "LEFT_FOOT_INDEX": 31,
    "RIGHT_FOOT_INDEX": 32
}

def analyze_pose_keypoints(pose_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze posture from MediaPipe pose keypoints
    Expects pose_data to contain 'landmarks' list with x, y, z coordinates
    """
    try:
        landmarks = pose_data.get('landmarks', [])
        if not landmarks or len(landmarks) < 33:
            return {
                "error": "Insufficient pose landmarks",
                "posture_score": 0.5,
                "analysis_quality": "failed"
            }
        
        # Convert landmarks to numpy array for easier processing
        points = []
        for lm in landmarks:
            if isinstance(lm, dict):
                points.append([lm.get('x', 0), lm.get('y', 0), lm.get('z', 0)])
            elif isinstance(lm, (list, tuple)) and len(lm) >= 2:
                points.append([lm[0], lm[1], lm[2] if len(lm) > 2 else 0])
            else:
                points.append([0, 0, 0])
        
        landmarks_array = np.array(points)
        
        # Analyze different aspects of posture
        analysis = {}
        
        # 1. Head posture (forward head position)
        analysis.update(analyze_head_posture(landmarks_array))
        
        # 2. Shoulder alignment
        analysis.update(analyze_shoulder_alignment(landmarks_array))
        
        # 3. Spinal alignment
        analysis.update(analyze_spinal_alignment(landmarks_array))
        
        # 4. Overall posture score
        posture_indicators = [
            analysis.get('head_forward_score', 0.5),
            analysis.get('shoulder_alignment_score', 0.5),
            analysis.get('spinal_alignment_score', 0.5)
        ]
        
        overall_score = float(np.mean(posture_indicators))
        analysis['posture_score'] = overall_score
        
        # 5. Generate recommendations
        recommendations = generate_posture_recommendations(analysis)
        analysis['recommendations'] = recommendations
        
        # 6. Risk assessment
        if overall_score < 0.3:
            risk_level = "high"
            urgency = "Address posture issues soon"
        elif overall_score < 0.6:
            risk_level = "moderate"
            urgency = "Consider posture improvements"
        else:
            risk_level = "low"
            urgency = "Maintain good posture"
        
        analysis.update({
            'risk_level': risk_level,
            'urgency': urgency,
            'analysis_quality': 'good'
        })
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing pose: {str(e)}")
        return {
            "error": str(e),
            "posture_score": 0.5,
            "analysis_quality": "failed"
        }

def analyze_head_posture(landmarks: np.ndarray) -> Dict[str, Any]:
    """Analyze forward head posture"""
    try:
        # Get key points
        nose = landmarks[POSE_LANDMARKS["NOSE"]]
        left_shoulder = landmarks[POSE_LANDMARKS["LEFT_SHOULDER"]]
        right_shoulder = landmarks[POSE_LANDMARKS["RIGHT_SHOULDER"]]
        
        # Calculate shoulder center
        shoulder_center = (left_shoulder + right_shoulder) / 2
        
        # Calculate head position relative to shoulders
        head_offset = nose[0] - shoulder_center[0]  # Horizontal offset
        head_height = shoulder_center[1] - nose[1]  # Vertical difference
        
        # Forward head ratio (ideal is close to 0)
        if head_height > 0:
            forward_head_ratio = abs(head_offset) / head_height
        else:
            forward_head_ratio = 1.0
        
        # Score: lower ratio = better posture
        head_forward_score = max(0.0, 1.0 - forward_head_ratio * 2)
        
        return {
            "head_forward_ratio": float(forward_head_ratio),
            "head_forward_score": float(head_forward_score),
            "head_position": "forward" if forward_head_ratio > 0.3 else "neutral"
        }
        
    except Exception as e:
        return {"head_forward_score": 0.5, "error": f"Head analysis error: {str(e)}"}

def analyze_shoulder_alignment(landmarks: np.ndarray) -> Dict[str, Any]:
    """Analyze shoulder alignment and elevation"""
    try:
        left_shoulder = landmarks[POSE_LANDMARKS["LEFT_SHOULDER"]]
        right_shoulder = landmarks[POSE_LANDMARKS["RIGHT_SHOULDER"]]
        
        # Calculate shoulder height difference
        height_diff = abs(left_shoulder[1] - right_shoulder[1])
        
        # Calculate shoulder angle
        shoulder_vector = right_shoulder - left_shoulder
        angle_radians = np.arctan2(shoulder_vector[1], shoulder_vector[0])
        angle_degrees = float(np.degrees(angle_radians))
        
        # Normalize angle to 0-180 range
        angle_deviation = abs(angle_degrees) if abs(angle_degrees) <= 90 else 180 - abs(angle_degrees)
        
        # Score: lower deviation = better alignment
        alignment_score = max(0.0, 1.0 - (angle_deviation / 30.0))  # 30 degrees as threshold
        
        return {
            "shoulder_height_diff": float(height_diff),
            "shoulder_angle": float(angle_degrees),
            "shoulder_alignment_score": float(alignment_score),
            "shoulder_status": "uneven" if height_diff > 0.05 else "aligned"
        }
        
    except Exception as e:
        return {"shoulder_alignment_score": 0.5, "error": f"Shoulder analysis error: {str(e)}"}

def analyze_spinal_alignment(landmarks: np.ndarray) -> Dict[str, Any]:
    """Analyze spinal curvature and alignment"""
    try:
        # Get key spinal reference points
        nose = landmarks[POSE_LANDMARKS["NOSE"]]
        left_shoulder = landmarks[POSE_LANDMARKS["LEFT_SHOULDER"]]
        right_shoulder = landmarks[POSE_LANDMARKS["RIGHT_SHOULDER"]]
        left_hip = landmarks[POSE_LANDMARKS["LEFT_HIP"]]
        right_hip = landmarks[POSE_LANDMARKS["RIGHT_HIP"]]
        
        # Calculate center points
        shoulder_center = (left_shoulder + right_shoulder) / 2
        hip_center = (left_hip + right_hip) / 2
        
        # Calculate spinal alignment vector
        spine_vector = shoulder_center - hip_center
        
        # Ideal spine should be mostly vertical
        spine_angle = np.arctan2(abs(spine_vector[0]), abs(spine_vector[1]))
        spine_deviation = float(np.degrees(spine_angle))
        
        # Score: closer to vertical = better
        spinal_score = max(0.0, 1.0 - (spine_deviation / 20.0))  # 20 degrees threshold
        
        return {
            "spine_deviation_degrees": spine_deviation,
            "spinal_alignment_score": float(spinal_score),
            "spinal_status": "misaligned" if spine_deviation > 15 else "aligned"
        }
        
    except Exception as e:
        return {"spinal_alignment_score": 0.5, "error": f"Spinal analysis error: {str(e)}"}

def generate_posture_recommendations(analysis: Dict[str, Any]) -> List[str]:
    """Generate specific posture improvement recommendations"""
    recommendations = []
    
    # Head posture recommendations
    if analysis.get('head_forward_score', 1.0) < 0.6:
        recommendations.extend([
            "Pull your chin back and imagine a string pulling the top of your head upward",
            "Take breaks from screen work every 20 minutes",
            "Consider neck stretches and strengthening exercises"
        ])
    
    # Shoulder recommendations
    if analysis.get('shoulder_alignment_score', 1.0) < 0.6:
        recommendations.extend([
            "Roll your shoulders back and down",
            "Check your workspace ergonomics",
            "Practice doorway chest stretches"
        ])
    
    # Spinal recommendations
    if analysis.get('spinal_alignment_score', 1.0) < 0.6:
        recommendations.extend([
            "Engage your core muscles for better spinal support",
            "Adjust your chair height and back support",
            "Consider yoga or pilates for core strengthening"
        ])
    
    # General recommendations
    if len(recommendations) == 0:
        recommendations.append("Your posture looks good! Keep maintaining awareness throughout the day.")
    else:
        recommendations.append("Set reminders to check your posture every hour")
    
    return recommendations[:4]  # Limit to 4 recommendations

# Alternative simplified analysis for basic pose detection
def analyze_pose_simple(keypoints: List[Dict[str, float]]) -> Dict[str, Any]:
    """
    Simplified pose analysis for basic posture assessment
    Expected format: [{"x": 0.5, "y": 0.3, "confidence": 0.9}, ...]
    """
    try:
        if len(keypoints) < 10:  # Minimum required keypoints
            return {"error": "Insufficient keypoints", "posture_score": 0.5}
        
        # Simple shoulder alignment check
        left_shoulder = next((kp for i, kp in enumerate(keypoints) if i == 5), None)  # Common left shoulder index
        right_shoulder = next((kp for i, kp in enumerate(keypoints) if i == 6), None)  # Common right shoulder index
        
        if left_shoulder and right_shoulder:
            height_diff = abs(left_shoulder['y'] - right_shoulder['y'])
            alignment_score = max(0.0, 1.0 - height_diff * 5)  # Simple scoring
            
            return {
                "posture_score": float(alignment_score),
                "shoulder_alignment": "good" if height_diff < 0.1 else "needs_attention",
                "analysis_quality": "basic",
                "recommendations": [
                    "Keep shoulders level and relaxed",
                    "Take regular posture breaks"
                ]
            }
        
        return {
            "posture_score": 0.7,
            "analysis_quality": "limited",
            "recommendations": ["Maintain good posture awareness"]
        }
        
    except Exception as e:
        return {"error": str(e), "posture_score": 0.5}