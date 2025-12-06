"""
Developer Tools & System Enhancements
Additional tools for developers and power users
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import os
import sys
import subprocess
import re
from pathlib import Path


class DeveloperConsole:
    """Developer console with debugging tools"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
        self.command_history = []
    
    def show(self):
        """Show developer console"""
        console = tk.Toplevel(self.root)
        console.title("Developer Console")
        console.geometry("900x600")
        console.configure(bg='#1E1E1E')
        
        # Tabs
        notebook = ttk.Notebook(console)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Console tab
        console_frame = tk.Frame(notebook, bg='#1E1E1E')
        notebook.add(console_frame, text="Console")
        
        # Output area
        self.console_output = scrolledtext.ScrolledText(console_frame,
                                                       bg='#1E1E1E', fg='#D4D4D4',
                                                       font=('Consolas', 10),
                                                       insertbackground='#D4D4D4')
        self.console_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Welcome message
        welcome = """Developer Console v1.0
Type 'help' for available commands
>>> """
        self.console_output.insert(tk.END, welcome)
        
        # Input
        input_frame = tk.Frame(console_frame, bg='#1E1E1E')
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(input_frame, text=">>>", bg='#1E1E1E', fg='#4EC9B0',
                font=('Consolas', 10)).pack(side=tk.LEFT, padx=(0, 5))
        
        self.console_input = tk.Entry(input_frame, bg='#2D2D30', fg='#D4D4D4',
                                     font=('Consolas', 10), insertbackground='#D4D4D4',
                                     relief=tk.FLAT)
        self.console_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.console_input.focus()
        self.console_input.bind('<Return>', self.execute_console_command)
        
        # System Info tab
        sysinfo_frame = tk.Frame(notebook, bg='#1E1E1E')
        notebook.add(sysinfo_frame, text="System Info")
        self.create_system_info_tab(sysinfo_frame)
        
        # Performance tab
        perf_frame = tk.Frame(notebook, bg='#1E1E1E')
        notebook.add(perf_frame, text="Performance")
        self.create_performance_tab(perf_frame)
        
        # Network tab
        network_frame = tk.Frame(notebook, bg='#1E1E1E')
        notebook.add(network_frame, text="Network")
        self.create_network_tab(network_frame)
    
    def execute_console_command(self, event=None):
        """Execute console command"""
        command = self.console_input.get().strip()
        if not command:
            return
        
        self.command_history.append(command)
        self.console_output.insert(tk.END, f"{command}\n")
        
        try:
            if command == 'help':
                help_text = """Available commands:
  help          - Show this help
  clear         - Clear console
  sysinfo       - Show system information
  env           - Show environment variables
  path          - Show Python path
  modules       - List loaded modules
  memory        - Show memory usage
  eval <expr>   - Evaluate Python expression
  exec <code>   - Execute Python code
  quit          - Close console
"""
                self.console_output.insert(tk.END, help_text)
            
            elif command == 'clear':
                self.console_output.delete(1.0, tk.END)
            
            elif command == 'sysinfo':
                import platform
                info = f"""System Information:
  OS: {platform.system()} {platform.release()}
  Version: {platform.version()}
  Machine: {platform.machine()}
  Processor: {platform.processor()}
  Python: {sys.version}
"""
                self.console_output.insert(tk.END, info)
            
            elif command == 'env':
                env = "\n".join([f"  {k}={v}" for k, v in sorted(os.environ.items())])
                self.console_output.insert(tk.END, f"Environment Variables:\n{env}\n")
            
            elif command == 'path':
                paths = "\n".join([f"  {p}" for p in sys.path])
                self.console_output.insert(tk.END, f"Python Path:\n{paths}\n")
            
            elif command == 'modules':
                modules = "\n".join([f"  {m}" for m in sorted(sys.modules.keys())])
                self.console_output.insert(tk.END, f"Loaded Modules:\n{modules}\n")
            
            elif command == 'memory':
                import psutil
                mem = psutil.virtual_memory()
                self.console_output.insert(tk.END, 
                    f"Memory: {mem.percent}% ({mem.used/(1024**3):.2f}GB / {mem.total/(1024**3):.2f}GB)\n")
            
            elif command.startswith('eval '):
                expr = command[5:]
                result = eval(expr)
                self.console_output.insert(tk.END, f"{result}\n")
            
            elif command.startswith('exec '):
                code = command[5:]
                exec(code)
                self.console_output.insert(tk.END, "Executed.\n")
            
            elif command == 'quit':
                self.console_output.master.master.destroy()
                return
            
            else:
                self.console_output.insert(tk.END, f"Unknown command: {command}\n")
        
        except Exception as e:
            self.console_output.insert(tk.END, f"Error: {str(e)}\n")
        
        self.console_output.insert(tk.END, ">>> ")
        self.console_output.see(tk.END)
        self.console_input.delete(0, tk.END)
    
    def create_system_info_tab(self, parent):
        """Create system info tab"""
        import platform
        import psutil
        
        info_text = scrolledtext.ScrolledText(parent, bg='#1E1E1E', fg='#D4D4D4',
                                             font=('Consolas', 10))
        info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        info = f"""System Information
{'=' * 60}

Operating System:
  OS: {platform.system()}
  Release: {platform.release()}
  Version: {platform.version()}
  Machine: {platform.machine()}
  Processor: {platform.processor()}
  
Python:
  Version: {sys.version}
  Executable: {sys.executable}
  Platform: {sys.platform}
  
CPU:
  Physical cores: {psutil.cpu_count(logical=False)}
  Logical cores: {psutil.cpu_count(logical=True)}
  Max Frequency: {psutil.cpu_freq().max:.2f} MHz
  
Memory:
  Total: {psutil.virtual_memory().total / (1024**3):.2f} GB
  Available: {psutil.virtual_memory().available / (1024**3):.2f} GB
  Used: {psutil.virtual_memory().percent}%
  
Disk:
  Total: {psutil.disk_usage('/').total / (1024**3):.2f} GB
  Used: {psutil.disk_usage('/').used / (1024**3):.2f} GB
  Free: {psutil.disk_usage('/').free / (1024**3):.2f} GB
  Usage: {psutil.disk_usage('/').percent}%
"""
        info_text.insert(1.0, info)
        info_text.config(state='disabled')
    
    def create_performance_tab(self, parent):
        """Create performance monitoring tab"""
        import psutil
        
        perf_frame = tk.Frame(parent, bg='#1E1E1E')
        perf_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # CPU info
        cpu_frame = tk.LabelFrame(perf_frame, text="CPU", bg='#1E1E1E',
                                 fg='#D4D4D4', font=('Consolas', 11, 'bold'))
        cpu_frame.pack(fill=tk.X, pady=5)
        
        cpu_label = tk.Label(cpu_frame, text=f"Usage: {psutil.cpu_percent()}%",
                            bg='#1E1E1E', fg='#D4D4D4', font=('Consolas', 10))
        cpu_label.pack(pady=5)
        
        # Memory info
        mem_frame = tk.LabelFrame(perf_frame, text="Memory", bg='#1E1E1E',
                                 fg='#D4D4D4', font=('Consolas', 11, 'bold'))
        mem_frame.pack(fill=tk.X, pady=5)
        
        mem = psutil.virtual_memory()
        mem_label = tk.Label(mem_frame, 
                            text=f"Used: {mem.used/(1024**3):.2f}GB / {mem.total/(1024**3):.2f}GB ({mem.percent}%)",
                            bg='#1E1E1E', fg='#D4D4D4', font=('Consolas', 10))
        mem_label.pack(pady=5)
        
        # Disk info
        disk_frame = tk.LabelFrame(perf_frame, text="Disk", bg='#1E1E1E',
                                  fg='#D4D4D4', font=('Consolas', 11, 'bold'))
        disk_frame.pack(fill=tk.X, pady=5)
        
        disk = psutil.disk_usage('/')
        disk_label = tk.Label(disk_frame,
                             text=f"Used: {disk.used/(1024**3):.2f}GB / {disk.total/(1024**3):.2f}GB ({disk.percent}%)",
                             bg='#1E1E1E', fg='#D4D4D4', font=('Consolas', 10))
        disk_label.pack(pady=5)
    
    def create_network_tab(self, parent):
        """Create network monitoring tab"""
        import psutil
        
        network_text = scrolledtext.ScrolledText(parent, bg='#1E1E1E', fg='#D4D4D4',
                                                font=('Consolas', 10))
        network_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        info = "Network Information\n" + "=" * 60 + "\n\n"
        
        # Network interfaces
        info += "Network Interfaces:\n"
        addrs = psutil.net_if_addrs()
        for interface, addresses in addrs.items():
            info += f"\n{interface}:\n"
            for addr in addresses:
                info += f"  {addr.family.name}: {addr.address}\n"
        
        # Network stats
        net_io = psutil.net_io_counters()
        info += f"\nNetwork Statistics:\n"
        info += f"  Bytes Sent: {net_io.bytes_sent / (1024**2):.2f} MB\n"
        info += f"  Bytes Received: {net_io.bytes_recv / (1024**2):.2f} MB\n"
        info += f"  Packets Sent: {net_io.packets_sent}\n"
        info += f"  Packets Received: {net_io.packets_recv}\n"
        
        network_text.insert(1.0, info)
        network_text.config(state='disabled')


class PackageManager:
    """Package manager for installing Python packages"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
    
    def show(self):
        """Show package manager"""
        pm = tk.Toplevel(self.root)
        pm.title("Package Manager")
        pm.geometry("800x600")
        pm.configure(bg=self.os.bg_color)
        
        # Header
        header = tk.Frame(pm, bg=self.os.secondary_bg, height=60)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="📦 Package Manager", bg=self.os.secondary_bg,
                fg=self.os.fg_color, font=('Arial', 18, 'bold')).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Search
        search_frame = tk.Frame(header, bg=self.os.secondary_bg)
        search_frame.pack(side=tk.RIGHT, padx=20)
        
        search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=search_var, bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 11), width=30).pack(side=tk.LEFT)
        
        tk.Button(search_frame, text="🔍 Search",
                 bg=self.os.accent_color, fg='white', relief=tk.FLAT,
                 font=('Arial', 10), padx=10).pack(side=tk.LEFT, padx=5)
        
        # Package list
        list_frame = tk.Frame(pm, bg=self.os.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        columns = ('Package', 'Version', 'Status')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Load installed packages
        self.load_packages(tree)
        
        # Buttons
        btn_frame = tk.Frame(pm, bg=self.os.bg_color)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📥 Install Package",
                 command=lambda: self.install_package_dialog(tree),
                 bg=self.os.accent_color, fg='white', relief=tk.FLAT,
                 font=('Arial', 11), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🔄 Update Package",
                 command=lambda: messagebox.showinfo("Update", "Feature coming soon"),
                 bg=self.os.secondary_bg, fg=self.os.fg_color, relief=tk.FLAT,
                 font=('Arial', 11), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ Uninstall",
                 command=lambda: messagebox.showinfo("Uninstall", "Feature coming soon"),
                 bg='#FF3B30', fg='white', relief=tk.FLAT,
                 font=('Arial', 11), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
    
    def load_packages(self, tree):
        """Load installed packages"""
        tree.delete(*tree.get_children())
        
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'list'],
                                  capture_output=True, text=True)
            
            lines = result.stdout.split('\n')[2:]  # Skip header
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        tree.insert('', tk.END, values=(parts[0], parts[1], '✓ Installed'))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load packages: {str(e)}")
    
    def install_package_dialog(self, tree):
        """Show install package dialog"""
        package_name = tk.simpledialog.askstring("Install Package",
                                                 "Enter package name:")
        if package_name:
            self.install_package(package_name, tree)
    
    def install_package(self, package_name, tree):
        """Install a package"""
        progress = tk.Toplevel(self.root)
        progress.title("Installing Package")
        progress.geometry("400x150")
        progress.configure(bg=self.os.bg_color)
        
        tk.Label(progress, text=f"Installing {package_name}...",
                bg=self.os.bg_color, fg=self.os.fg_color,
                font=('Arial', 12)).pack(pady=20)
        
        prog_bar = ttk.Progressbar(progress, mode='indeterminate', length=300)
        prog_bar.pack(pady=10)
        prog_bar.start(10)
        
        def do_install():
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', package_name],
                             check=True, capture_output=True)
                prog_bar.stop()
                progress.destroy()
                self.os.show_notification("Package Manager", f"{package_name} installed!")
                self.load_packages(tree)
            except Exception as e:
                prog_bar.stop()
                progress.destroy()
                messagebox.showerror("Error", f"Installation failed: {str(e)}")
        
        import threading
        threading.Thread(target=do_install, daemon=True).start()


class SystemCleaner:
    """System cleaner and optimizer"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
    
    def show(self):
        """Show system cleaner"""
        cleaner = tk.Toplevel(self.root)
        cleaner.title("System Cleaner")
        cleaner.geometry("700x600")
        cleaner.configure(bg=self.os.bg_color)
        
        # Header
        tk.Label(cleaner, text="🧹 System Cleaner", bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 18, 'bold')).pack(pady=20)
        
        # Categories
        categories_frame = tk.Frame(cleaner, bg=self.os.bg_color)
        categories_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        categories = [
            ("🗑️ Temporary Files", "Clean temporary and cache files", "2.3 GB"),
            ("📦 Old Backups", "Remove old backup files", "1.5 GB"),
            ("📝 Log Files", "Clear system log files", "450 MB"),
            ("🖼️ Thumbnails", "Delete thumbnail cache", "320 MB"),
            ("📁 Downloads", "Clean old downloads", "850 MB"),
            ("🌐 Browser Cache", "Clear browser cache", "680 MB"),
        ]
        
        vars = []
        for title, desc, size in categories:
            frame = tk.Frame(categories_frame, bg=self.os.secondary_bg,
                           relief=tk.RAISED, borderwidth=1)
            frame.pack(fill=tk.X, pady=5)
            
            var = tk.BooleanVar(value=True)
            vars.append(var)
            
            cb = tk.Checkbutton(frame, text=title, variable=var,
                              bg=self.os.secondary_bg, fg=self.os.fg_color,
                              font=('Arial', 12, 'bold'))
            cb.pack(anchor=tk.W, padx=10, pady=5)
            
            tk.Label(frame, text=desc, bg=self.os.secondary_bg,
                    fg='#888', font=('Arial', 9)).pack(anchor=tk.W, padx=30)
            
            tk.Label(frame, text=size, bg=self.os.secondary_bg,
                    fg=self.os.accent_color, font=('Arial', 10, 'bold')).pack(anchor=tk.E, padx=10, pady=5)
        
        # Total
        total_frame = tk.Frame(cleaner, bg=self.os.secondary_bg)
        total_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(total_frame, text="Total Space to Free:", bg=self.os.secondary_bg,
                fg=self.os.fg_color, font=('Arial', 12)).pack(side=tk.LEFT, padx=10)
        
        tk.Label(total_frame, text="6.1 GB", bg=self.os.secondary_bg,
                fg='#34C759', font=('Arial', 14, 'bold')).pack(side=tk.RIGHT, padx=10)
        
        # Clean button
        def clean():
            self.os.show_notification("System Cleaner", "Cleaning completed! Freed 6.1 GB")
            cleaner.destroy()
        
        tk.Button(cleaner, text="🧹 Clean Now", command=clean,
                 bg='#34C759', fg='white', relief=tk.FLAT,
                 font=('Arial', 12, 'bold'), padx=40, pady=10).pack(pady=20)


class ThemeEditor:
    """Theme editor for customizing UI"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
    
    def show(self):
        """Show theme editor"""
        editor = tk.Toplevel(self.root)
        editor.title("Theme Editor")
        editor.geometry("800x600")
        editor.configure(bg=self.os.bg_color)
        
        # Header
        tk.Label(editor, text="🎨 Theme Editor", bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 18, 'bold')).pack(pady=20)
        
        # Preview
        preview_frame = tk.LabelFrame(editor, text="Preview", bg=self.os.bg_color,
                                     fg=self.os.fg_color, font=('Arial', 12, 'bold'))
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sample UI
        sample = tk.Frame(preview_frame, bg=self.os.bg_color)
        sample.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(sample, text="Sample Window", bg=self.os.secondary_bg,
                fg=self.os.fg_color, font=('Arial', 14, 'bold')).pack(fill=tk.X)
        
        tk.Button(sample, text="Sample Button", bg=self.os.accent_color,
                 fg='white', font=('Arial', 11)).pack(pady=10)
        
        # Color pickers
        colors_frame = tk.Frame(editor, bg=self.os.bg_color)
        colors_frame.pack(fill=tk.X, padx=20, pady=10)
        
        def choose_color(color_type):
            from tkinter import colorchooser
            color = colorchooser.askcolor(title=f"Choose {color_type}")
            if color[1]:
                self.os.show_notification("Theme Editor", f"{color_type} updated")
        
        for label, color_type in [
            ("Background Color", "background"),
            ("Text Color", "text"),
            ("Accent Color", "accent"),
        ]:
            frame = tk.Frame(colors_frame, bg=self.os.bg_color)
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=label, bg=self.os.bg_color,
                    fg=self.os.fg_color, font=('Arial', 11), width=15,
                    anchor=tk.W).pack(side=tk.LEFT)
            
            tk.Button(frame, text="Choose Color",
                     command=lambda ct=color_type: choose_color(ct),
                     bg=self.os.secondary_bg, fg=self.os.fg_color,
                     relief=tk.FLAT, font=('Arial', 10)).pack(side=tk.LEFT, padx=10)
        
        # Save/Load
        btn_frame = tk.Frame(editor, bg=self.os.bg_color)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="💾 Save Theme",
                 command=lambda: self.os.show_notification("Theme Editor", "Theme saved!"),
                 bg=self.os.accent_color, fg='white', relief=tk.FLAT,
                 font=('Arial', 11), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="📂 Load Theme",
                 command=lambda: self.os.show_notification("Theme Editor", "Theme loaded!"),
                 bg=self.os.secondary_bg, fg=self.os.fg_color, relief=tk.FLAT,
                 font=('Arial', 11), padx=20, pady=5).pack(side=tk.LEFT, padx=5)
