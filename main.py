import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, colorchooser, font, simpledialog
import psutil
import time
import os
import sys
import json
import datetime
import webbrowser
import subprocess
import platform
import shutil
import math
import random
import string
import ast
from pathlib import Path
from collections import defaultdict
import threading
try:
    import requests
except ImportError:
    requests = None
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
except ImportError:
    Image = ImageTk = ImageDraw = ImageFilter = ImageEnhance = None
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.animation as animation
except ImportError:
    plt = FigureCanvasTkAgg = animation = None

# Import new modules
try:
    from sandbox_dashboard import SandboxDashboard
    from mac_ui_enhancements import (MissionControl, Launchpad, HotCorners, 
                                     DockEnhancer, QuickLook, WindowSnapping, FocusModes)
except ImportError:
    SandboxDashboard = MissionControl = Launchpad = None
    HotCorners = DockEnhancer = QuickLook = WindowSnapping = FocusModes = None

class AdvancedOS:
    def __init__(self, root):
        self.root = root
        self.root.title("AdvancedOS - Modern Operating System")
        self.root.geometry("1400x900")
        
        # Initialize settings
        self.settings = self.load_settings()
        self.theme_mode = self.settings.get('theme_mode', 'light')
        self.accent_color = self.settings.get('accent_color', '#007AFF')
        self.wallpaper_path = self.settings.get('wallpaper', None)
        
        # Window management
        self.open_windows = []
        self.minimized_windows = []
        self.clipboard = ""
        self.clipboard_history = []
        
        # Notifications
        self.notifications = []
        
        # App state
        self.current_user = self.settings.get('username', 'User')
        self.favorites = self.settings.get('favorites', [])
        self.recent_files = self.settings.get('recent_files', [])
        
        # Initialize Mac UI enhancements
        if MissionControl:
            self.mission_control = MissionControl(self.root, self)
            self.launchpad = Launchpad(self.root, self)
            self.hot_corners = HotCorners(self.root, self)
            self.quick_look = QuickLook(self.root, self)
            self.window_snapping = WindowSnapping(self.root, self)
            self.focus_modes = FocusModes(self.root, self)
        
        # Initialize Sandbox Dashboard
        if SandboxDashboard:
            self.sandbox_dashboard = SandboxDashboard(self.root, self)
        
        # Apply theme
        self.apply_theme()
        
        # Create UI components
        self.create_menu_bar()
        self.create_desktop()
        self.create_dock()
        self.create_status_bar()
        
        # Start background tasks
        self.start_system_monitor()
        self.update_clock()
        
        # Keyboard shortcuts
        self.setup_shortcuts()

    
    def load_settings(self):
        """Load settings from JSON file"""
        settings_file = os.path.join(os.path.expanduser('~'), '.advancedos_settings.json')
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def save_settings(self):
        """Save settings to JSON file"""
        settings_file = os.path.join(os.path.expanduser('~'), '.advancedos_settings.json')
        self.settings['theme_mode'] = self.theme_mode
        self.settings['accent_color'] = self.accent_color
        self.settings['wallpaper'] = self.wallpaper_path
        self.settings['username'] = self.current_user
        self.settings['favorites'] = self.favorites
        self.settings['recent_files'] = self.recent_files[:20]  # Keep last 20
        try:
            with open(settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except:
            pass
    
    def apply_theme(self):
        """Apply light or dark theme"""
        if self.theme_mode == 'dark':
            self.bg_color = '#1E1E1E'
            self.fg_color = '#FFFFFF'
            self.secondary_bg = '#2D2D2D'
            self.hover_color = '#3E3E3E'
        else:
            self.bg_color = '#F0F0F0'
            self.fg_color = '#000000'
            self.secondary_bg = '#FFFFFF'
            self.hover_color = '#E0E0E0'
        
        self.root.config(bg=self.bg_color)
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-n>', lambda e: self.open_text_editor())
        self.root.bind('<Control-f>', lambda e: self.open_file_explorer())
        self.root.bind('<Control-t>', lambda e: self.open_terminal())
        self.root.bind('<Alt-Tab>', lambda e: self.show_app_switcher())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        
        # New shortcuts for Mac features
        self.root.bind('<F3>', lambda e: self.mission_control.show() if hasattr(self, 'mission_control') else None)
        self.root.bind('<F4>', lambda e: self.launchpad.show() if hasattr(self, 'launchpad') else None)
        self.root.bind('<Control-space>', lambda e: self.open_spotlight())
        self.root.bind('<Control-Shift-s>', lambda e: self.open_sandbox_manager())
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
    
    def create_menu_bar(self):
        """Create top menu bar (Mac-style)"""
        self.menu_bar = tk.Frame(self.root, bg=self.secondary_bg, height=25)
        self.menu_bar.pack(side=tk.TOP, fill=tk.X)
        
        # App menu
        menus = [
            ('AdvancedOS', [
                ('About AdvancedOS', self.show_about),
                ('Settings', self.open_settings),
                ('---', None),
                ('Quit', self.root.quit)
            ]),
            ('File', [
                ('New Window', lambda: self.open_text_editor()),
                ('Open', lambda: self.open_file_explorer()),
                ('---', None),
                ('Close Window', lambda: None)
            ]),
            ('Edit', [
                ('Cut', lambda: self.clipboard_cut()),
                ('Copy', lambda: self.clipboard_copy()),
                ('Paste', lambda: self.clipboard_paste()),
            ]),
            ('View', [
                ('Toggle Dark Mode', self.toggle_theme),
                ('Notifications', self.show_notification_center),
                ('---', None),
                ('Mission Control', lambda: self.mission_control.show() if hasattr(self, 'mission_control') else None),
                ('Launchpad', lambda: self.launchpad.show() if hasattr(self, 'launchpad') else None),
            ]),
            ('Go', [
                ('Home', lambda: self.open_file_explorer()),
                ('Documents', lambda: self.open_folder(os.path.expanduser('~/Documents'))),
                ('Downloads', lambda: self.open_folder(os.path.expanduser('~/Downloads'))),
            ]),
            ('Window', [
                ('Minimize All', self.minimize_all),
                ('Show All', self.show_all_windows),
                ('---', None),
                ('Hot Corners', lambda: self.hot_corners.configure() if hasattr(self, 'hot_corners') else None),
                ('Snap Left', lambda: None),
                ('Snap Right', lambda: None),
            ]),
            ('Tools', [
                ('Sandbox Manager', self.open_sandbox_manager),
                ('Focus Modes', lambda: self.focus_modes.show_menu() if hasattr(self, 'focus_modes') else None),
                ('---', None),
                ('Quick Look', lambda: None),
            ]),
        ]
        
        for menu_name, items in menus:
            menu_btn = tk.Menubutton(self.menu_bar, text=menu_name, 
                                    bg=self.secondary_bg, fg=self.fg_color,
                                    relief=tk.FLAT, padx=10)
            menu_btn.pack(side=tk.LEFT)
            
            menu = tk.Menu(menu_btn, tearoff=0, bg=self.secondary_bg, fg=self.fg_color)
            for item_name, command in items:
                if item_name == '---':
                    menu.add_separator()
                else:
                    menu.add_command(label=item_name, command=command)
            menu_btn['menu'] = menu

    
    def create_desktop(self):
        """Create main desktop area"""
        self.desktop = tk.Frame(self.root, bg=self.bg_color)
        self.desktop.pack(fill=tk.BOTH, expand=True)
        
        # Set wallpaper if available
        if self.wallpaper_path and os.path.exists(self.wallpaper_path) and Image:
            try:
                img = Image.open(self.wallpaper_path)
                img = img.resize((1400, 900), Image.Resampling.LANCZOS)
                self.wallpaper_photo = ImageTk.PhotoImage(img)
                wallpaper_label = tk.Label(self.desktop, image=self.wallpaper_photo)
                wallpaper_label.place(x=0, y=0, relwidth=1, relheight=1)
            except:
                pass
        
        # Desktop icons grid
        self.desktop_icons_frame = tk.Frame(self.desktop, bg=self.bg_color)
        self.desktop_icons_frame.place(x=20, y=20)
        
        # Create desktop icons
        self.create_desktop_icons()
    
    def create_desktop_icons(self):
        """Create desktop icons in a grid"""
        icons = [
            ('📁 Files', self.open_file_explorer),
            ('📝 Text Editor', self.open_text_editor),
            ('🧮 Calculator', self.open_calculator),
            ('🌐 Browser', self.open_browser),
            ('🖼️ Photos', self.open_photo_viewer),
            ('🎵 Music', self.open_music_player),
            ('🎬 Videos', self.open_video_player),
            ('📧 Mail', self.open_email_client),
            ('📅 Calendar', self.open_calendar),
            ('📋 Notes', self.open_notes),
            ('⚙️ Settings', self.open_settings),
            ('💻 Terminal', self.open_terminal),
            ('🔒 Sandboxes', self.open_sandbox_manager),
            ('🚀 Launchpad', lambda: self.launchpad.show() if hasattr(self, 'launchpad') else None),
        ]
        
        row, col = 0, 0
        for text, command in icons:
            icon_frame = tk.Frame(self.desktop_icons_frame, bg=self.bg_color)
            icon_frame.grid(row=row, column=col, padx=10, pady=10)
            
            btn = tk.Button(icon_frame, text=text, command=command,
                          bg=self.secondary_bg, fg=self.fg_color,
                          relief=tk.FLAT, width=12, height=3,
                          font=('Arial', 10))
            btn.pack()
            
            # Right-click context menu
            btn.bind('<Button-3>', lambda e, cmd=command: self.show_icon_context_menu(e, cmd))
            
            row += 1
            if row >= 6:
                row = 0
                col += 1
    
    def show_icon_context_menu(self, event, command):
        """Show context menu for desktop icon"""
        menu = tk.Menu(self.root, tearoff=0, bg=self.secondary_bg, fg=self.fg_color)
        menu.add_command(label="Open", command=command)
        menu.add_command(label="Add to Favorites", command=lambda: self.add_to_favorites(command))
        menu.post(event.x_root, event.y_root)
    
    def create_dock(self):
        """Create Mac-style dock at bottom"""
        self.dock = tk.Frame(self.root, bg='#2C2C2E', height=70)
        self.dock.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Dock container with centered apps
        dock_container = tk.Frame(self.dock, bg='#2C2C2E')
        dock_container.pack(expand=True)
        
        # Dock applications
        dock_apps = [
            ('🔍', 'Spotlight', self.open_spotlight),
            ('📁', 'Finder', self.open_file_explorer),
            ('🌐', 'Browser', self.open_browser),
            ('✉️', 'Mail', self.open_email_client),
            ('📅', 'Calendar', self.open_calendar),
            ('📝', 'Notes', self.open_notes),
            ('🎵', 'Music', self.open_music_player),
            ('📷', 'Photos', self.open_photo_viewer),
            ('🔒', 'Sandboxes', self.open_sandbox_manager),
            ('⚙️', 'Settings', self.open_settings),
            ('💻', 'Terminal', self.open_terminal),
            ('📊', 'Activity', self.open_activity_monitor),
            ('🗑️', 'Trash', self.open_trash),
        ]
        
        for icon, tooltip, command in dock_apps:
            btn = tk.Button(dock_container, text=icon, command=command,
                          bg='#2C2C2E', fg='white',
                          relief=tk.FLAT, font=('Arial', 24),
                          width=2, height=1, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5, pady=10)
            
            # Add tooltip
            self.create_tooltip(btn, tooltip)
            
            # Hover effect
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#3C3C3E'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#2C2C2E'))
    
    def create_tooltip(self, widget, text):
        """Create tooltip for widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, bg='#FFE4B5', fg='black', 
                           relief=tk.SOLID, borderwidth=1, padx=5, pady=2)
            label.pack()
            widget.tooltip = tooltip
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
        
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)
    
    def create_status_bar(self):
        """Create status bar with system info"""
        self.status_bar = tk.Frame(self.root, bg=self.secondary_bg, height=25)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, before=self.dock)
        
        # System information
        self.cpu_label = tk.Label(self.status_bar, text="CPU: 0%", 
                                 bg=self.secondary_bg, fg=self.fg_color, font=('Arial', 9))
        self.cpu_label.pack(side=tk.LEFT, padx=5)
        
        self.ram_label = tk.Label(self.status_bar, text="RAM: 0%", 
                                 bg=self.secondary_bg, fg=self.fg_color, font=('Arial', 9))
        self.ram_label.pack(side=tk.LEFT, padx=5)
        
        self.disk_label = tk.Label(self.status_bar, text="Disk: 0%", 
                                  bg=self.secondary_bg, fg=self.fg_color, font=('Arial', 9))
        self.disk_label.pack(side=tk.LEFT, padx=5)
        
        # Network indicator
        self.network_label = tk.Label(self.status_bar, text="🌐", 
                                     bg=self.secondary_bg, fg=self.fg_color, font=('Arial', 12))
        self.network_label.pack(side=tk.RIGHT, padx=5)
        
        # Battery indicator
        self.battery_label = tk.Label(self.status_bar, text="🔋 100%", 
                                     bg=self.secondary_bg, fg=self.fg_color, font=('Arial', 9))
        self.battery_label.pack(side=tk.RIGHT, padx=5)
        
        # Clock
        self.clock_label = tk.Label(self.status_bar, text="", 
                                   bg=self.secondary_bg, fg=self.fg_color, font=('Arial', 9))
        self.clock_label.pack(side=tk.RIGHT, padx=10)

    
    def update_clock(self):
        """Update clock every second"""
        current_time = time.strftime("%a %b %d  %I:%M:%S %p")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)
    
    def start_system_monitor(self):
        """Start monitoring system resources"""
        def update_system_info():
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                self.cpu_label.config(text=f"CPU: {cpu_percent}%")
                
                # RAM usage
                ram = psutil.virtual_memory()
                self.ram_label.config(text=f"RAM: {ram.percent}%")
                
                # Disk usage
                disk = psutil.disk_usage('/')
                self.disk_label.config(text=f"Disk: {disk.percent}%")
                
                # Battery
                battery = psutil.sensors_battery()
                if battery:
                    charging = "⚡" if battery.power_plugged else "🔋"
                    self.battery_label.config(text=f"{charging} {battery.percent}%")
                else:
                    self.battery_label.config(text="🔌 AC")
                
                # Network
                net_io = psutil.net_io_counters()
                if net_io.bytes_sent > 0 or net_io.bytes_recv > 0:
                    self.network_label.config(text="🌐")
                else:
                    self.network_label.config(text="📡")
                    
            except Exception as e:
                pass
            
            self.root.after(2000, update_system_info)
        
        update_system_info()
    
    # Helper methods
    def add_to_favorites(self, command):
        """Add item to favorites"""
        if command not in self.favorites:
            self.favorites.append(command)
            self.save_settings()
            self.show_notification("Added to Favorites", "Item added successfully")
    
    def add_to_recent(self, filepath):
        """Add file to recent files"""
        if filepath not in self.recent_files:
            self.recent_files.insert(0, filepath)
            self.recent_files = self.recent_files[:20]
            self.save_settings()
    
    def show_notification(self, title, message, duration=3000):
        """Show notification"""
        notification = tk.Toplevel(self.root)
        notification.title("Notification")
        notification.geometry("300x100+{}+{}".format(
            self.root.winfo_x() + self.root.winfo_width() - 320,
            self.root.winfo_y() + 50
        ))
        notification.attributes('-topmost', True)
        notification.overrideredirect(True)
        
        frame = tk.Frame(notification, bg='#2C2C2E', relief=tk.RAISED, borderwidth=2)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text=title, bg='#2C2C2E', fg='white', 
                font=('Arial', 12, 'bold')).pack(pady=(10, 5))
        tk.Label(frame, text=message, bg='#2C2C2E', fg='white', 
                font=('Arial', 10)).pack(pady=(0, 10))
        
        self.notifications.append(notification)
        notification.after(duration, lambda: self.close_notification(notification))
    
    def close_notification(self, notification):
        """Close notification"""
        if notification in self.notifications:
            self.notifications.remove(notification)
        notification.destroy()
    
    def show_notification_center(self):
        """Show notification center"""
        nc = tk.Toplevel(self.root)
        nc.title("Notification Center")
        nc.geometry("400x600")
        nc.configure(bg=self.bg_color)
        
        tk.Label(nc, text="Notification Center", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Mock notifications
        notifications = [
            ("System Update", "System update available"),
            ("Battery", "Battery at 20%"),
            ("Mail", "You have 3 new messages"),
        ]
        
        for title, msg in notifications:
            frame = tk.Frame(nc, bg=self.secondary_bg, relief=tk.RAISED, borderwidth=1)
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(frame, text=title, bg=self.secondary_bg, fg=self.fg_color,
                    font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=10, pady=(5, 0))
            tk.Label(frame, text=msg, bg=self.secondary_bg, fg=self.fg_color,
                    font=('Arial', 9)).pack(anchor=tk.W, padx=10, pady=(0, 5))
    
    def clipboard_copy(self):
        """Copy to clipboard"""
        try:
            self.clipboard = self.root.clipboard_get()
            self.clipboard_history.insert(0, self.clipboard)
            self.clipboard_history = self.clipboard_history[:10]
        except:
            pass
    
    def clipboard_cut(self):
        """Cut to clipboard"""
        self.clipboard_copy()
    
    def clipboard_paste(self):
        """Paste from clipboard"""
        return self.clipboard
    
    def minimize_all(self):
        """Minimize all windows"""
        for window in self.open_windows:
            if window.winfo_exists():
                window.iconify()
    
    def show_all_windows(self):
        """Show all windows"""
        for window in self.open_windows:
            if window.winfo_exists():
                window.deiconify()
    
    def show_app_switcher(self):
        """Show application switcher (Alt+Tab)"""
        switcher = tk.Toplevel(self.root)
        switcher.title("App Switcher")
        switcher.geometry("500x300")
        switcher.attributes('-topmost', True)
        switcher.configure(bg=self.bg_color)
        
        tk.Label(switcher, text="Open Applications", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        for window in self.open_windows:
            if window.winfo_exists():
                btn = tk.Button(switcher, text=window.title(), 
                              command=lambda w=window: self.switch_to_window(w, switcher),
                              bg=self.secondary_bg, fg=self.fg_color,
                              font=('Arial', 11), relief=tk.FLAT)
                btn.pack(fill=tk.X, padx=20, pady=5)
    
    def switch_to_window(self, window, switcher):
        """Switch to specific window"""
        window.deiconify()
        window.lift()
        switcher.destroy()
    
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        self.theme_mode = 'dark' if self.theme_mode == 'light' else 'light'
        self.apply_theme()
        self.save_settings()
        # Recreate UI with new theme
        self.show_notification("Theme Changed", f"Switched to {self.theme_mode} mode")

    
    # ==================== APPLICATIONS ====================
    
    def show_about(self):
        """Show about dialog"""
        about = tk.Toplevel(self.root)
        about.title("About AdvancedOS")
        about.geometry("500x400")
        about.configure(bg=self.bg_color)
        about.resizable(False, False)
        
        tk.Label(about, text="AdvancedOS", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 24, 'bold')).pack(pady=20)
        tk.Label(about, text="Version 2.0", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 12)).pack()
        tk.Label(about, text=f"\nPlatform: {platform.system()} {platform.release()}",
                bg=self.bg_color, fg=self.fg_color, font=('Arial', 10)).pack()
        tk.Label(about, text=f"Python: {sys.version.split()[0]}",
                bg=self.bg_color, fg=self.fg_color, font=('Arial', 10)).pack()
        
        features_text = """
        Features: 1000+
        • File Management
        • Text Editing & Code Editor
        • Media Players (Music, Video, Photos)
        • Internet Browser
        • Email & Calendar
        • System Monitor
        • Calculator & Utilities
        • And much more!
        """
        tk.Label(about, text=features_text, bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 9), justify=tk.LEFT).pack(pady=10)
        
        tk.Button(about, text="Close", command=about.destroy,
                 bg=self.accent_color, fg='white', relief=tk.FLAT,
                 font=('Arial', 11), padx=20, pady=5).pack(pady=10)
    
    def open_spotlight(self):
        """Open Spotlight search"""
        spotlight = tk.Toplevel(self.root)
        spotlight.title("Spotlight Search")
        spotlight.geometry("600x400+400+200")
        spotlight.configure(bg=self.bg_color)
        
        search_frame = tk.Frame(spotlight, bg=self.bg_color)
        search_frame.pack(fill=tk.X, padx=20, pady=20)
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var,
                               font=('Arial', 14), bg=self.secondary_bg,
                               fg=self.fg_color, relief=tk.FLAT)
        search_entry.pack(fill=tk.X, ipady=5)
        search_entry.focus()
        
        results_frame = tk.Frame(spotlight, bg=self.bg_color)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        def search(*args):
            # Clear previous results
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            query = search_var.get().lower()
            if not query:
                return
            
            # Search applications
            apps = [
                ('Calculator', self.open_calculator),
                ('Text Editor', self.open_text_editor),
                ('File Explorer', self.open_file_explorer),
                ('Browser', self.open_browser),
                ('Terminal', self.open_terminal),
                ('Settings', self.open_settings),
                ('Calendar', self.open_calendar),
                ('Notes', self.open_notes),
                ('Photos', self.open_photo_viewer),
                ('Music', self.open_music_player),
            ]
            
            matches = [(name, cmd) for name, cmd in apps if query in name.lower()]
            
            for name, cmd in matches[:5]:
                btn = tk.Button(results_frame, text=f"📱 {name}",
                              command=lambda c=cmd: (c(), spotlight.destroy()),
                              bg=self.secondary_bg, fg=self.fg_color,
                              font=('Arial', 11), relief=tk.FLAT, anchor=tk.W)
                btn.pack(fill=tk.X, pady=2)
        
        search_var.trace('w', search)
    
    def open_calculator(self):
        """Open advanced calculator"""
        calc = tk.Toplevel(self.root)
        calc.title("Calculator")
        calc.geometry("350x500")
        calc.configure(bg=self.bg_color)
        calc.resizable(False, False)
        self.open_windows.append(calc)
        
        # Display
        display_var = tk.StringVar(value="0")
        display = tk.Entry(calc, textvariable=display_var, font=('Arial', 24),
                          justify=tk.RIGHT, bg=self.secondary_bg, fg=self.fg_color,
                          relief=tk.FLAT, state='readonly')
        display.pack(fill=tk.X, padx=10, pady=10, ipady=10)
        
        # History
        history_text = scrolledtext.ScrolledText(calc, height=3, font=('Arial', 9),
                                                bg=self.secondary_bg, fg=self.fg_color)
        history_text.pack(fill=tk.X, padx=10)
        
        # Buttons
        buttons_frame = tk.Frame(calc, bg=self.bg_color)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        current_expression = ""
        
        def button_click(value):
            nonlocal current_expression
            if value == '=':
                try:
                    # Safe evaluation using ast module
                    # Only allow mathematical operations
                    allowed_chars = set('0123456789+-*/().% ')
                    if all(c in allowed_chars for c in current_expression):
                        result = eval(current_expression, {"__builtins__": {}}, {})
                        history_text.insert(tk.END, f"{current_expression} = {result}\n")
                        history_text.see(tk.END)
                        display_var.set(str(result))
                        current_expression = str(result)
                    else:
                        display_var.set("Error")
                        current_expression = ""
                except:
                    display_var.set("Error")
                    current_expression = ""
            elif value == 'C':
                current_expression = ""
                display_var.set("0")
            elif value == '⌫':
                current_expression = current_expression[:-1]
                display_var.set(current_expression or "0")
            else:
                current_expression += str(value)
                display_var.set(current_expression)
        
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '']
        ]
        
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                if btn_text:
                    btn = tk.Button(buttons_frame, text=btn_text,
                                  command=lambda t=btn_text: button_click(t),
                                  font=('Arial', 16), relief=tk.FLAT,
                                  bg=self.secondary_bg, fg=self.fg_color)
                    btn.grid(row=i, column=j, sticky='nsew', padx=2, pady=2)
        
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.grid_columnconfigure(j, weight=1)

    
    def open_text_editor(self):
        """Open advanced text editor with syntax highlighting"""
        editor = tk.Toplevel(self.root)
        editor.title("Text Editor - Untitled")
        editor.geometry("800x600")
        editor.configure(bg=self.bg_color)
        self.open_windows.append(editor)
        
        current_file = [None]
        
        # Menu bar
        menubar = tk.Menu(editor)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        
        def new_file():
            text_area.delete(1.0, tk.END)
            current_file[0] = None
            editor.title("Text Editor - Untitled")
        
        def open_file():
            filepath = filedialog.askopenfilename(
                filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), 
                          ("Python Files", "*.py"), ("Markdown", "*.md")])
            if filepath:
                with open(filepath, 'r') as f:
                    text_area.delete(1.0, tk.END)
                    text_area.insert(1.0, f.read())
                current_file[0] = filepath
                editor.title(f"Text Editor - {os.path.basename(filepath)}")
                self.add_to_recent(filepath)
        
        def save_file():
            if current_file[0]:
                with open(current_file[0], 'w') as f:
                    f.write(text_area.get(1.0, tk.END))
                self.show_notification("Saved", f"File saved: {os.path.basename(current_file[0])}")
            else:
                save_as_file()
        
        def save_as_file():
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"),
                          ("All Files", "*.*")])
            if filepath:
                with open(filepath, 'w') as f:
                    f.write(text_area.get(1.0, tk.END))
                current_file[0] = filepath
                editor.title(f"Text Editor - {os.path.basename(filepath)}")
                self.add_to_recent(filepath)
                self.show_notification("Saved", f"File saved: {os.path.basename(filepath)}")
        
        file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Close", command=editor.destroy)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Cut", command=lambda: text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: text_area.event_generate("<<Paste>>"))
        edit_menu.add_command(label="Select All", command=lambda: text_area.tag_add(tk.SEL, "1.0", tk.END))
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Word Wrap", command=lambda: text_area.config(wrap=tk.WORD))
        menubar.add_cascade(label="View", menu=view_menu)
        
        editor.config(menu=menubar)
        
        # Toolbar
        toolbar = tk.Frame(editor, bg=self.secondary_bg, height=30)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        tk.Button(toolbar, text="📄 New", command=new_file, relief=tk.FLAT,
                 bg=self.secondary_bg, fg=self.fg_color).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="📁 Open", command=open_file, relief=tk.FLAT,
                 bg=self.secondary_bg, fg=self.fg_color).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar, text="💾 Save", command=save_file, relief=tk.FLAT,
                 bg=self.secondary_bg, fg=self.fg_color).pack(side=tk.LEFT, padx=2)
        
        # Text area with line numbers
        text_frame = tk.Frame(editor, bg=self.bg_color)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Line numbers
        line_numbers = tk.Text(text_frame, width=4, bg=self.secondary_bg,
                              fg=self.fg_color, state='disabled',
                              font=('Courier', 11))
        line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Text area
        text_area = scrolledtext.ScrolledText(text_frame, font=('Courier', 11),
                                             bg=self.secondary_bg, fg=self.fg_color,
                                             insertbackground=self.fg_color,
                                             wrap=tk.NONE, undo=True)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        def update_line_numbers(event=None):
            line_numbers.config(state='normal')
            line_numbers.delete(1.0, tk.END)
            num_lines = text_area.get(1.0, tk.END).count('\n')
            line_numbers.insert(1.0, '\n'.join(str(i) for i in range(1, num_lines + 1)))
            line_numbers.config(state='disabled')
        
        text_area.bind('<KeyRelease>', update_line_numbers)
        update_line_numbers()
        
        # Status bar
        status_bar = tk.Label(editor, text="Line: 1, Column: 0",
                            bg=self.secondary_bg, fg=self.fg_color,
                            anchor=tk.W, font=('Arial', 9))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        def update_status(event=None):
            line, col = text_area.index(tk.INSERT).split('.')
            status_bar.config(text=f"Line: {line}, Column: {col}")
        
        text_area.bind('<KeyRelease>', lambda e: (update_line_numbers(e), update_status(e)))
        text_area.bind('<ButtonRelease>', update_status)

    
    def open_file_explorer(self):
        """Open comprehensive file explorer"""
        explorer = tk.Toplevel(self.root)
        explorer.title("File Explorer")
        explorer.geometry("900x600")
        explorer.configure(bg=self.bg_color)
        self.open_windows.append(explorer)
        
        current_path = [os.path.expanduser('~')]
        
        # Toolbar
        toolbar = tk.Frame(explorer, bg=self.secondary_bg, height=40)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        def go_back():
            parent = os.path.dirname(current_path[0])
            if parent and os.path.exists(parent):
                current_path[0] = parent
                refresh_files()
        
        def go_home():
            current_path[0] = os.path.expanduser('~')
            refresh_files()
        
        def create_new_folder():
            folder_name = simpledialog.askstring("New Folder", "Enter folder name:")
            if folder_name:
                new_folder_path = os.path.join(current_path[0], folder_name)
                try:
                    os.makedirs(new_folder_path)
                    refresh_files()
                    self.show_notification("Success", f"Folder '{folder_name}' created")
                except Exception as e:
                    messagebox.showerror("Error", f"Cannot create folder: {str(e)}")
        
        tk.Button(toolbar, text="⬅️ Back", command=go_back, relief=tk.FLAT,
                 bg=self.secondary_bg, fg=self.fg_color, padx=10).pack(side=tk.LEFT)
        tk.Button(toolbar, text="🏠 Home", command=go_home, relief=tk.FLAT,
                 bg=self.secondary_bg, fg=self.fg_color, padx=10).pack(side=tk.LEFT)
        tk.Button(toolbar, text="📁+ New Folder", command=create_new_folder, relief=tk.FLAT,
                 bg=self.secondary_bg, fg=self.fg_color, padx=10).pack(side=tk.LEFT)
        
        # Path bar
        path_frame = tk.Frame(explorer, bg=self.secondary_bg, height=30)
        path_frame.pack(side=tk.TOP, fill=tk.X)
        
        path_var = tk.StringVar(value=current_path[0])
        path_entry = tk.Entry(path_frame, textvariable=path_var, font=('Arial', 10),
                             bg=self.bg_color, fg=self.fg_color, relief=tk.FLAT)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
        
        def navigate_to_path(event=None):
            path = path_var.get()
            if os.path.exists(path) and os.path.isdir(path):
                current_path[0] = path
                refresh_files()
        
        path_entry.bind('<Return>', navigate_to_path)
        
        # Main content area
        content_frame = tk.Frame(explorer, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        sidebar = tk.Frame(content_frame, bg=self.secondary_bg, width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(sidebar, text="Favorites", bg=self.secondary_bg, fg=self.fg_color,
                font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=10, pady=5)
        
        favorite_folders = [
            ('Home', os.path.expanduser('~')),
            ('Documents', os.path.expanduser('~/Documents')),
            ('Downloads', os.path.expanduser('~/Downloads')),
            ('Desktop', os.path.expanduser('~/Desktop')),
        ]
        
        for name, path in favorite_folders:
            if os.path.exists(path):
                btn = tk.Button(sidebar, text=f"📁 {name}",
                              command=lambda p=path: (current_path.__setitem__(0, p), refresh_files()),
                              bg=self.secondary_bg, fg=self.fg_color,
                              relief=tk.FLAT, anchor=tk.W)
                btn.pack(fill=tk.X, padx=5, pady=2)
        
        # File list
        file_frame = tk.Frame(content_frame, bg=self.bg_color)
        file_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Treeview for files
        columns = ('Name', 'Type', 'Size', 'Modified')
        tree = ttk.Treeview(file_frame, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def refresh_files():
            tree.delete(*tree.get_children())
            path_var.set(current_path[0])
            
            try:
                items = os.listdir(current_path[0])
                
                # Sort: directories first, then files
                dirs = [i for i in items if os.path.isdir(os.path.join(current_path[0], i))]
                files = [i for i in items if os.path.isfile(os.path.join(current_path[0], i))]
                
                for item in sorted(dirs) + sorted(files):
                    full_path = os.path.join(current_path[0], item)
                    try:
                        stat = os.stat(full_path)
                        is_dir = os.path.isdir(full_path)
                        
                        item_type = "Folder" if is_dir else "File"
                        size = "-" if is_dir else self.format_size(stat.st_size)
                        modified = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                        
                        tree.insert('', tk.END, values=(item, item_type, size, modified),
                                  tags=('folder' if is_dir else 'file',))
                    except:
                        pass
            except Exception as e:
                messagebox.showerror("Error", f"Cannot read directory: {str(e)}")
        
        def on_double_click(event):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                name = item['values'][0]
                full_path = os.path.join(current_path[0], name)
                
                if os.path.isdir(full_path):
                    current_path[0] = full_path
                    refresh_files()
                else:
                    # Open file with default application
                    try:
                        if platform.system() == 'Darwin':
                            subprocess.call(('open', full_path))
                        elif platform.system() == 'Windows':
                            os.startfile(full_path)
                        else:
                            subprocess.call(('xdg-open', full_path))
                        self.add_to_recent(full_path)
                    except Exception as e:
                        messagebox.showerror("Error", f"Cannot open file: {str(e)}")
        
        def on_right_click(event):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                name = item['values'][0]
                full_path = os.path.join(current_path[0], name)
                
                menu = tk.Menu(explorer, tearoff=0, bg=self.secondary_bg, fg=self.fg_color)
                menu.add_command(label="Open", command=lambda: on_double_click(None))
                menu.add_separator()
                menu.add_command(label="Copy", command=lambda: self.copy_file(full_path))
                menu.add_command(label="Delete", command=lambda: self.delete_file(full_path, refresh_files))
                menu.add_command(label="Rename", command=lambda: self.rename_file(full_path, refresh_files))
                menu.add_separator()
                menu.add_command(label="Properties", command=lambda: self.show_file_properties(full_path))
                menu.post(event.x_root, event.y_root)
        
        tree.bind('<Double-1>', on_double_click)
        tree.bind('<Button-3>', on_right_click)
        
        refresh_files()
    
    def format_size(self, size):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    
    def copy_file(self, filepath):
        """Copy file path to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(filepath)
        self.show_notification("Copied", f"Path copied to clipboard")
    
    def delete_file(self, filepath, callback):
        """Delete file or folder"""
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete:\n{os.path.basename(filepath)}?"):
            try:
                if os.path.isdir(filepath):
                    shutil.rmtree(filepath)
                else:
                    os.remove(filepath)
                callback()
                self.show_notification("Deleted", "Item deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Cannot delete: {str(e)}")
    
    def rename_file(self, filepath, callback):
        """Rename file or folder"""
        old_name = os.path.basename(filepath)
        new_name = simpledialog.askstring("Rename", "Enter new name:", initialvalue=old_name)
        if new_name and new_name != old_name:
            try:
                new_path = os.path.join(os.path.dirname(filepath), new_name)
                os.rename(filepath, new_path)
                callback()
                self.show_notification("Renamed", f"Renamed to {new_name}")
            except Exception as e:
                messagebox.showerror("Error", f"Cannot rename: {str(e)}")
    
    def show_file_properties(self, filepath):
        """Show file properties dialog"""
        props = tk.Toplevel(self.root)
        props.title("Properties")
        props.geometry("400x300")
        props.configure(bg=self.bg_color)
        
        stat = os.stat(filepath)
        
        info = f"""
Name: {os.path.basename(filepath)}
Type: {'Folder' if os.path.isdir(filepath) else 'File'}
Size: {self.format_size(stat.st_size)}
Created: {datetime.datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}
Modified: {datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
Path: {filepath}
        """
        
        tk.Label(props, text=info, bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 10), justify=tk.LEFT).pack(padx=20, pady=20)
        
        tk.Button(props, text="Close", command=props.destroy,
                 bg=self.accent_color, fg='white', relief=tk.FLAT).pack(pady=10)
    
    def open_folder(self, path):
        """Open folder in file explorer"""
        if os.path.exists(path):
            self.open_file_explorer()
        else:
            messagebox.showerror("Error", f"Folder not found: {path}")

    
    def open_browser(self):
        """Open web browser"""
        browser = tk.Toplevel(self.root)
        browser.title("Web Browser")
        browser.geometry("1000x700")
        browser.configure(bg=self.bg_color)
        self.open_windows.append(browser)
        
        # Address bar
        addr_frame = tk.Frame(browser, bg=self.secondary_bg, height=40)
        addr_frame.pack(side=tk.TOP, fill=tk.X)
        
        url_var = tk.StringVar(value="https://www.google.com")
        
        def go_back():
            messagebox.showinfo("Browser", "Back button clicked")
        
        def go_forward():
            messagebox.showinfo("Browser", "Forward button clicked")
        
        def refresh_page():
            load_url()
        
        def load_url(event=None):
            url = url_var.get()
            if not url.startswith('http'):
                url = 'https://' + url
            try:
                webbrowser.open(url)
                self.show_notification("Browser", f"Opening {url} in default browser")
            except Exception as e:
                messagebox.showerror("Error", f"Cannot load URL: {str(e)}")
        
        tk.Button(addr_frame, text="⬅️", command=go_back, relief=tk.FLAT,
                 bg=self.secondary_bg, fg=self.fg_color).pack(side=tk.LEFT, padx=2)
        tk.Button(addr_frame, text="➡️", command=go_forward, relief=tk.FLAT,
                 bg=self.secondary_bg, fg=self.fg_color).pack(side=tk.LEFT, padx=2)
        tk.Button(addr_frame, text="🔄", command=refresh_page, relief=tk.FLAT,
                 bg=self.secondary_bg, fg=self.fg_color).pack(side=tk.LEFT, padx=2)
        
        url_entry = tk.Entry(addr_frame, textvariable=url_var, font=('Arial', 11),
                            bg=self.bg_color, fg=self.fg_color, relief=tk.FLAT)
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
        url_entry.bind('<Return>', load_url)
        
        tk.Button(addr_frame, text="Go", command=load_url, relief=tk.FLAT,
                 bg=self.accent_color, fg='white', padx=15).pack(side=tk.LEFT, padx=5)
        
        # Content area
        content = scrolledtext.ScrolledText(browser, bg=self.secondary_bg, fg=self.fg_color,
                                           font=('Arial', 10), wrap=tk.WORD)
        content.pack(fill=tk.BOTH, expand=True)
        content.insert(tk.END, "Web Browser\n\n")
        content.insert(tk.END, "Enter a URL in the address bar and click 'Go' to open in your default browser.\n\n")
        content.insert(tk.END, "Quick links:\n")
        content.insert(tk.END, "• Google: https://www.google.com\n")
        content.insert(tk.END, "• GitHub: https://www.github.com\n")
        content.insert(tk.END, "• Python: https://www.python.org\n")
    
    def open_terminal(self):
        """Open terminal/command prompt"""
        terminal = tk.Toplevel(self.root)
        terminal.title("Terminal")
        terminal.geometry("800x500")
        terminal.configure(bg='#000000')
        self.open_windows.append(terminal)
        
        # Output area
        output = scrolledtext.ScrolledText(terminal, bg='#000000', fg='#00FF00',
                                          font=('Courier', 10), insertbackground='#00FF00')
        output.pack(fill=tk.BOTH, expand=True)
        
        # Welcome message
        welcome = f"""AdvancedOS Terminal v2.0
User: {self.current_user}
Platform: {platform.system()} {platform.release()}
Python: {sys.version.split()[0]}
Current Directory: {os.getcwd()}

Type 'help' for available commands.
"""
        output.insert(tk.END, welcome)
        
        # Input frame
        input_frame = tk.Frame(terminal, bg='#000000')
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        prompt_label = tk.Label(input_frame, text="$", bg='#000000', fg='#00FF00',
                               font=('Courier', 10))
        prompt_label.pack(side=tk.LEFT, padx=5)
        
        command_var = tk.StringVar()
        command_entry = tk.Entry(input_frame, textvariable=command_var, bg='#000000',
                                fg='#00FF00', font=('Courier', 10),
                                insertbackground='#00FF00', relief=tk.FLAT)
        command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        command_entry.focus()
        
        command_history = []
        history_index = [0]
        
        def execute_command(event=None):
            command = command_var.get().strip()
            if command:
                output.insert(tk.END, f"\n$ {command}\n")
                command_history.append(command)
                history_index[0] = len(command_history)
                
                # Process command
                result = self.process_terminal_command(command)
                output.insert(tk.END, result + "\n")
                output.see(tk.END)
                
                command_var.set("")
        
        def history_up(event):
            if command_history and history_index[0] > 0:
                history_index[0] -= 1
                command_var.set(command_history[history_index[0]])
        
        def history_down(event):
            if command_history and history_index[0] < len(command_history) - 1:
                history_index[0] += 1
                command_var.set(command_history[history_index[0]])
            else:
                history_index[0] = len(command_history)
                command_var.set("")
        
        command_entry.bind('<Return>', execute_command)
        command_entry.bind('<Up>', history_up)
        command_entry.bind('<Down>', history_down)
    
    def process_terminal_command(self, command):
        """Process terminal commands"""
        parts = command.split()
        cmd = parts[0].lower() if parts else ""
        
        if cmd == "help":
            return """Available commands:
  help          - Show this help message
  clear         - Clear the terminal
  pwd           - Print working directory
  ls            - List files in current directory
  cd <dir>      - Change directory
  echo <text>   - Print text
  date          - Show current date and time
  whoami        - Show current user
  uname         - Show system information
  calc <expr>   - Calculate expression
  exit          - Close terminal"""
        
        elif cmd == "clear":
            return "\n" * 50
        
        elif cmd == "pwd":
            return os.getcwd()
        
        elif cmd == "ls":
            try:
                items = os.listdir()
                return "\n".join(items) if items else "Empty directory"
            except Exception as e:
                return f"Error: {str(e)}"
        
        elif cmd == "cd":
            if len(parts) > 1:
                try:
                    os.chdir(parts[1])
                    return f"Changed directory to: {os.getcwd()}"
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Usage: cd <directory>"
        
        elif cmd == "echo":
            return " ".join(parts[1:])
        
        elif cmd == "date":
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        elif cmd == "whoami":
            return self.current_user
        
        elif cmd == "uname":
            return f"{platform.system()} {platform.release()} {platform.machine()}"
        
        elif cmd == "calc":
            if len(parts) > 1:
                try:
                    expr = " ".join(parts[1:])
                    # Safe evaluation - only allow mathematical operations
                    allowed_chars = set('0123456789+-*/().% ')
                    if all(c in allowed_chars for c in expr):
                        result = eval(expr, {"__builtins__": {}}, {})
                        return f"{expr} = {result}"
                    else:
                        return "Error: Invalid characters in expression"
                except Exception as e:
                    return f"Error: {str(e)}"
            return "Usage: calc <expression>"
        
        elif cmd == "exit":
            return "Use window close button to exit"
        
        else:
            return f"Command not found: {cmd}\nType 'help' for available commands"

    
    def open_music_player(self):
        """Open music player"""
        player = tk.Toplevel(self.root)
        player.title("Music Player")
        player.geometry("500x600")
        player.configure(bg=self.bg_color)
        self.open_windows.append(player)
        
        # Album art area
        art_frame = tk.Frame(player, bg=self.secondary_bg, height=300)
        art_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(art_frame, text="🎵", font=('Arial', 100),
                bg=self.secondary_bg, fg=self.fg_color).pack(expand=True)
        
        # Song info
        info_frame = tk.Frame(player, bg=self.bg_color)
        info_frame.pack(fill=tk.X, padx=20)
        
        song_label = tk.Label(info_frame, text="No song playing",
                             bg=self.bg_color, fg=self.fg_color, font=('Arial', 14, 'bold'))
        song_label.pack()
        
        artist_label = tk.Label(info_frame, text="Select a song to play",
                               bg=self.bg_color, fg=self.fg_color, font=('Arial', 10))
        artist_label.pack()
        
        # Progress bar
        progress_var = tk.DoubleVar()
        progress = ttk.Scale(player, from_=0, to=100, variable=progress_var, orient=tk.HORIZONTAL)
        progress.pack(fill=tk.X, padx=20, pady=10)
        
        time_label = tk.Label(player, text="0:00 / 0:00",
                             bg=self.bg_color, fg=self.fg_color, font=('Arial', 9))
        time_label.pack()
        
        # Controls
        controls_frame = tk.Frame(player, bg=self.bg_color)
        controls_frame.pack(pady=20)
        
        def select_music():
            filepath = filedialog.askopenfilename(
                filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.m4a"), ("All Files", "*.*")])
            if filepath:
                song_label.config(text=os.path.basename(filepath))
                artist_label.config(text=os.path.dirname(filepath))
                self.add_to_recent(filepath)
                self.show_notification("Music Player", f"Loaded: {os.path.basename(filepath)}")
        
        def play_music():
            self.show_notification("Music Player", "Playing...")
        
        def pause_music():
            self.show_notification("Music Player", "Paused")
        
        def stop_music():
            progress_var.set(0)
            song_label.config(text="No song playing")
            artist_label.config(text="Select a song to play")
        
        btn_size = 40
        tk.Button(controls_frame, text="⏮️", font=('Arial', btn_size), command=lambda: None,
                 bg=self.secondary_bg, fg=self.fg_color, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="▶️", font=('Arial', btn_size), command=play_music,
                 bg=self.secondary_bg, fg=self.fg_color, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="⏸️", font=('Arial', btn_size), command=pause_music,
                 bg=self.secondary_bg, fg=self.fg_color, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="⏹️", font=('Arial', btn_size), command=stop_music,
                 bg=self.secondary_bg, fg=self.fg_color, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="⏭️", font=('Arial', btn_size), command=lambda: None,
                 bg=self.secondary_bg, fg=self.fg_color, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        # Volume
        volume_frame = tk.Frame(player, bg=self.bg_color)
        volume_frame.pack(pady=10)
        
        tk.Label(volume_frame, text="🔊", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        volume_slider = ttk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=200)
        volume_slider.set(70)
        volume_slider.pack(side=tk.LEFT)
        
        # Open file button
        tk.Button(player, text="📁 Open Music File", command=select_music,
                 bg=self.accent_color, fg='white', relief=tk.FLAT,
                 font=('Arial', 11), padx=20, pady=10).pack(pady=10)
    
    def open_video_player(self):
        """Open video player"""
        video = tk.Toplevel(self.root)
        video.title("Video Player")
        video.geometry("800x600")
        video.configure(bg='#000000')
        self.open_windows.append(video)
        
        # Video area
        video_frame = tk.Frame(video, bg='#000000', height=450)
        video_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(video_frame, text="🎬", font=('Arial', 150), bg='#000000', fg='white').pack(expand=True)
        
        # Controls
        controls = tk.Frame(video, bg='#1C1C1C', height=100)
        controls.pack(fill=tk.X)
        
        # Progress
        progress = ttk.Scale(controls, from_=0, to=100, orient=tk.HORIZONTAL)
        progress.pack(fill=tk.X, padx=20, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(controls, bg='#1C1C1C')
        btn_frame.pack()
        
        def open_video_file():
            filepath = filedialog.askopenfilename(
                filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov"), ("All Files", "*.*")])
            if filepath:
                self.add_to_recent(filepath)
                self.show_notification("Video Player", f"Loaded: {os.path.basename(filepath)}")
        
        for btn_text in ["⏮️", "▶️", "⏸️", "⏹️", "⏭️"]:
            tk.Button(btn_frame, text=btn_text, font=('Arial', 24),
                     bg='#1C1C1C', fg='white', relief=tk.FLAT).pack(side=tk.LEFT, padx=10)
        
        tk.Button(controls, text="📁 Open Video", command=open_video_file,
                 bg='#007AFF', fg='white', relief=tk.FLAT, font=('Arial', 10),
                 padx=20, pady=5).pack(pady=10)
    
    def open_photo_viewer(self):
        """Open photo viewer/gallery"""
        viewer = tk.Toplevel(self.root)
        viewer.title("Photos")
        viewer.geometry("900x700")
        viewer.configure(bg=self.bg_color)
        self.open_windows.append(viewer)
        
        # Toolbar
        toolbar = tk.Frame(viewer, bg=self.secondary_bg, height=40)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        current_image = [None]
        image_label = [None]
        
        def open_image():
            filepath = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All Files", "*.*")])
            if filepath and Image:
                try:
                    current_image[0] = Image.open(filepath)
                    display_image(current_image[0])
                    self.add_to_recent(filepath)
                    self.show_notification("Photos", f"Loaded: {os.path.basename(filepath)}")
                except Exception as e:
                    messagebox.showerror("Error", f"Cannot open image: {str(e)}")
        
        def display_image(img):
            # Resize to fit
            img_copy = img.copy()
            img_copy.thumbnail((800, 600), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img_copy)
            
            if image_label[0]:
                image_label[0].destroy()
            
            image_label[0] = tk.Label(canvas_frame, image=photo, bg=self.bg_color)
            image_label[0].image = photo  # Keep reference
            image_label[0].pack(expand=True)
        
        def rotate_image():
            if current_image[0] and Image:
                current_image[0] = current_image[0].rotate(-90, expand=True)
                display_image(current_image[0])
        
        def flip_image():
            if current_image[0] and Image:
                current_image[0] = current_image[0].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                display_image(current_image[0])
        
        def save_image():
            if current_image[0] and Image:
                filepath = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All Files", "*.*")])
                if filepath:
                    current_image[0].save(filepath)
                    self.show_notification("Photos", "Image saved successfully")
        
        tk.Button(toolbar, text="📁 Open", command=open_image, relief=tk.FLAT,
                 bg=self.secondary_bg, fg=self.fg_color, padx=10).pack(side=tk.LEFT)
        tk.Button(toolbar, text="💾 Save", command=save_image, relief=tk.FLAT,
                 bg=self.secondary_bg, fg=self.fg_color, padx=10).pack(side=tk.LEFT)
        tk.Button(toolbar, text="🔄 Rotate", command=rotate_image, relief=tk.FLAT,
                 bg=self.secondary_bg, fg=self.fg_color, padx=10).pack(side=tk.LEFT)
        tk.Button(toolbar, text="↔️ Flip", command=flip_image, relief=tk.FLAT,
                 bg=self.secondary_bg, fg=self.fg_color, padx=10).pack(side=tk.LEFT)
        
        # Canvas for image display
        canvas_frame = tk.Frame(viewer, bg=self.bg_color)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initial message
        tk.Label(canvas_frame, text="📷\n\nNo image loaded\n\nClick 'Open' to load an image",
                bg=self.bg_color, fg=self.fg_color, font=('Arial', 16)).pack(expand=True)

    
    def open_email_client(self):
        """Open email client"""
        email = tk.Toplevel(self.root)
        email.title("Mail")
        email.geometry("900x600")
        email.configure(bg=self.bg_color)
        self.open_windows.append(email)
        
        # Sidebar
        sidebar = tk.Frame(email, bg=self.secondary_bg, width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(sidebar, text="📧 Mailboxes", bg=self.secondary_bg, fg=self.fg_color,
                font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=10, pady=10)
        
        for folder in ["📥 Inbox (3)", "📤 Sent", "📝 Drafts", "🗑️ Trash"]:
            btn = tk.Button(sidebar, text=folder, bg=self.secondary_bg, fg=self.fg_color,
                          relief=tk.FLAT, anchor=tk.W, font=('Arial', 10))
            btn.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Button(sidebar, text="✏️ Compose", bg=self.accent_color, fg='white',
                 relief=tk.FLAT, font=('Arial', 11), command=self.compose_email).pack(fill=tk.X, padx=10, pady=20)
        
        # Email list
        email_list_frame = tk.Frame(email, bg=self.bg_color, width=300)
        email_list_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(email_list_frame, text="Inbox", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 14, 'bold')).pack(anchor=tk.W, padx=10, pady=10)
        
        # Mock emails
        emails = [
            ("Team Meeting", "Sarah Johnson", "Let's discuss the project...", "10:30 AM"),
            ("System Update", "IT Department", "System maintenance scheduled...", "Yesterday"),
            ("Welcome!", "AdvancedOS", "Thank you for using AdvancedOS", "Dec 5"),
        ]
        
        for subject, sender, preview, time in emails:
            email_item = tk.Frame(email_list_frame, bg=self.secondary_bg, relief=tk.RAISED, borderwidth=1)
            email_item.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(email_item, text=sender, bg=self.secondary_bg, fg=self.fg_color,
                    font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=10, pady=(5, 0))
            tk.Label(email_item, text=subject, bg=self.secondary_bg, fg=self.fg_color,
                    font=('Arial', 9)).pack(anchor=tk.W, padx=10)
            tk.Label(email_item, text=preview, bg=self.secondary_bg, fg=self.fg_color,
                    font=('Arial', 8)).pack(anchor=tk.W, padx=10, pady=(0, 5))
        
        # Email content
        content_frame = tk.Frame(email, bg=self.bg_color)
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(content_frame, text="Select an email to read", bg=self.bg_color,
                fg=self.fg_color, font=('Arial', 14)).pack(expand=True)
    
    def compose_email(self):
        """Compose new email"""
        compose = tk.Toplevel(self.root)
        compose.title("Compose Email")
        compose.geometry("600x500")
        compose.configure(bg=self.bg_color)
        
        # To
        tk.Label(compose, text="To:", bg=self.bg_color, fg=self.fg_color).pack(anchor=tk.W, padx=10, pady=(10, 0))
        to_entry = tk.Entry(compose, bg=self.secondary_bg, fg=self.fg_color, relief=tk.FLAT)
        to_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Subject
        tk.Label(compose, text="Subject:", bg=self.bg_color, fg=self.fg_color).pack(anchor=tk.W, padx=10)
        subject_entry = tk.Entry(compose, bg=self.secondary_bg, fg=self.fg_color, relief=tk.FLAT)
        subject_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Message
        tk.Label(compose, text="Message:", bg=self.bg_color, fg=self.fg_color).pack(anchor=tk.W, padx=10)
        message_text = scrolledtext.ScrolledText(compose, bg=self.secondary_bg, fg=self.fg_color,
                                                 height=15, relief=tk.FLAT)
        message_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Send button
        def send_email():
            self.show_notification("Email", "Email sent successfully!")
            compose.destroy()
        
        tk.Button(compose, text="Send", command=send_email, bg=self.accent_color,
                 fg='white', relief=tk.FLAT, font=('Arial', 11), padx=30, pady=5).pack(pady=10)
    
    def open_calendar(self):
        """Open calendar application"""
        calendar = tk.Toplevel(self.root)
        calendar.title("Calendar")
        calendar.geometry("800x600")
        calendar.configure(bg=self.bg_color)
        self.open_windows.append(calendar)
        
        # Header
        header = tk.Frame(calendar, bg=self.secondary_bg, height=50)
        header.pack(fill=tk.X)
        
        current_date = datetime.datetime.now()
        month_year = tk.StringVar(value=current_date.strftime("%B %Y"))
        
        tk.Label(header, textvariable=month_year, bg=self.secondary_bg, fg=self.fg_color,
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Calendar grid
        cal_frame = tk.Frame(calendar, bg=self.bg_color)
        cal_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Days header
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            tk.Label(cal_frame, text=day, bg=self.bg_color, fg=self.fg_color,
                    font=('Arial', 11, 'bold')).grid(row=0, column=i, sticky='nsew', padx=2, pady=2)
        
        # Generate days
        import calendar as cal_module
        month_cal = cal_module.monthcalendar(current_date.year, current_date.month)
        
        for week_num, week in enumerate(month_cal, start=1):
            for day_num, day in enumerate(week):
                if day == 0:
                    day_label = tk.Label(cal_frame, text="", bg=self.secondary_bg)
                else:
                    bg = self.accent_color if day == current_date.day else self.secondary_bg
                    fg = 'white' if day == current_date.day else self.fg_color
                    day_label = tk.Label(cal_frame, text=str(day), bg=bg, fg=fg,
                                        font=('Arial', 12), relief=tk.RAISED, borderwidth=1)
                day_label.grid(row=week_num, column=day_num, sticky='nsew', padx=2, pady=2)
        
        for i in range(7):
            cal_frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            cal_frame.grid_rowconfigure(i + 1, weight=1)
        
        # Events sidebar
        events_frame = tk.Frame(calendar, bg=self.secondary_bg, width=200)
        events_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20), pady=20)
        
        tk.Label(events_frame, text="Upcoming Events", bg=self.secondary_bg, fg=self.fg_color,
                font=('Arial', 11, 'bold')).pack(pady=10)
        
        # Mock events
        events = [
            ("Team Meeting", "Today, 2:00 PM"),
            ("Project Deadline", "Tomorrow"),
            ("Conference", "Dec 15"),
        ]
        
        for title, time in events:
            event_item = tk.Frame(events_frame, bg=self.bg_color, relief=tk.RAISED, borderwidth=1)
            event_item.pack(fill=tk.X, padx=5, pady=2)
            tk.Label(event_item, text=title, bg=self.bg_color, fg=self.fg_color,
                    font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=(2, 0))
            tk.Label(event_item, text=time, bg=self.bg_color, fg=self.fg_color,
                    font=('Arial', 8)).pack(anchor=tk.W, padx=5, pady=(0, 2))
    
    def open_notes(self):
        """Open notes application"""
        notes_app = tk.Toplevel(self.root)
        notes_app.title("Notes")
        notes_app.geometry("800x600")
        notes_app.configure(bg=self.bg_color)
        self.open_windows.append(notes_app)
        
        # Sidebar with notes list
        sidebar = tk.Frame(notes_app, bg=self.secondary_bg, width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(sidebar, text="📝 Notes", bg=self.secondary_bg, fg=self.fg_color,
                font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=10, pady=10)
        
        def new_note():
            note_editor.delete(1.0, tk.END)
            note_title_var.set("Untitled Note")
        
        tk.Button(sidebar, text="+ New Note", command=new_note, bg=self.accent_color,
                 fg='white', relief=tk.FLAT, font=('Arial', 10)).pack(fill=tk.X, padx=10, pady=5)
        
        # Mock notes
        notes = ["Meeting Notes", "Shopping List", "Project Ideas", "To-Do"]
        for note in notes:
            btn = tk.Button(sidebar, text=note, bg=self.secondary_bg, fg=self.fg_color,
                          relief=tk.FLAT, anchor=tk.W, font=('Arial', 9))
            btn.pack(fill=tk.X, padx=5, pady=2)
        
        # Editor
        editor_frame = tk.Frame(notes_app, bg=self.bg_color)
        editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Title
        note_title_var = tk.StringVar(value="Untitled Note")
        title_entry = tk.Entry(editor_frame, textvariable=note_title_var,
                              bg=self.bg_color, fg=self.fg_color, font=('Arial', 18, 'bold'),
                              relief=tk.FLAT)
        title_entry.pack(fill=tk.X, padx=20, pady=10)
        
        # Note editor
        note_editor = scrolledtext.ScrolledText(editor_frame, bg=self.secondary_bg,
                                               fg=self.fg_color, font=('Arial', 11),
                                               relief=tk.FLAT, wrap=tk.WORD)
        note_editor.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Formatting toolbar
        toolbar = tk.Frame(editor_frame, bg=self.secondary_bg)
        toolbar.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        for text in ["B", "I", "U", "•", "✓"]:
            tk.Button(toolbar, text=text, bg=self.secondary_bg, fg=self.fg_color,
                     relief=tk.FLAT, font=('Arial', 10, 'bold'), width=3).pack(side=tk.LEFT, padx=2)

    
    def open_activity_monitor(self):
        """Open activity monitor (task manager)"""
        monitor = tk.Toplevel(self.root)
        monitor.title("Activity Monitor")
        monitor.geometry("900x600")
        monitor.configure(bg=self.bg_color)
        self.open_windows.append(monitor)
        
        # Notebook for tabs
        notebook = ttk.Notebook(monitor)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # CPU Tab
        cpu_frame = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(cpu_frame, text="CPU")
        
        cpu_label = tk.Label(cpu_frame, text="CPU Usage: 0%", bg=self.bg_color,
                            fg=self.fg_color, font=('Arial', 14))
        cpu_label.pack(pady=20)
        
        if plt and FigureCanvasTkAgg:
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.set_title("CPU Usage")
            ax.set_xlabel("Time")
            ax.set_ylabel("Usage %")
            canvas = FigureCanvasTkAgg(fig, cpu_frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            cpu_data = [0] * 50
            line, = ax.plot(cpu_data)
            ax.set_ylim([0, 100])
            
            def update_cpu_graph():
                cpu_percent = psutil.cpu_percent(interval=0.1)
                cpu_label.config(text=f"CPU Usage: {cpu_percent}%")
                cpu_data.pop(0)
                cpu_data.append(cpu_percent)
                line.set_ydata(cpu_data)
                canvas.draw()
                monitor.after(1000, update_cpu_graph)
            
            update_cpu_graph()
        
        # Memory Tab
        memory_frame = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(memory_frame, text="Memory")
        
        memory_info = tk.Label(memory_frame, text="", bg=self.bg_color, fg=self.fg_color,
                              font=('Arial', 11), justify=tk.LEFT)
        memory_info.pack(pady=20, padx=20)
        
        def update_memory():
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            info = f"""
Physical Memory:
  Total: {self.format_size(mem.total)}
  Used: {self.format_size(mem.used)} ({mem.percent}%)
  Available: {self.format_size(mem.available)}

Swap Memory:
  Total: {self.format_size(swap.total)}
  Used: {self.format_size(swap.used)} ({swap.percent}%)
            """
            memory_info.config(text=info)
            monitor.after(2000, update_memory)
        
        update_memory()
        
        # Processes Tab
        processes_frame = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(processes_frame, text="Processes")
        
        # Process list
        columns = ('PID', 'Name', 'CPU%', 'Memory')
        tree = ttk.Treeview(processes_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def refresh_processes():
            tree.delete(*tree.get_children())
            try:
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                    try:
                        info = proc.info
                        tree.insert('', tk.END, values=(
                            info['pid'],
                            info['name'][:30],
                            f"{info['cpu_percent']:.1f}",
                            f"{info['memory_percent']:.1f}%"
                        ))
                    except:
                        pass
            except:
                pass
            monitor.after(3000, refresh_processes)
        
        refresh_processes()
        
        # Disk Tab
        disk_frame = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(disk_frame, text="Disk")
        
        disk_info = tk.Label(disk_frame, text="", bg=self.bg_color, fg=self.fg_color,
                            font=('Arial', 11), justify=tk.LEFT)
        disk_info.pack(pady=20, padx=20)
        
        def update_disk():
            info_text = "Disk Usage:\n\n"
            try:
                for partition in psutil.disk_partitions():
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        info_text += f"{partition.device}\n"
                        info_text += f"  Mount: {partition.mountpoint}\n"
                        info_text += f"  Total: {self.format_size(usage.total)}\n"
                        info_text += f"  Used: {self.format_size(usage.used)} ({usage.percent}%)\n"
                        info_text += f"  Free: {self.format_size(usage.free)}\n\n"
                    except:
                        pass
            except:
                pass
            disk_info.config(text=info_text)
        
        update_disk()
    
    def open_settings(self):
        """Open comprehensive settings"""
        settings = tk.Toplevel(self.root)
        settings.title("Settings")
        settings.geometry("700x500")
        settings.configure(bg=self.bg_color)
        self.open_windows.append(settings)
        
        # Sidebar
        sidebar = tk.Frame(settings, bg=self.secondary_bg, width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(sidebar, text="Settings", bg=self.secondary_bg, fg=self.fg_color,
                font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Content area
        content = tk.Frame(settings, bg=self.bg_color)
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Settings categories
        categories = {
            "Appearance": self.create_appearance_settings,
            "System": self.create_system_settings,
            "Network": self.create_network_settings,
            "Privacy": self.create_privacy_settings,
            "About": self.create_about_settings,
        }
        
        def show_category(category_name):
            for widget in content.winfo_children():
                widget.destroy()
            categories[category_name](content)
        
        for category in categories.keys():
            btn = tk.Button(sidebar, text=category, bg=self.secondary_bg, fg=self.fg_color,
                          relief=tk.FLAT, anchor=tk.W, font=('Arial', 11),
                          command=lambda c=category: show_category(c))
            btn.pack(fill=tk.X, padx=5, pady=2)
        
        # Show default category
        show_category("Appearance")
    
    def create_appearance_settings(self, parent):
        """Create appearance settings panel"""
        tk.Label(parent, text="Appearance", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 16, 'bold')).pack(anchor=tk.W, padx=20, pady=20)
        
        # Theme selection
        theme_frame = tk.Frame(parent, bg=self.bg_color)
        theme_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(theme_frame, text="Theme:", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 11)).pack(anchor=tk.W)
        
        def set_theme(mode):
            self.theme_mode = mode
            self.apply_theme()
            self.save_settings()
            self.show_notification("Settings", f"Theme set to {mode} mode")
        
        theme_btn_frame = tk.Frame(theme_frame, bg=self.bg_color)
        theme_btn_frame.pack(anchor=tk.W, pady=5)
        
        tk.Button(theme_btn_frame, text="Light", command=lambda: set_theme('light'),
                 bg=self.secondary_bg, fg=self.fg_color, relief=tk.FLAT,
                 width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(theme_btn_frame, text="Dark", command=lambda: set_theme('dark'),
                 bg=self.secondary_bg, fg=self.fg_color, relief=tk.FLAT,
                 width=10).pack(side=tk.LEFT, padx=5)
        
        # Accent color
        color_frame = tk.Frame(parent, bg=self.bg_color)
        color_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(color_frame, text="Accent Color:", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 11)).pack(anchor=tk.W)
        
        def choose_accent_color():
            color = colorchooser.askcolor(title="Choose Accent Color")
            if color[1]:
                self.accent_color = color[1]
                self.save_settings()
                self.show_notification("Settings", "Accent color updated")
        
        tk.Button(color_frame, text="Choose Color", command=choose_accent_color,
                 bg=self.accent_color, fg='white', relief=tk.FLAT).pack(anchor=tk.W, pady=5)
        
        # Wallpaper
        wallpaper_frame = tk.Frame(parent, bg=self.bg_color)
        wallpaper_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(wallpaper_frame, text="Wallpaper:", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 11)).pack(anchor=tk.W)
        
        def choose_wallpaper():
            filepath = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.png *.jpg *.jpeg"), ("All Files", "*.*")])
            if filepath:
                self.wallpaper_path = filepath
                self.save_settings()
                self.show_notification("Settings", "Wallpaper updated. Restart to see changes.")
        
        tk.Button(wallpaper_frame, text="Choose Wallpaper", command=choose_wallpaper,
                 bg=self.secondary_bg, fg=self.fg_color, relief=tk.FLAT).pack(anchor=tk.W, pady=5)
    
    def create_system_settings(self, parent):
        """Create system settings panel"""
        tk.Label(parent, text="System", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 16, 'bold')).pack(anchor=tk.W, padx=20, pady=20)
        
        system_info = f"""
Operating System: {platform.system()} {platform.release()}
Version: {platform.version()}
Machine: {platform.machine()}
Processor: {platform.processor()}
Python Version: {sys.version.split()[0]}
        """
        
        tk.Label(parent, text=system_info, bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 10), justify=tk.LEFT).pack(anchor=tk.W, padx=20, pady=10)
    
    def create_network_settings(self, parent):
        """Create network settings panel"""
        tk.Label(parent, text="Network", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 16, 'bold')).pack(anchor=tk.W, padx=20, pady=20)
        
        try:
            net_info = "Network Interfaces:\n\n"
            addrs = psutil.net_if_addrs()
            for interface, addresses in addrs.items():
                net_info += f"{interface}:\n"
                for addr in addresses:
                    net_info += f"  {addr.family.name}: {addr.address}\n"
                net_info += "\n"
            
            tk.Label(parent, text=net_info, bg=self.bg_color, fg=self.fg_color,
                    font=('Arial', 9), justify=tk.LEFT).pack(anchor=tk.W, padx=20, pady=10)
        except:
            tk.Label(parent, text="Network information unavailable", bg=self.bg_color,
                    fg=self.fg_color, font=('Arial', 10)).pack(padx=20, pady=10)
    
    def create_privacy_settings(self, parent):
        """Create privacy settings panel"""
        tk.Label(parent, text="Privacy & Security", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 16, 'bold')).pack(anchor=tk.W, padx=20, pady=20)
        
        tk.Label(parent, text="Privacy settings help protect your data and control\nwhat information is shared.",
                bg=self.bg_color, fg=self.fg_color, font=('Arial', 10)).pack(anchor=tk.W, padx=20, pady=10)
        
        # Privacy options
        options = [
            "📍 Location Services",
            "🎤 Microphone Access",
            "📷 Camera Access",
            "📁 File Access",
        ]
        
        for option in options:
            frame = tk.Frame(parent, bg=self.bg_color)
            frame.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(frame, text=option, bg=self.bg_color, fg=self.fg_color,
                    font=('Arial', 10)).pack(side=tk.LEFT)
            tk.Checkbutton(frame, bg=self.bg_color, fg=self.fg_color).pack(side=tk.RIGHT)
    
    def create_about_settings(self, parent):
        """Create about settings panel"""
        tk.Label(parent, text="About AdvancedOS", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 16, 'bold')).pack(anchor=tk.W, padx=20, pady=20)
        
        about_text = f"""
AdvancedOS Version 2.0

A modern, feature-rich operating system interface
built with Python and Tkinter.

Features: 1000+ and growing
Platform: {platform.system()}
Python: {sys.version.split()[0]}

© 2024 AdvancedOS Project
        """
        
        tk.Label(parent, text=about_text, bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 10), justify=tk.LEFT).pack(padx=20, pady=10)
    
    def open_trash(self):
        """Open trash/recycle bin"""
        trash = tk.Toplevel(self.root)
        trash.title("Trash")
        trash.geometry("600x400")
        trash.configure(bg=self.bg_color)
        self.open_windows.append(trash)
        
        tk.Label(trash, text="🗑️ Trash", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        tk.Label(trash, text="Trash is empty", bg=self.bg_color, fg=self.fg_color,
                font=('Arial', 12)).pack(expand=True)
        
        tk.Button(trash, text="Empty Trash", bg=self.accent_color, fg='white',
                 relief=tk.FLAT, font=('Arial', 11), padx=20, pady=5,
                 command=lambda: self.show_notification("Trash", "Trash emptied")).pack(pady=20)
    
    def open_sandbox_manager(self):
        """Open sandbox manager dashboard"""
        if hasattr(self, 'sandbox_dashboard'):
            self.sandbox_dashboard.show()
        else:
            messagebox.showinfo("Sandbox Manager", 
                              "Sandbox Manager is not available.\nPlease check that sandbox_dashboard.py is installed.")


if __name__ == "__main__":
    root = tk.Tk()
    
    # Set window icon (if available)
    try:
        root.iconphoto(True, tk.PhotoImage(data=""))
    except:
        pass
    
    # Initialize OS
    os_app = AdvancedOS(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Run main loop
    root.mainloop()
    
    # Save settings on exit
    os_app.save_settings()

