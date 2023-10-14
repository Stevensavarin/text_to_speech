import tkinter as tk
from tkinter import filedialog
from gtts import gTTS
from googletrans import LANGUAGES
import os
from tkinter import ttk
import threading


def convert_to_audio():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        selected_language_code = language_combobox.get()
        selected_language = LANGUAGES[selected_language_code]

        def conversion_thread():
            progress_bar.start()
            convert_button["state"] = "disabled"

            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                tts = gTTS(text, lang=selected_language_code)
                audio_file = os.path.splitext(os.path.basename(file_path))[0] + ".wav"
                audio_path = os.path.join("converted", audio_file)
                tts.save(audio_path)

            progress_bar.stop()
            convert_button["state"] = "active"
            status_label.config(text=f"Audio converted and saved as {audio_file} in the 'converted' folder.")

        conversion_thread = threading.Thread(target=conversion_thread)
        conversion_thread.start()

def exit_app():
    window.quit()

window = tk.Tk()
window.title("Text To Speech by Steven")

window.geometry("400x350")

window.iconbitmap("img/icono.ico")

bg_image = tk.PhotoImage(file="img/background_image.png")
bg_label = tk.Label(window, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

label = tk.Label(window, text="Select a text file:")
label.pack(pady=10)

open_button = tk.Button(window, text="Select Text File", command=convert_to_audio)
open_button.pack()

language_label = tk.Label(window, text="Select Language:")
language_label.pack(pady=10)
languages = sorted(LANGUAGES.items(), key=lambda x: x[1])
language_var = tk.StringVar(window)
language_var.set("en")
language_combobox = ttk.Combobox(window, textvariable=language_var, 
                                 values=[lang[0] for lang in languages], state="readonly")
language_combobox.pack()


progress_bar = ttk.Progressbar(window, mode="indeterminate")
progress_bar.pack(pady=10)

convert_button = tk.Button(window, text="Convert to Audio", command=convert_to_audio)
convert_button.pack()

status_label = tk.Label(window, text="")
status_label.pack(pady=10)

exit_button = tk.Button(window, text="Exit", command=exit_app)
exit_button.pack(pady=10)

os.makedirs("converted", exist_ok=True)

if __name__ == "__main__":
    window.mainloop()

