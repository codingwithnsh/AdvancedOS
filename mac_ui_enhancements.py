"""
Mac UI Enhancements - Advanced Mac-style UI components and animations
Provides Mission Control, Launchpad, Hot Corners, and enhanced visual effects
"""

import tkinter as tk
from tkinter import ttk
import time
import math


class MissionControl:
    """Mission Control - Virtual desktop manager with overview"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
        self.desktops = [{'name': 'Desktop 1', 'windows': []}]
        self.current_desktop = 0
    
    def show(self):
        """Show Mission Control overview"""
        mc = tk.Toplevel(self.root)
        mc.title("Mission Control")
        mc.attributes('-fullscreen', True)
        mc.configure(bg='#1a1a1a')
        
        # Header
        header = tk.Frame(mc, bg='#1a1a1a', height=60)
        header.pack(fill=tk.X, pady=20)
        
        tk.Label(header, text="Mission Control", bg='#1a1a1a', fg='white',
                font=('Arial', 24, 'bold')).pack()
        
        # Desktop previews
        previews_frame = tk.Frame(mc, bg='#1a1a1a')
        previews_frame.pack(expand=True)
        
        for i, desktop in enumerate(self.desktops):
            desktop_frame = tk.Frame(previews_frame, bg='#2a2a2a', 
                                    relief=tk.RAISED, borderwidth=2,
                                    width=400, height=250)
            desktop_frame.pack(side=tk.LEFT, padx=20, pady=20)
            
            # Desktop label
            label_bg = '#007AFF' if i == self.current_desktop else '#2a2a2a'
            tk.Label(desktop_frame, text=desktop['name'], bg=label_bg, fg='white',
                    font=('Arial', 14, 'bold')).pack(pady=10)
            
            # Window count
            window_count = len(desktop['windows'])
            tk.Label(desktop_frame, text=f"{window_count} windows", 
                    bg='#2a2a2a', fg='#888', font=('Arial', 10)).pack()
            
            # Click to switch
            desktop_frame.bind('<Button-1>', 
                             lambda e, idx=i: self.switch_desktop(idx, mc))
        
        # Add desktop button
        add_btn = tk.Button(previews_frame, text="+\nNew Desktop", 
                          command=lambda: self.add_desktop(mc),
                          bg='#2a2a2a', fg='white', relief=tk.FLAT,
                          font=('Arial', 16), width=10, height=8)
        add_btn.pack(side=tk.LEFT, padx=20)
        
        # Close button
        close_btn = tk.Button(mc, text="✕ Close", command=mc.destroy,
                            bg='#007AFF', fg='white', relief=tk.FLAT,
                            font=('Arial', 12), padx=20, pady=10)
        close_btn.pack(pady=20)
        
        # ESC to close
        mc.bind('<Escape>', lambda e: mc.destroy())
    
    def add_desktop(self, mc_window):
        """Add a new virtual desktop"""
        desktop_num = len(self.desktops) + 1
        self.desktops.append({'name': f'Desktop {desktop_num}', 'windows': []})
        mc_window.destroy()
        self.show()
    
    def switch_desktop(self, index, mc_window):
        """Switch to a different desktop"""
        self.current_desktop = index
        mc_window.destroy()
        self.os.show_notification("Mission Control", 
                                 f"Switched to {self.desktops[index]['name']}")


class Launchpad:
    """Launchpad - Full-screen application launcher grid"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
    
    def show(self):
        """Show Launchpad"""
        lp = tk.Toplevel(self.root)
        lp.title("Launchpad")
        lp.attributes('-fullscreen', True)
        
        # Blur effect background
        bg_color = '#1a1a1a' if self.os.theme_mode == 'dark' else '#f0f0f0'
        lp.configure(bg=bg_color)
        
        # Search bar
        search_frame = tk.Frame(lp, bg=bg_color)
        search_frame.pack(pady=30)
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var,
                               font=('Arial', 16), width=40,
                               bg='#2a2a2a' if self.os.theme_mode == 'dark' else 'white',
                               fg='white' if self.os.theme_mode == 'dark' else 'black',
                               relief=tk.FLAT)
        search_entry.pack(ipady=10)
        search_entry.focus()
        
        # App grid
        grid_frame = tk.Frame(lp, bg=bg_color)
        grid_frame.pack(expand=True)
        
        apps = [
            ('📁', 'Finder', self.os.open_file_explorer),
            ('🌐', 'Browser', self.os.open_browser),
            ('📧', 'Mail', self.os.open_email_client),
            ('📅', 'Calendar', self.os.open_calendar),
            ('📝', 'Notes', self.os.open_notes),
            ('🎵', 'Music', self.os.open_music_player),
            ('📷', 'Photos', self.os.open_photo_viewer),
            ('🎬', 'Videos', self.os.open_video_player),
            ('💻', 'Terminal', self.os.open_terminal),
            ('⚙️', 'Settings', self.os.open_settings),
            ('📊', 'Activity', self.os.open_activity_monitor),
            ('🧮', 'Calculator', self.os.open_calculator),
            ('📝', 'TextEdit', self.os.open_text_editor),
        ]
        
        # Filter function
        def filter_apps(*args):
            query = search_var.get().lower()
            for widget in grid_frame.winfo_children():
                widget.destroy()
            
            filtered = [(icon, name, cmd) for icon, name, cmd in apps 
                       if query in name.lower()]
            
            display_apps(filtered if query else apps)
        
        def display_apps(app_list):
            row, col = 0, 0
            max_cols = 6
            
            for icon, name, command in app_list:
                app_frame = tk.Frame(grid_frame, bg=bg_color)
                app_frame.grid(row=row, column=col, padx=30, pady=30)
                
                # Icon button
                btn = tk.Button(app_frame, text=icon, 
                              command=lambda c=command: (c(), lp.destroy()),
                              bg='#2a2a2a' if self.os.theme_mode == 'dark' else 'white',
                              fg='white' if self.os.theme_mode == 'dark' else 'black',
                              relief=tk.FLAT, font=('Arial', 48),
                              width=3, height=1, cursor='hand2')
                btn.pack()
                
                # App name
                tk.Label(app_frame, text=name, bg=bg_color,
                        fg='white' if self.os.theme_mode == 'dark' else 'black',
                        font=('Arial', 11)).pack(pady=5)
                
                # Hover effect
                btn.bind('<Enter>', lambda e, b=btn: b.config(
                    bg='#3a3a3a' if self.os.theme_mode == 'dark' else '#e0e0e0'))
                btn.bind('<Leave>', lambda e, b=btn: b.config(
                    bg='#2a2a2a' if self.os.theme_mode == 'dark' else 'white'))
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
        
        # Initial display
        display_apps(apps)
        
        # Bind search
        search_var.trace('w', filter_apps)
        
        # Close on ESC or click outside
        lp.bind('<Escape>', lambda e: lp.destroy())
        lp.bind('<Button-1>', lambda e: lp.destroy() if e.widget == lp else None)


class HotCorners:
    """Hot Corners - Trigger actions by moving mouse to screen corners"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
        self.corners = {
            'top_left': None,
            'top_right': None,
            'bottom_left': None,
            'bottom_right': None
        }
        self.enabled = False
    
    def configure(self):
        """Configure hot corners"""
        config_win = tk.Toplevel(self.root)
        config_win.title("Hot Corners")
        config_win.geometry("500x400")
        config_win.configure(bg=self.os.bg_color)
        
        tk.Label(config_win, text="Hot Corners Configuration", 
                bg=self.os.bg_color, fg=self.os.fg_color,
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        tk.Label(config_win, text="Assign actions to screen corners:",
                bg=self.os.bg_color, fg=self.os.fg_color,
                font=('Arial', 11)).pack(pady=10)
        
        actions = [
            ('None', None),
            ('Mission Control', 'mission_control'),
            ('Launchpad', 'launchpad'),
            ('Desktop', 'desktop'),
            ('App Windows', 'app_windows'),
            ('Lock Screen', 'lock_screen')
        ]
        
        corners_frame = tk.Frame(config_win, bg=self.os.bg_color)
        corners_frame.pack(pady=20)
        
        for corner_name, corner_key in [
            ('Top Left', 'top_left'),
            ('Top Right', 'top_right'),
            ('Bottom Left', 'bottom_left'),
            ('Bottom Right', 'bottom_right')
        ]:
            frame = tk.Frame(corners_frame, bg=self.os.bg_color)
            frame.pack(fill=tk.X, pady=5, padx=20)
            
            tk.Label(frame, text=f"{corner_name}:", bg=self.os.bg_color,
                    fg=self.os.fg_color, font=('Arial', 10), width=15,
                    anchor=tk.W).pack(side=tk.LEFT)
            
            var = tk.StringVar(value=self.corners.get(corner_key, 'None'))
            combo = ttk.Combobox(frame, textvariable=var, 
                               values=[a[0] for a in actions],
                               state='readonly', width=20)
            combo.pack(side=tk.LEFT, padx=10)
            
            def save_corner(key=corner_key, v=var):
                self.corners[key] = v.get()
            
            combo.bind('<<ComboboxSelected>>', lambda e, k=corner_key, v=var: save_corner(k, v))
        
        # Enable/Disable
        enable_var = tk.BooleanVar(value=self.enabled)
        tk.Checkbutton(config_win, text="Enable Hot Corners",
                      variable=enable_var, bg=self.os.bg_color,
                      fg=self.os.fg_color, font=('Arial', 11),
                      command=lambda: setattr(self, 'enabled', enable_var.get())).pack(pady=20)
        
        tk.Button(config_win, text="Done", command=config_win.destroy,
                 bg=self.os.accent_color, fg='white', relief=tk.FLAT,
                 font=('Arial', 11), padx=30, pady=8).pack(pady=10)


class DockEnhancer:
    """Enhanced dock with magnification and animations"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
        self.magnification = True
        self.animation_speed = 0.2
    
    def create_enhanced_dock(self, parent):
        """Create enhanced dock with animations"""
        dock = tk.Frame(parent, bg='#2C2C2E', height=80)
        
        # Dock apps with magnification
        apps = [
            ('🔍', 'Spotlight', self.os.open_spotlight),
            ('📁', 'Finder', self.os.open_file_explorer),
            ('🌐', 'Browser', self.os.open_browser),
            ('✉️', 'Mail', self.os.open_email_client),
            ('📅', 'Calendar', self.os.open_calendar),
            ('📝', 'Notes', self.os.open_notes),
            ('🎵', 'Music', self.os.open_music_player),
            ('📷', 'Photos', self.os.open_photo_viewer),
        ]
        
        container = tk.Frame(dock, bg='#2C2C2E')
        container.pack(expand=True)
        
        for icon, tooltip, command in apps:
            btn = tk.Button(container, text=icon, command=command,
                          bg='#2C2C2E', fg='white',
                          relief=tk.FLAT, font=('Arial', 28),
                          width=2, height=1, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5)
            
            # Hover magnification effect
            def on_enter(e, b=btn):
                if self.magnification:
                    b.config(font=('Arial', 36))
            
            def on_leave(e, b=btn):
                if self.magnification:
                    b.config(font=('Arial', 28))
            
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
        
        return dock


class QuickLook:
    """Quick Look - Preview files without opening them"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
    
    def preview(self, filepath):
        """Show quick look preview for file"""
        import os
        
        ql = tk.Toplevel(self.root)
        ql.title(f"Quick Look - {os.path.basename(filepath)}")
        ql.geometry("800x600")
        ql.configure(bg='#1a1a1a')
        
        # Header
        header = tk.Frame(ql, bg='#2a2a2a', height=50)
        header.pack(fill=tk.X)
        
        tk.Label(header, text=os.path.basename(filepath), bg='#2a2a2a',
                fg='white', font=('Arial', 14, 'bold')).pack(pady=15)
        
        # Content area
        content = tk.Frame(ql, bg='#1a1a1a')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Check file type and display preview
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext in ['.txt', '.py', '.md', '.json', '.xml', '.html', '.css', '.js']:
            # Text preview
            import tkinter.scrolledtext as scrolledtext
            text_widget = scrolledtext.ScrolledText(content, bg='#2a2a2a',
                                                   fg='white', font=('Courier', 11),
                                                   wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True)
            
            try:
                with open(filepath, 'r') as f:
                    text_widget.insert('1.0', f.read())
                text_widget.config(state='disabled')
            except:
                text_widget.insert('1.0', "Cannot preview this file")
        
        elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
            # Image preview
            try:
                from PIL import Image, ImageTk
                img = Image.open(filepath)
                img.thumbnail((760, 500), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                label = tk.Label(content, image=photo, bg='#1a1a1a')
                label.image = photo  # Keep reference
                label.pack(expand=True)
            except:
                tk.Label(content, text="Cannot preview image", bg='#1a1a1a',
                        fg='white', font=('Arial', 14)).pack(expand=True)
        
        else:
            # Generic info
            import datetime
            stat = os.stat(filepath)
            info = f"""
File: {os.path.basename(filepath)}
Type: {ext or 'Unknown'}
Size: {self.os.format_size(stat.st_size)}
Modified: {datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
            """
            tk.Label(content, text=info, bg='#1a1a1a', fg='white',
                    font=('Arial', 12), justify=tk.LEFT).pack(expand=True)
        
        # Close button
        tk.Button(ql, text="Close", command=ql.destroy,
                 bg='#007AFF', fg='white', relief=tk.FLAT,
                 font=('Arial', 11), padx=30, pady=8).pack(pady=10)
        
        # Space to close
        ql.bind('<space>', lambda e: ql.destroy())
        ql.bind('<Escape>', lambda e: ql.destroy())


class WindowSnapping:
    """Window snapping and tiling manager"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
    
    def snap_window(self, window, position):
        """Snap window to screen position"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        if position == 'left':
            window.geometry(f"{screen_width//2}x{screen_height}+0+0")
        elif position == 'right':
            window.geometry(f"{screen_width//2}x{screen_height}+{screen_width//2}+0")
        elif position == 'top':
            window.geometry(f"{screen_width}x{screen_height//2}+0+0")
        elif position == 'bottom':
            window.geometry(f"{screen_width}x{screen_height//2}+0+{screen_height//2}")
        elif position == 'top_left':
            window.geometry(f"{screen_width//2}x{screen_height//2}+0+0")
        elif position == 'top_right':
            window.geometry(f"{screen_width//2}x{screen_height//2}+{screen_width//2}+0")
        elif position == 'bottom_left':
            window.geometry(f"{screen_width//2}x{screen_height//2}+0+{screen_height//2}")
        elif position == 'bottom_right':
            window.geometry(f"{screen_width//2}x{screen_height//2}+{screen_width//2}+{screen_height//2}")
        elif position == 'maximize':
            window.state('zoomed')
        elif position == 'center':
            width = screen_width // 2
            height = screen_height // 2
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            window.geometry(f"{width}x{height}+{x}+{y}")


class FocusModes:
    """Focus modes and Do Not Disturb"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
        self.current_mode = None
        self.modes = {
            'do_not_disturb': {'name': 'Do Not Disturb', 'icon': '🌙'},
            'work': {'name': 'Work', 'icon': '💼'},
            'personal': {'name': 'Personal', 'icon': '🏠'},
            'sleep': {'name': 'Sleep', 'icon': '😴'}
        }
    
    def show_menu(self):
        """Show focus mode menu"""
        menu = tk.Toplevel(self.root)
        menu.title("Focus")
        menu.geometry("300x400")
        menu.configure(bg=self.os.bg_color)
        
        tk.Label(menu, text="Focus", bg=self.os.bg_color, fg=self.os.fg_color,
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        for mode_id, mode_info in self.modes.items():
            frame = tk.Frame(menu, bg=self.os.secondary_bg, 
                           relief=tk.RAISED, borderwidth=1)
            frame.pack(fill=tk.X, padx=20, pady=5)
            
            is_active = self.current_mode == mode_id
            bg_color = self.os.accent_color if is_active else self.os.secondary_bg
            
            btn = tk.Button(frame, 
                          text=f"{mode_info['icon']} {mode_info['name']}",
                          command=lambda m=mode_id: self.toggle_mode(m, menu),
                          bg=bg_color, fg='white' if is_active else self.os.fg_color,
                          relief=tk.FLAT, font=('Arial', 12),
                          anchor=tk.W, padx=20, pady=10)
            btn.pack(fill=tk.X)
        
        tk.Button(menu, text="Done", command=menu.destroy,
                 bg=self.os.accent_color, fg='white', relief=tk.FLAT,
                 font=('Arial', 11), padx=30, pady=8).pack(pady=20)
    
    def toggle_mode(self, mode_id, menu_window):
        """Toggle focus mode"""
        if self.current_mode == mode_id:
            self.current_mode = None
            self.os.show_notification("Focus", "Focus mode disabled")
        else:
            self.current_mode = mode_id
            mode_name = self.modes[mode_id]['name']
            self.os.show_notification("Focus", f"{mode_name} mode enabled")
        
        menu_window.destroy()
        self.show_menu()
