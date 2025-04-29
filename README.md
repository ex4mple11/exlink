ExLink
ExLink is a Python-based GUI application built with PyQt5 that allows users to manage a list of URLs and open them either manually or automatically on a timer. The application runs in the background with a system tray icon, supports random or sequential URL opening, and stores URLs in a JSON file for persistence.
Features

Manage URLs: Add, remove, and view URLs in a user-friendly interface.
Open URLs: Open URLs manually (randomly or sequentially) or automatically on a timer (5, 10, 30, 60, or 300 seconds).
System Tray: Minimize to the system tray for background operation, with a context menu to show or quit the app.
Persistent Storage: URLs are saved in a links.json file.
Modern Design: Dark-themed GUI with a clean, professional look.
Cross-Platform: Runs on Windows, macOS, and Linux (Windows compilation instructions provided).

Screenshots
(Add screenshots of the GUI here for better visualization. For example, show the main window, system tray icon, and URL list.)
Prerequisites

Python 3.6 or higher (tested with Python 3.13).
PyQt5 library for the GUI.
(Optional) PyInstaller for compiling to .exe on Windows.
(Optional) A PNG icon file (icon.png) for the system tray and .exe icon.

Installation

Clone the repository:
git clone https://github.com/ex4mple11/ExLink.git
cd ExLink


Install dependencies:
pip install PyQt5


Prepare the icon (optional):

Place a icon.png file (16x16 or 32x32 pixels recommended) in the project directory for the system tray icon.
If no icon is available, modify exlink.py to use QIcon() instead of QIcon("icon.png") in the init_tray method.


Run the application:
python exlink.py



Usage

Add URLs:

Enter a URL in the input field and click "Add".
URLs are saved to links.json in the same directory.


Remove URLs:

Select a URL in the list and click "Remove Selected".


Open URLs:

Manually: Click "Open Random" to open a random URL or "Open Next" to open the next URL in sequence.
Automatically: Select a timer interval (5, 10, 30, 60, or 300 seconds) from the dropdown. The app will open a random URL at the specified interval.


System Tray:

Close the window to minimize the app to the system tray.
Right-click the tray icon to show the app or quit.


Background Operation:

The timer continues to open random URLs even when the app is minimized to the tray.



Compiling to .exe (Windows)
To create a standalone .exe file without a console window:

Install PyInstaller:
pip install pyinstaller


Compile the script:
pyinstaller --onefile --windowed --icon=icon.png --add-data "icon.png;." exlink.py


--onefile: Creates a single .exe.
--windowed: Hides the console window (GUI-only).
--icon=icon.png: Sets the .exe icon.
--add-data "icon.png;.": Includes icon.png for the system tray.


Find the .exe:

The exlink.exe file will be in the dist folder.
Run it by double-clicking. Ensure icon.png is included in the build for the tray icon to work.


(Optional) Include links.json:

To include a pre-populated links.json, add:--add-data "links.json;."





File Structure

exlink.py: Main Python script for the application.
links.json: Auto-generated file to store URLs (created on first URL addition).
icon.png: (Optional) Icon for the system tray and .exe.
README.md: This documentation file.

Example links.json
[
    "https://example.com",
    "https://google.com",
    "https://github.com"
]

Troubleshooting

No system tray icon:
Ensure icon.png is in the project directory and included in the .exe build with --add-data.
Alternatively, replace QIcon("icon.png") with QIcon() in exlink.py.


URLs not opening:
Verify that your default web browser is set correctly.
Check that URLs in links.json are valid.


.exe not running:
Ensure PyQt5 is installed before compiling (pip install PyQt5).
Run the .exe from the command line to see any error messages:.\dist\exlink.exe




Antivirus flags .exe:
Add the .exe to your antivirus exclusions or use a digital certificate to sign it.



Contributing

Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit changes (git commit -m "Add feature").
Push to the branch (git push origin feature-name).
Open a Pull Request.

License
This project is proprietary and not licensed for public use. Contact the author for permissions.
Contact
For questions or suggestions, open an issue or contact Telegram: @ex4mple11bio.

Built with ❤️ using Python and PyQt5.
