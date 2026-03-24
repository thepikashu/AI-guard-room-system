def check_passcode(user_input, secret_passcode):
    """Check if user input contains the secret passcode."""
    if not user_input:
        return False
    
    # Normalize both strings (lowercase, remove extra spaces)
    user_normalized = re.sub(r'\s+', ' ', user_input.lower().strip())
    passcode_normalized = secret_passcode.lower().strip()
    
    # Check if passcode is in the user's response
    return passcode_normalized in user_normalized

def detect_force_entry_attempt(user_input):
    """Detect if user is trying to force entry."""
    if not user_input:
        return False
    
    force_keywords = [
        "let me in", "open the door", "move", "get out of my way",
        "i'm going in", "step aside", "coming through", "coming in",
        "don't care", "whatever", "who cares"
    ]
    
    user_lower = user_input.lower()
    return any(keyword in user_lower for keyword in force_keywords)

def handle_unauthorized_dialogue(secret_passcode):
    """Handle escalating dialogue with unauthorized person."""
    
    # Escalation Level 1: Polite but professional
    dialogue_l1 = {
        "prompt": "Hello. I don't recognize you as an authorized person. Please state your name and the purpose of your visit.",
        "wait_for_response": True
    }
    
    # Escalation Level 2: Firm and direct
    dialogue_l2 = {
        "prompt": "I need proper authorization to grant you access. Do you have an access code?",
        "wait_for_response": True
    }
    
    # Escalation Level 3: Final warning / Ultimatum
    dialogue_l3 = {
        "prompt": "This is your final warning. This is a restricted area. You do not have authorization. Security has been alerted and will arrive shortly. Do not attempt to proceed.",
        "wait_for_response": False
    }
    
    dialogue_sequence = [dialogue_l1, dialogue_l2, dialogue_l3]

    print("UNAUTHORIZED PERSON DETECTED")
    print("\nInitiating security protocol...\n")
    
    for level, dialogue in enumerate(dialogue_sequence, 1):
        print(f"ESCALATION LEVEL {level}/3")
        print(f"\nAgent: {dialogue['prompt']}")
        speak(dialogue['prompt'])
        
        if dialogue['wait_for_response']:
            user_response = listen_for_response()
            
            # Check for passcode
            if check_passcode(user_response, secret_passcode):
                print("PASSCODE VERIFIED")
                success_msg = "Access code verified. Welcome. You may proceed."
                print(f"\nAgent: {success_msg}\n")
                speak(success_msg)
                return "PASSCODE_GRANTED"
            
            # Check for force entry attempt
            if detect_force_entry_attempt(user_response):
                print("\nFORCING ENTRY DETECTED - SKIPPING TO FINAL WARNING\n")
                # Skip to level 3
                print("ESCALATION LEVEL 3/3 - FINAL WARNING")
                print(f"\nAgent: {dialogue_l3['prompt']}")
                speak(dialogue_l3['prompt'])
                time.sleep(2)
                return "SECURITY_CALLED"
            
            # If no passcode and not forcing entry, continue to next level
            if level < 3:
                print(f"Escalating to Level {level + 1}...")
                time.sleep(1)
        else:
            # Level 3 - just wait a moment
            time.sleep(2)
    
    print("SECURITY ALERT: Unauthorized access attempt logged")
    return "SECURITY_CALLED"
