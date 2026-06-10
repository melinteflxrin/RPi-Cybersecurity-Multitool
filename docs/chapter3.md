# Chapter 3: Technologies, Tools & Methods

This chapter details the technologies, hardware components, and tools that form the foundation of the security research platform. The platform unifies multiple industry-standard security tools through a single Python orchestrator, enabling educational demonstration of WiFi, Bluetooth Low Energy, and Bluetooth Classic vulnerabilities.

## 3.1 Operating System & Platform Selection

### 3.1.1 Target Platform: Raspberry Pi Zero 2 W

The Raspberry Pi Zero 2 W was chosen as the primary target platform for its balance between educational affordability, practical capability, and real-world relevance:

**Processor & Memory:**
- CPU: ARM Cortex-A53 (4 cores, 1.0 GHz)
- RAM: 512 MB
- Storage: MicroSD card (32 GB recommended for large packet captures)
- Architecture: ARMv7 (32-bit)

**Built-in Features:**
- Broadcom BCM43438 wireless chip (WiFi 802.11b/g/n + Bluetooth 4.2 BLE)
- Compact form factor (65mm × 30mm × 5mm)
- No external power jack (USB micro power input)

**Cost & Accessibility:**
- Hardware cost: ~$15-20 for board alone (educational pricing available)
- Total deployment cost with WiFi adapter: ~$45-60 per student station
- Widely available through educational distributors worldwide
- Affordable for large-scale classroom deployment (vs. $5000+ professional platforms)

**Why Raspberry Pi Zero 2 W:**
- Educational purpose: Low cost enables widespread adoption in academic labs
- Real-world relevance: Same toolchain as larger Linux systems (just more constrained)
- Learning constraint: 512 MB RAM teaches optimization and resource awareness
- Bluetooth built-in: Eliminates need for separate adapter for BLE/Bluetooth Classic
- Community support: Extensive documentation and troubleshooting resources available

**Constraints & Trade-offs:**
- Limited RAM impacts certain operations (e.g., hashcat cracking, parallel processing)
- Single-core performance is slower than desktop systems (affects packet processing)
- Thermal throttling under sustained load requires active cooling
- All attacks designed to work within 512 MB RAM limitation

### 3.1.2 Development Platform: x86 Linux Desktop

While the target deployment is Raspberry Pi, development occurs on more powerful x86 Linux systems:

**Advantages:**
- Faster iteration cycles (compilation, testing, debugging)
- More RAM available for complex operations (packet analysis, cracking)
- Same Linux/Debian codebase as Pi ensures portability
- Easier to debug errors with full stack traces and debugging tools

**Consistency Requirement:**
- Identical Python code runs on both platforms
- Tool versions remain consistent (aircrack-ng, mdk4, hping3)
- Only performance characteristics differ, not functionality
- Testing on desktop validates code before Pi deployment

### 3.1.3 Why Linux/Debian as Primary Platform

**WiFi Monitor Mode:**
- Linux kernel natively supports monitor mode for WiFi adapters (promiscuous packet capture)
- Windows and macOS have limited or no monitor mode support
- Educational value: Students learn native Linux networking, not workarounds

**Package Management (apt):**
- System packages installed via `apt-get` (Debian/Ubuntu)
- Consistent dependency resolution across machines
- Reproducible installations (same package versions)
- Fewer compatibility issues compared to manual installation

**Driver Availability:**
- Extensive Linux driver support for both mainstream and specialized WiFi adapters
- Open-source drivers (e.g., 8821au for TP-Link adapters)
- Kernel module compilation via DKMS (automatic recompilation on kernel updates)

**Accessibility & Cost:**
- Raspberry Pi OS (Debian-based) is free
- No licensing costs compared to Windows Server or specialized security OSes
- Large community for troubleshooting and support

### 3.1.4 Cross-Platform Compatibility Considerations

**Python Portability:**
- Python 3 code is platform-independent
- Identical codebase works on Pi and x86 Linux without modification
- Standard libraries (subprocess, asyncio, threading) behave consistently

**Tool Availability:**
- Primary tools (aircrack-ng, mdk4, hping3, bluez) available on all Linux distributions
- Installation procedures identical across platforms (only processor differences)

**Platform Incompatibility:**
- **Windows:** No monitor mode support, WiFi adapter drivers limited, different package management
- **macOS:** Limited monitor mode (requires special tools), driver support sporadic
- **Decision:** Linux-only platform chosen for native support, not OS portability

**Design Consequence:**
- Code written explicitly for Linux environment
- No cross-platform abstraction layer (simplifies design)
- Educational value: Students learn Linux system-level networking

---

## 3.2 Hardware Components

### 3.2.1 Raspberry Pi Zero 2 W Specifications

**Physical Specifications:**
- Dimensions: 65mm × 30mm × 5mm (half the size of Pi 4)
- Weight: ~9 grams
- GPIO pins: 40-pin header (Raspberry Pi standard)
- Connectors: USB micro-B (power), mini-HDMI, micro-USB OTG (data)

**Processing Power:**
- 4× ARM Cortex-A53 @ 1.0 GHz (quad-core)
- CPU: Broadcom BCM2710A1
- 512 MB SDRAM (shared with GPU)
- No built-in SATA or eSATA connectors

**Wireless Connectivity:**
- WiFi: Broadcom BCM43438 802.11b/g/n (2.4 GHz only)
- Bluetooth: 4.2 BLE (integrated)
- Antenna: Single PCB trace (omnidirectional)
- Built-in antenna provides ~-40 dBm sensitivity

**Storage:**
- MicroSD card slot (up to 512 GB supported)
- Recommended: 32 GB Class 10 U3 card for packet capture storage
- No eMMC (unlike Pi 4 variants)

**Cost Considerations:**
- Wholesale cost: ~$15 (educational discount available)
- Typical retail: $15-20 USD
- Global availability through authorized distributors

### 3.2.2 WiFi Adapter: TP-Link Archer T2U PLUS

The external WiFi adapter provides enhanced capabilities beyond the Pi's integrated wireless:

**Hardware Specifications:**
- Chipset: Realtek RTL8821AU
- Type: Dual-band USB WiFi adapter
- Frequency: 802.11a/b/g/n/ac support
  - 2.4 GHz: 1-13 channels (region-dependent)
  - 5.0 GHz: 36-165 channels (UNII 1-4)
- Data Rates: Up to 867 Mbps (AC) / 300 Mbps (N)
- Antenna: 2× removable 5 dBi omni-directional antennas
- Connector: USB 3.0 Type-A (backward compatible with USB 2.0)

**Monitor Mode Capability:**
- RTL8821AU chipset widely supported in Linux community
- Monitor mode: Enabled for packet capture and injection
- Packet injection: Supported (essential for deauth attacks)
- Frame crafting: Full 802.11 frame injection capability

**Dual-Band Advantage:**
- 2.4 GHz: Higher range (≈30-50m), lower bandwidth
- 5.0 GHz: Lower range (≈10-20m), higher bandwidth
- Attack diversity: Some networks on each band
- Educational value: Teaches band selection strategies

**Cost & Availability:**
- Typical price: $30-40 USD
- Readily available from major electronics retailers
- Community support for driver installation
- Open-source driver maintained by community (morrownr GitHub)

### 3.2.3 System Architecture & Integration

**USB Hub Requirement:**
```
[USB Power Adapter] ─→ [USB Hub] ─→ [TP-Link T2U PLUS]
                            ↓
                      [Raspberry Pi]
```
- Pi has limited USB current (≤500 mA)
- T2U PLUS requires ≥300 mA peak
- Powered USB hub (≥2A) recommended for stable operation
- Separate 5V/2A power supply prevents brownout during high load

**Power Management:**
- Pi consumption: ~300-400 mA at idle, ~600-800 mA under load
- T2U PLUS consumption: ~200-400 mA (varies with transmit power)
- Total: 0.8-1.2 A typical usage
- Requirement: 5V/2A power supply minimum

**Thermal Management:**
- Pi Zero 2 W throttles at 80°C
- Active attacks generate heat (CPU + WiFi transmit)
- Solution: Passive aluminum enclosure with thermal pads
- Alternative: Small active cooling fan (adds $5-10, reduces throttling)
- Benefit: Sustained attack execution without performance degradation

**Network Configuration:**
- Integrated Bluetooth for L2CAP attacks
- External WiFi adapter for 802.11 attacks
- Both interfaces independent (no interference)
- Optional: Ethernet dongle for management network

---

## 3.3 Core Tools & Libraries

This section details the software stack enabling the platform. Tools are organized by category (system packages, Python libraries, WiFi drivers).

### 3.3.1 System Packages (Debian/Ubuntu)

All packages installed via `apt-get` from standard repositories. Complete installation commands available in [SETUP.md](SETUP.md).

**Development Tools:**
```bash
sudo apt-get install -y python3 python3-pip python3-dev
sudo apt-get install -y git curl wget
sudo apt-get install -y build-essential dkms
sudo apt-get install -y bc linux-headers-generic
```
- `python3`: Python 3 interpreter (v3.9+ recommended)
- `python3-pip`: Package manager for Python libraries
- `python3-dev`: Header files for compiled Python modules
- `build-essential`: GCC, make, and build tools (required for driver compilation)
- `dkms`: Dynamic Kernel Module Support (automatic driver recompilation on kernel updates)
- `linux-headers-generic`: Kernel headers required for driver compilation

**Bluetooth Stack:**
```bash
sudo apt-get install -y bluez bluez-tools
sudo apt-get install -y python3-bluez python3-dbus
sudo apt-get install -y libbluetooth-dev
```
- `bluez`: Official Linux Bluetooth stack daemon
- `bluez-tools`: Utilities (hciconfig, btmgmt, hcitool)
- `python3-bluez`: PyBluez Python bindings (low-level Bluetooth API)
- `python3-dbus`: D-Bus interface for system services
- `libbluetooth-dev`: C headers for Bluetooth development

**WiFi Security Tools:**
```bash
sudo apt-get install -y aircrack-ng mdk4 wifite
```
- `aircrack-ng`: Comprehensive WiFi security toolkit
  - `airodump-ng`: Passive network scanner and monitor
  - `aireplay-ng`: Packet injection tool (transmit frames)
  - `airmon-ng`: Monitor mode manager
- `mdk4`: Dedicated WiFi DoS tool (beacon spam, deauth)
- `wifite`: Automated WiFi attack wrapper (optional, for reference)

**Network Tools:**
```bash
sudo apt-get install -y dnsmasq hostapd iptables
sudo apt-get install -y arp-scan hping3
```
- `dnsmasq`: Lightweight DNS/DHCP server (phishing network setup)
- `hostapd`: Access point daemon (fake AP creation)
- `iptables`: Firewall and packet routing
- `arp-scan`: ARP network discovery scanner
- `hping3`: Packet crafting and flooding tool (IP/ICMP/UDP DoS)

**Python Libraries:**
```bash
sudo apt install -y python3-bleak python3-yaml
```
- `python3-bleak`: Python BLE scanning library (async operations)
- `python3-yaml`: YAML configuration file parsing

**System Utilities:**
```bash
sudo apt-get install -y rfkill hciconfig btmgmt nmcli
```
- `rfkill`: RF device state management (enable/disable WiFi/Bluetooth)
- `hciconfig`: Bluetooth adapter configuration and status
- `btmgmt`: Bluetooth management (power, pairing, discoverability)
- `nmcli`: NetworkManager command-line interface (WiFi network management)

### 3.3.2 Python Libraries (Detailed)

Beyond system packages, three key Python libraries handle protocol-specific operations:

#### Bleak: Bluetooth Low Energy Scanning

**Installation:**
```bash
pip3 install bleak
```

**Purpose:** Async BLE device discovery and advertisement handling

**Used In:** `ble/device_scanner.py`

**Key Functions:**
- Concurrent scanning of multiple BLE devices
- Advertisement data parsing (manufacturer data, flags, TX power)
- RSSI (signal strength) measurement
- Cross-platform BLE abstraction (Linux uses BlueZ backend)

**Code Example - Async BLE Scanning:**
```python
import asyncio
from bleak import BleakScanner

async def scan_devices(duration=10):
    """Scan for nearby BLE devices for specified duration."""
    scanner = BleakScanner()
    
    # Start scanning in background
    await scanner.start()
    
    # Collect devices over time
    await asyncio.sleep(duration)
    
    # Get discovered devices
    devices = await scanner.get_discovered_devices()
    
    await scanner.stop()
    
    return devices

# Run the async scan
devices = asyncio.run(scan_devices(duration=10))
for device in devices:
    print(f"Found: {device.address} - Signal: {device.rssi} dBm")
```

**Why Async?**
- BLE communication is inherently concurrent (multiple devices broadcasting simultaneously)
- `asyncio` allows polling multiple devices without blocking on single device
- Bleak's async interface enables responsive UI updates during scanning
- Educational value: Students learn async patterns used in modern Python

**Constraints:**
- Requires BlueZ 5.50+ on Linux (provides HCI socket interface)
- Scanner range limited by WiFi adapter antenna (~30-50m outdoor)
- RSSI measurements noisy (fluctuate ±3-5 dBm) due to multipath fading

#### PyYAML: Configuration File Parsing

**Installation:**
```bash
pip3 install pyyaml
```

**Purpose:** Parse structured configuration files in human-readable YAML format

**Used In:** `ble/device_scanner.py` (company identifier database)

**Code Example - Loading Company Identifiers:**
```python
import yaml
import os

def load_company_ids(filename):
    """Load BLE manufacturer company IDs from YAML file."""
    company_ids = {}
    
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
            
            if data and 'company_identifiers' in data:
                for entry in data['company_identifiers']:
                    hex_id = entry.get('value', '')
                    name = entry.get('name', '')
                    
                    if hex_id and name:
                        company_id = int(hex_id, 16)
                        company_ids[company_id] = name
                
                return company_ids
    except Exception as e:
        print(f"Warning: Could not load company IDs: {e}")
    
    # Fallback to hardcoded values
    return fallback_company_ids()

# Load on startup
company_map = load_company_ids('company_identifiers.yaml')

# Use for device identification
device_company = company_map.get(0x004C, "Unknown")  # 0x004C = Apple
print(f"Device manufacturer: {device_company}")
```

**BLE Company ID YAML Format:**
```yaml
company_identifiers:
  - value: '0x004C'
    name: 'Apple'
  - value: '0x006B'
    name: 'Google'
  - value: '0x0059'
    name: 'Nordic'
  # ... more entries
```

**Why YAML?**
- Human-readable format (vs. binary or JSON)
- Easy for students to add new company IDs
- Comments supported for documentation
- Standard configuration format in DevOps/SRE workflows

#### PyBluez: Low-Level Bluetooth Access

**Installation:**
```bash
pip3 install pybluez
```

**Purpose:** Direct access to Bluetooth Classic L2CAP layer

**Used In:** `bt/l2cap_dos_attack.py`

**Key Functions:**
- Socket-based L2CAP connection (Bluetooth protocol layer)
- Raw socket operations for connection flooding
- Adapter enumeration and device discovery

**Why L2CAP?**
- L2CAP = Logical Link Control and Adaptation Protocol
- Layer 2 in Bluetooth stack (below higher-level protocols)
- DoS attacks most effective at L2CAP layer (connection resource exhaustion)
- PyBluez provides Python interface to Linux BlueZ stack

**Constraints:**
- Requires root/sudo privilege (direct kernel socket access)
- Deprecated in favor of newer libraries (but still works)
- Linux-only (no macOS/Windows support)

### 3.3.3 Standard Python Libraries

The project uses several standard library components:

**Subprocess Module:**
```python
import subprocess

# Run external tool with real-time output streaming
process = subprocess.Popen(
    ['mdk4', 'wlan1mon', 'd'],  # Command as list
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,                   # String output, not bytes
    bufsize=1                    # Line-buffered output
)

# Stream output line-by-line
while True:
    output = process.stdout.readline()
    if output:
        print(output.rstrip())
    
    # Check if process finished
    if process.poll() is not None:
        break

# Get return code
success = process.returncode == 0
```
- Launches external tools (aircrack-ng, mdk4, hping3)
- Captures output in real-time
- Handles Ctrl+C interruption gracefully

**Asyncio Module:**
- Event loop for concurrent BLE scanning
- Allows responsive UI during long-running operations
- Educational value: Async patterns common in modern Python

**Threading Module:**
- Background tasks (HTTP server for phishing)
- Concurrent attack execution (limited use due to GIL)

**Socket & HTTP.server Modules:**
- Network communication
- Phishing server HTTP request handling

### 3.3.4 WiFi Driver: RTL8821AU with DKMS

The TP-Link Archer T2U PLUS requires a driver for Linux support:

**Driver Installation:**
```bash
# Clone driver repository
cd ~
git clone https://github.com/morrownr/8821au-20210708.git
cd 8821au-20210708

# Run automated install script
sudo ./install-driver.sh

# Reboot to load kernel module
sudo reboot
```

**DKMS (Dynamic Kernel Module Support):**
- Automatically recompiles driver when kernel updates
- Prevents "driver not found" errors after `apt-get upgrade`
- One-time setup eliminates manual recompilation

**Monitor Mode Enablement:**
```bash
# Verify adapter is recognized
lsusb | grep "Realtek"

# Unmanage the interface (prevent NetworkManager interference)
sudo nmcli device set wlan1 managed no

# Bring interface down, change to monitor mode, bring up
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up

# Verify monitor mode enabled
iwconfig wlan1
# Should show: Mode:Monitor
```

**Why Monitor Mode?**
- Normal WiFi adapters only capture frames destined for their MAC address
- Monitor mode captures ALL 802.11 frames in range (promiscuous)
- Required for passive scanning, packet capture, frame injection
- Educational value: Students see how WiFi eavesdropping works

**Constraints:**
- Requires Linux kernel ≥3.10 (very old requirement)
- Some WiFi adapters lack driver support
- Adapter and driver must both support monitor mode
- Cannot be associated to network while in monitor mode

### 3.3.5 Optional: Cloudflare Tunnel Integration

For phishing demonstrations requiring external access:

**Installation:**
```bash
# Download cloudflared for ARM64 (Pi Zero 2 W)
wget https://github.com/cloudflare/cloudflared/releases/download/2024.12.0/cloudflared-linux-arm64

# Make executable and install
chmod +x cloudflared-linux-arm64
sudo mv cloudflared-linux-arm64 /usr/local/bin/cloudflared

# Verify installation
cloudflared --version
```

**Use Case:** Creating public HTTPS URLs for phishing pages

**How It Works:**
1. Cloudflare Tunnel creates outbound connection from Pi to Cloudflare edge
2. Cloudflare generates public URL pointing back through tunnel
3. Phishing server running locally accessible via public internet
4. No port forwarding, firewall rules, or public IP needed

**Educational Value:**
- Demonstrates how attackers bypass network isolation
- Shows real-world attack infrastructure (reverse tunnels)
- Cloud services enable attacks from constrained environments

**Security Consideration:**
- Only installed on systems explicitly needing external access
- Disabled by default in basic deployment

---

## 3.4 Development Methodology

### 3.4.1 Object-Oriented Design Approach

The platform uses object-oriented principles for code organization:

**Attack Module Class Hierarchy:**
- All attacks inherit from base class
- Standard interface: `validate_parameters()` → `execute()` → `display_results()`
- Polymorphism enables modular attack selection
- Educational value: Teaches OOP principles through practical example

**Class Structure Benefits:**
- Code reuse: Common validation, error handling, UI patterns
- Extensibility: Adding new attack is simple class extension
- Testability: Each attack module independently testable
- Maintainability: Changes to one attack don't affect others

### 3.4.2 Modular Design Pattern

**Single Responsibility Principle:**
- Each attack module handles ONE attack type
- UI module handles ALL terminal output
- Each tool wrapper module handles ONE external tool

**Module Organization:**
```
personal_project/
├── main.py              # Orchestrator (menu system)
├── ui/console.py        # Terminal colors and formatting
├── wifi/                # 8 WiFi attack modules
├── ble/                 # 5 BLE attack modules
├── bt/                  # Bluetooth Classic attacks
└── phishing/            # Phishing server modules
```

**Benefits:**
- Concurrent development (multiple people working simultaneously)
- Easier debugging (isolate failures to specific module)
- Clear dependencies (what each module requires)

### 3.4.3 UI/UX Design: Color-Coded Console

**Terminal Output Patterns:**
```python
# Information message (light blue)
iprint("Scanning for networks...")

# Warning message (yellow)
wprint("Interface not in monitor mode!")

# Error message (red)
eprint("Attack failed: insufficient permissions")

# Success message (green)
sprint("Attack completed successfully!")

# Colored output (cyan)
cprint("Network found: HOME-NETWORK (CH 6)", CYAN)
```

**Why Color-Coding?**
- Rapid visual feedback (error detection before reading)
- Reduces cognitive load (color is processed faster than text)
- Educational principle: Immediate feedback reinforces learning
- Professional appearance (more usable than plain text)

### 3.4.4 Error Handling Strategy

**Graceful Degradation:**
```python
try:
    # Attempt to load configuration file
    config = load_config()
except FileNotFoundError:
    # Use sensible defaults if file missing
    config = DEFAULT_CONFIG
    wprint("Config file not found, using defaults")
except Exception as e:
    # Catch unexpected errors
    eprint(f"Error: {e}")
    return False

# Continue execution with available configuration
```

**User Feedback:**
- Clear error messages explaining what went wrong
- Suggestions for fixes when possible
- Graceful exit rather than crashes
- Don't expose raw stack traces to end users

---

## 3.5 Tool Integration & Compatibility

### 3.5.1 Subprocess Integration Pattern

External tools invoked via subprocess with real-time output streaming:

**WiFi Scanner Example - Using `airodump-ng`:**
```python
import subprocess
from ui import cprint, CYAN

def run_network_scanner(interface):
    """
    Scan for WiFi networks using airodump-ng.
    Display output in real-time.
    """
    try:
        # Build command as list (safer than string)
        cmd = ['airodump-ng', '--output-format', 'csv', 
               '--write', 'networks', interface]
        
        # Start process with output pipes
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # Line-buffered: one line at a time
        )
        
        # Stream output line-by-line to user
        while True:
            output = process.stdout.readline()
            if output:
                cprint(output.rstrip(), CYAN)
            
            # Check if process ended
            if process.poll() is not None:
                break
        
        # Return success/failure
        return process.returncode == 0
        
    except KeyboardInterrupt:
        # Handle Ctrl+C: graceful shutdown
        process.terminate()
        return False
    except Exception as e:
        eprint(f"Error: {e}")
        return False
```

**Key Pattern Features:**
1. **Command as list** (`['airodump-ng', ...]`): Subprocess handles quoting/escaping automatically
2. **Real-time streaming** (`readline()` loop): User sees output as it happens
3. **Buffering** (`bufsize=1`): Line-buffered output prevents buffered delays
4. **Ctrl+C handling** (`KeyboardInterrupt`): Graceful cleanup on user interruption
5. **Error detection** (check `returncode`): Know if tool succeeded
6. **Proper termination** (`.terminate()`): Don't leave orphaned processes

**Why This Pattern?**
- **Immediate feedback:** User sees progress, not blank screen
- **Ctrl+C stops tool:** Can interrupt long-running attacks
- **No data loss:** Output captured even on error
- **Educational:** Shows how to integrate external tools safely

### 3.5.2 Dependency Management

**Python Package Management:**
```bash
# Install all Python dependencies
pip3 install -r requirements.txt

# Typical requirements.txt:
bleak>=0.20.0
pyyaml>=6.0
# pydbus installed via system packages
```

**System Package Dependencies:**
- Install via `apt-get` (from official repositories)
- Versions managed by OS
- No version conflicts (apt resolves dependencies)

**DKMS Kernel Module:**
- Automatically recompiles when kernel updates
- Persists across system upgrades
- Eliminates post-update driver issues

**Version Pinning:**
- requirements.txt pins package versions for reproducibility
- Same code runs identically across different machines
- Important for classroom deployments (all students same experience)

---

## 3.6 Implementation Patterns

### 3.6.1 Attack Module Base Class Pattern

All attacks follow a standardized interface for consistency:

**Base Class Definition:**
```python
class AttackModule:
    """Base class for all security attacks."""
    
    def __init__(self, interface=None):
        self.interface = interface
    
    def validate_parameters(self):
        """
        Validate user input before attack execution.
        Raises exception if validation fails.
        """
        raise NotImplementedError
    
    def execute(self):
        """
        Execute the attack using validated parameters.
        Returns True on success, False on failure.
        """
        raise NotImplementedError
    
    def display_results(self):
        """Display attack results to user."""
        raise NotImplementedError
```

**Concrete Implementation - Deauthentication Attack:**
```python
class DeauthAttack(AttackModule):
    """Wireless deauthentication attack."""
    
    def __init__(self, interface):
        super().__init__(interface)
        self.target = None
        self.duration = None
    
    def validate_parameters(self):
        """Validate interface and target before attack."""
        # Check interface is in monitor mode
        if not self.verify_monitor_mode():
            raise ValueError("Interface not in monitor mode")
        
        # Get target from user
        self.target = input("Target MAC or SSID: ")
        
        # Validate format (basic check)
        if not self.is_valid_mac(self.target):
            raise ValueError(f"Invalid target: {self.target}")
    
    def execute(self):
        """Run deauthentication attack."""
        try:
            cmd = ['mdk4', self.interface, 'd', '-t', self.target]
            
            process = subprocess.Popen(cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True)
            
            # Stream output to user
            while True:
                output = process.stdout.readline()
                if output:
                    cprint(output.rstrip(), CYAN)
                if process.poll() is not None:
                    break
            
            return process.returncode == 0
        except Exception as e:
            eprint(f"Attack failed: {e}")
            return False
    
    def display_results(self):
        """Show attack completion status."""
        if success:
            sprint("Deauthentication attack completed!")
        else:
            eprint("Attack failed!")
```

**Benefits of This Pattern:**
- **Consistency:** Every attack follows same validate→execute→display flow
- **Teachability:** Students understand all attacks at high level
- **Extensibility:** Adding new attack is simply subclassing
- **Error Handling:** Standard validation prevents bad inputs

### 3.6.2 Subprocess Integration Pattern

Real-time tool execution with proper error handling:

**Complete Example - Network Scanner:**
```python
def start_scan(self):
    """Start continuous network scanning."""
    try:
        # Verify prerequisites
        if not self.verify_monitor_mode():
            eprint("Not in monitor mode!")
            return False
        
        # Build command as list (safer)
        cmd = ['airodump-ng', '-w', 'scan_output', 
               '--output-format', 'csv', self.interface]
        
        iprint("Starting scan... (Ctrl+C to stop)")
        print()
        
        # Launch process
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Monitor and display output
        while self.process.poll() is None:
            output = self.process.stdout.readline()
            if output:
                # Color-code output for readability
                cprint(f"[NETWORK] {output.rstrip()}", GREEN)
        
        # Collect any remaining output
        remaining = self.process.stdout.read()
        if remaining:
            cprint(remaining, GREEN)
        
        sprint(f"Scan complete! Results: scan_output-01.csv")
        return True
        
    except KeyboardInterrupt:
        wprint("\nScan stopped by user")
        if self.process:
            self.process.terminate()
        return False
        
    except Exception as e:
        eprint(f"Error: {e}")
        return False
```

### 3.6.3 Async BLE Scanning Pattern

Concurrent device discovery using asyncio:

```python
import asyncio
from bleak import BleakScanner

async def scan_devices(self):
    """Continuously scan for BLE devices."""
    scanner = BleakScanner()
    
    # Start scanning
    await scanner.start()
    
    iprint(f"Scanning for BLE devices... (Ctrl+C to stop)")
    print()
    
    try:
        # Keep scanning until user interrupts
        while True:
            # Collect devices discovered in last 2 seconds
            await asyncio.sleep(2)
            
            devices = await scanner.get_discovered_devices()
            
            # Display new/updated devices
            for device in devices:
                company = self.get_company(device.rssi)
                distance = self.rssi_to_distance(device.rssi)
                
                cprint(f"[{device.address}] {device.name} "
                       f"({company}) RSSI:{device.rssi} dBm "
                       f"({distance:.1f}m)", CYAN)
    
    except KeyboardInterrupt:
        wprint("\nScanning stopped")
    finally:
        await scanner.stop()

# Run async function
asyncio.run(scan_devices())
```

**Why Async for BLE?**
- Concurrent device discovery (don't wait for single device)
- Responsive to user input (can interrupt anytime)
- Natural for network operations (many operations in parallel)
- Educational: Teaches async patterns used throughout Python ecosystem

---

## 3.7 Summary: Technology Stack Rationale

| Layer | Technology | Why Chosen | Alternative |
|-------|-----------|-----------|-------------|
| **OS** | Debian Linux | Monitor mode native, package management | Windows, macOS limited |
| **Language** | Python 3 | Educational clarity, cross-platform | C/C++, Go, Rust |
| **BLE** | bleak library | Async, clean API, cross-platform | bluez direct, pybluez |
| **Config** | YAML files | Human-readable, extensible | JSON, INI, TOML |
| **WiFi Tools** | aircrack-ng, mdk4 | Industry-standard, well-documented | wifite, custom tools |
| **Bluetooth** | bluez stack | Linux native, RFC-compliant | Platform alternatives N/A |
| **HTTP Server** | http.server stdlib | Simple, no dependencies | Flask, Django (heavy) |
| **External Tools** | subprocess | Safe tool integration | shell=True (dangerous) |

**Design Philosophy:**
- **Educational first:** Code clarity prioritized over performance
- **Transparent:** Students see actual tools, not black boxes
- **Self-contained:** Everything needed in single codebase
- **Linux-native:** Leverage OS strengths, not fight against them
- **Affordable:** No expensive licenses or proprietary tools

This foundation enables the architecture (Chapter 4) and implementation (Chapter 5) described in subsequent chapters.

---

**Word Count: ~4,200 words**  
**Recommended Page Allocation: 10-12 pages (with figures and diagrams)**
