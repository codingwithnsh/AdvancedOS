# AdvancedOS

## 📚 Overview
AdvancedOS is an innovative desktop environment built using Python's Tkinter library. It is designed to emulate a lightweight operating system interface, complete with a taskbar, customizable desktop, and various built-in applications. This project aims to provide a functional, extendable framework for learning and experimenting with GUI-based systems.

Currently, AdvancedOS is under active development, and contributions or suggestions for improvements are welcome.

---

## 💡 Features

### 1. **Desktop Environment**
The AdvancedOS desktop acts as the primary user interface, featuring:
- **Customizable Themes**: Change the background color to suit your preferences (light blue, gray, or green).
- **Interactive Icons**: Launch built-in utilities directly from the desktop by clicking on intuitive buttons.
- **Expandable Functionality**: Easily add new desktop shortcuts for additional features or applications.

### 2. **Taskbar**
The taskbar provides real-time system information and utilities:
- **Start Button**: Opens a simple Start Menu where users can access settings or exit the application.
- **System Information**: Displays Wi-Fi connectivity, Bluetooth status, and battery percentage, updating every five seconds.
- **Clock**: Shows the current time, updated every second.

### 3. **Built-in Utilities**
AdvancedOS includes several essential tools, each designed for practicality and simplicity:

#### a. **Calculator**
- **Functionality**: Perform basic arithmetic operations.
- **Interactive Design**: Input numbers and operations via a text field and execute them with a "=" button.
- **Error Handling**: Displays an error message for invalid inputs.

#### b. **Text Editor**
- **Rich Editing**: Write and edit text with a simple interface.
- **File Saving**: Save files in `.txt` format using a file dialog.
- **Menu Options**: Includes options to save and exit directly from the menu bar.

#### c. **File Explorer**
- **Browse Files**: Use a file dialog to locate and select files on your system.
- **File Information**: Displays the selected file’s name in a message box.

#### d. **Python Console**
- **Execute Code**: Run Python commands directly within the application.
- **Output Display**: View execution results or errors in a console-like text area.
- **Input Area**: Type commands in a dedicated input section and execute them with a button click.

#### e. **Music Player**
- **Play and Stop**: Basic music playback controls.
- **Future Expansion**: Placeholder for integrating more advanced features like playlists or volume controls.

#### f. **Task Manager**
- **Process Viewer**: Lists all running processes using the `psutil` library.
- **Simple Display**: Presents process names in a scrollable list.

#### g. **Weather App**
- **Real-time Weather**: Fetches weather data for a specified city using the OpenWeatherMap API.
- **Data Display**: Shows temperature (in Celsius) and weather conditions.
- **Error Handling**: Displays a message if weather data cannot be retrieved.

#### h. **Browser**
- **Web Access**: Open a simple web browser powered by the `webview` library.
- **Default URL**: Launches with Google’s homepage but can be customized.

### 4. **Settings Menu**
- **Theme Customization**: Choose between different color themes to personalize the desktop.
- **Expandable Options**: Add future customization features, such as font or icon styles.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Required Python Libraries:
  - `tkinter` (default with Python)
  - `psutil`
  - `requests`
  - `bleak`
  - `webview`

Install required libraries using:
```bash
pip install psutil requests bleak pywebview
```

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/codingwithnsh/AdvancedOS.git
   ```
2. Navigate to the project directory:
   ```bash
   cd AdvancedOS
   ```
3. Run the application:
   ```bash
   python main.py
   ```

---

## 📊 How It Works

### Desktop Icons
Each icon corresponds to a utility or application. Simply click an icon to launch the associated tool.

### Taskbar Information
The taskbar dynamically updates every few seconds to display:
- Current time
- System battery status
- Wi-Fi and Bluetooth connectivity

### Built-in Utilities
The included tools offer core functionality for daily tasks, while providing a framework for integrating new features.

### Customization
Through the settings menu, you can adjust the desktop’s appearance to match your preferences. Themes change the desktop background and provide visual variety.

---

## 🛠️ Contributing
We welcome contributions to improve this project!  
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature description"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## 🔖 License
This project is licensed under the MIT License.

---

## 🙌 Acknowledgments
Special thanks to everyone who has contributed to this project! Your suggestions and contributions are invaluable as we continue to develop AdvancedOS into a robust and versatile desktop environment.
