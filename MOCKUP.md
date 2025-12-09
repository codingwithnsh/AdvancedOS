# Sandbox Manager UI Mockup

## Main Dashboard

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                   ║
║  🔒 Sandbox Manager                          [➕ Create New Sandbox]  [🔄 Refresh]║
║  Create and manage isolated virtual environments                                  ║
║                                                                                   ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                   ║
║   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   ║
║   │      5        │  │      3        │  │      1        │  │      1        │   ║
║   │ Total         │  │ Running       │  │ Stopped       │  │ Paused        │   ║
║   │ Sandboxes     │  │               │  │               │  │               │   ║
║   └───────────────┘  └───────────────┘  └───────────────┘  └───────────────┘   ║
║                                                                                   ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║ Virtual Machines                                           │ Controls            ║
║                                                            │                     ║
║ ┌────────────────────────────────────────────────────────┐│ Lifecycle          ║
║ │ Name      │ Type     │ Status      │ CPU% │ Memory    ││ [▶️  Start]        ║
║ ├───────────┼──────────┼─────────────┼──────┼───────────┤│ [⏸️  Pause]        ║
║ │ Dev Box   │ Dev      │🟢 Running   │ 12.3 │ 256 MB   ││ [▶️  Resume]       ║
║ │ Test Env  │ Testing  │🟡 Paused    │ 0.0  │ 128 MB   ││ [⏹️  Stop]         ║
║ │ Build     │ Heavy    │🟢 Running   │ 45.2 │ 1024 MB  ││                     ║
║ │ Sandbox1  │ General  │🔴 Stopped   │ 0.0  │ 0 MB     ││ ────────────────   ║
║ │ Sandbox2  │ Light    │🟢 Running   │ 8.1  │ 64 MB    ││                     ║
║ └────────────────────────────────────────────────────────┘│ Management         ║
║                                                            │ [📊 View Details]  ║
║                                                            │ [💻 Open Terminal] ║
║                                                            │                     ║
║                                                            │ ────────────────   ║
║                                                            │                     ║
║                                                            │ Danger Zone        ║
║                                                            │ [🗑️  Delete]        ║
║                                                            │                     ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

## Create Sandbox Dialog

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                      Create New Virtual Machine                          ║
║              Configure your isolated sandbox environment                 ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  Machine Name                                                            ║
║  ┌─────────────────────────────────────────────────────────────────────┐ ║
║  │ My Sandbox                                                          │ ║
║  └─────────────────────────────────────────────────────────────────────┘ ║
║                                                                           ║
║  Template                                                                ║
║  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  ║
║  │     🔧       │  │     💻       │  │     🧪       │                  ║
║  │   General    │  │ Development  │  │   Testing    │                  ║
║  │  CPU: 50%    │  │  CPU: 75%    │  │  CPU: 50%    │                  ║
║  │  RAM: 512MB  │  │  RAM: 1024MB │  │  RAM: 512MB  │                  ║
║  └──────────────┘  └──────────────┘  └──────────────┘                  ║
║                                                                           ║
║  ┌──────────────┐  ┌──────────────┐                                     ║
║  │     ⚡       │  │     🚀       │                                     ║
║  │ Lightweight  │  │ Heavy Load   │                                     ║
║  │  CPU: 25%    │  │  CPU: 100%   │                                     ║
║  │  RAM: 256MB  │  │  RAM: 2048MB │                                     ║
║  └──────────────┘  └──────────────┘                                     ║
║                                                                           ║
║  A general-purpose sandbox for running applications                      ║
║                                                                           ║
║  Resource Limits                                                         ║
║  ┌─────────────────────────────────────────────────────────────────────┐ ║
║  │ CPU Limit                                             50%           │ ║
║  │ ━━━━━━━━━━━━━━━━━━━━━━━━━●────────────────────────                 │ ║
║  │                                                                      │ ║
║  │ Memory Limit                                          512 MB        │ ║
║  │ ━━━━━━━━━━━━━━━●───────────────────────────────────                 │ ║
║  │                                                                      │ ║
║  │ Disk Limit                                            1024 MB       │ ║
║  │ ━━━━━━━━━━━━━━━━━━━━●──────────────────────────────                 │ ║
║  └─────────────────────────────────────────────────────────────────────┘ ║
║                                                                           ║
║                                                                           ║
║         [   Create Virtual Machine   ]         [   Cancel   ]           ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Sandbox Details View

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                         📦 Development Box                                ║
║                           ● RUNNING                                       ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      ║
║  │  CPU Usage       │  │  Memory Usage    │  │  Disk Usage      │      ║
║  │                  │  │                  │  │                  │      ║
║  │      12.3%       │  │      256 MB      │  │      45 MB       │      ║
║  │                  │  │                  │  │                  │      ║
║  │    of 75%        │  │   of 1024 MB     │  │   of 2048 MB     │      ║
║  └──────────────────┘  └──────────────────┘  └──────────────────┘      ║
║                                                                           ║
║  Detailed Information                                                    ║
║  ┌─────────────────────────────────────────────────────────────────────┐ ║
║  │ ╔═════════════════════════════════════════════════════════════════╗ │ ║
║  │ ║              SANDBOX INFORMATION                                ║ │ ║
║  │ ╚═════════════════════════════════════════════════════════════════╝ │ ║
║  │                                                                      │ ║
║  │ 🆔 Sandbox ID:     a1b2c3d4                                         │ ║
║  │ 📛 Name:            Development Box                                 │ ║
║  │ 🏷️  Type:            Development                                    │ ║
║  │ 📅 Created:         2024-12-09T05:15:30                            │ ║
║  │                                                                      │ ║
║  │ ╔═════════════════════════════════════════════════════════════════╗ │ ║
║  │ ║              RESOURCE LIMITS                                    ║ │ ║
║  │ ╚═════════════════════════════════════════════════════════════════╝ │ ║
║  │                                                                      │ ║
║  │ 💻 CPU Limit:       75%                                             │ ║
║  │ 🧠 Memory Limit:    1024 MB                                         │ ║
║  │ 💾 Disk Limit:      2048 MB                                         │ ║
║  │                                                                      │ ║
║  │ ╔═════════════════════════════════════════════════════════════════╗ │ ║
║  │ ║              FILE SYSTEM PATHS                                  ║ │ ║
║  │ ╚═════════════════════════════════════════════════════════════════╝ │ ║
║  │                                                                      │ ║
║  │ 📁 Base Directory:  /home/user/.advancedos/sandboxes/a1b2c3d4      │ ║
║  │ 🗂️  Root Directory:  /home/user/.advancedos/sandboxes/.../root      │ ║
║  │ 💼 Data Directory:  /home/user/.advancedos/sandboxes/.../data      │ ║
║  └─────────────────────────────────────────────────────────────────────┘ ║
║                                                                           ║
║                          [   Close   ]                                   ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Quick Start Guide

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                  🚀 Welcome to Sandbox Manager!                           ║
║         Create isolated virtual environments for your applications       ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  🔒 What are Sandboxes?                                                  ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║  Sandboxes are isolated virtual machines that provide:                   ║
║                                                                           ║
║    ✅ Security - Run untrusted applications safely                       ║
║    ✅ Isolation - Each sandbox has its own file system                   ║
║    ✅ Resource Control - Set CPU, memory, and disk limits                ║
║    ✅ Easy Management - Create, start, stop, and delete with ease        ║
║                                                                           ║
║                                                                           ║
║  📋 Getting Started                                                      ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║  1. Click "Create New Sandbox" button                                    ║
║  2. Choose a name for your virtual machine                               ║
║  3. Select a template (or customize resources)                           ║
║  4. Click "Create Virtual Machine"                                       ║
║  5. Use the control panel to manage your sandbox                         ║
║                                                                           ║
║                                                                           ║
║  🎯 Available Templates                                                  ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║    🔧 General Purpose - For everyday tasks                               ║
║    💻 Development - Enhanced resources for coding                        ║
║    🧪 Testing - Isolated environment for safe testing                    ║
║    ⚡ Lightweight - Minimal resources for simple tasks                   ║
║    🚀 Heavy Workload - Maximum resources for demanding apps              ║
║                                                                           ║
║                                                                           ║
║  💡 Tips                                                                 ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║    • Use the Terminal feature to execute commands in a sandbox           ║
║    • Monitor resource usage in real-time                                 ║
║    • Pause sandboxes when not in use to save resources                   ║
║    • Delete sandboxes you no longer need to free up space                ║
║                                                                           ║
║                                                                           ║
║         [   Create My First Sandbox   ]         [   Close   ]           ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Color Scheme Reference

### Dark Mode
- Background: `#1a1a1a` ░░░░░░░
- Cards: `#2d2d30` ▒▒▒▒▒▒▒
- Hover: `#3c3c3c` ▓▓▓▓▓▓▓
- Text: `#ffffff` ███████
- Muted: `#888888` ▓▓▓▓▓▓▓

### Light Mode  
- Background: `#f5f5f5` ░░░░░░░
- Cards: `#ffffff` ███████
- Hover: `#e8e8e8` ▒▒▒▒▒▒▒
- Text: `#1a1a1a` ███████
- Muted: `#888888` ▓▓▓▓▓▓▓

### Accent Colors
- Primary: `#007acc` █████ (Blue)
- Success: `#4ec9b0` █████ (Green)
- Warning: `#dcdcaa` █████ (Yellow)
- Error: `#f14c4c` █████ (Red)
- Stop: `#ce9178` █████ (Orange)

## Interaction Flows

### Creating a Sandbox
1. User clicks "Create New Sandbox"
2. Dialog opens with template selection
3. User selects template (card highlights blue)
4. Resource sliders update automatically
5. User adjusts resources if needed
6. User enters sandbox name
7. User clicks "Create Virtual Machine"
8. Status shows "Creating virtual machine..."
9. On success: Shows ✅ message, waits 1s, closes
10. Dashboard refreshes automatically

### Managing a Sandbox
1. User selects sandbox from list
2. Status indicators show current state
3. User clicks control button
4. Action executes immediately
5. Notification appears
6. List refreshes to show new status

### Viewing Details
1. User selects sandbox
2. User clicks "View Details"
3. Dialog opens with resource cards
4. Information displayed in formatted sections
5. User can close when done
