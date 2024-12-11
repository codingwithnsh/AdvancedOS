import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import psutil
import webview
import time
import os
import requests
from bleak import discover  # Import bleak for Bluetooth functionality

class AdvancedOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced OS")
        self.root.geometry("1200x800")
        self.root.config(bg="lightgray")

        # Default theme color
        self.theme_color = "lightblue"

        # Create taskbar
        self.create_taskbar()

        # Create desktop
        self.create_desktop()

        # Start system info updater
        self.start_system_info_updater()

        # Update clock every second
        self.update_clock()

    def create_taskbar(self):
        self.taskbar = tk.Frame(self.root, bg="black", height=40)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Start Menu Button
        self.start_btn = tk.Button(self.taskbar, text="Start", bg="darkgray", fg="white", command=self.show_start_menu)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        # System Info
        self.sys_info_label = tk.Label(self.taskbar, text="Wi-Fi: -- | Bluetooth: -- | Battery: --%", bg="black", fg="white", font=("Arial", 10))
        self.sys_info_label.pack(side=tk.LEFT, padx=10)

        # Clock
        self.clock_label = tk.Label(self.taskbar, text="", bg="black", fg="white", font=("Arial", 12))
        self.clock_label.pack(side=tk.RIGHT, padx=10)

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def create_desktop(self):
        self.desktop = tk.Frame(self.root, bg=self.theme_color)
        self.desktop.pack(fill=tk.BOTH, expand=True)

        # Desktop icons
        icons = [
            ("Notepad", self.open_text_editor),
            ("File Explorer", self.open_file_explorer),
            ("Calculator", self.open_calculator),
            ("Browser", self.open_browser),
            ("Python Console", self.open_python_console),
            ("Music Player", self.open_music_player),
            ("Task Manager", self.open_task_manager),
            ("Weather", self.open_weather_app),
        ]

        for i, (text, command) in enumerate(icons):
            icon = tk.Button(self.desktop, text=text, command=command, width=15, height=2)
            icon.place(x=50, y=50 + i * 70)

    def show_start_menu(self):
        start_menu = tk.Toplevel(self.root)
        start_menu.title("Start Menu")
        start_menu.geometry("200x300")
        start_menu.resizable(False, False)

        tk.Label(start_menu, text="Start Menu", font=("Arial", 14)).pack(pady=10)

        btn_settings = tk.Button(start_menu, text="Settings", command=self.open_settings)
        btn_settings.pack(fill=tk.X, pady=5)

        btn_exit = tk.Button(start_menu, text="Exit", command=self.root.quit)
        btn_exit.pack(fill=tk.X, pady=5)

    def open_calculator(self):
        calc = tk.Toplevel(self.root)
        calc.title("Calculator")
        calc.geometry("300x400")
        calc.resizable(False, False)

        def calculate():
            try:
                result = eval(entry.get())
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(result))
            except Exception:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error")

        entry = tk.Entry(calc, font=("Arial", 18), justify="right")
        entry.pack(fill=tk.BOTH, padx=10, pady=10)

        btn_calc = tk.Button(calc, text="=", command=calculate, font=("Arial", 14))
        btn_calc.pack(fill=tk.BOTH, padx=10, pady=10)

    def open_text_editor(self):
        editor = tk.Toplevel(self.root)
        editor.title("Text Editor")
        editor.geometry("600x400")
        editor.resizable(True, True)

        text_area = tk.Text(editor, font=("Arial", 12))
        text_area.pack(fill=tk.BOTH, expand=True)

        def save_file():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(text_area.get(1.0, tk.END))
                messagebox.showinfo("File Saved", f"File saved at {file_path}")

        menu_bar = tk.Menu(editor)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save", command=save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=editor.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        editor.config(menu=menu_bar)

    def open_file_explorer(self):
        file_explorer = tk.Toplevel(self.root)
        file_explorer.title("File Explorer")
        file_explorer.geometry("500x300")

        def browse_files():
            file_path = filedialog.askopenfilename()
            if file_path:
                messagebox.showinfo("File Selected", f"You selected: {file_path}")

        tk.Button(file_explorer, text="Browse Files", command=browse_files).pack(pady=20)

    def open_browser(self):
        # Launch the browser in the main thread to avoid the pywebview error
        webview.create_window("Advanced Browser", "https://www.google.com")
        webview.start()

    def open_music_player(self):
        music_player = tk.Toplevel(self.root)
        music_player.title("Music Player")
        music_player.geometry("300x200")
        
        def play_music():
            messagebox.showinfo("Music Player", "Playing music...")

        def stop_music():
            messagebox.showinfo("Music Player", "Music stopped.")
        
        tk.Button(music_player, text="Play", command=play_music).pack(pady=20)
        tk.Button(music_player, text="Stop", command=stop_music).pack(pady=5)

    def open_task_manager(self):
        task_manager = tk.Toplevel(self.root)
        task_manager.title("Task Manager")
        task_manager.geometry("400x300")

        processes = [proc.info['name'] for proc in psutil.process_iter(['name'])]
        processes_list = '\n'.join(processes)
        tk.Label(task_manager, text=f"Running Processes:\n{processes_list}", font=("Arial", 10)).pack(pady=10)

    def open_weather_app(self):
        weather_app = tk.Toplevel(self.root)
        weather_app.title("Weather")
        weather_app.geometry("400x300")

        city = "New York"
        api_key = "YOUR_API_KEY_HERE"  # Replace with a valid OpenWeatherMap API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q=udupi&appid={api_key}"

        response = requests.get(url)
        weather_data = response.json()

        if weather_data.get("cod") == 200:
            main_data = weather_data['main']
            temp = main_data['temp'] - 273.15  # Convert Kelvin to Celsius
            weather_desc = weather_data['weather'][0]['description']
            temp_text = f"Temperature: {temp:.2f}°C\nCondition: {weather_desc.capitalize()}"
            tk.Label(weather_app, text=temp_text, font=("Arial", 12)).pack(pady=20)
        else:
            tk.Label(weather_app, text="Failed to retrieve data.", font=("Arial", 12)).pack(pady=20)

    def open_settings(self):
        settings = tk.Toplevel(self.root)
        settings.title("Settings")
        settings.geometry("400x300")
        settings.resizable(False, False)

        tk.Label(settings, text="Settings", font=("Arial", 16)).pack(pady=10)

        def change_theme(color):
            self.theme_color = color
            self.desktop.config(bg=color)

        tk.Button(settings, text="Blue Theme", command=lambda: change_theme("lightblue")).pack(fill=tk.X, pady=5)
        tk.Button(settings, text="Gray Theme", command=lambda: change_theme("gray")).pack(fill=tk.X, pady=5)
        tk.Button(settings, text="Green Theme", command=lambda: change_theme("lightgreen")).pack(fill=tk.X, pady=5)

    def open_python_console(self):
        console = tk.Toplevel(self.root)
        console.title("Python Console")
        console.geometry("600x400")
        console.resizable(True, True)

        # Text area for console output
        text_area = tk.Text(console, font=("Courier", 12))
        text_area.pack(fill=tk.BOTH, expand=True)

        def execute_command():
            try:
                # Get user input and execute it
                code = input_area.get(1.0, tk.END)
                exec(code)
                output = eval(code)
                text_area.insert(tk.END, f"\n{output}\n")
            except Exception as e:
                text_area.insert(tk.END, f"Error: {e}\n")

        input_area = tk.Text(console, font=("Courier", 12), height=5)
        input_area.pack(fill=tk.X, padx=10, pady=10)

        # Execute button to run the Python code
        execute_btn = tk.Button(console, text="Execute", command=execute_command)
        execute_btn.pack(pady=5)

    def start_system_info_updater(self):
        def update_system_info():
            battery = psutil.sensors_battery()
            wifi = "Connected" if psutil.net_if_addrs().get("Wi-Fi") else "Not Connected"
            bluetooth = self.get_bluetooth_status()  # Get Bluetooth status using bleak
            battery_percent = battery.percent if battery else "--"
            self.sys_info_label.config(text=f"Wi-Fi: {wifi} | Bluetooth: {bluetooth} | Battery: {battery_percent}%")
            self.root.after(5000, update_system_info)

        update_system_info()

    def get_bluetooth_status(self):
        # Use bleak to check Bluetooth status
        devices = discover()
        if devices:
            return "On"
        else:
            return "Off"

if __name__ == "__main__":
    root = tk.Tk()
    os_app = AdvancedOS(root)
    root.mainloop()
