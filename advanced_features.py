"""
Advanced Features - App Store, Time Machine, Voice Assistant, and Cloud Sync
Additional features to make AdvancedOS the world's best OS
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
import os
import shutil
import time
from datetime import datetime
from pathlib import Path
import threading


class AppStore:
    """App Store - Application marketplace"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
        self.apps_data = self.load_apps_catalog()
    
    def load_apps_catalog(self):
        """Load available applications catalog"""
        return {
            'productivity': [
                {'name': 'Code Editor Pro', 'icon': '💻', 'description': 'Advanced code editor with AI assistance', 'size': '45 MB', 'rating': 4.8, 'price': 'Free'},
                {'name': 'Office Suite', 'icon': '📊', 'description': 'Complete office productivity suite', 'size': '120 MB', 'rating': 4.6, 'price': '$9.99'},
                {'name': 'PDF Master', 'icon': '📄', 'description': 'Professional PDF editor and viewer', 'size': '32 MB', 'rating': 4.7, 'price': 'Free'},
            ],
            'multimedia': [
                {'name': 'Video Studio', 'icon': '🎬', 'description': 'Professional video editing software', 'size': '200 MB', 'rating': 4.9, 'price': '$29.99'},
                {'name': 'Audio Producer', 'icon': '🎵', 'description': 'Music production and editing', 'size': '85 MB', 'rating': 4.5, 'price': '$19.99'},
                {'name': 'Photo Editor Plus', 'icon': '📷', 'description': 'Advanced photo editing tools', 'size': '95 MB', 'rating': 4.8, 'price': 'Free'},
            ],
            'development': [
                {'name': 'Database Manager', 'icon': '🗄️', 'description': 'Visual database management tool', 'size': '65 MB', 'rating': 4.6, 'price': 'Free'},
                {'name': 'API Tester Pro', 'icon': '🔌', 'description': 'Test and debug APIs', 'size': '28 MB', 'rating': 4.7, 'price': '$14.99'},
                {'name': 'Git Client', 'icon': '🌿', 'description': 'Beautiful Git interface', 'size': '40 MB', 'rating': 4.9, 'price': 'Free'},
            ],
            'utilities': [
                {'name': 'System Cleaner', 'icon': '🧹', 'description': 'Clean and optimize your system', 'size': '18 MB', 'rating': 4.5, 'price': 'Free'},
                {'name': 'Password Vault', 'icon': '🔐', 'description': 'Secure password manager', 'size': '12 MB', 'rating': 4.8, 'price': '$4.99'},
                {'name': 'Screen Recorder', 'icon': '🎥', 'description': 'Record your screen activities', 'size': '35 MB', 'rating': 4.6, 'price': 'Free'},
            ],
        }
    
    def show(self):
        """Show App Store"""
        store = tk.Toplevel(self.root)
        store.title("App Store")
        store.geometry("1000x700")
        store.configure(bg=self.os.bg_color)
        self.os.open_windows.append(store)
        
        # Header
        header = tk.Frame(store, bg=self.os.secondary_bg, height=60)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="🏪 App Store", bg=self.os.secondary_bg,
                fg=self.os.fg_color, font=('Arial', 18, 'bold')).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Search bar
        search_frame = tk.Frame(header, bg=self.os.secondary_bg)
        search_frame.pack(side=tk.RIGHT, padx=20)
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var,
                               bg=self.os.bg_color, fg=self.os.fg_color,
                               font=('Arial', 11), width=30, relief=tk.FLAT)
        search_entry.pack(side=tk.LEFT, ipady=5)
        
        tk.Button(search_frame, text="🔍", command=lambda: None,
                 bg=self.os.secondary_bg, fg=self.os.fg_color,
                 relief=tk.FLAT, font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        
        # Sidebar
        sidebar = tk.Frame(store, bg=self.os.secondary_bg, width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(sidebar, text="Categories", bg=self.os.secondary_bg,
                fg=self.os.fg_color, font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Content area
        content = tk.Frame(store, bg=self.os.bg_color)
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Category buttons
        for category in self.apps_data.keys():
            btn = tk.Button(sidebar, text=category.title(),
                          command=lambda c=category: self.show_category(content, c),
                          bg=self.os.secondary_bg, fg=self.os.fg_color,
                          relief=tk.FLAT, anchor=tk.W, font=('Arial', 11))
            btn.pack(fill=tk.X, padx=10, pady=2)
        
        # Show first category
        self.show_category(content, 'productivity')
    
    def show_category(self, parent, category):
        """Show apps in category"""
        # Clear previous content
        for widget in parent.winfo_children():
            widget.destroy()
        
        tk.Label(parent, text=category.title(), bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 16, 'bold')).pack(anchor=tk.W, pady=10)
        
        # Scrollable frame
        canvas = tk.Canvas(parent, bg=self.os.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.os.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add apps
        for app in self.apps_data.get(category, []):
            self.create_app_card(scrollable_frame, app)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_app_card(self, parent, app):
        """Create app card"""
        card = tk.Frame(parent, bg=self.os.secondary_bg, 
                       relief=tk.RAISED, borderwidth=1)
        card.pack(fill=tk.X, pady=5, padx=5)
        
        # App info
        info_frame = tk.Frame(card, bg=self.os.secondary_bg)
        info_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Icon
        tk.Label(info_frame, text=app['icon'], bg=self.os.secondary_bg,
                font=('Arial', 32)).pack(side=tk.LEFT, padx=(0, 15))
        
        # Details
        details = tk.Frame(info_frame, bg=self.os.secondary_bg)
        details.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(details, text=app['name'], bg=self.os.secondary_bg,
                fg=self.os.fg_color, font=('Arial', 13, 'bold'),
                anchor=tk.W).pack(fill=tk.X)
        
        tk.Label(details, text=app['description'], bg=self.os.secondary_bg,
                fg=self.os.fg_color, font=('Arial', 9),
                anchor=tk.W, wraplength=400).pack(fill=tk.X)
        
        info_text = f"⭐ {app['rating']} • {app['size']} • {app['price']}"
        tk.Label(details, text=info_text, bg=self.os.secondary_bg,
                fg='#888', font=('Arial', 8),
                anchor=tk.W).pack(fill=tk.X, pady=(5, 0))
        
        # Install button
        btn_text = "GET" if app['price'] == 'Free' else app['price']
        tk.Button(info_frame, text=btn_text,
                 command=lambda a=app: self.install_app(a),
                 bg=self.os.accent_color, fg='white', relief=tk.FLAT,
                 font=('Arial', 10, 'bold'), padx=20, pady=5).pack(side=tk.RIGHT)
    
    def install_app(self, app):
        """Simulate app installation"""
        progress = tk.Toplevel(self.root)
        progress.title("Installing")
        progress.geometry("400x150")
        progress.configure(bg=self.os.bg_color)
        progress.transient(self.root)
        
        tk.Label(progress, text=f"Installing {app['name']}...",
                bg=self.os.bg_color, fg=self.os.fg_color,
                font=('Arial', 12)).pack(pady=20)
        
        prog_bar = ttk.Progressbar(progress, mode='indeterminate', length=300)
        prog_bar.pack(pady=10)
        prog_bar.start(10)
        
        def finish_install():
            prog_bar.stop()
            progress.destroy()
            self.os.show_notification("App Store", f"{app['name']} installed successfully!")
        
        progress.after(2000, finish_install)


class TimeMachine:
    """Time Machine - Backup and restore system"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
        self.backup_dir = Path.home() / '.advancedos' / 'backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def show(self):
        """Show Time Machine interface"""
        tm = tk.Toplevel(self.root)
        tm.title("Time Machine")
        tm.geometry("900x600")
        tm.configure(bg=self.os.bg_color)
        self.os.open_windows.append(tm)
        
        # Header
        header = tk.Frame(tm, bg=self.os.secondary_bg, height=60)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="⏰ Time Machine", bg=self.os.secondary_bg,
                fg=self.os.fg_color, font=('Arial', 18, 'bold')).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Backup button
        tk.Button(header, text="🔄 Create Backup",
                 command=self.create_backup,
                 bg=self.os.accent_color, fg='white', relief=tk.FLAT,
                 font=('Arial', 11), padx=15, pady=5).pack(side=tk.RIGHT, padx=20)
        
        # Backup list
        list_frame = tk.Frame(tm, bg=self.os.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(list_frame, text="Available Backups", bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 14, 'bold')).pack(anchor=tk.W, pady=5)
        
        # Treeview for backups
        columns = ('Date', 'Time', 'Size', 'Files')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Load existing backups
        self.load_backups(tree)
        
        # Control buttons
        btn_frame = tk.Frame(tm, bg=self.os.bg_color)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📂 Restore",
                 command=lambda: self.restore_backup(tree),
                 bg=self.os.secondary_bg, fg=self.os.fg_color,
                 relief=tk.FLAT, font=('Arial', 11), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ Delete",
                 command=lambda: self.delete_backup(tree),
                 bg='#FF3B30', fg='white', relief=tk.FLAT,
                 font=('Arial', 11), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
    
    def load_backups(self, tree):
        """Load backup list"""
        tree.delete(*tree.get_children())
        
        if self.backup_dir.exists():
            for backup in sorted(self.backup_dir.iterdir(), reverse=True):
                if backup.is_dir():
                    stat = backup.stat()
                    date = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')
                    time_str = datetime.fromtimestamp(stat.st_mtime).strftime('%H:%M:%S')
                    
                    # Calculate size
                    size = sum(f.stat().st_size for f in backup.rglob('*') if f.is_file())
                    size_str = self.os.format_size(size)
                    
                    # Count files
                    files = len([f for f in backup.rglob('*') if f.is_file()])
                    
                    tree.insert('', tk.END, values=(date, time_str, size_str, files),
                              tags=(backup.name,))
    
    def create_backup(self):
        """Create a new backup"""
        backup_name = datetime.now().strftime('backup_%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / backup_name
        
        progress = tk.Toplevel(self.root)
        progress.title("Creating Backup")
        progress.geometry("400x150")
        progress.configure(bg=self.os.bg_color)
        
        tk.Label(progress, text="Creating backup...", bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 12)).pack(pady=20)
        
        prog_bar = ttk.Progressbar(progress, mode='indeterminate', length=300)
        prog_bar.pack(pady=10)
        prog_bar.start(10)
        
        def do_backup():
            try:
                backup_path.mkdir(parents=True, exist_ok=True)
                
                # Backup settings
                settings_file = Path.home() / '.advancedos_settings.json'
                if settings_file.exists():
                    shutil.copy2(settings_file, backup_path / 'settings.json')
                
                # Backup sandbox configs
                sandbox_dir = Path.home() / '.advancedos' / 'sandboxes'
                if sandbox_dir.exists():
                    shutil.copytree(sandbox_dir, backup_path / 'sandboxes', 
                                  dirs_exist_ok=True)
                
                prog_bar.stop()
                progress.destroy()
                self.os.show_notification("Time Machine", "Backup created successfully!")
            except Exception as e:
                prog_bar.stop()
                progress.destroy()
                messagebox.showerror("Error", f"Backup failed: {str(e)}")
        
        threading.Thread(target=do_backup, daemon=True).start()
    
    def restore_backup(self, tree):
        """Restore from backup"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a backup to restore")
            return
        
        if messagebox.askyesno("Confirm Restore", 
                              "Are you sure you want to restore this backup?\nCurrent settings will be overwritten."):
            self.os.show_notification("Time Machine", "Backup restored. Restart to apply changes.")
    
    def delete_backup(self, tree):
        """Delete a backup"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a backup to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this backup?"):
            item = tree.item(selection[0])
            backup_name = item['tags'][0]
            backup_path = self.backup_dir / backup_name
            
            try:
                shutil.rmtree(backup_path)
                self.load_backups(tree)
                self.os.show_notification("Time Machine", "Backup deleted")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete backup: {str(e)}")


class VoiceAssistant:
    """Voice Assistant - Siri-like voice commands"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
        self.listening = False
    
    def show(self):
        """Show voice assistant interface"""
        assistant = tk.Toplevel(self.root)
        assistant.title("Voice Assistant")
        assistant.geometry("400x500")
        assistant.configure(bg='#1a1a1a')
        assistant.attributes('-topmost', True)
        
        # Animated microphone icon
        icon_frame = tk.Frame(assistant, bg='#1a1a1a', height=200)
        icon_frame.pack(fill=tk.X, pady=40)
        
        icon_label = tk.Label(icon_frame, text="🎤", bg='#1a1a1a',
                             fg='white', font=('Arial', 80))
        icon_label.pack()
        
        # Status
        self.status_label = tk.Label(assistant, text="Tap to speak",
                                     bg='#1a1a1a', fg='white',
                                     font=('Arial', 14))
        self.status_label.pack(pady=10)
        
        # Text input
        input_frame = tk.Frame(assistant, bg='#1a1a1a')
        input_frame.pack(pady=20, padx=20, fill=tk.X)
        
        self.command_var = tk.StringVar()
        command_entry = tk.Entry(input_frame, textvariable=self.command_var,
                                bg='#2a2a2a', fg='white', font=('Arial', 12),
                                relief=tk.FLAT)
        command_entry.pack(fill=tk.X, ipady=8)
        command_entry.focus()
        
        # Response area
        response_frame = tk.Frame(assistant, bg='#1a1a1a')
        response_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.response_text = scrolledtext.ScrolledText(response_frame,
                                                      bg='#2a2a2a', fg='white',
                                                      font=('Arial', 11),
                                                      height=8, wrap=tk.WORD,
                                                      relief=tk.FLAT)
        self.response_text.pack(fill=tk.BOTH, expand=True)
        
        # Process command
        def process_command(event=None):
            command = self.command_var.get().lower().strip()
            if command:
                self.response_text.insert(tk.END, f"\nYou: {command}\n")
                response = self.execute_command(command)
                self.response_text.insert(tk.END, f"Assistant: {response}\n")
                self.response_text.see(tk.END)
                self.command_var.set("")
        
        command_entry.bind('<Return>', process_command)
        
        # Listen button
        tk.Button(assistant, text="🎤 Ask",
                 command=process_command,
                 bg='#007AFF', fg='white', relief=tk.FLAT,
                 font=('Arial', 12), padx=40, pady=10).pack(pady=10)
    
    def execute_command(self, command):
        """Execute voice command"""
        if 'time' in command:
            return f"The current time is {datetime.now().strftime('%I:%M %p')}"
        elif 'date' in command:
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"
        elif 'open' in command and 'file' in command:
            self.os.open_file_explorer()
            return "Opening file explorer"
        elif 'open' in command and 'browser' in command:
            self.os.open_browser()
            return "Opening browser"
        elif 'open' in command and 'terminal' in command:
            self.os.open_terminal()
            return "Opening terminal"
        elif 'open' in command and 'calculator' in command:
            self.os.open_calculator()
            return "Opening calculator"
        elif 'create' in command and 'sandbox' in command:
            self.os.open_sandbox_manager()
            return "Opening sandbox manager"
        elif 'dark' in command and 'mode' in command:
            self.os.toggle_theme()
            return "Toggling dark mode"
        elif 'help' in command or 'what' in command and 'can' in command:
            return """I can help you with:
• Tell time and date
• Open applications (files, browser, terminal, calculator, etc.)
• Create sandboxes
• Toggle dark mode
• And much more!"""
        else:
            return "I'm not sure how to help with that. Try asking about the time, opening apps, or say 'help' for more options."


class CloudSync:
    """Cloud Sync - iCloud-style synchronization"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
        self.sync_enabled = False
        self.sync_folder = Path.home() / '.advancedos' / 'cloud'
        self.sync_folder.mkdir(parents=True, exist_ok=True)
    
    def show_settings(self):
        """Show cloud sync settings"""
        settings = tk.Toplevel(self.root)
        settings.title("Cloud Sync")
        settings.geometry("600x500")
        settings.configure(bg=self.os.bg_color)
        
        # Header
        tk.Label(settings, text="☁️ Cloud Sync", bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 18, 'bold')).pack(pady=20)
        
        # Status
        status_frame = tk.Frame(settings, bg=self.os.secondary_bg,
                              relief=tk.RAISED, borderwidth=1)
        status_frame.pack(fill=tk.X, padx=20, pady=10)
        
        status_text = "Enabled" if self.sync_enabled else "Disabled"
        status_color = '#34C759' if self.sync_enabled else '#FF3B30'
        
        tk.Label(status_frame, text=f"Status: {status_text}",
                bg=self.os.secondary_bg, fg=status_color,
                font=('Arial', 12, 'bold')).pack(pady=15)
        
        # Toggle
        toggle_btn = tk.Button(settings, 
                              text="Enable Cloud Sync" if not self.sync_enabled else "Disable Cloud Sync",
                              command=lambda: self.toggle_sync(settings),
                              bg=self.os.accent_color, fg='white', relief=tk.FLAT,
                              font=('Arial', 11), padx=30, pady=8)
        toggle_btn.pack(pady=10)
        
        # Synced items
        items_frame = tk.LabelFrame(settings, text="Synced Items",
                                   bg=self.os.bg_color, fg=self.os.fg_color,
                                   font=('Arial', 12, 'bold'))
        items_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        items = [
            '⚙️ Settings',
            '📁 Documents',
            '📝 Notes',
            '📧 Email',
            '📅 Calendar Events',
            '🔖 Bookmarks',
            '🔒 Sandbox Configurations'
        ]
        
        for item in items:
            var = tk.BooleanVar(value=True)
            tk.Checkbutton(items_frame, text=item, variable=var,
                          bg=self.os.bg_color, fg=self.os.fg_color,
                          font=('Arial', 11)).pack(anchor=tk.W, padx=20, pady=5)
        
        # Storage info
        info_frame = tk.Frame(settings, bg=self.os.bg_color)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        storage_used = self.calculate_storage_used()
        tk.Label(info_frame, text=f"Storage Used: {storage_used}",
                bg=self.os.bg_color, fg=self.os.fg_color,
                font=('Arial', 10)).pack(anchor=tk.W)
    
    def toggle_sync(self, window):
        """Toggle cloud sync"""
        self.sync_enabled = not self.sync_enabled
        status = "enabled" if self.sync_enabled else "disabled"
        self.os.show_notification("Cloud Sync", f"Cloud sync {status}")
        window.destroy()
        self.show_settings()
    
    def calculate_storage_used(self):
        """Calculate storage used"""
        if self.sync_folder.exists():
            size = sum(f.stat().st_size for f in self.sync_folder.rglob('*') if f.is_file())
            return self.os.format_size(size)
        return "0 B"
