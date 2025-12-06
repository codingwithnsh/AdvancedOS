"""
Sandbox Manager - Isolated execution environments for AdvancedOS
Provides secure, isolated sandboxes for running applications and managing resources
"""

import os
import json
import shutil
import subprocess
import threading
import time
import uuid
from pathlib import Path
from datetime import datetime
import psutil


class Sandbox:
    """Represents an isolated sandbox environment"""
    
    def __init__(self, sandbox_id, name, sandbox_type="general", config=None):
        self.id = sandbox_id
        self.name = name
        self.type = sandbox_type
        self.created_at = datetime.now().isoformat()
        self.status = "stopped"  # stopped, running, paused
        self.processes = []
        self.config = config or {}
        
        # Resource limits
        self.cpu_limit = self.config.get('cpu_limit', 50)  # percentage
        self.memory_limit = self.config.get('memory_limit', 512)  # MB
        self.disk_limit = self.config.get('disk_limit', 1024)  # MB
        
        # Sandbox directory structure
        self.base_path = Path.home() / '.advancedos' / 'sandboxes' / self.id
        self.root_path = self.base_path / 'root'
        self.data_path = self.base_path / 'data'
        self.config_path = self.base_path / 'config.json'
        
        # Statistics
        self.stats = {
            'cpu_usage': 0,
            'memory_usage': 0,
            'disk_usage': 0,
            'uptime': 0,
            'last_started': None
        }
    
    def create(self):
        """Create sandbox directory structure"""
        try:
            # Create directories
            self.base_path.mkdir(parents=True, exist_ok=True)
            self.root_path.mkdir(exist_ok=True)
            self.data_path.mkdir(exist_ok=True)
            
            # Create subdirectories
            for subdir in ['bin', 'home', 'tmp', 'lib', 'usr', 'var']:
                (self.root_path / subdir).mkdir(exist_ok=True)
            
            # Save configuration
            self.save_config()
            
            return True
        except (OSError, PermissionError) as e:
            print(f"Error creating sandbox: {e}")
            return False
    
    def start(self):
        """Start the sandbox"""
        if self.status == "running":
            return False
        
        try:
            self.status = "running"
            self.stats['last_started'] = datetime.now().isoformat()
            self.save_config()
            return True
        except (OSError, IOError) as e:
            print(f"Error starting sandbox: {e}")
            return False
    
    def stop(self):
        """Stop the sandbox"""
        if self.status != "running":
            return False
        
        try:
            # Kill all processes in sandbox
            for proc in self.processes[:]:
                try:
                    proc.terminate()
                    proc.wait(timeout=3)
                except (subprocess.TimeoutExpired, ProcessLookupError):
                    try:
                        proc.kill()
                    except (ProcessLookupError, PermissionError):
                        pass
                finally:
                    if proc in self.processes:
                        self.processes.remove(proc)
            
            self.status = "stopped"
            self.save_config()
            return True
        except (OSError, IOError, ProcessLookupError) as e:
            print(f"Error stopping sandbox: {e}")
            return False
    
    def pause(self):
        """Pause the sandbox"""
        if self.status != "running":
            return False
        
        try:
            # Pause all processes
            for proc in self.processes:
                try:
                    proc.suspend()
                except (AttributeError, ProcessLookupError, PermissionError):
                    pass
            
            self.status = "paused"
            self.save_config()
            return True
        except (OSError, IOError) as e:
            print(f"Error pausing sandbox: {e}")
            return False
    
    def resume(self):
        """Resume the sandbox"""
        if self.status != "paused":
            return False
        
        try:
            # Resume all processes
            for proc in self.processes:
                try:
                    proc.resume()
                except (AttributeError, ProcessLookupError, PermissionError):
                    pass
            
            self.status = "running"
            self.save_config()
            return True
        except (OSError, IOError) as e:
            print(f"Error resuming sandbox: {e}")
            return False
    
    def delete(self):
        """Delete the sandbox and all its data"""
        try:
            # Stop sandbox first
            self.stop()
            
            # Remove sandbox directory
            if self.base_path.exists():
                shutil.rmtree(self.base_path)
            
            return True
        except Exception as e:
            print(f"Error deleting sandbox: {e}")
            return False
    
    def execute_command(self, command, args=None):
        """Execute a command within the sandbox"""
        if self.status != "running":
            return None
        
        try:
            # Change to sandbox root directory
            cwd = str(self.root_path)
            
            # Create environment variables
            env = os.environ.copy()
            env['SANDBOX_ID'] = self.id
            env['SANDBOX_NAME'] = self.name
            env['SANDBOX_ROOT'] = str(self.root_path)
            
            # Execute command
            if args:
                full_command = [command] + args
            else:
                full_command = command.split()
            
            proc = subprocess.Popen(
                full_command,
                cwd=cwd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.processes.append(proc)
            return proc
        except Exception as e:
            print(f"Error executing command: {e}")
            return None
    
    def update_stats(self):
        """Update sandbox resource usage statistics"""
        try:
            total_cpu = 0
            total_memory = 0
            
            # Calculate resource usage from processes
            for proc in self.processes[:]:
                try:
                    p = psutil.Process(proc.pid)
                    total_cpu += p.cpu_percent(interval=0.1)
                    total_memory += p.memory_info().rss / (1024 * 1024)  # MB
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    if proc in self.processes:
                        self.processes.remove(proc)
            
            self.stats['cpu_usage'] = round(total_cpu, 2)
            self.stats['memory_usage'] = round(total_memory, 2)
            
            # Calculate disk usage
            if self.base_path.exists():
                disk_usage = sum(f.stat().st_size for f in self.base_path.rglob('*') if f.is_file())
                self.stats['disk_usage'] = round(disk_usage / (1024 * 1024), 2)  # MB
            
            # Calculate uptime
            if self.stats['last_started']:
                start_time = datetime.fromisoformat(self.stats['last_started'])
                uptime = (datetime.now() - start_time).total_seconds()
                self.stats['uptime'] = int(uptime)
            
        except Exception as e:
            print(f"Error updating stats: {e}")
    
    def save_config(self):
        """Save sandbox configuration to file"""
        try:
            config = {
                'id': self.id,
                'name': self.name,
                'type': self.type,
                'created_at': self.created_at,
                'status': self.status,
                'config': self.config,
                'stats': self.stats,
                'cpu_limit': self.cpu_limit,
                'memory_limit': self.memory_limit,
                'disk_limit': self.disk_limit
            }
            
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def to_dict(self):
        """Convert sandbox to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'created_at': self.created_at,
            'status': self.status,
            'stats': self.stats,
            'cpu_limit': self.cpu_limit,
            'memory_limit': self.memory_limit,
            'disk_limit': self.disk_limit
        }


class SandboxManager:
    """Manages multiple sandboxes"""
    
    def __init__(self):
        self.sandboxes = {}
        self.base_path = Path.home() / '.advancedos' / 'sandboxes'
        self.config_file = Path.home() / '.advancedos' / 'sandbox_manager.json'
        
        # Create base directory
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing sandboxes
        self.load_sandboxes()
        
        # Start monitoring thread
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_sandboxes, daemon=True)
        self.monitor_thread.start()
    
    def create_sandbox(self, name, sandbox_type="general", config=None):
        """Create a new sandbox"""
        try:
            # Generate unique ID
            sandbox_id = str(uuid.uuid4())[:8]
            
            # Create sandbox object
            sandbox = Sandbox(sandbox_id, name, sandbox_type, config)
            
            # Create sandbox structure
            if not sandbox.create():
                return None
            
            # Add to manager
            self.sandboxes[sandbox_id] = sandbox
            
            # Save configuration
            self.save_config()
            
            return sandbox
        except Exception as e:
            print(f"Error creating sandbox: {e}")
            return None
    
    def get_sandbox(self, sandbox_id):
        """Get sandbox by ID"""
        return self.sandboxes.get(sandbox_id)
    
    def list_sandboxes(self):
        """List all sandboxes"""
        return list(self.sandboxes.values())
    
    def delete_sandbox(self, sandbox_id):
        """Delete a sandbox"""
        try:
            sandbox = self.sandboxes.get(sandbox_id)
            if not sandbox:
                return False
            
            # Delete sandbox
            if sandbox.delete():
                del self.sandboxes[sandbox_id]
                self.save_config()
                return True
            
            return False
        except Exception as e:
            print(f"Error deleting sandbox: {e}")
            return False
    
    def load_sandboxes(self):
        """Load sandboxes from disk"""
        try:
            # Scan sandbox directories
            if self.base_path.exists():
                for sandbox_dir in self.base_path.iterdir():
                    if sandbox_dir.is_dir():
                        config_file = sandbox_dir / 'config.json'
                        if config_file.exists():
                            try:
                                with open(config_file, 'r') as f:
                                    config = json.load(f)
                                
                                sandbox = Sandbox(
                                    config['id'],
                                    config['name'],
                                    config.get('type', 'general'),
                                    config.get('config', {})
                                )
                                sandbox.created_at = config.get('created_at', sandbox.created_at)
                                sandbox.status = 'stopped'  # Always start as stopped
                                sandbox.stats = config.get('stats', sandbox.stats)
                                sandbox.cpu_limit = config.get('cpu_limit', 50)
                                sandbox.memory_limit = config.get('memory_limit', 512)
                                sandbox.disk_limit = config.get('disk_limit', 1024)
                                
                                self.sandboxes[sandbox.id] = sandbox
                            except Exception as e:
                                print(f"Error loading sandbox {sandbox_dir}: {e}")
        except Exception as e:
            print(f"Error loading sandboxes: {e}")
    
    def save_config(self):
        """Save manager configuration"""
        try:
            config = {
                'sandboxes': [sb.id for sb in self.sandboxes.values()],
                'updated_at': datetime.now().isoformat()
            }
            
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def _monitor_sandboxes(self):
        """Monitor sandboxes in background"""
        while self.monitoring:
            try:
                for sandbox in self.sandboxes.values():
                    if sandbox.status == "running":
                        sandbox.update_stats()
                        
                        # Check resource limits
                        if sandbox.stats['cpu_usage'] > sandbox.cpu_limit:
                            print(f"Sandbox {sandbox.name} exceeded CPU limit")
                        
                        if sandbox.stats['memory_usage'] > sandbox.memory_limit:
                            print(f"Sandbox {sandbox.name} exceeded memory limit")
                        
                        if sandbox.stats['disk_usage'] > sandbox.disk_limit:
                            print(f"Sandbox {sandbox.name} exceeded disk limit")
                
                time.sleep(2)
            except Exception as e:
                print(f"Error in monitor: {e}")
                time.sleep(5)
    
    def stop_monitoring(self):
        """Stop the monitoring thread"""
        self.monitoring = False
        if self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
    
    def get_templates(self):
        """Get available sandbox templates"""
        return {
            'general': {
                'name': 'General Purpose',
                'description': 'A general-purpose sandbox for running applications',
                'cpu_limit': 50,
                'memory_limit': 512,
                'disk_limit': 1024
            },
            'development': {
                'name': 'Development',
                'description': 'Sandbox for software development with more resources',
                'cpu_limit': 75,
                'memory_limit': 1024,
                'disk_limit': 2048
            },
            'testing': {
                'name': 'Testing',
                'description': 'Isolated environment for testing applications',
                'cpu_limit': 50,
                'memory_limit': 512,
                'disk_limit': 512
            },
            'lightweight': {
                'name': 'Lightweight',
                'description': 'Minimal resources for simple tasks',
                'cpu_limit': 25,
                'memory_limit': 256,
                'disk_limit': 512
            },
            'heavy': {
                'name': 'Heavy Workload',
                'description': 'Maximum resources for demanding applications',
                'cpu_limit': 100,
                'memory_limit': 2048,
                'disk_limit': 4096
            }
        }
