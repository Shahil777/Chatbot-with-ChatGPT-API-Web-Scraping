# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Original file is located at
    https://colab.research.google.com/drive/166MtHw2KJdPQH5iMMBOBrPwMP3PyVUtm
"""

import os
import requests
import google.generativeai as genai
from bs4 import BeautifulSoup

# ✅ Set up Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBFcW92giviOlUJenfuiP21jKUoNhqAD54")  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Function to scrape website content
def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_data = [p.text.strip() for p in soup.find_all('p')]
            return " ".join(text_data)[:3000]  # Limit to 3000 characters for API efficiency
        else:
            return "Error: Unable to fetch website data."
    except Exception as e:
        return f"Error: {str(e)}"

# ✅ Chatbot function using Gemini API
def chatbot(website_url):
    website_data = scrape_website(website_url)
    if "Error" in website_data:
        print(website_data)
        return

    print("\n✅ Chatbot is ready! Type 'exit' to stop.\n")

    model = genai.GenerativeModel("gemini-2.0-flash")  # ✅ Use the correct model

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("🚪 Chatbot session ended.")
            break

        try:
            response = model.generate_content([
                {"role": "user", "parts": [{"text": f"Website info: {website_data}"}]},
                {"role": "user", "parts": [{"text": user_input}]}
            ])
            chatbot_reply = response.text
            print("\nBot:", chatbot_reply, "\n")

        except Exception as e:
            print("Error communicating with Gemini API:", str(e))

# ✅ Main execution
if __name__ == "__main__":
    website_url = input("Enter the website URL to scrape: ")
    chatbot(website_url)
