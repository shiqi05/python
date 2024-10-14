import requests
import json
import os
import time
from tkinter import Tk, Entry, Button, Text, END, messagebox, Frame, Scrollbar
from tkinter.font import Font

# 遵循PEP8规范，常量使用全大写字母命名
API_URL = 'http://api.qingyunke.com/api.php'
API_KEY = 'free'
APPID = 0
FONT = ("Arial", 10)

def send(event=None):
    user_input = input_entry.get()
    if not user_input:
        messagebox.showwarning("提示", "请输入内容后再发送。")
        return
    if user_input.lower() == "关机":
        os.system("shutdown /s /t 0")
        return

    # 构建请求URL，符合API要求
    url = f"{API_URL}?key={API_KEY}&appid={APPID}&msg={user_input}"

    try:
        # 控制请求频率，这里简单示例，每10分钟内最多200次请求
        if can_send_request():
            response = requests.post(url, timeout=5)
            data = response.json()
            text_area.config(state='normal')
            formatted_question = f"{user_input}：问"
            text_area.insert(END, f"{formatted_question}\n", 'question')
            text_area.tag_configure('question', justify='right', font=FONT)
            text_area.insert(END, f"答：{data.get('content', '')}\n", 'answer')
            text_area.tag_configure('answer', foreground='green', font=FONT)
            text_area.config(state='disabled')
            # 记录请求时间，用于控制频率
            update_last_request_time()
        else:
            raise requests.RequestException("请求过于频繁，请稍后再试。")
    except requests.exceptions.Timeout:
        text_area.config(state='normal')
        text_area.insert(END, "请求超时，请检查网络连接或稍后再试。")
        text_area.tag_configure('error', foreground='red', font=FONT)
        text_area.config(state='disabled')
    except requests.exceptions.RequestException as e:
        error_message = f"请求错误：{str(e)}。请检查输入内容或网络连接。"
        text_area.config(state='normal')
        text_area.insert(END, error_message + '\n', 'error')
        text_area.tag_configure('error', foreground='red', font=FONT)
        text_area.config(state='disabled')
    except json.JSONDecodeError as jde:
        error_message = f"JSON解析错误：{str(jde)}。请检查输入内容格式。"
        text_area.config(state='normal')
        text_area.insert(END, error_message + '\n', 'error')
        text_area.tag_configure('error', foreground='red', font=FONT)
        text_area.config(state='disabled')
    input_entry.delete(0, END)

# 用于记录上次请求时间
last_request_time = 0

def can_send_request():
    current_time = time.time()
    # 10分钟时间限制，单位为秒
    time_limit = 10 * 60
    if current_time - last_request_time > time_limit:
        return True
    return False

def update_last_request_time():
    global last_request_time
    last_request_time = time.time()

root = Tk()
root.title("作者拾柒(1.4版本)")
scrollbar = Scrollbar(root)
scrollbar.pack(side='right', fill='y')
text_area = Text(root, height=30, width=40, yscrollcommand=scrollbar.set)
text_area.config(state='disabled', exportselection=False)
text_area.tag_config('question', foreground='blue')
text_area.tag_config('answer', foreground='green')
text_area.tag_config('error', foreground='red')
text_area.pack()
scrollbar.config(command=text_area.yview)
input_frame = Frame(root)
input_frame.pack(side='bottom', pady=10)
input_entry = Entry(input_frame, width=33)
input_entry.bind("<Return>", send)
input_entry.pack(side='left')
send_button = Button(input_frame, text="\u2191", command=send, font=FONT)
send_button.pack(side='left', padx=5)
root.mainloop()