import cv2
import time
import numpy as np
import os
from gtts import gTTS
import pygame
import speech_recognition as sr
from deepface import DeepFace
import re

def main():
    """Main loop for the video-based AI Guard Room system."""
    
    print("AI GUARD ROOM AGENT v2.0")
    print()
    
    # Enroll trusted users
    known_embeddings = enroll_trusted_users(known_faces_path)
    
    if not known_embeddings:
        print("Warning: No trusted users enrolled. All faces will be unauthorized.\n")
    
    video_path = "entry_video.mp4"
    
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found\n")
        return
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file\n")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video loaded: {total_frames} frames @ {fps:.1f} FPS\n")
    
    interaction_complete = False
    frame_count = 0
    check_interval = 30
    
    print("Starting video analysis...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("\nEnd of video reached.")
            break
        
        frame_count += 1
        
        if frame_count % check_interval != 0:
            continue
        
        progress = (frame_count / total_frames) * 100
        print(f"Processing frame {frame_count}/{total_frames} ({progress:.1f}%)", end="\r")
        
        try:
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            
            faces = DeepFace.extract_faces(
                img_path=small_frame, 
                detector_backend='opencv', 
                enforce_detection=False
            )
            
            if faces and len(faces) > 0 and not interaction_complete:
                print(f"\n\nFace detected at frame {frame_count}")
                
                face_data = faces[0]
                face_img = face_data['face']
                
                result = DeepFace.represent(
                    img_path=face_img, 
                    model_name="VGG-Face", 
                    enforce_detection=False
                )
                face_embedding = result[0]['embedding']
                
                identified_user = identify_user(face_embedding, known_embeddings)
                
                if identified_user == "Unauthorised":
                    # Start escalating dialogue with passcode checking
                    result = handle_unauthorized_dialogue(SECRET_PASSCODE)
                    
                    if result == "PASSCODE_GRANTED":
                        print("Access granted via passcode\n")
                    else:
                        print("Access denied - Security notified\n")
                    
                    interaction_complete = True
                    break
                    
                else:
                    # Authorized user
                    print(f"\nAUTHORIZED USER: {identified_user}")
                    welcome_msg = f"Hello {identified_user}. Welcome back. Access granted."
                    print(f"Agent: {welcome_msg}\n")
                    speak(welcome_msg)
                    interaction_complete = True
                    time.sleep(2)
                    break
        
        except Exception as e:
            print(f"\nProcessing error at frame {frame_count}: {e}")
        
        if interaction_complete:
            break
    
    cap.release()
    print("System Shutdown")

if __name__ == "__main__":
    main()
