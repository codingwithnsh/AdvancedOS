"""
Sandbox Dashboard - GUI for creating, managing, and monitoring sandboxes
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
from sandbox_manager import SandboxManager
import threading


class SandboxDashboard:
    """Dashboard for managing sandboxes"""
    
    def __init__(self, root, os_instance):
        self.root = root
        self.os = os_instance
        self.manager = SandboxManager()
        self.refresh_interval = 2000  # ms
        self.auto_refresh = True
    
    def show(self):
        """Show sandbox dashboard"""
        dashboard = tk.Toplevel(self.root)
        dashboard.title("Sandbox Manager")
        dashboard.geometry("1000x700")
        dashboard.configure(bg=self.os.bg_color)
        self.os.open_windows.append(dashboard)
        
        # Header
        header = tk.Frame(dashboard, bg=self.os.secondary_bg, height=60)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="🔒 Sandbox Manager", bg=self.os.secondary_bg,
                fg=self.os.fg_color, font=('Arial', 18, 'bold')).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Toolbar
        toolbar = tk.Frame(header, bg=self.os.secondary_bg)
        toolbar.pack(side=tk.RIGHT, padx=20)
        
        tk.Button(toolbar, text="➕ New Sandbox", 
                 command=lambda: self.create_sandbox_dialog(dashboard),
                 bg=self.os.accent_color, fg='white', relief=tk.FLAT,
                 font=('Arial', 11), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(toolbar, text="🔄 Refresh",
                 command=lambda: self.refresh_sandbox_list(sandbox_list),
                 bg=self.os.secondary_bg, fg=self.os.fg_color, relief=tk.FLAT,
                 font=('Arial', 11), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        # Main content area
        content = tk.Frame(dashboard, bg=self.os.bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sandbox list
        list_frame = tk.Frame(content, bg=self.os.bg_color)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(list_frame, text="Sandboxes", bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 14, 'bold')).pack(anchor=tk.W, pady=5)
        
        # Treeview for sandboxes
        columns = ('Name', 'Type', 'Status', 'CPU%', 'Memory', 'Disk')
        sandbox_list = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            sandbox_list.heading(col, text=col)
            if col == 'Name':
                sandbox_list.column(col, width=150)
            elif col == 'Type':
                sandbox_list.column(col, width=100)
            elif col == 'Status':
                sandbox_list.column(col, width=80)
            else:
                sandbox_list.column(col, width=80)
        
        sandbox_list.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=sandbox_list.yview)
        sandbox_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Control panel
        control_panel = tk.Frame(content, bg=self.os.secondary_bg, width=250)
        control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        tk.Label(control_panel, text="Controls", bg=self.os.secondary_bg,
                fg=self.os.fg_color, font=('Arial', 14, 'bold')).pack(pady=15)
        
        # Control buttons
        def get_selected_sandbox():
            selection = sandbox_list.selection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a sandbox first")
                return None
            
            item = sandbox_list.item(selection[0])
            sandbox_name = item['values'][0]
            
            # Find sandbox by name
            for sb in self.manager.list_sandboxes():
                if sb.name == sandbox_name:
                    return sb
            return None
        
        def start_sandbox():
            sb = get_selected_sandbox()
            if sb and sb.start():
                self.os.show_notification("Sandbox", f"Started {sb.name}")
                self.refresh_sandbox_list(sandbox_list)
        
        def stop_sandbox():
            sb = get_selected_sandbox()
            if sb and sb.stop():
                self.os.show_notification("Sandbox", f"Stopped {sb.name}")
                self.refresh_sandbox_list(sandbox_list)
        
        def pause_sandbox():
            sb = get_selected_sandbox()
            if sb and sb.pause():
                self.os.show_notification("Sandbox", f"Paused {sb.name}")
                self.refresh_sandbox_list(sandbox_list)
        
        def resume_sandbox():
            sb = get_selected_sandbox()
            if sb and sb.resume():
                self.os.show_notification("Sandbox", f"Resumed {sb.name}")
                self.refresh_sandbox_list(sandbox_list)
        
        def delete_sandbox():
            sb = get_selected_sandbox()
            if sb:
                if messagebox.askyesno("Confirm Delete", 
                                      f"Are you sure you want to delete '{sb.name}'?\nAll data will be lost."):
                    if self.manager.delete_sandbox(sb.id):
                        self.os.show_notification("Sandbox", f"Deleted {sb.name}")
                        self.refresh_sandbox_list(sandbox_list)
        
        def view_details():
            sb = get_selected_sandbox()
            if sb:
                self.show_sandbox_details(sb)
        
        def open_terminal():
            sb = get_selected_sandbox()
            if sb:
                self.open_sandbox_terminal(sb)
        
        button_config = {
            'bg': self.os.secondary_bg,
            'fg': self.os.fg_color,
            'relief': tk.FLAT,
            'font': ('Arial', 10),
            'width': 20
        }
        
        tk.Button(control_panel, text="▶️ Start", command=start_sandbox,
                 **button_config).pack(pady=5, padx=10)
        tk.Button(control_panel, text="⏸️ Pause", command=pause_sandbox,
                 **button_config).pack(pady=5, padx=10)
        tk.Button(control_panel, text="▶️ Resume", command=resume_sandbox,
                 **button_config).pack(pady=5, padx=10)
        tk.Button(control_panel, text="⏹️ Stop", command=stop_sandbox,
                 **button_config).pack(pady=5, padx=10)
        
        tk.Frame(control_panel, bg=self.os.secondary_bg, height=20).pack()
        
        tk.Button(control_panel, text="📊 Details", command=view_details,
                 **button_config).pack(pady=5, padx=10)
        tk.Button(control_panel, text="💻 Terminal", command=open_terminal,
                 **button_config).pack(pady=5, padx=10)
        tk.Button(control_panel, text="🗑️ Delete", command=delete_sandbox,
                 bg='#FF3B30', fg='white', relief=tk.FLAT,
                 font=('Arial', 10), width=20).pack(pady=5, padx=10)
        
        # Initial load
        self.refresh_sandbox_list(sandbox_list)
        
        # Auto-refresh
        def auto_refresh_loop():
            if self.auto_refresh and dashboard.winfo_exists():
                self.refresh_sandbox_list(sandbox_list)
                dashboard.after(self.refresh_interval, auto_refresh_loop)
        
        dashboard.after(self.refresh_interval, auto_refresh_loop)
        
        # Cleanup on close
        def on_close():
            self.auto_refresh = False
            dashboard.destroy()
        
        dashboard.protocol("WM_DELETE_WINDOW", on_close)
    
    def refresh_sandbox_list(self, treeview):
        """Refresh the sandbox list"""
        # Clear existing items
        for item in treeview.get_children():
            treeview.delete(item)
        
        # Add sandboxes
        for sb in self.manager.list_sandboxes():
            sb.update_stats()
            
            status_icon = {
                'running': '🟢',
                'paused': '🟡',
                'stopped': '🔴'
            }.get(sb.status, '⚪')
            
            treeview.insert('', tk.END, values=(
                sb.name,
                sb.type.title(),
                f"{status_icon} {sb.status.title()}",
                f"{sb.stats['cpu_usage']:.1f}",
                f"{sb.stats['memory_usage']:.0f} MB",
                f"{sb.stats['disk_usage']:.0f} MB"
            ))
    
    def create_sandbox_dialog(self, parent):
        """Show dialog to create new sandbox"""
        dialog = tk.Toplevel(parent)
        dialog.title("Create New Sandbox")
        dialog.geometry("500x600")
        dialog.configure(bg=self.os.bg_color)
        dialog.transient(parent)
        dialog.grab_set()
        
        tk.Label(dialog, text="Create New Sandbox", bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Name
        name_frame = tk.Frame(dialog, bg=self.os.bg_color)
        name_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(name_frame, text="Name:", bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 11), width=15,
                anchor=tk.W).pack(side=tk.LEFT)
        
        name_var = tk.StringVar(value="My Sandbox")
        name_entry = tk.Entry(name_frame, textvariable=name_var,
                             bg=self.os.secondary_bg, fg=self.os.fg_color,
                             font=('Arial', 11), relief=tk.FLAT)
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        # Template
        template_frame = tk.Frame(dialog, bg=self.os.bg_color)
        template_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(template_frame, text="Template:", bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 11), width=15,
                anchor=tk.W).pack(side=tk.LEFT)
        
        templates = self.manager.get_templates()
        template_var = tk.StringVar(value='general')
        template_combo = ttk.Combobox(template_frame, textvariable=template_var,
                                     values=list(templates.keys()),
                                     state='readonly')
        template_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Template description
        desc_label = tk.Label(dialog, text="", bg=self.os.bg_color,
                             fg=self.os.fg_color, font=('Arial', 9),
                             wraplength=450, justify=tk.LEFT)
        desc_label.pack(pady=5, padx=20)
        
        def update_description(*args):
            template = template_var.get()
            if template in templates:
                desc = templates[template]['description']
                desc_label.config(text=desc)
        
        template_var.trace('w', update_description)
        update_description()
        
        # Resource limits
        limits_frame = tk.LabelFrame(dialog, text="Resource Limits",
                                    bg=self.os.bg_color, fg=self.os.fg_color,
                                    font=('Arial', 11, 'bold'))
        limits_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # CPU limit
        cpu_frame = tk.Frame(limits_frame, bg=self.os.bg_color)
        cpu_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(cpu_frame, text="CPU Limit (%):", bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 10), width=15,
                anchor=tk.W).pack(side=tk.LEFT)
        
        cpu_var = tk.IntVar(value=50)
        cpu_scale = tk.Scale(cpu_frame, from_=1, to=100, orient=tk.HORIZONTAL,
                            variable=cpu_var, bg=self.os.bg_color,
                            fg=self.os.fg_color, font=('Arial', 9),
                            highlightthickness=0)
        cpu_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Memory limit
        mem_frame = tk.Frame(limits_frame, bg=self.os.bg_color)
        mem_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(mem_frame, text="Memory (MB):", bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 10), width=15,
                anchor=tk.W).pack(side=tk.LEFT)
        
        mem_var = tk.IntVar(value=512)
        mem_scale = tk.Scale(mem_frame, from_=128, to=4096, orient=tk.HORIZONTAL,
                            variable=mem_var, bg=self.os.bg_color,
                            fg=self.os.fg_color, font=('Arial', 9),
                            highlightthickness=0)
        mem_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Disk limit
        disk_frame = tk.Frame(limits_frame, bg=self.os.bg_color)
        disk_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(disk_frame, text="Disk (MB):", bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 10), width=15,
                anchor=tk.W).pack(side=tk.LEFT)
        
        disk_var = tk.IntVar(value=1024)
        disk_scale = tk.Scale(disk_frame, from_=256, to=8192, orient=tk.HORIZONTAL,
                             variable=disk_var, bg=self.os.bg_color,
                             fg=self.os.fg_color, font=('Arial', 9),
                             highlightthickness=0)
        disk_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Update limits from template
        def update_limits(*args):
            template = template_var.get()
            if template in templates:
                t = templates[template]
                cpu_var.set(t['cpu_limit'])
                mem_var.set(t['memory_limit'])
                disk_var.set(t['disk_limit'])
        
        template_var.trace('w', update_limits)
        update_limits()
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=self.os.bg_color)
        button_frame.pack(pady=20)
        
        def create():
            name = name_var.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a name")
                return
            
            config = {
                'cpu_limit': cpu_var.get(),
                'memory_limit': mem_var.get(),
                'disk_limit': disk_var.get()
            }
            
            sandbox = self.manager.create_sandbox(name, template_var.get(), config)
            if sandbox:
                self.os.show_notification("Sandbox", f"Created '{name}'")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to create sandbox")
        
        tk.Button(button_frame, text="Create", command=create,
                 bg=self.os.accent_color, fg='white', relief=tk.FLAT,
                 font=('Arial', 11), padx=30, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 bg=self.os.secondary_bg, fg=self.os.fg_color, relief=tk.FLAT,
                 font=('Arial', 11), padx=30, pady=8).pack(side=tk.LEFT, padx=5)
    
    def show_sandbox_details(self, sandbox):
        """Show detailed information about a sandbox"""
        details = tk.Toplevel(self.root)
        details.title(f"Sandbox Details - {sandbox.name}")
        details.geometry("600x500")
        details.configure(bg=self.os.bg_color)
        
        # Header
        tk.Label(details, text=f"📦 {sandbox.name}", bg=self.os.bg_color,
                fg=self.os.fg_color, font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Info
        info_frame = tk.Frame(details, bg=self.os.secondary_bg,
                             relief=tk.RAISED, borderwidth=1)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        info_text = scrolledtext.ScrolledText(info_frame, bg=self.os.secondary_bg,
                                             fg=self.os.fg_color, font=('Courier', 10),
                                             relief=tk.FLAT, wrap=tk.WORD)
        info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Update stats
        sandbox.update_stats()
        
        info = f"""
Sandbox Information
{'=' * 50}

ID:              {sandbox.id}
Name:            {sandbox.name}
Type:            {sandbox.type.title()}
Status:          {sandbox.status.title()}
Created:         {sandbox.created_at}

Resource Limits
{'-' * 50}
CPU Limit:       {sandbox.cpu_limit}%
Memory Limit:    {sandbox.memory_limit} MB
Disk Limit:      {sandbox.disk_limit} MB

Current Usage
{'-' * 50}
CPU Usage:       {sandbox.stats['cpu_usage']:.2f}%
Memory Usage:    {sandbox.stats['memory_usage']:.2f} MB
Disk Usage:      {sandbox.stats['disk_usage']:.2f} MB
Uptime:          {sandbox.stats['uptime']} seconds

Paths
{'-' * 50}
Base:            {sandbox.base_path}
Root:            {sandbox.root_path}
Data:            {sandbox.data_path}

Processes:       {len(sandbox.processes)} running
        """
        
        info_text.insert('1.0', info)
        info_text.config(state='disabled')
        
        # Close button
        tk.Button(details, text="Close", command=details.destroy,
                 bg=self.os.accent_color, fg='white', relief=tk.FLAT,
                 font=('Arial', 11), padx=30, pady=8).pack(pady=10)
    
    def open_sandbox_terminal(self, sandbox):
        """Open terminal in sandbox context"""
        terminal = tk.Toplevel(self.root)
        terminal.title(f"Terminal - {sandbox.name}")
        terminal.geometry("800x500")
        terminal.configure(bg='#000000')
        
        # Output area
        output = scrolledtext.ScrolledText(terminal, bg='#000000', fg='#00FF00',
                                         font=('Courier', 10), insertbackground='#00FF00')
        output.pack(fill=tk.BOTH, expand=True)
        
        # Welcome message
        welcome = f"""Sandbox Terminal - {sandbox.name}
{'=' * 60}
Sandbox ID: {sandbox.id}
Status: {sandbox.status}
Root Path: {sandbox.root_path}

Type 'help' for available commands.
Type 'exit' to close terminal.
"""
        output.insert(tk.END, welcome)
        
        # Input frame
        input_frame = tk.Frame(terminal, bg='#000000')
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        prompt_label = tk.Label(input_frame, text=f"[{sandbox.name}]$",
                               bg='#000000', fg='#00FF00',
                               font=('Courier', 10))
        prompt_label.pack(side=tk.LEFT, padx=5)
        
        command_var = tk.StringVar()
        command_entry = tk.Entry(input_frame, textvariable=command_var,
                                bg='#000000', fg='#00FF00',
                                font=('Courier', 10),
                                insertbackground='#00FF00', relief=tk.FLAT)
        command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        command_entry.focus()
        
        def execute_command(event=None):
            command = command_var.get().strip()
            if command:
                output.insert(tk.END, f"\n[{sandbox.name}]$ {command}\n")
                
                if command == 'exit':
                    terminal.destroy()
                    return
                elif command == 'help':
                    help_text = """
Available commands:
  help     - Show this help
  info     - Show sandbox info
  status   - Show sandbox status
  start    - Start sandbox
  stop     - Stop sandbox
  exit     - Close terminal
                    """
                    output.insert(tk.END, help_text + "\n")
                elif command == 'info':
                    info = f"Sandbox: {sandbox.name} ({sandbox.id})\nType: {sandbox.type}\n"
                    output.insert(tk.END, info + "\n")
                elif command == 'status':
                    sandbox.update_stats()
                    status = f"Status: {sandbox.status}\nCPU: {sandbox.stats['cpu_usage']}%\n"
                    status += f"Memory: {sandbox.stats['memory_usage']} MB\n"
                    output.insert(tk.END, status + "\n")
                elif command == 'start':
                    if sandbox.start():
                        output.insert(tk.END, "Sandbox started\n")
                    else:
                        output.insert(tk.END, "Failed to start sandbox\n")
                elif command == 'stop':
                    if sandbox.stop():
                        output.insert(tk.END, "Sandbox stopped\n")
                    else:
                        output.insert(tk.END, "Failed to stop sandbox\n")
                else:
                    output.insert(tk.END, f"Unknown command: {command}\n")
                
                output.see(tk.END)
                command_var.set("")
        
        command_entry.bind('<Return>', execute_command)
