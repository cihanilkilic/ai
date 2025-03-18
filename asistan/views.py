from django.shortcuts import render
import google.generativeai as genai #pip install google-generativeai
import speech_recognition as sr #pip install SpeechRecognition
from gtts import gTTS #pip install gTTS
from django.http import JsonResponse
import io
import base64
import threading
import queue


def text_to_speech(ai_response, audio_queue):
    """AI yanıtını ses dosyasına çevir ve Base64 olarak kuyruğa ekle"""
    tts = gTTS(text=ai_response, lang="tr")
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    audio_base64 = base64.b64encode(mp3_fp.read()).decode("utf-8")
    audio_queue.put(audio_base64)

def speech_to_text(request):
    """Konuşmayı metne çevir ve AI yanıtını asenkron sesli olarak döndür"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Konuşmayı dinliyorum...")
        audio = recognizer.listen(source)

    try:
        user_text = recognizer.recognize_google(audio, language="tr-TR")

        # === AI Modelinden Yanıt Al ===
        genai.configure(api_key="AIzaSyCAXB_dpcnWNSmyQYtrnwh1dopd_wFUP20")  # API anahtarınızı buraya ekleyin.
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(user_text)
        ai_response = response.text

        # === Yanıtı Asenkron Olarak Seslendirme (Text-to-Speech) ===
        audio_queue = queue.Queue()
        thread = threading.Thread(target=text_to_speech, args=(ai_response, audio_queue))
        thread.start()
        thread.join()  # Ses işleme tamamlanana kadar bekleme

        audio_base64 = audio_queue.get()

        return JsonResponse({"text": ai_response, "audio": audio_base64})

    except sr.UnknownValueError:
        return JsonResponse({"error": "Ses anlaşılamadı."})
    except sr.RequestError:
        return JsonResponse({"error": "Google servislerine erişilemiyor."})
    

def asistan(request):
    """Ana sayfa render edilir"""
    return render(request, "asistan/voice_assistant.html")