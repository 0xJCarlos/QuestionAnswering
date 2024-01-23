from dotenv import load_dotenv
import os
import requests 
import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button
from bs4 import BeautifulSoup
import requests

#Cargar variable de entorno
load_dotenv()

class QABotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Question Answering Chat Bot")

        self.url_label = tk.Label(root, text="Enter URL:")
        self.url_entry = tk.Entry(root, width=50)
        self.url_button = tk.Button(root, text="Fetch Data", command=self.fetch_data)

        self.chat_scrollbar = Scrollbar(root)
        self.chat_display = Text(root, height=20, width=80, yscrollcommand=self.chat_scrollbar.set)
        self.chat_display.config(state=tk.DISABLED)

        self.question_entry = Entry(root, width=60)
        self.ask_button = Button(root, text="Ask", command=self.ask_question)

        # Pack widgets
        self.url_label.pack(pady=5)
        self.url_entry.pack(pady=5)
        self.url_button.pack(pady=5)

        self.chat_display.pack(pady=10)
        self.chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.question_entry.pack(pady=5)
        self.ask_button.pack(pady=5)

    def fetch_data(self):
        url = self.url_entry.get()
        if url:
            content = self.extract_content(url)
            self.display_message("User", f"Fetched data from {url}")

    def ask_question(self):
        question = self.question_entry.get()
        if question:
            context = self.extract_content(self.url_entry.get())
            payload = {'inputs': {'question': question, 'context': context}}
            print(f"Payload sent to Hugging Face: {payload}")
            answer = self.query(payload)
            self.display_message("User", f"User: {question}")
            self.display_message("Bot", f"Bot: {answer.get('answer')}")
            print(f"Bot's Answer: {answer.get('answer')}")

    def extract_content(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return f"Error accessing the URL: {e}"

        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find('div', {'class': 'mw-content-ltr mw-parser-output'})

        if main_content:
            page_text = main_content.get_text()
            return page_text
        else:
            return "No content found"

    def query(self, payload):
        model_id = "mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"
        API_TOKEN = os.getenv('API_TOKEN')
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    def display_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = QABotGUI(root)
    root.mainloop()