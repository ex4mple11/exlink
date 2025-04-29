import sys
import json
import webbrowser
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLineEdit, QListWidget, QSystemTrayIcon, QMenu,
                            QAction, QComboBox, QLabel)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
from pathlib import Path

class LinkOpener(QMainWindow):
    def __init__(self):
        super().__init__()
        self.links = []
        self.config_file = Path("links.json")
        self.load_links()
        self.initUI()
        self.init_tray()

    def initUI(self):
        self.setWindowTitle("exlink")
        self.setFixedSize(400, 500)
        
        # Set modern style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #3c3f41;
                border: 1px solid #555;
                color: #ffffff;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QListWidget {
                background-color: #3c3f41;
                border: 1px solid #555;
                color: #ffffff;
                border-radius: 3px;
            }
            QComboBox {
                background-color: #3c3f41;
                border: 1px solid #555;
                color: #ffffff;
                padding: 5px;
                border-radius: 3px;
            }
            QLabel {
                color: #ffffff;
            }
        """)

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # URL input
        input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL...")
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_link)
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(add_button)
        layout.addLayout(input_layout)

        # Links list
        self.links_list = QListWidget()
        self.update_links_list()
        layout.addWidget(self.links_list)

        # Remove button
        remove_button = QPushButton("Remove Selected")
        remove_button.clicked.connect(self.remove_link)
        layout.addWidget(remove_button)

        # Timer settings
        timer_layout = QHBoxLayout()
        timer_label = QLabel("Timer (seconds):")
        self.timer_input = QComboBox()
        self.timer_input.addItems(["Off", "5", "10", "30", "60", "300"])
        timer_layout.addWidget(timer_label)
        timer_layout.addWidget(self.timer_input)
        layout.addLayout(timer_layout)

        # Buttons layout for open actions
        buttons_layout = QHBoxLayout()
        
        # Open random button
        open_random_button = QPushButton("Open Random")
        open_random_button.clicked.connect(self.open_random_link)
        buttons_layout.addWidget(open_random_button)

        # Open next button (kept for sequential opening)
        open_button = QPushButton("Open Next")
        open_button.clicked.connect(self.open_next_link)
        buttons_layout.addWidget(open_button)
        
        layout.addLayout(buttons_layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.open_random_link)
        self.timer_input.currentTextChanged.connect(self.update_timer)
        
        self.current_link_index = 0

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))  # You'll need to provide an icon file
        
        tray_menu = QMenu()
        show_action = QAction("Show", self)
        quit_action = QAction("Quit", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
    def load_links(self):
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                try:
                    content = f.read().strip()
                    if content:
                        self.links = json.loads(content)
                    else:
                        self.links = []
                except json.JSONDecodeError:
                    self.links = []
        else:
            self.links = []

    def save_links(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.links, f, indent=4)

    def add_link(self):
        url = self.url_input.text().strip()
        if url and url not in self.links:
            self.links.append(url)
            self.update_links_list()
            self.save_links()
            self.url_input.clear()

    def remove_link(self):
        selected = self.links_list.selectedItems()
        if selected:
            url = selected[0].text()
            self.links.remove(url)
            self.update_links_list()
            self.save_links()

    def update_links_list(self):
        self.links_list.clear()
        for url in self.links:
            self.links_list.addItem(url)

    def update_timer(self, value):
        self.timer.stop()
        if value != "Off":
            interval = int(value) * 1000  # Convert to milliseconds
            self.timer.start(interval)

    def open_random_link(self):
        if self.links:
            random_url = random.choice(self.links)
            webbrowser.open(random_url)

    def open_next_link(self):
        if self.links:
            webbrowser.open(self.links[self.current_link_index])
            self.current_link_index = (self.current_link_index + 1) % len(self.links)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "exlink",
            "Application minimized to system tray",
            QSystemTrayIcon.Information,
            2000
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LinkOpener()
    ex.show()
    sys.exit(app.exec_())
