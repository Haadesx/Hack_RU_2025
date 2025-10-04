# modules/pose_analysis.py
import numpy as np
import mediapipe as mp
import cv2
from typing import Dict, List, Optional

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def analyze_pose_from_keypoints(keypoints_data: Dict) -> Dict:
    """
    Analyze pose keypoints for posture and tension indicators
    keypoints_data should contain landmark coordinates
    """
    try:
        if not keypoints_data or 'landmarks' not in keypoints_data:
            return {"ok": False, "error": "No pose landmarks provided"}
        
        landmarks = keypoints_data['landmarks']
        
        # Convert to numpy arrays for easier calculation
        def get_landmark_coords(landmark_idx):
            if landmark_idx < len(landmarks):
                return np.array([landmarks[landmark_idx]['x'], landmarks[landmark_idx]['y']])
            return None
        
        # Key landmarks for posture analysis
        nose = get_landmark_coords(0)
        left_shoulder = get_landmark_coords(11)
        right_shoulder = get_landmark_coords(12)
        left_hip = get_landmark_coords(23)
        right_hip = get_landmark_coords(24)
        left_ear = get_landmark_coords(7)
        right_ear = get_landmark_coords(8)
        
        if not all([nose, left_shoulder, right_shoulder, left_hip, right_hip]):
            return {"ok": False, "error": "Insufficient landmarks for analysis"}
        
        # Calculate shoulder midpoint
        shoulder_midpoint = (left_shoulder + right_shoulder) / 2
        hip_midpoint = (left_hip + right_hip) / 2
        
        # 1. Forward Head Posture Analysis
        # Calculate angle between ear-shoulder-hip line
        if left_ear is not None:
            ear_shoulder_vec = left_ear - left_shoulder
            shoulder_hip_vec = left_shoulder - left_hip
        else:
            ear_shoulder_vec = nose - left_shoulder
            shoulder_hip_vec = left_shoulder - left_hip
        
        # Calculate angle between vectors
        cos_angle = np.dot(ear_shoulder_vec, shoulder_hip_vec) / (
            np.linalg.norm(ear_shoulder_vec) * np.linalg.norm(shoulder_hip_vec)
        )
        forward_head_angle = np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))
        
        # 2. Shoulder Alignment Analysis
        shoulder_height_diff = abs(left_shoulder[1] - right_shoulder[1])
        shoulder_alignment_score = 1.0 - min(1.0, shoulder_height_diff * 10)
        
        # 3. Hip Alignment Analysis  
        hip_height_diff = abs(left_hip[1] - right_hip[1])
        hip_alignment_score = 1.0 - min(1.0, hip_height_diff * 10)
        
        # 4. Spinal Alignment (shoulder-hip line angle)
        spine_vector = shoulder_midpoint - hip_midpoint
        spine_angle = np.degrees(np.arctan2(spine_vector[0], spine_vector[1]))
        
        # 5. Overall Posture Score
        posture_components = [
            max(0, 1 - forward_head_angle / 30),  # Forward head penalty
            shoulder_alignment_score,              # Shoulder alignment
            hip_alignment_score,                   # Hip alignment
            max(0, 1 - abs(spine_angle) / 15)      # Spinal alignment
        ]
        overall_posture_score = np.mean(posture_components)
        
        # 6. Tension Indicators
        tension_flags = {
            "forward_head": forward_head_angle > 15,
            "shoulder_misalignment": shoulder_height_diff > 0.05,
            "hip_misalignment": hip_height_diff > 0.05,
            "spinal_deviation": abs(spine_angle) > 10
        }
        
        # 7. Recommendations
        recommendations = []
        if tension_flags["forward_head"]:
            recommendations.append("Consider chin tucks to reduce forward head posture")
        if tension_flags["shoulder_misalignment"]:
            recommendations.append("Try shoulder blade squeezes to improve alignment")
        if tension_flags["hip_misalignment"]:
            recommendations.append("Focus on hip flexor stretches and core strengthening")
        if tension_flags["spinal_deviation"]:
            recommendations.append("Practice gentle spinal twists and side stretches")
        
        if not recommendations:
            recommendations.append("Great posture! Keep up the good work with regular movement breaks")
        
        return {
            "ok": True,
            "forward_head_angle": float(forward_head_angle),
            "shoulder_alignment_score": float(shoulder_alignment_score),
            "hip_alignment_score": float(hip_alignment_score),
            "spine_angle": float(spine_angle),
            "overall_posture_score": float(overall_posture_score),
            "tension_flags": tension_flags,
            "recommendations": recommendations,
            "analysis_timestamp": np.datetime64('now').astype(str)
        }
        
    except Exception as e:
        return {
            "ok": False, 
            "error": f"Pose analysis failed: {str(e)}",
            "forward_head_angle": 0.0,
            "shoulder_alignment_score": 0.5,
            "hip_alignment_score": 0.5,
            "spine_angle": 0.0,
            "overall_posture_score": 0.5,
            "tension_flags": {},
            "recommendations": ["Unable to analyze posture at this time"]
        }

def analyze_pose_from_image(image_path: str) -> Dict:
    """
    Analyze pose from image file using MediaPipe
    """
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            return {"ok": False, "error": "Could not read image"}
        
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Initialize MediaPipe pose
        with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
            results = pose.process(image_rgb)
            
            if not results.pose_landmarks:
                return {"ok": False, "error": "No pose detected in image"}
            
            # Convert landmarks to our format
            landmarks = []
            for landmark in results.pose_landmarks.landmark:
                landmarks.append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z,
                    'visibility': landmark.visibility
                })
            
            keypoints_data = {'landmarks': landmarks}
            return analyze_pose_from_keypoints(keypoints_data)
            
    except Exception as e:
        return {
            "ok": False,
            "error": f"Image pose analysis failed: {str(e)}"
        }