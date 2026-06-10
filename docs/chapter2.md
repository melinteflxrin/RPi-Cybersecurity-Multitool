# Chapter 2: Domain Analysis – WiFi & Bluetooth Security

This chapter explains the security concepts behind the attacks I implemented. Before writing code, I needed to understand how WiFi and Bluetooth actually work and where they're vulnerable. This chapter covers the motivation for the project, the Flipper Zero device that inspired it, the technical fundamentals of each protocol, and why this tool fills an educational gap that existing solutions don't address.

---

## 2.0 Motivation, Use Cases & Problem Analysis

### 2.0.1 Educational Gap in Cybersecurity

There's a disconnect between what students learn in cybersecurity courses and what they can actually do hands-on. Courses teach WiFi protocol layers, encryption algorithms, and Bluetooth pairing processes — but students rarely get to see these concepts in action. They learn that deauthentication attacks exploit unprotected management frames, but they never actually send a deauthentication frame and watch a device disconnect.

This gap exists for several reasons:

**Tool integration complexity.** To perform even a simple WiFi attack, a student needs to understand how to put a WiFi adapter into monitor mode, how to use airodump-ng to find targets, how to use aireplay-ng or mdk4 to send packets, and how to interpret the output. That's 3-4 different tools just for one attack. For a full lab covering WiFi, Bluetooth, and phishing, students would need to learn 5-10 different tools with different interfaces, command-line arguments, and output formats.

**Cost barriers for institutions.** Professional security testing platforms like those from Rapid7 or Tenable cost $5,000 or more per deployment. Even the Flipper Zero, a portable hacking tool that inspired this project, costs $399 per unit. For a university lab with 20 stations, that's $8,000 just for Flipper Zeros — and they don't even show students the source code. My platform costs approximately $50 per station (a $15 Raspberry Pi Zero 2 W plus a $35 WiFi adapter), making large-scale classroom deployment realistic.

**Transparency need.** Most security tools are either closed-source commercial products or complex open-source frameworks with thousands of lines of code. Students who use Metasploit or the Flipper Zero can execute attacks, but they can't easily see how the attack works underneath. They press a button, something happens, and they move on. This is the opposite of education — it's the "black box" problem. Students need to see the actual code that crafts a deauthentication frame or constructs a fake BLE advertisement to truly understand the vulnerability.

### 2.0.2 Real-World Use Cases

This platform addresses several practical scenarios:

**Use Case 1: University Cybersecurity Lab.** An instructor teaching a network security course needs a way to demonstrate WiFi vulnerabilities in a controlled classroom environment. With this platform, each student station costs ~$50, and students can run attacks like deauthentication, beacon broadcasting, and BLE scanning against a test network set up specifically for the class. The open-source code means students can read how each attack works, modify it for exercises, and learn both security concepts and software engineering patterns simultaneously.

**Use Case 2: Penetration Testing Training.** Junior security professionals preparing for certifications like CEH (Certified Ethical Hacker) or OSCP (Offensive Security Certified Professional) need hands-on practice before spending $1,000+ on course equipment and exam fees. This platform provides a $50 practice environment where they can learn attack techniques, understand tool integration, and build foundational skills. The modular code structure also teaches them how real security tools are built internally.

**Use Case 3: Home Network Security Assessment.** Network administrators who want to test their own network defenses can use the platform to scan for nearby WiFi networks, test whether their router is vulnerable to deauthentication attacks, and check which BLE devices are broadcasting in their environment. The packet capture feature allows them to record traffic for analysis in Wireshark, which is the industry standard for network forensics.

**Use Case 4: Security Research.** Researchers analyzing WiFi and Bluetooth vulnerability patterns can use the platform as a starting point. Because the code is open source and modular, they can modify specific attack modules, add measurement instrumentation, and publish findings with a reproducible methodology. The consistent attack interface (validate → execute → display) makes it straightforward to automate testing across different configurations.

**Use Case 5: Security Awareness Training.** Organizations can use the phishing modules to demonstrate how easy it is to create a convincing fake login page. Showing a non-technical audience a live phishing demonstration — where a fake Facebook page captures credentials and the attacker sees them in real-time — is far more persuasive than a PowerPoint slide about phishing risks. This builds security culture and helps justify investments in security infrastructure.

### 2.0.3 Educational Value Proposition

The platform provides educational value on multiple levels:

- **Transparency:** Every attack's source code is available for inspection. Students can read exactly how a beacon frame is constructed, how BLE advertisements are spoofed, or how a phishing server captures credentials.
- **Learning by Doing:** Students don't just read about vulnerabilities — they execute attacks in a controlled environment and observe the effects firsthand.
- **Architecture Lessons:** The modular design (separate modules for WiFi, BLE, Bluetooth Classic, and phishing) illustrates software engineering principles like separation of concerns, single responsibility, and the strategy pattern.
- **Workflow Understanding:** Students see how individual tools (aircrack-ng, mdk4, hping3, bleak) integrate into a unified workflow, which mirrors how professional security assessments combine multiple tools.
- **Reproducibility:** The complete source code and setup instructions enable independent verification and extension of every attack.
- **Customization:** Students can modify attack parameters, add new attacks, or change the UI — something impossible with closed-source alternatives.

### 2.0.4 Comparison to Existing Solutions

**vs. Kali Linux / Individual Tools:**
Kali Linux ships with hundreds of security tools, but using them requires significant expertise. A student who wants to perform a deauthentication attack needs to know that they should use `airmon-ng` to enable monitor mode, `airodump-ng` to find the target, and `aireplay-ng` or `mdk4` to send the frames. Each tool has its own command-line interface, output format, and error messages. Our platform wraps these tools behind a simple menu system: pick "WiFi Attacks" → "Deauthentication" → enter the target, and the platform handles the rest. Beginners can start immediately; experts can still access the underlying tools if they want to.

**vs. Flipper Zero (Inspiration & Limitations):**
The Flipper Zero is a portable multi-tool device that can perform WiFi attacks, BLE spam, Sub-GHz radio analysis, infrared control, and NFC operations. It costs $399+ and is closed source, meaning students can't inspect how its attacks are implemented. It's also computationally limited — it runs on an STM32 microcontroller with 256 KB of RAM, which restricts what it can do. Our platform runs on a Raspberry Pi with 512 MB of RAM and a full Linux operating system, providing desktop-class performance with complete code transparency. The Flipper Zero excels at portability; our platform excels at educational depth and affordability. Section 2.1 explores this comparison in detail.

**vs. Commercial Enterprise Tools:**
Professional security platforms (Metasploit Pro, Burp Suite Professional, Nessus) optimize for efficiency and coverage. They're designed for professional penetration testers who need to assess large networks quickly. They don't teach how attacks work — they just run them. Their licensing costs ($1,000-10,000+ per year) make them impractical for student labs. Our platform is free, open source, and designed specifically for learning.

**Our Position:**
This platform occupies a unique position: it's affordable enough for classroom deployment (~$50 per station), transparent enough for educational inspection (full source code), and comprehensive enough to demonstrate real security concepts across WiFi, Bluetooth, and phishing domains. It's not trying to replace professional tools — it's trying to teach students how those tools work.

---

## 2.1 Flipper Zero Device: Inspiration & Reality

### 2.1.1 What is Flipper Zero?

The Flipper Zero is a portable hacking device designed for security researchers and hobbyists. It was launched via Kickstarter in 2020 and has become one of the most popular consumer security tools.

**Hardware specifications:**
- Processor: STM32WB55 (ARM Cortex-M4 + Cortex-M0+, 64 MHz)
- RAM: 256 KB SRAM + 1 MB Flash
- Display: 1.4" monochrome LCD (128×64 pixels)
- Battery: 2000 mAh (lasts several days with normal use)
- Form factor: Compact, pocket-sized (~100×40×25 mm)
- Price: $169 base + modules ($399+ fully equipped)

**Built-in modules:**
- Sub-GHz radio: Transmit and receive on frequencies below 1 GHz (garage doors, car key fobs, weather stations)
- 125 kHz RFID: Read and emulate low-frequency RFID cards
- NFC: Read, write, and emulate NFC tags and cards
- Infrared: Universal remote control for TVs, air conditioners, etc.
- GPIO: General-purpose pins for hardware hacking
- Bluetooth Low Energy: BLE scanning and simple attacks
- WiFi (via add-on module): Limited WiFi capabilities with ESP32 board

**Use cases:**
The Flipper Zero is used for security testing, hardware research, education, and general tinkering. Its appeal is portability — you can carry it in your pocket and test devices on the go. Its dolphin mascot and gamified interface make it approachable for beginners.

**Why it inspired this project:**
The Flipper Zero showed me that a small, affordable device could perform meaningful security operations. But it also showed me the limitations of closed-source, hardware-constrained platforms. I wanted to build something that went deeper educationally — where students could read every line of code, modify attacks, and understand the protocols at a fundamental level.

### 2.1.2 Flipper Zero's WiFi Module

The Flipper Zero's WiFi capabilities come from an optional ESP32-based module (the WiFi Devboard). This module provides:

- **Beacon broadcasting:** Creating fake WiFi networks that appear in nearby devices' network lists
- **Deauthentication attacks:** Sending disconnect frames to kick devices off networks
- **Network scanning:** Discovering nearby WiFi networks and connected devices

These are the same core WiFi capabilities our platform provides. However, the Flipper's WiFi module is limited by the ESP32's processing power and the closed-source firmware. Users can run attacks but can't see how frames are constructed or modify the behavior. Our platform uses mdk4 and aircrack-ng on a full Linux system, giving users complete control over every parameter and the ability to inspect the actual commands being executed.

### 2.1.3 Flipper Zero's Bluetooth Module

The Flipper Zero has built-in BLE capabilities:

- **BLE spam attacks:** Broadcasting fake device advertisements (similar to our AirPods spam and Android spam)
- **Device tracking:** Scanning for and tracking BLE devices
- **Bluetooth Classic attacks:** Limited support for some Classic Bluetooth operations

Our platform matches these capabilities with BLE device scanning, AirPods spam, Android spam, Apple ad spam, and name spoofing attacks. We also add Bluetooth Classic L2CAP DoS attacks, which the Flipper handles differently due to its limited Bluetooth Classic support.

### 2.1.4 Other Modules We Didn't Implement (Why & Why Not)

**Sub-GHz Module:**
The Flipper Zero's most distinctive feature is its Sub-GHz radio, which can interact with devices operating below 1 GHz — garage door openers, car key fobs, weather stations, and remote controls. We didn't implement this because:
- No affordable SDR (Software-Defined Radio) hardware was found that worked reliably with the Raspberry Pi
- Entry-level SDRs like HackRF One ($300+) or USRP ($700+) would significantly increase the platform cost
- Sub-GHz attacks require extensive research into proprietary protocols, adding 3+ months of development time
- The educational focus of this project is WiFi and Bluetooth, not radio frequency analysis

**Infrared Module:**
The Flipper Zero includes an infrared transmitter/receiver for controlling TVs and other IR devices. We didn't implement this because:
- IR control is not related to cybersecurity education
- It would require additional hardware (IR LED and receiver)
- The educational value is minimal for a security-focused thesis

**NFC Module:**
NFC (Near Field Communication) allows the Flipper to read, write, and emulate contactless cards. We didn't implement this because:
- NFC security is a separate domain from WiFi/Bluetooth
- It would require an NFC reader/writer module
- The scope would expand beyond what's practical for a bachelor thesis

These exclusions were intentional design decisions, not limitations. By focusing on WiFi, Bluetooth, and phishing, the platform provides depth rather than breadth in the domains most relevant to introductory cybersecurity education.

---

## 2.2 WiFi Security Fundamentals

This section explains the WiFi concepts that underlie the 8 WiFi attacks implemented in the platform.

### 2.2.1 802.11 Protocol Stack

WiFi networks operate using the IEEE 802.11 family of standards. Understanding the protocol stack is essential for understanding why the attacks in this platform work.

**Physical Layer (PHY):**
The physical layer handles the actual radio transmission. WiFi operates primarily on two frequency bands:
- **2.4 GHz:** Channels 1-14 (varies by region). Longer range (~30-50m indoors), more interference from other devices (microwaves, Bluetooth, baby monitors). Used by 802.11b/g/n.
- **5 GHz:** Channels 36-165. Shorter range (~10-20m indoors), less interference, higher bandwidth. Used by 802.11a/n/ac/ax.

Our TP-Link Archer T2U PLUS WiFi adapter supports both bands, allowing attacks on both 2.4 GHz and 5 GHz networks.

**MAC Layer:**
The MAC (Media Access Control) layer manages how devices share the radio medium. It defines three types of frames:

1. **Management frames:** Used for network discovery and connection management. This includes:
   - **Beacon frames:** Sent by access points (routers) every ~100ms to announce their presence. These contain the network name (SSID), supported data rates, and security capabilities. Our beacon broadcast attack creates fake beacon frames to spoof networks.
   - **Probe request/response:** Sent by client devices to find networks. Our ESSID bruteforce attack sends probe requests with common network names to discover hidden networks.
   - **Authentication/deauthentication frames:** Used to join or leave a network. Our deauthentication attack sends forged deauthentication frames to disconnect devices.

2. **Control frames:** Used for flow control (RTS/CTS, ACK). Not directly exploited by our attacks.

3. **Data frames:** Carry the actual network traffic. Our packet capture tool records these frames for analysis.

**Critical vulnerability:** Management frames are NOT encrypted or authenticated in standard WiFi (pre-WPA3). This means anyone with a monitor-mode WiFi adapter can forge management frames and inject them into the network. This is the fundamental vulnerability that makes deauthentication attacks, beacon spoofing, and ESSID enumeration possible.

### 2.2.2 WiFi Authentication Methods

WiFi networks use authentication to control who can connect. The evolution of WiFi security shows a progression from weak to strong:

**WEP (Wired Equivalent Privacy):**
The original WiFi encryption from 1997. Uses RC4 stream cipher with a 24-bit initialization vector (IV). Critically flawed — the short IV means key material is reused, allowing attacks to recover the key in minutes. WEP has been deprecated since 2004 and should never be used.

**WPA (WiFi Protected Access):**
Introduced in 2003 as a temporary fix for WEP. Uses TKIP (Temporal Key Integrity Protocol) which rotates keys more frequently. Better than WEP but still vulnerable to dictionary attacks against the pre-shared key.

**WPA2 (WiFi Protected Access 2):**
The current standard since 2004, using AES-CCMP encryption. Significantly stronger than WPA. However, the 4-way handshake used to establish connections can be captured and subjected to offline dictionary attacks. This is the basis for PMKID-based password cracking (which we removed from our platform due to memory constraints on the Raspberry Pi — see Section 5.1.3).

**WPA3 (WiFi Protected Access 3):**
The newest standard (2018), using SAE (Simultaneous Authentication of Equals) which provides forward secrecy and protection against offline dictionary attacks. WPA3 also introduces Protected Management Frames (PMF), which encrypts management frames and mitigates deauthentication attacks. However, WPA3 adoption is still limited — most home routers use WPA2, which is why our deauthentication attack works on modern networks.

**4-Way Handshake:**
When a device connects to a WPA2 network, it performs a 4-way handshake:
1. Access point sends a random number (ANonce) to the client
2. Client generates its own random number (SNonce), computes the Pairwise Transient Key (PTK), and sends a message with the SNonce and a Message Integrity Code (MIC)
3. Access point computes the same PTK and sends the Group Temporal Key (GTK)
4. Client confirms receipt

This handshake can be captured with our packet capture tool and analyzed in Wireshark. The captured handshake could theoretically be cracked offline to recover the WiFi password, but we removed this capability because the Pi's limited memory cannot run hashcat effectively.

### 2.2.3 Common WiFi Vulnerabilities

Our platform demonstrates several categories of WiFi vulnerabilities:

**Deauthentication Attacks:**
WiFi deauthentication frames tell a device to disconnect from the network. Because management frames are unprotected in WPA2, any device in monitor mode can forge these frames. The attacker spoofs the source MAC address to look like the access point and sends a deauthentication frame to the target. The target device sees what appears to be a legitimate disconnect command and complies. This is implemented in our `deauth_attack.py` module using mdk4.

**SSID Enumeration:**
Hidden networks don't broadcast their name in beacon frames, but they still respond to probe requests that contain the correct SSID. Our ESSID bruteforce attack sends probe requests with common network names (from a wordlist file) and listens for responses. If the network responds, we've discovered its name. This attack is implemented in our `essid_bruteforce.py` module.

**Beacon Spoofing:**
Any device in monitor mode can broadcast beacon frames with arbitrary SSIDs. This creates fake networks that appear in nearby devices' WiFi lists. Our `beacon_broadcast.py` and `ap_network_flood.py` modules demonstrate this by broadcasting one or many fake networks simultaneously using mdk4.

**Network-Level DoS:**
Once on a local network, an attacker can flood a target device with packets. Our `localdos.py` module uses arp-scan to discover devices on the network, then uses hping3 to send a continuous stream of SYN packets to the target. This overwhelms the target's ability to handle new connections. In testing, this attack caused an iPhone to completely freeze within seconds.

**HTTP Flooding:**
Web servers can be overwhelmed by sending many requests simultaneously. Our `http_dos.py` module uses 50 threads to send HTTP requests with randomized User-Agent headers. While this is not powerful enough to take down a real production server (which would require a distributed attack from thousands of sources), it effectively demonstrates the concept of resource exhaustion.

### 2.2.4 Attack Surface in Educational Context

**Why these attacks matter for education:**

Understanding WiFi attacks is essential for defending against them. Network administrators who have seen a deauthentication attack in action are more likely to:
- Enable WPA3 with Protected Management Frames (PMF) on their routers
- Monitor for suspicious management frames using intrusion detection systems
- Understand why SSID hiding is not a security measure (since hidden networks can be enumerated)
- Implement proper network segmentation to limit the impact of local DoS attacks

**Defense mechanisms:**
Each attack has corresponding defenses that students should understand:
- **Against deauthentication:** Enable WPA3 with PMF, or use 802.11w Management Frame Protection
- **Against SSID enumeration:** Don't rely on hidden SSIDs as a security measure; use strong WPA2/3 passwords instead
- **Against beacon spoofing:** Client devices should verify network identity through certificate-based authentication (802.1X)
- **Against local DoS:** Rate limiting, network segmentation, and intrusion detection systems
- **Against HTTP flooding:** Load balancers, Web Application Firewalls (WAF), and rate limiting

---

## 2.3 Bluetooth Security Fundamentals

This section covers the Bluetooth concepts behind the 5 BLE attacks and 1 Bluetooth Classic attack implemented in the platform.

### 2.3.1 Bluetooth Low Energy (BLE) Protocol

Bluetooth Low Energy (BLE), also called Bluetooth Smart, was introduced in Bluetooth 4.0 (2010). It's designed for low-power devices that need to communicate small amounts of data — fitness trackers, smart home sensors, wireless earbuds, and location beacons.

**BLE vs. Bluetooth Classic:**
BLE and Bluetooth Classic are separate protocols that happen to share the Bluetooth name. Key differences:
- **Power consumption:** BLE uses significantly less power, enabling years of battery life for small devices
- **Data rate:** BLE transfers less data (1-2 Mbps vs. 3 Mbps for Classic)
- **Connection model:** BLE supports connectionless communication through advertisements, while Classic requires explicit pairing
- **Range:** Both typically reach 10-30 meters indoors

**Advertisement Frames:**
BLE devices communicate their presence by broadcasting advertisement frames. These are short packets (up to 31 bytes of payload) sent on three dedicated advertising channels (37, 38, 39) in the 2.4 GHz band. Advertisements contain:
- **Device address:** A 6-byte address (similar to a MAC address) that can be either public (fixed) or random (changing)
- **Advertisement data:** Structured fields containing device name, manufacturer data, service UUIDs, TX power level, and flags
- **Manufacturer-specific data:** A 2-byte company identifier followed by arbitrary data specific to the manufacturer

**How scanning works:**
When a device (like a smartphone) wants to discover nearby BLE devices, it enters a scanning mode where it listens on the advertising channels. Each advertisement it receives is processed to extract the device's name, signal strength (RSSI), and manufacturer information. Our BLE device scanner (`device_scanner.py`) uses the bleak library to perform this scanning asynchronously, collecting advertisements from all nearby devices and displaying them in a real-time table.

**Company identifiers:**
The Bluetooth SIG (Special Interest Group) maintains a registry of company identifiers — 2-byte codes assigned to each manufacturer. For example, Apple is `0x004C`, Google is `0x006B`, and Samsung is `0x0075`. Our platform uses a YAML database of these identifiers to display the manufacturer name for each discovered device.

### 2.3.2 BLE Spam & Manipulation

BLE advertisements are inherently trusting — there is no built-in authentication mechanism to verify that an advertisement actually comes from the device it claims to be. This creates several attack opportunities that our platform demonstrates:

**Advertisement Spoofing:**
Any device with a Bluetooth adapter can broadcast advertisements claiming to be any type of device. Our AirPods spam attack (`airpods_spam.py`) broadcasts fake Apple AirPods advertisements using Apple's manufacturer ID (`0x004C`) and the correct advertisement format for AirPods proximity pairing. When an iPhone receives these advertisements, it displays a pairing popup — even though no real AirPods exist. The fake advertisements include randomized battery levels to make each packet unique and prevent the iPhone from filtering duplicates.

**Apple Device Spoofing:**
Similar to AirPods spam, our Apple ad spam attack (`ad_spam.py`) broadcasts advertisements pretending to be various Apple devices — AirTags, Apple TVs, HomePods, and more. This triggers different types of notifications on nearby iOS and macOS devices, creating confusion and demonstrating the lack of advertisement verification.

**Android Device Spoofing:**
Our Android spam attack (`android_spam.py`) targets Google Play Services and Samsung devices by broadcasting advertisements with the appropriate manufacturer data. This shows that the vulnerability is not Apple-specific — all BLE implementations that trust advertisements without verification are affected.

**Device Name Spoofing:**
Our name spoofer attack (`name_spoofer.py`) rapidly changes the Bluetooth adapter's name using the `btmgmt` system tool. This creates a "fog" of fake device names in the environment, demonstrating that device names are not a reliable way to identify Bluetooth devices. The name is simply a string that any device can set to any value.

**Why these attacks work:**
BLE advertisements are designed for discoverability, not security. The protocol assumes that devices broadcasting on advertising channels are legitimate. There is no signature verification, no certificate checking, and no way for a receiving device to confirm the sender's identity based solely on the advertisement. This is a fundamental design trade-off — stronger authentication would increase power consumption and complexity, contradicting BLE's design goals.

### 2.3.3 Bluetooth Classic L2CAP

Bluetooth Classic (the older, higher-bandwidth Bluetooth protocol) uses a layered protocol stack. L2CAP (Logical Link Control and Adaptation Protocol) sits between the lower-level baseband layer and higher-level protocols like RFCOMM and BNEP.

**L2CAP's role:**
L2CAP multiplexes data from multiple higher-level protocols over a single Bluetooth connection. It handles:
- **Connection establishment:** Setting up logical channels between devices
- **Data segmentation:** Breaking large packets into smaller frames for transmission
- **Quality of service:** Negotiating parameters like bandwidth and latency

**DoS vulnerability:**
When a device receives an L2CAP connection request, it allocates resources (memory, CPU time) to handle the connection. Our L2CAP DoS attack (`l2cap_dos_attack.py`) exploits this by sending rapid L2CAP echo request packets (l2ping) to a target device. The target must process each request, consuming CPU time and potentially preventing it from handling legitimate connections. With multiple adapters sending requests simultaneously, the effect is amplified.

**Limitations:**
Modern Bluetooth implementations include rate limiting for L2CAP connections, which mitigates this attack. The target device may simply stop responding to new connection requests after receiving too many in a short period. This is an important lesson: protocols evolve to address known vulnerabilities.

### 2.3.4 Social Engineering Component

Several of our Bluetooth attacks have a social engineering dimension:

**Device naming attacks:** If an attacker can make their device appear as "Conference Room Speaker" or "IT Department Printer" in a Bluetooth scan, users might attempt to connect to it, potentially exposing sensitive data or enabling further attacks. Our name spoofer demonstrates how trivial it is to impersonate any device name.

**Fake peripheral alerts:** The AirPods and Apple ad spam attacks trigger notifications on victims' phones. These notifications ("AirPods detected nearby") can be used to:
- Distract users during a physical security assessment
- Condition users to dismiss Bluetooth notifications (which might include legitimate security warnings)
- Demonstrate the annoyance potential of unverified BLE advertisements

**Discovery and visibility issues:** BLE scanning reveals which devices are in an area, their signal strength (which correlates with distance), and their manufacturer. This information can be used for surveillance — tracking when specific devices (and their owners) enter or leave an area. Our BLE device scanner demonstrates this capability, showing MAC addresses, signal strengths, estimated distances, and first/last seen timestamps.

---

## 2.4 Application Security & Phishing

### 2.4.1 Fake Login Pages

Phishing is one of the most effective attack vectors in cybersecurity. According to Verizon's Data Breach Investigations Report, phishing is involved in over 30% of data breaches. Our platform includes two phishing modules that demonstrate why this attack is so effective.

**How phishing works:**
1. The attacker creates a replica of a legitimate website's login page (in our case, Facebook and Google)
2. The replica is hosted on a web server and made accessible to the target
3. The target visits the fake page, sees a familiar login form, and enters their credentials
4. The credentials are captured and logged by the attacker's server
5. The target is redirected to the real website, so they may not realize anything happened

**Our implementation:**
The phishing modules (`facebook_phish.py` and `google_phish.py`) use Python's built-in `http.server` module to host fake login pages. The HTML/CSS for these pages is embedded directly in the Python files and is designed to closely mimic the real login pages. When a victim submits the form, the server captures the username and password, logs them to a file with a timestamp and the victim's IP address, and redirects the victim to the real website.

**Cloudflare Tunnel for public access:**
To make the phishing page accessible beyond the local network, we use Cloudflare Tunnel (`cloudflared`). This creates an outbound connection from the Raspberry Pi to Cloudflare's edge network, which generates a public HTTPS URL (like `https://something.trycloudflare.com`). The attacker sends this URL to the target, who sees what appears to be a legitimate login page served over HTTPS.

**Educational purpose:**
The phishing modules are included strictly for educational demonstration. They show:
- How trivially easy it is to create a convincing fake login page (the Facebook replica takes less than 200 lines of HTML/CSS)
- How Cloudflare Tunnel eliminates the traditional barriers to hosting a phishing page (no port forwarding, no public IP, no SSL certificate management)
- Why users should always check the URL before entering credentials
- Why organizations need security awareness training — even technically sophisticated users can be fooled by a well-crafted phishing page

**Ethical considerations:**
Phishing attacks are illegal when performed without authorization. Our platform includes warnings at every stage reminding users that these tools are for educational purposes only. The phishing modules should only be used in controlled environments with explicit permission from all participants. The platform does not include any mechanisms for mass-distribution of phishing URLs (no email sending, no SMS, no social media integration). The educational value lies in understanding how the attack works so that students and organizations can better defend against it.

---

## 2.5 Why This Tool Fills an Educational Gap

### 2.5.1 Existing Approaches & Their Limitations

**Individual Tools (aircrack-ng, hcitool, etc.):**
These are powerful, industry-standard tools that form the backbone of most WiFi and Bluetooth security testing. However, they present several challenges for learners:
- **Learning challenge:** Students don't understand how the tools fit together. aircrack-ng is a suite of 10+ individual programs (airmon-ng, airodump-ng, aireplay-ng, aircrack-ng, etc.), each with different parameters and purposes. Understanding which tool does what — and in which order to use them — requires significant background knowledge.
- **Integration complexity:** Performing a complete attack (e.g., capturing a handshake and cracking the password) requires chaining 3-4 tools together with correct parameters. One wrong flag and the attack fails silently.
- **No unified interface:** Each tool has its own command-line interface, output format, and error handling. There's no central place to see all available attacks and choose one.
- **Cost:** The tools themselves are free, but the expertise required to use them effectively takes weeks or months to develop.

**Closed-Source Commercial Solutions:**
Enterprise security platforms like Metasploit Pro and Nessus Professional are designed for speed and coverage, not education:
- **Opacity problem:** Students can run vulnerability scans and exploits, but they can't see how the scanner identifies vulnerabilities or how exploits are constructed. This creates surface-level knowledge that doesn't transfer to new situations.
- **Cost barrier:** Professional licenses range from $1,000 to $10,000+ per year, making them impractical for student use. Free versions (Metasploit Framework, Nessus Essentials) exist but require significant configuration and lack educational scaffolding.
- **Overwhelming scope:** These platforms contain thousands of modules. A student looking for "WiFi attacks" would need to navigate hundreds of unrelated modules for web vulnerabilities, OS exploits, and network reconnaissance.

**Comprehensive Security Platforms (Metasploit, Burp Suite):**
Even the free versions of comprehensive platforms present barriers:
- **Learning curve:** Metasploit Framework alone has hundreds of commands and concepts (workspaces, sessions, payloads, encoders, auxiliary modules). Before a student can run their first WiFi attack, they need to learn Metasploit's entire workflow.
- **Overhead:** These platforms are designed for professional use cases, not education. Features like session management, pivoting, and post-exploitation are essential for real penetration testing but confusing for students learning basic WiFi security.
- **Hardware assumptions:** Most frameworks assume access to powerful hardware with multiple network interfaces. Running them on a $15 Raspberry Pi Zero 2 W would require significant adaptation.

### 2.5.2 Our Contribution

Our platform addresses these limitations with a focused, educational approach:

**Transparent implementation.** Every attack module is a single Python file with clear, commented code. A student can open `deauth_attack.py` and see exactly how the deauthentication command is constructed, how the subprocess is launched, how output is streamed, and how errors are handled. There are no abstraction layers to navigate, no plugin systems to understand, and no framework conventions to learn before reading the code.

**Guided learning path.** The menu-driven interface scaffolds discovery. New users don't need to know which tool to use or what parameters it requires — they pick an attack category (WiFi, BLE, Bluetooth Classic, Phishing), choose a specific attack, and follow the prompts. The interface validates inputs, provides clear error messages, and guides users through each step.

**Practical demonstration.** Each attack runs against real protocols and produces real effects. A deauthentication attack actually disconnects devices. BLE spam actually triggers notifications on nearby phones. The phishing server actually captures credentials. These are not simulations — they're real attacks in a controlled environment, which provides a fundamentally different learning experience than reading about vulnerabilities in a textbook.

**Research-ready.** Because the code is open source and modular, researchers can extend it without starting from scratch. Adding a new WiFi attack means writing one Python class that follows the established pattern (validate → execute → display). The platform handles menu integration, user input, error handling, and output formatting.

**Reproducible science.** The complete source code, setup instructions, and hardware specifications enable anyone to reproduce every attack. This is essential for academic research, where reproducibility is a core requirement. A reviewer can build the exact same platform, run the same attacks, and verify the same results.

**Scalable affordability.** At ~$50 per station (Raspberry Pi Zero 2 W + TP-Link WiFi adapter), universities can deploy 20 stations for $1,000 — less than the cost of two Flipper Zero devices, and with far more educational value per dollar.

**Self-Contained Learning Platform.** Everything needed to learn, set up, and execute attacks is in one repository:
- Complete setup instructions for starting with a fresh Raspberry Pi
- WiFi adapter configuration guides for the TP-Link Archer T2U PLUS
- Monitor mode enablement with driver installation instructions (RTL8821AU DKMS setup)
- Dependency installation guides for all required tools (aircrack-ng, mdk4, hping3, bluez, etc.)
- Full working code examples for all 15 attacks
- No need to gather information from multiple sources or external repositories
- Students learn from code inspection, setup experience, and attack execution — all in one place

---

## Summary

This chapter established the context for the platform's design decisions:

1. **The educational gap is real:** Students learn WiFi and Bluetooth security theory but lack hands-on practice with transparent, affordable tools.
2. **The Flipper Zero inspired the project** but its closed-source nature, $399 price, and hardware limitations motivated building an open, affordable alternative.
3. **WiFi vulnerabilities** — particularly unprotected management frames — enable attacks like deauthentication, beacon spoofing, and SSID enumeration that our platform demonstrates.
4. **BLE advertisement trust** — the lack of authentication in BLE advertising — enables spoofing attacks that our platform exploits for educational purposes.
5. **Bluetooth Classic L2CAP** connection handling can be overwhelmed by rapid connection requests, demonstrating protocol-level DoS.
6. **Phishing remains effective** because creating convincing fake login pages is trivial, and tools like Cloudflare Tunnel eliminate infrastructure barriers.
7. **Our platform fills the gap** by combining affordability, transparency, and comprehensive coverage in a single, self-contained repository.

The technical implementation of these concepts — the tools, libraries, and hardware that make them possible — is detailed in Chapter 3.
