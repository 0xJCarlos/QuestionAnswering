from dotenv import load_dotenv
import os
import requests 
import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button, StringVar
from tkinter.ttk import Combobox
from bs4 import BeautifulSoup
import requests

#Cargar variable de entorno
load_dotenv()

class QABotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Preguntale a BERT")

        self.url_label = tk.Label(root, text="Ingresa una URL:")
        self.url_entry = tk.Entry(root, width=50)
        self.url_button = tk.Button(root, text="Conseguir datos", command=self.fetch_data)

        # Initialize a list to store history
        self.history = []

        # Entry field to display selected history item
        self.selected_history = StringVar()
        self.history_combobox = Combobox(root, textvariable=self.selected_history, state="readonly", width=46)
        self.history_combobox.bind("<<ComboboxSelected>>", self.load_selected_history)

        self.chat_scrollbar = Scrollbar(root)
        self.chat_display = Text(root, height=20, width=80, yscrollcommand=self.chat_scrollbar.set)
        self.chat_display.config(state=tk.DISABLED)

        self.question_entry = Entry(root, width=60)
        self.ask_button = Button(root, text="Preguntar", command=self.ask_question)

        # Pack widgets
        self.url_label.pack(pady=5)
        self.url_entry.pack(pady=5)

        self.history_combobox.pack(pady=5)

        self.url_button.pack(pady=5)

        self.chat_display.pack(pady=10)
        self.chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.question_entry.pack(pady=5)
        self.ask_button.pack(pady=5)

    def fetch_data(self):
        url = self.url_entry.get()
        if url:
            # Save unique URLs to history
            if url not in self.history:
                self.history.append(url)
                self.update_history_combobox()

            content = self.extract_content(url)
            self.display_message("Sistema: ", f"Datos recuperados de: {url}")

    def update_history_combobox(self):
        # Clear and update the Combobox with unique URLs
        self.history_combobox["values"] = tuple(self.history)

    def load_selected_history(self, event):
        # Load the selected history item into the URL entry field
        selected_url = self.selected_history.get()
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, selected_url)

    def ask_question(self):
        question = self.question_entry.get()
        if question:
            context = self.extract_content(self.url_entry.get())
            self.question_entry.delete(0,'end')

            # Display loading message
            loading_message = self.display_message("Sistema: ", "Cargando...")

            payload = {'inputs': {'question': question, 'context': context}}
            answer = self.query(payload)
            print("Answer" + str(answer))
            if (str(answer.get('answer')) == "None"):
                answer = "El modelo se encuentra cargando, espera unos segundos..."
            

            # Display the user's question and the bot's answer
            self.display_message("Pregunta", f": {question}")
            self.display_message("Respuesta", f": {answer.get('answer')}")
            print(f"Respuesta del Bot: {answer.get('answer')}")


    def extract_content(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return f"Error accessing the URL: {e}"

        soup = BeautifulSoup(response.text, 'html.parser')

        # Directly check if the URL contains 
        if "https://es.wikipedia.org/wiki" in url:
            main_content = soup.find('div', {'class': 'mw-content-ltr mw-parser-output'})

        else:
            # Default action for other websites
            main_content = soup

        if main_content:
            page_text = main_content.get_text()
            return page_text
        else:
            return "No se encontró contenido"

    def query(self, payload):
        model_id = "MMG/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es-finetuned-sqac"
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