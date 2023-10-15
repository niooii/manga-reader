import logging
import sys
from datetime import datetime
from tkinter import messagebox

from manga_ocr import MangaOcr
import pyperclip as pc
from PIL import ImageGrab
import time
import requests
import ctypes
import tkinter
import threading

run = True

consoleIndex = 0


def getTimeStampedString(string):
    timestamp = datetime.now().timestamp()
    date_time = datetime.fromtimestamp(timestamp)
    str_date_time = date_time.strftime("%m-%d-%Y %H:%M:%S")
    return '[' + str_date_time + ']  ' + string


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def consoleLog(string):
    global consoleIndex
    consoleIndex += 1
    # console.insert(consoleIndex, getTimeStampedString(string))
    # console.yview(consoleIndex)


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def translate(text: str):
    payload = {
        'key': f'{"trnsl.1.1.20230613T034449Z.d095ac9242cfee22.2a116578a7196b2c435f49f847b2b224156f9ea4"}',
        'text': f'{text}',
        'lang': 'ja-en'
    }

    r = requests.post(f"https://translate.yandex.net/api/v1.5/tr/translate", data=payload)
    # print(r.content)
    if r.status_code == 200:
        yes = r.text.index('<text>')
        no = r.text.index('</text>')
        return text, r.text[yes + 6:no]
    else:
        return "error", "error"


# window = tkinter.Tk()
# window.geometry("800x800")


# def on_closing():
#     if messagebox.askokcancel("Are you sure?", "Closing this window will end all threads. Proceed?"):
#         window.destroy()
#         sys.exit(0)


# window.protocol("WM_DELETE_WINDOW", on_closing)
#
# window.title("Translationer")
# frame = tkinter.Frame(window)
# frame.pack()
#
# inputFrame = tkinter.LabelFrame(frame, text="Information")
# inputFrame.grid(row=0, column=0, padx=20, pady=20)
#
# authTokenLabel = tkinter.Label(inputFrame, text="Toggle")
# authTokenLabel.grid(row=0, column=0)


def toggle():
    global run
    run = not run
    consoleLog("Model running." if run else "Model paused.")


# toggleButton = tkinter.Button(inputFrame, text="Toggle", command=toggle)
# toggleButton.grid(row=1, column=0, sticky="news", padx=20, pady=10)
#
# for widget in inputFrame.winfo_children():
#     widget.grid_configure(padx=10, pady=5)
#
# consoleFrame = tkinter.LabelFrame(frame, text="Console")
# consoleFrame.grid(row=1, column=0, sticky="news", padx=20, pady=10)
#
# console = tkinter.Listbox(consoleFrame)
# console.pack(fill="both", expand=True)


mocr = MangaOcr()


def listeningLoop():
    while 1:
        while run:
            try:
                img = ImageGrab.grabclipboard()
                text = mocr(img)
                text = translate(text)
                print(text[0])
                print(text[1])
                Mbox("Translation complete!", "Original text: " + text[0] + "\nTranslation: " + text[1], 1)
                pc.copy('')
                time.sleep(0.1)

            except ValueError:
                time.sleep(0.1)
            except OSError:
                time.sleep(0.1)


# t = threading.Thread(target=listeningLoop)
# t.daemon = True
# t.start()

listeningLoop()


# window.mainloop()
