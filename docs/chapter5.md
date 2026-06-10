# Chapter 5: Implementation Details

## 5.1 Development Process & Challenges

### 5.1.1 Iterative Development Approach

I built the modules step by step, starting simple and adding more complex attacks as I went. I started with the basic WiFi attacks first (beacon broadcast and network scanning) to figure out how everything should work and then added more attacks once I understood the pattern.

This approach had some advantages:

- **Reusable Patterns:** The first WiFi attacks gave me a template I could use for all the other attacks
- **Error Handling:** Early attacks let me figure out how to handle errors and validate user input
- **Easy Testing:** I could test each attack independently before adding it to the main menu
- **Not Too Complicated:** I started simple to see how everything should work together

All development and testing happened directly on Raspberry Pi Zero 2 W. I wrote the code and transferred it to the device for testing using WinSCP.

### 5.1.2 Key Challenges & Solutions

**Challenge 1: Monitor Mode Setup**

To send WiFi packets or listen to WiFi traffic you need your network adapter in "monitor mode." This mode is different depending on what Linux you're using and what drivers you have.

*Solution:* I added a `verify_monitor_mode()` function in each WiFi attack to check if the wifi adapter is actually in monitor mode:
```python
def verify_monitor_mode(self):
    """Check if the network card is in monitor mode."""
    try:
        result = subprocess.run(
            ["iwconfig", self.interface],
            capture_output=True,
            text=True,
            timeout=5
        )
        return "Monitor" in result.stdout
    except Exception:
        return False
```

This stops the attacks from running on the wrong interface and gives the user a clear error message.

**Challenge 2: Driver Compatibility (RTL8821AU)**

The TP-Link WiFi adapter I used needs special drivers to work on Linux. When Linux updates, the driver breaks and needs to be recompiled.

*Solution:* I used DKMS (Dynamic Kernel Module Support) to automatically recompile the driver when Linux updates.

**Challenge 3: The Pi is Slow**

The Raspberry Pi Zero 2 W is not very powerful. It can't do heavy calculations quickly, especially things like processing packets in real-time or cracking passwords.

*Solution:* 
- I used external tools (aircrack-ng, mdk4, hping3) to do the heavy lifting instead of doing it in Python
- For the HTTP DoS attack, I used 50 threads to send requests in parallel
- I avoided storing huge amounts of data in memory, which would make the Pi very slow

**Challenge 4: Not Enough Memory**

The Pi only has 512 MB of RAM. When I tried to load big files or process lots of data, it ran out of memory.

*Solution:*
- I removed the PMKID password cracking feature (see Section 5.1.3)
- I printed output as it happened instead of saving everything in memory
- I cleaned up memory after each attack
- I only kept track of recent devices, not all of them

### 5.1.3 Why We Removed PMKID Cracking

I originally planned to add PMKID cracking. This would capture WiFi passwords and try to crack them using a tool called hashcat. But I had to remove it.

*Why it didn't work on the Pi:*

- **GPU Not Available:** hashcat is designed for GPUs, and the Pi doesn't have one
- **Way Too Slow:** Cracking a password on the Pi's CPU would take too long
- **Not Enough Memory:** hashcat needs 2-4 GB of RAM. The Pi only has 512 MB
- **Won't Compile:** The existing password cracking tools can't even run on ARM

*What I did instead:* 

Instead of making a broken feature, I focused on attacks that actually work on the Pi. I chose to have more attacks that actually work rather than trying to do complicated stuff that doesn't work on such a small device.

---

## 5.2 WiFi Attack Implementation

I built 8 WiFi attacks split into 3 groups: **scanning networks**, **breaking connections**, and **flooding attacks**. They all work the same way: check the network adapter is set up → ask the user what to attack → run the attack → show what happened.

### 5.2.1 Network Discovery Attacks

**Network Scanner & Packet Capture**

These attacks just scan the WiFi network without doing anything to it:

- **Network Scanner:** Uses a tool called airodump-ng to show all the WiFi networks nearby and the devices connected to them. Shows the network name, signal strength, encryption type, and how many devices are connected.

- **Packet Capture:** Records all the WiFi packets going by and saves them to a file (with a timestamp). You can open this file in Wireshark later to look at all the traffic. This is useful for seeing what encryption is being used and how devices are talking to each other.

Both of these are just watching, meaning I don't send any attacks, so nothing detects them.

### 5.2.2 Beacon & SSID Spoofing

**Beacon Broadcast & ESSID Bruteforce**

These attacks mess with how WiFi networks are discovered:

- **Beacon Broadcast:** Uses a tool called mdk4 to broadcast fake WiFi networks. Your phone or other devices will see these fake networks in the list of available WiFi. I can broadcast real network names, corrupted network names, or random made-up names. The point is to show that anyone can pretend to be a WiFi network.

- **ESSID Bruteforce:** Some networks don't broadcast their name, meaning they're "hidden". This attack guesses the hidden network name by trying common names from a given text file and seeing if the network responds. If it does respond, we found it. This only works if the network agrees to respond, and newer networks can turn this off.

**Note:** Newer WiFi networks have protection that makes these attacks not work. So these may only work on older networks.

### 5.2.3 Kicking Devices Off WiFi

**Deauthentication Attack**

This attack sends special WiFi signals that tell devices to disconnect from the network. I implemented two options:

- **Disconnect every device off a network:** Target a specific WiFi network name and all devices get disconnected
- **Disconnect a specific device:** You can target just one device's MAC address

WiFi uses unencrypted management frames for control purposes, including deauthentication frames that tell a device to disconnect. The mdk4 tool crafts these frames with the target device's MAC address and sends them continuously. The device sees what looks like a legitimate disconnect command from the network and disconnects.

**How it works in real life:**
- Devices get temporarily disconnected and have to reconnect
- Internet stops working while the attack is happening
- While newer WiFi networks can have protection to stop this attack, most modern home routers don't have it enabled. I tested this on my own WiFi and a test WiFi router, and both got attacked successfully. So this vulnerability exists on pretty modern routers too, not just old ones
- This shows that the disconnect messages aren't protected by default in most WiFi implementations

### 5.2.4 Flooding Attacks

**HTTP DoS & Local Network DoS**

Two different ways to overwhelm a device:

**HTTP DoS:** I send 50 requests at the same time (1000 total) to a web server. Each request pretends to be from a different browser to try to get around basic protections. Real servers can handle this easily though. You'd need thousands of sources to actually take down a real website. This is just to show how basic flooding works.

**Local Network DoS:** Instead of attacking something on the internet, this attacks devices on your local WiFi network. Here's what it does:
1. Find all devices on the network
2. You pick which one to attack
3. Flood it with network packets

The attack uses hping3 to send a continuous stream of SYN packets to the target device on a random port. This overwhelms the target's ability to handle new connections and the device spends CPU time processing each connection attempt instead of handling user input or running apps.

In practice, when I ran the attack against my iPhone, after a few seconds the device froze. Buttons didn't respond, videos stopped, audio stopped. The whole screen became unresponsive. As soon as I stopped the attack, the phone unfroze and worked normally again. This works better than internet DoS because I'm right there on the network and there's no routing delays.

**[FIGURE 5.2: WiFi Attack Execution Example Output]**
*Placeholder: Screenshot showing main menu and example WiFi attack output (beacon broadcast, deauth, or network scanner results)*

---

## 5.3 BLE (Bluetooth Low Energy) Attack Implementation

BLE is Bluetooth on the 2.4 GHz band which is different from WiFi even though they use the same frequency. I use Python's async features to handle multiple Bluetooth devices at the same time using the bleak library.

### 5.3.1 Finding Bluetooth Devices

**BLE Scanner:** Scans for Bluetooth devices nearby and shows:
- The device's MAC address and name
- How strong the signal is (RSSI)
- How far away it is (calculated from signal strength)
- What company made it (Apple, Samsung, Google, etc.)
- When we first saw it and last saw it

**How it works:** I use the bleak library to scan:
```python
scanner = BleakScanner()
await scanner.start()
devices = await scanner.get_discovered_devices()
```

Shows all Bluetooth devices nearby with their signal strength updating in real-time.

### 5.3.2 Fake Bluetooth Devices

**Four Types of Fake Device Attacks:**

1. **Fake AirPods:** Broadcasts fake Apple AirPods advertisements. I add fake battery information to make them look real. This makes the fake AirPods look exactly like real ones in the iOS settings. It shows how your phone trusts Bluetooth advertisements without actually checking if they're real.

2. **Fake Apple Devices:** Broadcasts fake Apple device advertisements; things like AirTags, Apple TVs, and other Apple products. Uses the real Apple manufacturer ID but spoofs different device types. This creates tons of fake notifications on nearby iOS/macOS devices saying "New AirTag Found" or "Apple TV Nearby," causing confusion and annoyance.

3. **Fake Android Devices:** Same as AirPods but fakes Google Play Services or Samsung devices. Sends lots of advertisements to confuse the scanning.

4. **Name Spoofer:** Changes the device name frequently cycling through names from a text file that you can customize. This shows that trusting the device name as a way to identify devices is not a good security idea, since the name can be changed whenever you want.

**What they all do:** Each one broadcasts advertisements repeatedly, making it look like lots of different devices are nearby.

**Why this matters:** Shows that Bluetooth advertisements aren't verified. Any device can pretend to be whatever it wants.

In total, I built 5 BLE attacks: one scanner and four fake device attacks (AirPods, Apple devices, Android devices, and name spoofer).

**[FIGURE 5.3: BLE Device Scanner Output]**
*Placeholder: Screenshot showing BLE scanner results with nearby devices, signal strength, company names, and battery levels*

---

## 5.4 Bluetooth Classic & Phishing

### 5.4.1 L2CAP DoS Attack

L2CAP is the part of Bluetooth that handles connections. This attack tries to open a bunch of connections at the same time, forcing the target device to handle them all. The device spends 30+ seconds dealing with each connection, so it becomes too busy to do anything else.

I use the pydbus library to try multiple connections at the same time. Modern Bluetooth can stop this pretty easily though - it just rate-limits connections from the same device.

**Why it matters:** Shows that even basic protocols like Bluetooth connection setup can be attacked. The device is too trusting when accepting connections.

### 5.4.2 Phishing Server

This is a fake login page server. I set up a website with a fake Facebook or Google login to show how easy phishing is. I use Cloudflare Tunnel to make it accessible to targets anywhere. Here's what happens:

1. Start an HTTP server on port 8000
2. Use `cloudflared tunnel` to create a public HTTPS URL (like `https://something.trycloudflare.com`)
3. Send the victim the public URL
4. They see what looks like Facebook or Google
5. They type in their username and password
6. I save their credentials
7. I redirect them to the real site so they don't know something's wrong

**How it works:**
- I have copies of the real Facebook and Google login pages (HTML and CSS)
- When someone enters their credentials and clicks login, I capture it with their IP address and timestamp
- I save it to a log file
- Then I send them to the real site

**Why it matters:** Shows how easy it is to make a fake login page and trick people into giving up their credentials. The fact that I can expose it to the internet globally with just one command (cloudflared tunnel) shows why people need to be careful about where they enter their passwords. It also shows why HTTPS and checking certificates matters - a real HTTPS site would show the real company's certificate, not a fake one.

**[FIGURE 5.4: Phishing Server Interaction]**
*Placeholder: Screenshot showing fake login page (Facebook or Google replica) and example of captured credentials in log file*

---

## 5.5 How the App Works

### 5.5.1 Initialization and Module Loading

When the app starts, it doesn't load all attack modules right away. Instead, it only imports a module when the user selects that specific attack. When the user picks an attack, the code imports that specific module, creates an instance of the attack class, runs the attack, and displays results.

### 5.5.2 Menu System Implementation

**[FIGURE 5.1: Application Main Menu]**
*Placeholder: Screenshot showing the main menu with attack categories (WiFi, BLE, Bluetooth Classic, Phishing) and submenu structure*

The app has a menu with 3 layers: Main Menu → Pick an attack type → Pick a specific attack. I use a dictionary to route choices to the right attack.

### 5.5.3 Attack Execution Workflow

**How each attack runs:**
1. **Ask for info** - Which network adapter, what to attack, how long to run, etc.
2. **Check the info** - Make sure the network adapter exists, the IP address is valid, etc.
3. **Run it** - Start the attack and show what's happening in real-time
4. **Handle Ctrl+C** - Let the user stop the attack cleanly
5. **Show results** - Tell them if it worked, how many packets, etc.

Everything is wrapped in try-except to handle errors nicely:
```python
try:
    # Run the attack
except ImportError as e:
    eprint(f"Missing module: {e}")
except KeyboardInterrupt:
    wprint("\nYou stopped the attack")
except Exception as e:
    eprint(f"Something went wrong: {e}")
```

## 5.6 Key Implementation Code Snippets

### 5.6.1 Code Organization Pattern

All attacks follow the same subprocess pattern: build the command → stream output in real-time → handle Ctrl+C → check return code. This consistency makes the codebase easy to extend with new attacks.

### 5.6.2 Menu System Integration

The menu system uses a dictionary-based dispatch pattern to route user choices to the right attack. See Chapter 4, section 4.6.4 for the detailed architectural explanation of this pattern and why it's scalable and maintainable. The same pattern is used consistently across all four attack categories (WiFi, BLE, Bluetooth Classic, Phishing).

Check Appendix C for the full source code of all 15 attacks.

---

## Summary

I built 15 security attacks: 8 WiFi, 5 BLE, 1 Bluetooth Classic, and 2 phishing. All of them follow the same basic ideas:

1. **Modular** - Each attack is its own separate Python class
2. **External tools** - I use mdk4, aircrack-ng, hping3, etc. through subprocess calls
3. **Easy to use** - Ask for info → check it → run it → show results
4. **Live output** - Show what's happening as it happens
5. **Error handling** - If something goes wrong, show a clear error message

The attacks go from simple (just scanning networks) to more complex (kicking devices off, flooding, phishing). It shows real security aspects of WiFi, Bluetooth, and users.

I kept everything simple and focused on making it work on the Raspberry Pi. This chapter shows that meaningful security testing doesn't require expensive hardware, just good planning and understanding the protocols.
