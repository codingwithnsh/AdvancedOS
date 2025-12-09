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
        dashboard.title("Sandbox Manager - Virtual Machine Dashboard")
        dashboard.geometry("1200x750")
        dashboard.configure(bg='#1a1a1a' if self.os.theme_mode == 'dark' else '#f5f5f5')
        self.os.open_windows.append(dashboard)
        
        # Modern header with gradient effect simulation
        header = tk.Frame(dashboard, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Title section
        title_frame = tk.Frame(header, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff')
        title_frame.pack(side=tk.LEFT, padx=30, pady=20)
        
        tk.Label(title_frame, text="🔒 Sandbox Manager", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                font=('Arial', 22, 'bold')).pack(anchor=tk.W)
        
        tk.Label(title_frame, text="Create and manage isolated virtual environments", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#888888',
                font=('Arial', 10)).pack(anchor=tk.W)
        
        # Toolbar with modern buttons
        toolbar = tk.Frame(header, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff')
        toolbar.pack(side=tk.RIGHT, padx=30, pady=20)
        
        # New Sandbox button with enhanced styling
        new_btn = tk.Button(toolbar, text="➕ Create New Sandbox", 
                 command=lambda: self.create_sandbox_dialog(dashboard),
                 bg='#007acc', fg='white', relief=tk.FLAT,
                 font=('Arial', 11, 'bold'), padx=20, pady=10,
                 cursor='hand2', activebackground='#005a9e')
        new_btn.pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        refresh_btn = tk.Button(toolbar, text="🔄 Refresh",
                 command=lambda: self.refresh_sandbox_list(sandbox_list),
                 bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#e0e0e0', 
                 fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                 relief=tk.FLAT,
                 font=('Arial', 11), padx=15, pady=10,
                 cursor='hand2')
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Statistics bar
        stats_frame = tk.Frame(dashboard, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#e8e8e8', height=60)
        stats_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        stats_frame.pack_propagate(False)
        
        # Count total sandboxes
        total_sandboxes = len(self.manager.list_sandboxes())
        running_sandboxes = sum(1 for sb in self.manager.list_sandboxes() if sb.status == 'running')
        stopped_sandboxes = sum(1 for sb in self.manager.list_sandboxes() if sb.status == 'stopped')
        paused_sandboxes = sum(1 for sb in self.manager.list_sandboxes() if sb.status == 'paused')
        
        # Stats cards
        def create_stat_card(parent, title, value, color):
            card = tk.Frame(parent, bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#ffffff', 
                          relief=tk.FLAT, bd=1)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)
            
            tk.Label(card, text=str(value), bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#ffffff',
                    fg=color, font=('Arial', 20, 'bold')).pack(pady=(10, 0))
            tk.Label(card, text=title, bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#ffffff',
                    fg='#888888', font=('Arial', 9)).pack(pady=(0, 10))
        
        create_stat_card(stats_frame, 'Total Sandboxes', total_sandboxes, '#007acc')
        create_stat_card(stats_frame, 'Running', running_sandboxes, '#4ec9b0')
        create_stat_card(stats_frame, 'Stopped', stopped_sandboxes, '#ce9178')
        create_stat_card(stats_frame, 'Paused', paused_sandboxes, '#dcdcaa')
        
        # Main content area
        content = tk.Frame(dashboard, bg='#1a1a1a' if self.os.theme_mode == 'dark' else '#f5f5f5')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sandbox list with enhanced styling
        list_frame = tk.Frame(content, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff', 
                             relief=tk.FLAT, bd=1)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # List header
        list_header = tk.Frame(list_frame, bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#f0f0f0', height=40)
        list_header.pack(fill=tk.X)
        list_header.pack_propagate(False)
        
        tk.Label(list_header, text="Virtual Machines", 
                bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#f0f0f0',
                fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=15, pady=10)
        
        # Treeview for sandboxes with better styling
        tree_frame = tk.Frame(list_frame, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('Name', 'Type', 'Status', 'CPU%', 'Memory', 'Disk')
        sandbox_list = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configure column widths and headings
        for col in columns:
            sandbox_list.heading(col, text=col)
            if col == 'Name':
                sandbox_list.column(col, width=180)
            elif col == 'Type':
                sandbox_list.column(col, width=120)
            elif col == 'Status':
                sandbox_list.column(col, width=100)
            else:
                sandbox_list.column(col, width=90)
        
        sandbox_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=sandbox_list.yview)
        sandbox_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enhanced control panel
        control_panel = tk.Frame(content, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff', 
                                width=280, relief=tk.FLAT, bd=1)
        control_panel.pack(side=tk.RIGHT, fill=tk.Y)
        control_panel.pack_propagate(False)
        
        # Control panel header
        cp_header = tk.Frame(control_panel, bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#f0f0f0', height=40)
        cp_header.pack(fill=tk.X)
        cp_header.pack_propagate(False)
        
        tk.Label(cp_header, text="Controls", 
                bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#f0f0f0',
                fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Control buttons section
        controls_content = tk.Frame(control_panel, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff')
        controls_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
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
            if sb:
                if sb.start():
                    self.os.show_notification("Sandbox Manager", f"✅ Started '{sb.name}'")
                    self.refresh_sandbox_list(sandbox_list)
                else:
                    messagebox.showerror("Error", f"Failed to start sandbox '{sb.name}'")
        
        def stop_sandbox():
            sb = get_selected_sandbox()
            if sb:
                if sb.stop():
                    self.os.show_notification("Sandbox Manager", f"⏹️ Stopped '{sb.name}'")
                    self.refresh_sandbox_list(sandbox_list)
                else:
                    messagebox.showerror("Error", f"Failed to stop sandbox '{sb.name}'")
        
        def pause_sandbox():
            sb = get_selected_sandbox()
            if sb:
                if sb.pause():
                    self.os.show_notification("Sandbox Manager", f"⏸️ Paused '{sb.name}'")
                    self.refresh_sandbox_list(sandbox_list)
                else:
                    messagebox.showerror("Error", f"Failed to pause sandbox '{sb.name}'")
        
        def resume_sandbox():
            sb = get_selected_sandbox()
            if sb:
                if sb.resume():
                    self.os.show_notification("Sandbox Manager", f"▶️ Resumed '{sb.name}'")
                    self.refresh_sandbox_list(sandbox_list)
                else:
                    messagebox.showerror("Error", f"Failed to resume sandbox '{sb.name}'")
        
        def delete_sandbox():
            sb = get_selected_sandbox()
            if sb:
                if messagebox.askyesno("Confirm Delete", 
                                      f"Are you sure you want to delete '{sb.name}'?\n\n⚠️ All data will be permanently lost!"):
                    if self.manager.delete_sandbox(sb.id):
                        self.os.show_notification("Sandbox Manager", f"🗑️ Deleted '{sb.name}'")
                        self.refresh_sandbox_list(sandbox_list)
                    else:
                        messagebox.showerror("Error", f"Failed to delete sandbox '{sb.name}'")
        
        def view_details():
            sb = get_selected_sandbox()
            if sb:
                self.show_sandbox_details(sb)
        
        def open_terminal():
            sb = get_selected_sandbox()
            if sb:
                self.open_sandbox_terminal(sb)
        
        # Modern button styling
        button_style = {
            'relief': tk.FLAT,
            'font': ('Arial', 10),
            'width': 22,
            'pady': 10,
            'cursor': 'hand2'
        }
        
        # Lifecycle controls
        tk.Label(controls_content, text="Lifecycle", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#888888',
                font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(5, 10))
        
        start_btn = tk.Button(controls_content, text="▶️ Start", command=start_sandbox,
                 bg='#4ec9b0', fg='white', **button_style)
        start_btn.pack(pady=3)
        
        pause_btn = tk.Button(controls_content, text="⏸️ Pause", command=pause_sandbox,
                 bg='#dcdcaa', fg='#1a1a1a', **button_style)
        pause_btn.pack(pady=3)
        
        resume_btn = tk.Button(controls_content, text="▶️ Resume", command=resume_sandbox,
                 bg='#4ec9b0', fg='white', **button_style)
        resume_btn.pack(pady=3)
        
        stop_btn = tk.Button(controls_content, text="⏹️ Stop", command=stop_sandbox,
                 bg='#ce9178', fg='white', **button_style)
        stop_btn.pack(pady=3)
        
        # Separator
        tk.Frame(controls_content, bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#e0e0e0', 
                height=1).pack(fill=tk.X, pady=15)
        
        # Management controls
        tk.Label(controls_content, text="Management", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#888888',
                font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(5, 10))
        
        details_btn = tk.Button(controls_content, text="📊 View Details", command=view_details,
                 bg='#007acc', fg='white', **button_style)
        details_btn.pack(pady=3)
        
        terminal_btn = tk.Button(controls_content, text="💻 Open Terminal", command=open_terminal,
                 bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#5a5a5a', 
                 fg='white', **button_style)
        terminal_btn.pack(pady=3)
        
        # Separator
        tk.Frame(controls_content, bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#e0e0e0', 
                height=1).pack(fill=tk.X, pady=15)
        
        # Danger zone
        tk.Label(controls_content, text="Danger Zone", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#f48771',
                font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(5, 10))
        
        delete_btn = tk.Button(controls_content, text="🗑️ Delete Sandbox", command=delete_sandbox,
                 bg='#f14c4c', fg='white', **button_style)
        delete_btn.pack(pady=3)
        
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
        dialog.title("Create New Virtual Machine")
        dialog.geometry("600x700")
        dialog.configure(bg='#1a1a1a' if self.os.theme_mode == 'dark' else '#f5f5f5')
        dialog.transient(parent)
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="Create New Virtual Machine", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                font=('Arial', 18, 'bold')).pack(pady=(20, 5))
        
        tk.Label(header, text="Configure your isolated sandbox environment", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#888888',
                font=('Arial', 10)).pack()
        
        # Content area
        content = tk.Frame(dialog, bg='#1a1a1a' if self.os.theme_mode == 'dark' else '#f5f5f5')
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Name section
        name_section = tk.Frame(content, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                               relief=tk.FLAT, bd=1)
        name_section.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(name_section, text="Machine Name", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        name_var = tk.StringVar(value="My Sandbox")
        name_entry = tk.Entry(name_section, textvariable=name_var,
                             bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#ffffff',
                             fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                             font=('Arial', 11), relief=tk.FLAT, bd=1)
        name_entry.pack(fill=tk.X, padx=20, pady=(0, 15), ipady=8)
        
        # Template section
        template_section = tk.Frame(content, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                                   relief=tk.FLAT, bd=1)
        template_section.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(template_section, text="Template", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        templates = self.manager.get_templates()
        template_var = tk.StringVar(value='general')
        
        # Template buttons grid
        template_grid = tk.Frame(template_section, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff')
        template_grid.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        template_buttons = []
        template_icons = {
            'general': '🔧',
            'development': '💻',
            'testing': '🧪',
            'lightweight': '⚡',
            'heavy': '🚀'
        }
        
        row, col = 0, 0
        for template_id, template_info in templates.items():
            btn_frame = tk.Frame(template_grid, bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#e8e8e8',
                                relief=tk.FLAT, bd=1, cursor='hand2')
            btn_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            icon = template_icons.get(template_id, '📦')
            tk.Label(btn_frame, text=icon, 
                    bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#e8e8e8',
                    font=('Arial', 24)).pack(pady=(10, 5))
            
            tk.Label(btn_frame, text=template_info['name'], 
                    bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#e8e8e8',
                    fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                    font=('Arial', 9, 'bold')).pack()
            
            tk.Label(btn_frame, text=f"CPU: {template_info['cpu_limit']}%", 
                    bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#e8e8e8',
                    fg='#888888',
                    font=('Arial', 8)).pack()
            
            tk.Label(btn_frame, text=f"RAM: {template_info['memory_limit']}MB", 
                    bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#e8e8e8',
                    fg='#888888',
                    font=('Arial', 8)).pack(pady=(0, 10))
            
            def select_template(tid=template_id, frame=btn_frame):
                template_var.set(tid)
                # Highlight selected
                for btn in template_buttons:
                    btn.config(bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#e8e8e8')
                frame.config(bg='#007acc')
                update_description()
                update_limits()
            
            btn_frame.bind('<Button-1>', lambda e, tid=template_id, frame=btn_frame: select_template(tid, frame))
            for child in btn_frame.winfo_children():
                child.bind('<Button-1>', lambda e, tid=template_id, frame=btn_frame: select_template(tid, frame))
            
            template_buttons.append(btn_frame)
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        for i in range(3):
            template_grid.columnconfigure(i, weight=1, uniform='template')
        
        # Template description
        desc_label = tk.Label(template_section, text="", 
                             bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                             fg='#888888',
                             font=('Arial', 9), wraplength=520, justify=tk.LEFT)
        desc_label.pack(pady=(0, 15), padx=20)
        
        def update_description(*args):
            template = template_var.get()
            if template in templates:
                desc = templates[template]['description']
                desc_label.config(text=desc)
        
        update_description()
        
        # Resource limits
        limits_frame = tk.Frame(content, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                               relief=tk.FLAT, bd=1)
        limits_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(limits_frame, text="Resource Limits", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        # CPU limit
        cpu_frame = tk.Frame(limits_frame, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff')
        cpu_frame.pack(fill=tk.X, padx=20, pady=5)
        
        cpu_label_frame = tk.Frame(cpu_frame, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff')
        cpu_label_frame.pack(fill=tk.X)
        
        tk.Label(cpu_label_frame, text="CPU Limit", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        cpu_var = tk.IntVar(value=50)
        cpu_value_label = tk.Label(cpu_label_frame, text="50%", 
                                   bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                                   fg='#007acc',
                                   font=('Arial', 10, 'bold'))
        cpu_value_label.pack(side=tk.RIGHT)
        
        cpu_scale = tk.Scale(cpu_frame, from_=1, to=100, orient=tk.HORIZONTAL,
                            variable=cpu_var, 
                            bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                            fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                            font=('Arial', 9), highlightthickness=0, showvalue=False,
                            troughcolor='#3c3c3c' if self.os.theme_mode == 'dark' else '#d0d0d0',
                            command=lambda v: cpu_value_label.config(text=f"{int(float(v))}%"))
        cpu_scale.pack(fill=tk.X, pady=(0, 5))
        
        # Memory limit
        mem_frame = tk.Frame(limits_frame, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff')
        mem_frame.pack(fill=tk.X, padx=20, pady=5)
        
        mem_label_frame = tk.Frame(mem_frame, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff')
        mem_label_frame.pack(fill=tk.X)
        
        tk.Label(mem_label_frame, text="Memory Limit", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        mem_var = tk.IntVar(value=512)
        mem_value_label = tk.Label(mem_label_frame, text="512 MB", 
                                   bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                                   fg='#4ec9b0',
                                   font=('Arial', 10, 'bold'))
        mem_value_label.pack(side=tk.RIGHT)
        
        mem_scale = tk.Scale(mem_frame, from_=128, to=4096, orient=tk.HORIZONTAL,
                            variable=mem_var, 
                            bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                            fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                            font=('Arial', 9), highlightthickness=0, showvalue=False,
                            troughcolor='#3c3c3c' if self.os.theme_mode == 'dark' else '#d0d0d0',
                            command=lambda v: mem_value_label.config(text=f"{int(float(v))} MB"))
        mem_scale.pack(fill=tk.X, pady=(0, 5))
        
        # Disk limit
        disk_frame = tk.Frame(limits_frame, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff')
        disk_frame.pack(fill=tk.X, padx=20, pady=(5, 15))
        
        disk_label_frame = tk.Frame(disk_frame, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff')
        disk_label_frame.pack(fill=tk.X)
        
        tk.Label(disk_label_frame, text="Disk Limit", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        disk_var = tk.IntVar(value=1024)
        disk_value_label = tk.Label(disk_label_frame, text="1024 MB", 
                                    bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                                    fg='#dcdcaa',
                                    font=('Arial', 10, 'bold'))
        disk_value_label.pack(side=tk.RIGHT)
        
        disk_scale = tk.Scale(disk_frame, from_=256, to=8192, orient=tk.HORIZONTAL,
                             variable=disk_var, 
                             bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                             fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                             font=('Arial', 9), highlightthickness=0, showvalue=False,
                             troughcolor='#3c3c3c' if self.os.theme_mode == 'dark' else '#d0d0d0',
                             command=lambda v: disk_value_label.config(text=f"{int(float(v))} MB"))
        disk_scale.pack(fill=tk.X)
        
        # Update limits from template
        def update_limits(*args):
            template = template_var.get()
            if template in templates:
                t = templates[template]
                cpu_var.set(t['cpu_limit'])
                mem_var.set(t['memory_limit'])
                disk_var.set(t['disk_limit'])
        
        update_limits()
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='#1a1a1a' if self.os.theme_mode == 'dark' else '#f5f5f5')
        button_frame.pack(pady=(0, 20))
        
        status_label = tk.Label(button_frame, text="", 
                               bg='#1a1a1a' if self.os.theme_mode == 'dark' else '#f5f5f5',
                               fg='#888888',
                               font=('Arial', 9))
        status_label.pack(pady=(0, 10))
        
        def create():
            name = name_var.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a machine name")
                return
            
            # Show creating status
            status_label.config(text="Creating virtual machine...", fg='#007acc')
            dialog.update()
            
            config = {
                'cpu_limit': cpu_var.get(),
                'memory_limit': mem_var.get(),
                'disk_limit': disk_var.get()
            }
            
            try:
                sandbox = self.manager.create_sandbox(name, template_var.get(), config)
                if sandbox:
                    status_label.config(text="✅ Virtual machine created successfully!", fg='#4ec9b0')
                    dialog.update()
                    self.os.show_notification("Sandbox Manager", 
                                             f"✅ Created new sandbox '{name}'")
                    # Wait a moment for user to see success message
                    dialog.after(1000, dialog.destroy)
                else:
                    status_label.config(text="❌ Failed to create virtual machine", fg='#f14c4c')
                    messagebox.showerror("Error", "Failed to create sandbox. Please check logs.")
            except Exception as e:
                status_label.config(text=f"❌ Error: {str(e)}", fg='#f14c4c')
                messagebox.showerror("Error", f"Failed to create sandbox: {str(e)}")
        
        btn_frame = tk.Frame(button_frame, bg='#1a1a1a' if self.os.theme_mode == 'dark' else '#f5f5f5')
        btn_frame.pack()
        
        create_btn = tk.Button(btn_frame, text="Create Virtual Machine", command=create,
                 bg='#007acc', fg='white', relief=tk.FLAT,
                 font=('Arial', 11, 'bold'), padx=30, pady=12,
                 cursor='hand2', activebackground='#005a9e')
        create_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                 bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#d0d0d0',
                 fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                 relief=tk.FLAT,
                 font=('Arial', 11), padx=30, pady=12,
                 cursor='hand2')
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def show_sandbox_details(self, sandbox):
        """Show detailed information about a sandbox"""
        details = tk.Toplevel(self.root)
        details.title(f"Sandbox Details - {sandbox.name}")
        details.geometry("700x600")
        details.configure(bg='#1a1a1a' if self.os.theme_mode == 'dark' else '#f5f5f5')
        
        # Header
        header = tk.Frame(details, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text=f"📦 {sandbox.name}", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                font=('Arial', 18, 'bold')).pack(pady=(20, 5))
        
        # Status badge
        status_colors = {
            'running': '#4ec9b0',
            'paused': '#dcdcaa',
            'stopped': '#ce9178'
        }
        status_color = status_colors.get(sandbox.status, '#888888')
        
        tk.Label(header, text=f"● {sandbox.status.upper()}", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg=status_color,
                font=('Arial', 11, 'bold')).pack()
        
        # Content area
        content = tk.Frame(details, bg='#1a1a1a' if self.os.theme_mode == 'dark' else '#f5f5f5')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Update stats
        sandbox.update_stats()
        
        # Resource usage cards
        resources_frame = tk.Frame(content, bg='#1a1a1a' if self.os.theme_mode == 'dark' else '#f5f5f5')
        resources_frame.pack(fill=tk.X, pady=(0, 15))
        
        def create_resource_card(parent, title, current, limit, color):
            card = tk.Frame(parent, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                          relief=tk.FLAT, bd=1)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            tk.Label(card, text=title, 
                    bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                    fg='#888888',
                    font=('Arial', 9)).pack(pady=(15, 5))
            
            tk.Label(card, text=str(current), 
                    bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                    fg=color,
                    font=('Arial', 20, 'bold')).pack()
            
            tk.Label(card, text=f"of {limit}", 
                    bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                    fg='#888888',
                    font=('Arial', 9)).pack(pady=(0, 15))
        
        create_resource_card(resources_frame, 'CPU Usage', 
                           f"{sandbox.stats['cpu_usage']:.1f}%",
                           f"{sandbox.cpu_limit}%", '#007acc')
        
        create_resource_card(resources_frame, 'Memory Usage', 
                           f"{sandbox.stats['memory_usage']:.0f} MB",
                           f"{sandbox.memory_limit} MB", '#4ec9b0')
        
        create_resource_card(resources_frame, 'Disk Usage', 
                           f"{sandbox.stats['disk_usage']:.0f} MB",
                           f"{sandbox.disk_limit} MB", '#dcdcaa')
        
        # Info section
        info_frame = tk.Frame(content, bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                             relief=tk.FLAT, bd=1)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Info header
        tk.Label(info_frame, text="Detailed Information", 
                bg='#2d2d30' if self.os.theme_mode == 'dark' else '#ffffff',
                fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        info_text = scrolledtext.ScrolledText(info_frame, 
                                             bg='#3c3c3c' if self.os.theme_mode == 'dark' else '#f5f5f5',
                                             fg='#ffffff' if self.os.theme_mode == 'dark' else '#1a1a1a',
                                             font=('Courier', 10),
                                             relief=tk.FLAT, wrap=tk.WORD)
        info_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        info = f"""
╔═══════════════════════════════════════════════════════╗
║              SANDBOX INFORMATION                      ║
╚═══════════════════════════════════════════════════════╝

🆔 Sandbox ID:     {sandbox.id}
📛 Name:            {sandbox.name}
🏷️  Type:            {sandbox.type.title()}
📅 Created:         {sandbox.created_at}

╔═══════════════════════════════════════════════════════╗
║              RESOURCE LIMITS                          ║
╚═══════════════════════════════════════════════════════╝

💻 CPU Limit:       {sandbox.cpu_limit}%
🧠 Memory Limit:    {sandbox.memory_limit} MB
💾 Disk Limit:      {sandbox.disk_limit} MB

╔═══════════════════════════════════════════════════════╗
║              CURRENT USAGE                            ║
╚═══════════════════════════════════════════════════════╝

📊 CPU Usage:       {sandbox.stats['cpu_usage']:.2f}%
🧠 Memory Usage:    {sandbox.stats['memory_usage']:.2f} MB
💾 Disk Usage:      {sandbox.stats['disk_usage']:.2f} MB
⏱️  Uptime:          {sandbox.stats['uptime']} seconds

╔═══════════════════════════════════════════════════════╗
║              FILE SYSTEM PATHS                        ║
╚═══════════════════════════════════════════════════════╝

📁 Base Directory:  {sandbox.base_path}
🗂️  Root Directory:  {sandbox.root_path}
💼 Data Directory:  {sandbox.data_path}

╔═══════════════════════════════════════════════════════╗
║              PROCESS INFORMATION                      ║
╚═══════════════════════════════════════════════════════╝

🔢 Running Processes: {len(sandbox.processes)}
        """
        
        info_text.insert('1.0', info)
        info_text.config(state='disabled')
        
        # Close button
        tk.Button(details, text="Close", command=details.destroy,
                 bg='#007acc', fg='white', relief=tk.FLAT,
                 font=('Arial', 11), padx=30, pady=10,
                 cursor='hand2').pack(pady=(0, 20))
    
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
