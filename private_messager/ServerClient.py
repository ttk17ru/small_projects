import sys
import socket
import threading
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel,
    QComboBox, QFileDialog, QInputDialog
)
from PyQt6.QtCore import Qt

class ChatClient(QWidget):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.username = None
        self.current_room = "main"

        self.init_ui()
        self.connect_to_server()
        self.start_receive_thread()

    def init_ui(self):
        self.setWindowTitle("TTK Private Messager")
        # Set window icon
        self.setWindowIcon(QIcon("hacky.png"))
        self.resize(600, 400)

        # Dark theme style
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                font-family: Segoe UI, Arial, sans-serif;
                font-size: 18px;
                color: #66FF66;
            }
            QTextEdit {
                background-color: black;
                border: 1px solid #333333;
            }
            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                color: #eeeeee;
            }
            QPushButton {
                background-color: #2a82da;
                border-radius: 5px;
                padding: 6px;
                color: white;
            }
            QPushButton:hover {
                background-color: #1f5bb5;
            }
            QComboBox {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                color: #eeeeee;
            }
        """)

        layout = QVBoxLayout()

        # Room selection dropdown
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Room:"))
        self.room_combo = QComboBox()
        self.room_combo.addItems(["main", "room1", "room2"])
        self.room_combo.currentTextChanged.connect(self.change_room)
        top_layout.addWidget(self.room_combo)
        layout.addLayout(top_layout)

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Message input + send button + file upload button
        bottom_layout = QHBoxLayout()
        self.msg_input = QLineEdit()
        self.msg_input.returnPressed.connect(self.send_message)
        bottom_layout.addWidget(self.msg_input)

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        bottom_layout.addWidget(self.send_btn)

        self.file_btn = QPushButton("Upload File")
        self.file_btn.clicked.connect(self.upload_file)
        bottom_layout.addWidget(self.file_btn)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)

        # Prompt for username on start
        self.prompt_username()

    def prompt_username(self):
        username, ok = QInputDialog.getText(self, "Enter Username", "Please enter your username:")
        if ok and username.strip():
            self.username = username.strip()
            self.chat_display.append(f"*** Welcome, {self.username}! ***")
        else:
            self.close()  # Exit app if no username

    def connect_to_server(self):
        try:
            self.sock.connect((self.host, self.port))
            # Send username as initial message (optional)
            self.sock.send(self.username.encode())
            # Join initial room
            self.sock.send(f"/room {self.current_room}".encode())
        except Exception as e:
            self.chat_display.append(f"Connection error: {e}")
            self.close()

    def start_receive_thread(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break

                # Check if it's a file
                if data.startswith(b"[FILE] "):
                    header, file_data = data.split(b"\n", 1)
                    filename = header[7:].decode(errors="ignore")  # Remove "[FILE] "

                    # Save file locally
                    with open(f"received_{filename}", "wb") as f:
                        f.write(file_data)

                    self.chat_display.append(f"[Received file] saved as received_{filename}")
                    continue

                # Else: normal chat text
                text = data.decode(errors='ignore')
                self.chat_display.append(text)

            except Exception as e:
                self.chat_display.append(f"Connection lost: {e}")
                break


    def send_message(self):
        msg = self.msg_input.text().strip()
        if msg:
            try:
                self.sock.send(msg.encode())
                self.chat_display.append(f"[Me] {msg}")
                self.msg_input.clear()
            except Exception as e:
                self.chat_display.append(f"Send error: {e}")

    def change_room(self, room_name):
        self.current_room = room_name
        try:
            self.sock.send(f"/room {room_name}".encode())
            self.chat_display.append(f"*** Switched to room: {room_name} ***")
        except Exception as e:
            self.chat_display.append(f"Room change error: {e}")

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file to upload")
        if file_path:
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                filename = file_path.split("/")[-1]
                self.sock.send(f"/file {filename}".encode())
                self.sock.send(f"{len(content):<16}".encode())
                self.sock.sendall(content)
                self.chat_display.append(f"[Me] Sent file: {filename}")
            except Exception as e:
                self.chat_display.append(f"File upload error: {e}")

    def closeEvent(self, event):
        try:
            self.sock.close()
        except:
            pass
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = ChatClient("127.0.0.1", 6999)
    client.show()
    sys.exit(app.exec())
