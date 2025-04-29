import sys
import json
import webbrowser
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QListWidget, QComboBox, QSystemTrayIcon, QMenu, QLabel)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon, QKeySequence

class ExLink(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ExLink")
        self.setGeometry(100, 100, 400, 600)
        self.links = []
        self.current_link_index = 0
        self.key_code = Qt.Key_F5  # Код клавиши по умолчанию
        self.is_setting_key = False
        self.load_links()
        self.init_ui()
        self.init_tray()

    def init_ui(self):
        # Главный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Поле ввода URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Введите URL")
        main_layout.addWidget(self.url_input)

        # Кнопка "Добавить"
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_link)
        main_layout.addWidget(self.add_button)

        # Список ссылок
        self.links_list = QListWidget()
        self.links_list.addItems(self.links)
        main_layout.addWidget(self.links_list)

        # Кнопка "Удалить выбранное"
        self.remove_button = QPushButton("Удалить выбранное")
        self.remove_button.clicked.connect(self.remove_link)
        main_layout.addWidget(self.remove_button)

        # Layout для кнопок открытия
        open_buttons_layout = QHBoxLayout()

        # Кнопка "Открыть случайно"
        self.open_random_button = QPushButton("Открыть случайно")
        self.open_random_button.clicked.connect(self.open_random_link)
        open_buttons_layout.addWidget(self.open_random_button)

        # Кнопка "Открыть следующий"
        self.open_next_button = QPushButton("Открыть следующий")
        self.open_next_button.clicked.connect(self.open_next_link)
        open_buttons_layout.addWidget(self.open_next_button)

        main_layout.addLayout(open_buttons_layout)

        # Выпадающее меню для таймера
        self.timer_combo = QComboBox()
        self.timer_combo.addItems(["Без таймера", "5 сек", "10 сек", "30 сек", "60 сек", "300 сек"])
        self.timer_combo.currentIndexChanged.connect(self.update_timer)
        main_layout.addWidget(self.timer_combo)

        # Интерфейс для задания клавиши
        key_layout = QHBoxLayout()
        key_label = QLabel("Клавиша для случайного открытия:")
        key_layout.addWidget(key_label)
        self.key_display = QLabel(self.key_to_string(self.key_code))
        key_layout.addWidget(self.key_display)
        self.set_key_button = QPushButton("Задать клавишу")
        self.set_key_button.clicked.connect(self.start_setting_key)
        key_layout.addWidget(self.set_key_button)
        main_layout.addLayout(key_layout)

        # Таймер
        self.timer = QTimer()
        self.timer.timeout.connect(self.open_random_link)

        # Стили (темная тема)
        self.setStyleSheet("""
            QMainWindow, QWidget { background-color: #2b2b2b; color: #ffffff; }
            QLineEdit, QListWidget, QComboBox, QLabel { 
                background-color: #3c3f41; 
                color: #ffffff; 
                border: 1px solid #555555; 
                padding: 5px;
            }
            QPushButton { 
                background-color: #4a90e2; 
                color: #ffffff; 
                border: none; 
                padding: 8px; 
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #357abd; }
        """)

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self)
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Показать")
        quit_action = tray_menu.addAction("Выход")
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(QApplication.quit)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_activated)
        self.tray_icon.show()

    def tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def load_links(self):
        try:
            with open("links.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    self.links = []
                    self.key_code = Qt.Key_F5
                else:
                    data = json.loads(content)
                    self.links = data.get("links", [])
                    self.key_code = data.get("key_code", Qt.Key_F5)
        except (FileNotFoundError, json.JSONDecodeError):
            self.links = []
            self.key_code = Qt.Key_F5

    def save_links(self):
        data = {
            "links": self.links,
            "key_code": self.key_code
        }
        with open("links.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def add_link(self):
        url = self.url_input.text().strip()
        if url:
            self.links.append(url)
            self.links_list.addItem(url)
            self.url_input.clear()
            self.save_links()

    def remove_link(self):
        selected_items = self.links_list.selectedItems()
        for item in selected_items:
            self.links.remove(item.text())
            self.links_list.takeItem(self.links_list.row(item))
        self.save_links()

    def open_random_link(self):
        if self.links:
            url = random.choice(self.links)
            webbrowser.open(url)

    def open_next_link(self):
        if self.links:
            url = self.links[self.current_link_index]
            webbrowser.open(url)
            self.current_link_index = (self.current_link_index + 1) % len(self.links)

    def update_timer(self):
        interval = self.timer_combo.currentText()
        self.timer.stop()
        if interval != "Без таймера":
            seconds = int(interval.split()[0])
            self.timer.start(seconds * 1000)

    def start_setting_key(self):
        self.is_setting_key = True
        self.set_key_button.setText("Нажмите клавишу...")
        self.set_key_button.setEnabled(False)

    def key_to_string(self, key_code):
        return QKeySequence(key_code).toString() or "Unknown"

    def keyPressEvent(self, event):
        if self.is_setting_key:
            self.key_code = event.key()
            self.key_display.setText(self.key_to_string(self.key_code))
            self.is_setting_key = False
            self.set_key_button.setText("Задать клавишу")
            self.set_key_button.setEnabled(True)
            self.save_links()
        elif event.key() == self.key_code:
            self.open_random_link()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "ExLink",
            "Приложение свернуто в системный трей.",
            QSystemTrayIcon.Information,
            2000
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExLink()
    window.show()
    sys.exit(app.exec_())
