known_faces_path = "known_faces"

def enroll_trusted_users(known_faces_path='known_faces'):
    """Enrolls trusted users by their face images."""
    known_embeddings = {}
    
    if not os.path.exists(known_faces_path):
        print(f"Error: Directory '{known_faces_path}' not found.")
        return known_embeddings
    
    print(f"Enrolling trusted users from '{known_faces_path}' directory...")
    
    for name in os.listdir(known_faces_path):
        person_dir = os.path.join(known_faces_path, name)
        if os.path.isdir(person_dir):
            for filename in os.listdir(person_dir):
                if filename.lower().endswith((".jpg", ".png", ".jpeg")):
                    img_path = os.path.join(person_dir, filename)
                    try:
                        result = DeepFace.represent(
                            img_path=img_path, 
                            model_name="VGG-Face", 
                            enforce_detection=False
                        )
                        embedding = result[0]['embedding']
                        known_embeddings[name] = embedding
                        print(f"✓ Enrolled: {name}")
                        break
                    except Exception as e:
                        print(f"✗ Failed to enroll {name}: {e}")
    
    print(f"Total enrolled users: {len(known_embeddings)}\n")
    return known_embeddings

def identify_user(face_embedding, known_embeddings, threshold=0.6):
    """Identifies a user based on their face embedding."""
    min_distance = float('inf')
    identified_name = "Unauthorised"
    
    for name, known_embedding in known_embeddings.items():
        distance = np.linalg.norm(np.array(face_embedding) - np.array(known_embedding))
        if distance < min_distance:
            min_distance = distance
            if distance < threshold:
                identified_name = name
    
    print(f"  Distance: {min_distance:.4f} (threshold: {threshold})")
    return identified_name
