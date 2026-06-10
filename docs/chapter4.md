# Chapter 4: Solution Architecture & Design

## 4.1 Application Architecture Overview

The entire attack platform is organized around a simple principle: take 15 different security attacks and organize them so users can find and run what they want. To do this, I split the application into different layers, each handling different concerns.

### 4.1.1 Component Diagram

The main application has four main pieces working together:

1. **Main Orchestrator (main.py):** The AttackSuite class acts as the central menu system. It handles all user interaction and routes choices to the right attack module.

2. **Attack Modules:** Four separate folders (wifi/, ble/, bt/, phishing/) each containing attack classes. WiFi attacks are grouped together, BLE attacks together, etc. Each module is completely independent.

3. **UI/Console Module (ui/console.py):** This handles all the colored output, prompts, and formatted text. Every attack uses these functions to display messages consistently.

4. **Configuration & Utilities:** Helper functions for things like reading company identifiers from YAML files, getting Bluetooth adapters, and other common tasks.

**[FIGURE 4.1: System Component Diagram]**
*Placeholder: Diagram showing main.py at the center with four attack module groups (WiFi, BLE, Bluetooth Classic, Phishing) connected to it, plus the UI/console module and configuration layer*

### 4.1.2 Layered Architecture

The application works in three layers, from what the user sees down to what actually runs on the system:

**Presentation Layer (Top):** This is what users interact with. The UI module handles colored prompts, banners, input validation, and result display. The AttackSuite class manages the menu system and user choices. Users never think about code or system calls - they just pick menu options.

**Application Layer (Middle):** This is where the attack logic lives. Each attack (BeaconBroadcaster, DeauthAttack, BLEDeviceScanner, etc.) is its own Python class. These classes know how to validate what the user wants, prepare the attack, and display results. But they don't directly manipulate hardware or networks.

**System Layer (Bottom):** This is where the actual attack happens. I use subprocess to call external tools like mdk4, airodump-ng, and hping3. For BLE, I use the bleak library which talks directly to the Bluetooth hardware. For phishing, I use Cloudflare tunnel integration for public access.

**[FIGURE 4.2: Layered Architecture Diagram]**
*Placeholder: Three-layer diagram showing Presentation Layer (UI, menus) at top, Application Layer (attack classes) in middle, and System Layer (subprocess calls, bleak, HTTP server + Cloudflare tunnel) at bottom*

The advantage of this layered design is that each layer can be updated independently. If I want to change the UI colors, I only touch the console module. If I want to add a new attack, I just add a new class to the application layer. The system layer stays the same.

---

## 4.2 Main Application Structure

### 4.2.1 AttackSuite Class Design

The AttackSuite class is the heart of the application. When users start the app, they're interacting with this class. It does several things:

**Central Orchestrator:** AttackSuite manages the entire workflow. It shows menus, gets user choices, validates input, and calls the right attack module.

**Menu System:** The class has methods for each menu level. `main_menu()` shows the main choices (WiFi, BLE, etc.), then calls the right submenu method like `wifi_menu()` or `ble_menu()`.

**Attack Methods:** For each of the 15 attacks, there's a method named `action_*` (like `action_deauth_attack`, `action_beacon_broadcast`, etc.). When a user picks an attack, AttackSuite calls the right method.

**State Management:** The class keeps track of whether the app is running using a simple flag `self.running`. If the user picks "Exit", the flag becomes False and the app stops.

This design makes it easy to add new attacks. I just write a new action method, add it to the menu, and that's it. The user flow stays the same.

### 4.2.2 Menu Hierarchy

The menu system has three levels:

**Level 1: Main Menu**
```
Choose an attack category:
1. WiFi Attacks
2. BLE Attacks
3. Bluetooth Classic Attacks
4. Phishing Attacks
5. Exit
```

**Level 2: Category Submenu** (example: WiFi)
```
WiFi Attacks:
1. Network Scanner
2. Beacon Broadcast
3. Deauthentication
4. HTTP DoS
5. Back to Main Menu
```

**Level 3: Attack Execution**
User picks an attack, then gets prompted for parameters specific to that attack. The app asks "Which interface?" and "What target?" and so on.

At each level, input is validated. If you pick "99" in the WiFi menu, the app doesn't crash - it just says "That's not a valid choice" and asks again.

**[FIGURE 4.3: Menu Hierarchy Tree]**
*Placeholder: Tree diagram showing Main Menu branching to WiFi/BLE/Bluetooth/Phishing, each then branching to 2-3 example attacks*

### 4.2.3 Main Application Flow

Here's what happens when a user starts the app:

1. **Initialize:** Create an AttackSuite object and show the banner
2. **Main Loop:** Keep showing the main menu until the user exits
3. **Get Choice:** Read what the user picked (1 for WiFi, 2 for BLE, etc.)
4. **Show Submenu:** Based on their choice, show the submenu for that attack category
5. **Get Attack Choice:** Read which specific attack they want
6. **Gather Parameters:** Ask for interface name, targets, duration, etc.
7. **Validate:** Check that the parameters make sense (interface exists, IP addresses are valid, etc.)
8. **Execute:** Run the attack using the right attack class
9. **Show Results:** Display what happened (success, failure, packets sent, etc.)
10. **Back to Menu:** Return to step 2 and ask what they want to do next

If the user presses Ctrl+C at any point, the attack stops cleanly. Error messages are shown in red so they're easy to spot.

**[FIGURE 4.4: Main Application Flow Diagram]**
*Placeholder: Flowchart showing the circular flow: Main Menu → Choose Category → Choose Attack → Gather Parameters → Validate → Execute → Results → back to Main Menu, with Ctrl+C handling shown as an exit from Execute*

---

## 4.3 Attack Module Architecture

I organized the 15 attacks into four groups based on what they target. Let me explain the architecture of each group.

### 4.3.1 WiFi Attack Modules (8 total)

Each WiFi attack is its own Python class in the wifi/ folder. They all follow the same pattern:

**BeaconBroadcaster** - Broadcasts fake WiFi networks. Takes interface, SSID, and number of beacons as parameters.

**APNetworkFlooder** - Broadcasts multiple fake networks from a wordlist. Same interface concept but loads network names from a file.

**NetworkScanner** - Listens to WiFi traffic and displays networks and devices. Uses airodump-ng to do the heavy lifting.

**DeauthAttack** - Kicks devices off the network by sending deauth frames. Targets either a specific SSID or a specific device MAC address.

**ESSIDBruteforcer** - Discovers hidden WiFi networks by probing for common SSID names. Listens for responses to figure out what networks exist.

**PacketCapture** - Records all WiFi traffic to a file for later analysis in Wireshark.

**HTTPDoSAttack** - Floods a web server with requests. Uses multiple threads to send requests in parallel.

**LocalNetworkDoS** - Floods a device on the local network. Finds all devices, lets the user pick one, then sends packets to overwhelm it.

All of these follow the same basic pattern internally: verify the network interface is set up correctly → ask the user for parameters → validate those parameters → run the external tool (mdk4, airodump-ng, hping3) → stream the output to the user → handle interruption (Ctrl+C) → show results.

**[FIGURE 4.5: WiFi Attack Module Class Hierarchy]**
*Placeholder: Diagram showing 8 WiFi attack classes, optionally with a base class they inherit from*

### 4.3.2 BLE Attack Modules (5 total)

The BLE attacks are different from WiFi attacks because Bluetooth uses async scanning. Multiple devices can be discovered at the same time, so I use Python's asyncio library to handle that.

**BLEDeviceScanner** - Scans for nearby Bluetooth devices and displays them in a real-time table. Shows device name, signal strength, company name, distance estimate, and when it was first/last seen.

**AirPodsSpam** - Broadcasts fake Apple AirPods advertisements. Makes nearby iOS devices think lots of AirPods are around.

**AndroidSpam** - Broadcasts fake Android/Google device advertisements. Similar to AirPods spam but targets Android devices.

**AdSpam** - Broadcasts fake Apple device advertisements (AirTags, Apple TVs, etc.). Shows how any device can pretend to be any other device in BLE.

**NameSpoof** - Changes the Bluetooth adapter name frequently. Creates a "fog" of fake device names by rotating through a list.

All BLE attacks use the bleak library, which is a Python library for BLE. It handles the low-level Bluetooth protocol stuff, so I just call functions like `BleakScanner()` and it gives me devices.

**[FIGURE 4.6: BLE Attack Module Architecture]**
*Placeholder: Diagram showing 5 BLE attack classes, with emphasis on the bleak library and async/await pattern*

### 4.3.3 Bluetooth Classic Module (1 total)

**L2CAPDoS** - Attacks the Bluetooth connection setup process. Instead of attacking BLE advertisements, this tries to open many connections at the same time to force the target device to spend CPU time handling them.

Uses the pydbus library to talk to the Bluetooth system directly.

### 4.3.4 Phishing Modules (2 total)

**FacebookPhishing** - Sets up a fake Facebook login page. When someone enters their credentials and clicks login, I save them and then redirect to the real Facebook so they don't realize they were phished.

**GooglePhishing** - Same thing but for Google login.

These work by starting an HTTP server on port 8000 and using Cloudflare Tunnel to expose it to the internet. The `cloudflared` tool automatically creates a public HTTPS URL (like `https://something.trycloudflare.com`) that I can send to my target. No SSH setup needed - they just visit the public URL, see the fake login page, and I capture their credentials.

**[FIGURE 4.7: Phishing Server Architecture]**
*Placeholder: Diagram showing HTTP server (port 8000) → Cloudflare tunnel creating public HTTPS URL → fake login page → credential capture → logging to file → redirect to real site*

---

## 4.4 UI/Console Module Design

Every attack needs to show output to the user. Instead of having each attack write its own print statements with its own colors and styles, I created a UI module that all attacks use. This makes everything look consistent.

### 4.4.1 Color System

The console.py module defines color constants using ANSI escape codes:

- Regular colors: RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, BLACK
- Light versions: LIGHT_RED, LIGHT_GREEN, LIGHT_CYAN, etc.
- Styles: RESET, BRIGHT, BOLD, UNDERLINE, etc.

These are just strings like `'\033[31m'` (the escape code for red). When you print a string with `RED` in front of it and `RESET` at the end, the terminal shows it in red.

### 4.4.2 Message Type Functions

I created helper functions so attacks don't have to deal with the escape codes directly:

**`iprint(text)`** - Prints an info message in light blue with an `[INFO]` prefix. Used for status updates like "Starting attack..." or "Found 5 networks".

**`wprint(text)`** - Prints a warning in yellow with a `[WARN]` prefix. Used for things like "Missing tool" or "Adapter not in monitor mode".

**`eprint(text)`** - Prints an error in red with an `[ERROR]` prefix. Used when something goes wrong.

**`sprint(text)`** - Prints a success message in green with no prefix. Used to celebrate when an attack finishes successfully.

**`cprint(text, color)`** - Prints custom colored text. Used for regular output during attacks, often in cyan to show data flowing.

**`cinput(prompt, color)`** - Gets colored input from the user. The prompt is shown in the specified color so users know what to do.

### 4.4.3 Formatting Utilities

Beyond colored text, I have utilities for common formatting tasks:

**`clear()`** - Clears the terminal screen. Works on both Windows and Linux.

**`print_banner(text, color)`** - Prints a centered header with border lines. Used at the start of each attack to show which attack is running.

**`print_line(color)`** - Prints a horizontal line. Used to separate sections of output.

These simple functions make the UI look professional without requiring any attack code to think about formatting.

### 4.4.4 Design Benefits

This centralized UI approach has several advantages:

- **Consistency:** All attacks look the same. Users know that red means error, green means success, cyan means information.
- **Message Hierarchy:** Information messages, warnings, and errors are visually distinct, so users can quickly scan output.
- **Easy to Update:** If I want to change all info messages from light blue to cyan, I only change it in one place.
- **Cross-Platform:** Works on both Windows (cmd.exe) and Linux (bash, sh).
- **User Learning:** Clear visual feedback helps new users understand what's happening.

**[FIGURE 4.8: UI Color Scheme & Message Types]**
*Placeholder: Screenshot or diagram showing examples of [INFO] messages in light blue, [WARN] in yellow, [ERROR] in red, success in green, colored data in cyan*

---

## 4.5 Data Flow Diagrams

### 4.5.1 WiFi Attack Execution Flow

Here's what happens when you run a WiFi attack like deauthentication:

1. **Ask for Interface:** "What WiFi interface do you want to use?" User enters "wlan1mon"
2. **Verify Setup:** Check that the interface actually exists and is in monitor mode
3. **Ask for Target:** "What network/device do you want to attack?" User enters a BSSID or ESSID
4. **Validate Target:** Check that the target looks valid (MAC address format, etc.)
5. **Ask for Duration:** "How long should the attack run?" User enters a number
6. **Prepare Command:** Build the mdk4 command with the right parameters
7. **Execute:** Run mdk4 as a subprocess
8. **Stream Output:** Show each line of mdk4's output to the user as it happens
9. **Handle Interruption:** If the user presses Ctrl+C, stop mdk4 and clean up
10. **Show Results:** Display "Attack completed successfully!" or error if something went wrong

**[FIGURE 4.9: WiFi Attack Execution Flow]**
*Placeholder: Flowchart showing the 10-step flow above: User input → Interface verification → Target input → Target validation → Duration input → Command building → Execution → Output streaming → Ctrl+C handling → Results display. Should show decision points for validation and error paths.*

### 4.5.2 BLE Scanning & Spoofing Flow

BLE attacks work differently because they use async/await:

**For Device Scanner:**
1. **Start Scanner:** Create a BleakScanner and start it
2. **Discover Devices:** As devices are found, add them to a dictionary
3. **Enrich Data:** Look up company names, calculate distance from signal strength
4. **Update Display:** Show a real-time table that updates as new devices are seen
5. **Track Timing:** Remember when each device was first seen and last updated
6. **Loop Until Ctrl+C:** Keep scanning and updating the display

**For Advertisement Spoofing:**
1. **Generate Advertisements:** Create fake BLE advertisement payloads (fake AirPods, fake Apple devices, etc.)
2. **Set Interval:** Decide how often to broadcast (e.g., every 200ms)
3. **Loop:** Broadcast the advertisement repeatedly
4. **Rotate if Needed:** Some attacks change the advertisement each time to create more confusion
5. **Run Until Ctrl+C or Timeout:** Keep going until user stops it or timer runs out
6. **Cleanup:** Stop the advertisement broadcast

### 4.5.3 Phishing Server Flow

The phishing attacks work like a web application:

1. **Start Server:** Create an HTTP server listening on port 8000
2. **Setup Cloudflare Tunnel:** Launch `cloudflared tunnel --url http://127.0.0.1:8000` to expose the server to the internet and generate a public HTTPS URL (e.g., `https://something.trycloudflare.com`)
3. **Display Instructions:** Show the user the public URL to send to their target
4. **Wait for Connection:** The HTTP server sits and waits for someone to visit the public URL
5. **Serve Fake Page:** When someone visits, serve the fake Facebook or Google login page
6. **Capture Credentials:** When they submit the form, read their username and password
7. **Log Credentials:** Save username/password to a file with timestamp and IP address
8. **Redirect:** Send them to the real Facebook/Google login page
9. **Display Success:** Show the user that credentials were captured
10. **Repeat:** Wait for the next target

---

## 4.6 Core Implementation Patterns

Rather than explaining every detail of every attack, let me show the key patterns that make the system work.

### 4.6.1 Attack Module Base Pattern

Every attack class follows the same basic structure:

```python
class AttackName:
    def __init__(self, parameters):
        # Store what the user asked for
        self.interface = interface
        self.target = target
        self.duration = duration
    
    def validate_parameters(self):
        # Check that parameters make sense
        # Verify interface exists
        # Verify target format is correct
        return is_valid
    
    def execute(self):
        # Do the actual attack
        # Run subprocess or call library
        # Stream output to user
    
    def display_results(self):
        # Show what happened
        # Success/failure message
        # Summary of packets sent, devices found, etc.
```

This structure means:
- All attacks have the same "contract" - they can be called the same way
- Adding a new attack is straightforward - copy this pattern
- Each attack knows how to validate itself
- Execution is separated from results display

### 4.6.2 Subprocess Integration Pattern

WiFi attacks use external tools, so they need to run subprocesses. This is the pattern:

```python
def attack_by_mac(self, target_mac):
    try:
        iprint(f"Targeting device: {target_mac}")
        iprint("Starting deauthentication frames (Ctrl+C to stop)\n")
        
        # Build command as a list
        cmd = ['mdk4', self.interface, 'd', '-t', target_mac]
        
        # Start the subprocess
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Stream output in real-time
        while True:
            output = process.stdout.readline()
            if output:
                cprint(output.rstrip(), CYAN)
            
            # Check if process ended
            if process.poll() is not None:
                break
        
        sprint("Deauthentication attack completed!")
        return process.returncode == 0
        
    except KeyboardInterrupt:
        wprint("\nAttack stopped by user")
        process.terminate()
        return False
    except Exception as e:
        eprint(f"Error: {e}")
        return False
```

Why this pattern works:
- **Building command as list:** Subprocess handles quoting and escaping automatically
- **Real-time streaming:** User sees output as it happens, not all at the end
- **Ctrl+C handling:** Gracefully stops the tool when user interrupts
- **Error checking:** Return code tells us if the tool succeeded
- **Cleanup:** Subprocess is properly terminated on error

### 4.6.2b WiFi Packet Crafting with Scapy

Before we send packets via subprocess (mdk4), we need to understand how to construct them. Here's how the beacon broadcast attack builds WiFi frames:

```python
from scapy.all import RadioTap, Dot11, Dot11Beacon, Dot11Elt

def create_beacon_frame(self, ssid, bssid, channel):
    """Create a WiFi beacon frame with the given SSID and MAC address."""
    # Build frame layers from bottom to top
    frame = (RadioTap() /                          # Radio header for TX info
             Dot11(addr1="ff:ff:ff:ff:ff:ff",     # Destination (broadcast)
                   addr2=bssid,                    # Source (our fake BSSID)
                   addr3=bssid) /                  # BSSID (same as source)
             Dot11Beacon(cap=0x2401) /             # Beacon capabilities
             Dot11Elt(ID="SSID", info=ssid) /     # SSID information element
             Dot11Elt(ID="Rates",                 # Supported rates
                     info="\x82\x84\x8b\x96") /
             Dot11Elt(ID="DSset",                 # Channel information
                     info=chr(channel)))
    return frame
```

Key concepts:
- **Layer stacking:** Each `/` adds another protocol layer
- **RadioTap:** Contains transmission parameters (power, antenna, etc.)
- **Dot11:** WiFi frame header with MAC addresses
- **Dot11Beacon:** Makes this a beacon frame (network announcement)
- **Dot11Elt:** Information elements (SSID, supported rates, channel)
- **MAC addresses:** `addr1` = destination, `addr2` = source, `addr3` = BSSID
- **Broadcast:** `ff:ff:ff:ff:ff:ff` means everyone hears it

Once the frame is built, mdk4 injects it into the WiFi interface using monitor mode.

### 4.6.3 Async BLE Scanning Pattern

BLE scanning uses Python's asyncio to handle multiple devices at once:

```python
async def scan_devices(self, duration):
    scanner = BleakScanner()
    await scanner.start()
    
    # Let it run for the specified duration
    await asyncio.sleep(duration)
    
    devices = await scanner.get_discovered_devices()
    
    await scanner.stop()
    
    return devices
```

The key difference from WiFi:
- **Async/await:** Allows scanning multiple devices concurrently
- **No blocking:** While scanning one device, we can process others
- **Natural:** Code reads like "start → wait → get results → stop"

### 4.6.4 Menu Handler Dispatch Pattern

The main menu system uses a dictionary to route choices to the right action method:

```python
def handle_wifi_menu(self, choice):
    """Send the user's choice to the right attack."""
    action_map = {
        '1': self.action_beacon_broadcast,
        '2': self.action_ap_network_flood,
        '3': self.action_network_scanner,
        '4': self.action_deauth_attack,
        '5': self.action_essid_bruteforce,
        '6': self.action_packet_capture,
        '7': self.action_http_dos,
        '8': self.action_local_dos,
    }
    
    if choice in action_map:
        action_map[choice]()
    else:
        eprint("That's not a valid choice")
```

Why this is better than if-elif chains:
- **Scalable:** Adding a new attack is just one line
- **Readable:** Easy to see all options at a glance
- **Maintainable:** Changes are localized to the dictionary
- **No duplication:** The pattern is the same for WiFi, BLE, Bluetooth, and Phishing menus

---

## Summary

The architecture of this application is built on several key principles:

1. **Modularity:** Each attack is its own class, completely independent
2. **Consistency:** All attacks follow the same validate → execute → display pattern
3. **Separation of Concerns:** UI layer separate from attack logic separate from system calls
4. **Extensibility:** Adding a new attack takes just a few lines of code
5. **User Experience:** Color-coded messages and consistent menu structure guide users
6. **Error Handling:** Graceful degradation - if something fails, the app doesn't crash
7. **Simplicity:** Complex tasks (subprocess calls, BLE scanning) are hidden behind simple function calls

This design made it possible to build 15 different attacks while keeping the code organized and maintainable. It also makes the code easier to learn from and modify, which was important for an educational project.

**Check Appendix D for full source code and class diagrams.**
