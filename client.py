from customtkinter import *
from socket import *
import threading


class MainWindow(CTk):
  def __init__(self):
      super().__init__()
      self.geometry("400x300")
      self.label = None
      # menu
      self.menu_frame = CTkFrame(self, width=30, height=300)
      self.menu_frame.pack_propagate(False)
      self.menu_frame.place(x=0, y=0)
      self.is_show_menu = False
      self.speed_animate_menu = -5
      self.btn = CTkButton(self, text="Run", command=self.toogle_show_menu, width=30)
      self.btn.place(x=0, y=0)
      # main
      self.chat_field = CTkTextbox(self, font=("Arial", 14, "bold"), state="disable")
      self.chat_field.place(x=0, y=0)
      # self.message_entry = CTkEntry(self, height=40,
      #                               placeholder_text="Ведіть повідомлення:")
      # self.message_entry.place(x=40, y=0)
      # self.send_button = CTkButton(self, text="Відправити", width=50,
      #                              height=40, command=self.send_message)
      # self.send_button.place(x=0, y=0)
      self.bottom_frame = CTkFrame(self, height=40)
      self.bottom_frame.pack(side="bottom", fill="x")


      self.send_button = CTkButton(
          self.bottom_frame,
          text="Відправити",
          width=100,
          height=40,
          command=self.send_message
      )
      self.send_button.pack(side="right")


      self.message_entry = CTkEntry(
          self.bottom_frame,
          height=40,
          placeholder_text="Введіть повідомлення:"
      )
      self.message_entry.pack(side="left", fill="x", expand=True)




      self.username = "So77ar91(Точно не Павло, ага)"




      try:
          self.sock = socket(AF_INET, SOCK_STREAM)
          self.sock.connect(("localhost", 8080))
          hello = (f"TEXT@{self.username}@[SYSTEM]{self.username} "
                   f"приєднався(лася) до чату!\n")
          self.sock.send(hello.encode("utf-8"))
          threading.Thread(target=self.recv_message, daemon=True).start()
      except Exception as e:
          self.add_message(f"Не вдалося підключитися до сервера: {e}")
      self.adaptive_ui()




  def toogle_show_menu(self):
      if self.is_show_menu:
          self.is_show_menu = False
          self.speed_animate_menu *= -1
          self.btn.configure(text="Run")
          self.show_menu()
      else:
          self.is_show_menu = True
          self.speed_animate_menu *= -1
          self.btn.configure(text="Stop")
          self.show_menu()
          self.label = CTkLabel(self.menu_frame, text="Ім'я")
          self.label.pack(pady=30)
          self.entry = CTkEntry(self.menu_frame)
          self.entry.pack()




  def show_menu(self):
      self.menu_frame.configure(height=self.winfo_height())
      self.chat_field.place(x=self.menu_frame.winfo_width())
      self.chat_field.configure(width=self.winfo_width() - self.menu_frame.winfo_width(),
                                height=self.winfo_height() - 40)
      self.send_button.place(x=self.winfo_width() - 50, y=self.winfo_height() - 40)
      self.message_entry.place(x=self.menu_frame.winfo_width() + 40,
                               y=self.send_button.winfo_y())
      self.message_entry.configure(width=self.winfo_width() -
                                         self.menu_frame.winfo_width() -
                                         self.send_button.winfo_width())
      self.after(50, self.adaptive_ui)




  def send_message(self):
      message = self.message_entry.get()
      if message:
          self.add_message(f"{self.username}: {message}")
          data = f"TEXT@{self.username}@{message}\n"
          try:
              self.sock.sendall(data.encode())
          except:
              pass
          self.message_entry.delete(0, END)




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


  def add_message(self, text):
      self.chat_field.configure(state="normal")
      self.chat_field.insert(END, "Я " + text + "\n")
      self.chat_field.configure(state="disable")


  def adaptive_ui(self):
      self.menu_frame.configure(height=self.winfo_height())
      self.chat_field.place(
          x=self.menu_frame.winfo_width(),
          y=0
      )
      self.chat_field.configure(
          width=self.winfo_width() - self.menu_frame.winfo_width(),
          height=self.winfo_height() - 40
      )
      self.after(50, self.adaptive_ui)

def handle_line(self,line):
  if not line:
      return
  parts = line.split("@", 3)
  msg_type = parts[0]
  if msg_type == "TEXT":
      if len(parts) >= 3:
          author = parts[1]
          message = parts[2]
          self.add_message(f"{author} : {message}")
  elif msg_type == "IMAGE":
      if len(parts) >= 4:
          author = parts[1]
          filename = parts[2]
          self.add_message(f"{author} надіслав(ла) зображення: {filename}")
  else:
      self.add_message(line)


win = MainWindow()
win.mainloop()



