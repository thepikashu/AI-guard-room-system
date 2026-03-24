SECRET_PASSCODE = "alpha"  
# The user must say this phrase (not case-sensitive)

def speak(text):
    """Converts text to speech and plays it."""
    try:
        import pygame
        tts = gTTS(text=text, lang='en', tld='com', slow=False)
        audio_file = f"response_{time.time()}.mp3"
        tts.save(audio_file)
        
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        pygame.mixer.quit()
        os.remove(audio_file)
    except Exception as e:
        print(f"Speech error: {e}")
        print(f"Agent says: {text}")

def listen_for_response(timeout=15):
    """Listens for the user's voice and returns the transcribed text."""
    r = sr.Recognizer()
    r.energy_threshold = 3000
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1.5
    
    try:
        with sr.Microphone() as source:
            print("\nListening... (you have 15 seconds)")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=timeout, phrase_time_limit=15)
        
        print("Processing speech...")
        response = r.recognize_google(audio, language='en-US')
        print(f"You said: '{response}'\n")
        return response
        
    except sr.UnknownValueError:
        print("Could not understand audio\n")
        return ""
    except sr.WaitTimeoutError:
        print("No speech detected\n")
        return ""
    except Exception as e:
        if "Bad CPU" not in str(e):
            print(f"Error: {e}\n")
        return ""
