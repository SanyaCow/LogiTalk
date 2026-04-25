from customtkinter import *
from socket import *
import threading

class MainWindow(CTk):
   def __init__(self):
       super().__init__()
       self.geometry('400x300')

       self.frame = CTkFrame(self, width=200, height=self.winfo_height())
       self.frame.pack_propagate(False)
       self.frame.configure(width=0)
       self.frame.place(x=0, y=0)
       self.is_show_menu = False
       self.frame_width = 0

       self.label = CTkLabel(self.frame, text='Ваше Ім`я')
       self.label.pack(pady=30)
       self.entry = CTkEntry(self.frame)
       self.entry.pack()
       self.label_theme = CTkOptionMenu(self.frame, values=['Темна', 'Світла'], command=self.change_theme)
       self.label_theme.pack(side='bottom', pady=20)
       self.theme = None
       self.btn = CTkButton(self, text='▶', command=self.toggle_show_menu, width=30)
       self.btn.place(x=0, y=0)
       self.menu_show_speed = 20

       self.chat_text = CTkTextbox(self, state='disable')
       self.chat_text.place(x=0, y=30)

       self.laughing_emoji_btn = CTkButton(self.chat_text,width = 40,height= 40,text ="🤣",command=self.laughing_emoji)
       self.laughing_emoji_btn.place(x=360, y=200)

       self.sad_emoji_btn = CTkButton(self.chat_text, width=40, height=40, text="😥", command=self.sad_emoji)
       self.sad_emoji_btn.place(x=360, y=160)

       self.money_emoji_btn = CTkButton(self.chat_text, width=40, height=40, text="🤑", command=self.money_emoji)
       self.money_emoji_btn.place(x=360, y=120)

       self.sleepy_emoji_btn = CTkButton(self.chat_text, width=40, height=40, text="😴", command=self.sleepy_emoji)
       self.sleepy_emoji_btn.place(x=320, y=200)

       self.angry_emoji_btn = CTkButton(self.chat_text, width=40, height=40, text="😡", command=self.angry_emoji)
       self.angry_emoji_btn.place(x=320, y=160)

       self.upside_emoji_btn = CTkButton(self.chat_text, width=40, height=40, text="🙃", command=self.upside_emoji)
       self.upside_emoji_btn.place(x=320, y=120)

       self.message_input = CTkEntry(self, placeholder_text='Введіть повідомлення:')
       self.message_input.place(x=0, y=250)
       self.send_button = CTkButton(self, text='▶', width=40, height=30, command=self.send_message)
       self.send_button.place(x=200, y=250)

       self.username = "Username"
       try:
           self.sock = socket(AF_INET, SOCK_STREAM)
           self.sock.connect(('localhost', 8080))
           hello = f"TEXT@{self.username}@[SYSTEM] {self.username} приэднався(лася) до чату!\n"
           self.sock.send(hello.encode("utf-8"))
           threading.Thread(target=self.recv_message).start()
       except Exception as e:
           self.add_message(f"Не вдалося підключитися до сервера: {e}")
       self.adaptive_ui()

   def toggle_show_menu(self):
       if self.is_show_menu:
           self.is_show_menu = False
           self.close_menu()
       else:
           self.is_show_menu = True
           self.show_menu()

   def show_menu(self):
       if self.frame_width <= 200:
           self.frame_width += self.menu_show_speed
           self.frame.configure(width=self.frame_width, height=self.winfo_height())
           if self.frame_width >= 30:
               self.btn.configure(width=self.frame_width, text='◀')
       if self.is_show_menu:
           self.after(20, self.show_menu)

   def close_menu(self):
       if self.frame_width >= 0:
           self.frame_width -= self.menu_show_speed
           self.frame.configure(width=self.frame_width)
           if self.frame_width >= 30:
               self.btn.configure(width=self.frame_width, text='▶')
       if not self.is_show_menu:
           self.after(20, self.close_menu)

   def change_theme(self, value):
       if value == 'Темна':
           set_appearance_mode('dark')
       else:
           set_appearance_mode('light')

   def adaptive_ui(self):
       self.chat_text.configure(width=self.winfo_width()-self.frame.winfo_width(), height=self.winfo_height()-self.message_input.winfo_height() - 30)
       self.chat_text.place(x=self.frame.winfo_width()-1)

       self.message_input.configure(width=self.winfo_width()-self.frame.winfo_width()-self.send_button.winfo_width())
       self.message_input.place(x=self.frame.winfo_width(), y=self.winfo_height()-self.send_button.winfo_height())

       self.send_button.place(x=self.winfo_width()-self.send_button.winfo_width(), y=self.winfo_height()-self.send_button.winfo_height())

       self.after(20, self.adaptive_ui)
   def add_message(self,text):
       self.chat_text.configure(state='normal')
       self.chat_text.insert(END, "Я:" + text + "\n")
       self.chat_text.configure(state='disable')

   def send_message(self):
       message = self.entry.get()
       if message:
           self.username = self.entry.get()
           self.add_message(f"{self.username}: {message}")
           data = f"TEXT@{self.username}: {message}@{message}\n"
           try:
               self.sock.sendall(data.encode())
           except:
               pass
       self.message_input.delete(0, END)
       self.entry.delete(0, END)
   def recv_message(self):
       buffer = ""
       while True:
           try:
               chunk = self.sock.recv(4096)
               if not chunk:
                   break
               buffer += chunk.decode()

               while "\n" in buffer:
                   line, buffer = buffer.split("\n", 1)
                   self.handle_line(line.strip())
           except:
               break
       self.sock.close()

   def handle_line(self, line):
       if not line:
           return
       parts = line.split("@",3)
       msg_type = parts[0]

       if msg_type == "TEXT":
           if len(parts) >= 3:
               author = parts[1]
               message = parts[2]
               self.add_message(f"{author}: {message}")
       else:
           self.add_message(line)
   def laughing_emoji(self):
       self.message_input.insert("end","🤣")

   def sad_emoji(self):
       self.message_input.insert("end","😥")

   def money_emoji(self):
       self.message_input.insert("end","🤑")

   def sleepy_emoji(self):
       self.message_input.insert("end", "😴")

   def angry_emoji(self):
       self.message_input.insert("end", "😡")

   def upside_emoji(self):
       self.message_input.insert("end", "🙃")

win = MainWindow()
win.mainloop()