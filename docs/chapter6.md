# Chapter 6: Flipper Zero vs Our Implementation – Feature Comparison

This chapter presents a direct comparison between the Flipper Zero — the device that inspired this project — and the platform we built. The goal is not to argue that one is "better" but to show where they overlap, where each one has advantages, and why the differences exist.

---

## 6.1 Feature Parity Analysis

Several core capabilities are shared between the Flipper Zero and our platform:

**WiFi Attacks:**
Both platforms support beacon broadcasting (creating fake WiFi networks), deauthentication attacks (disconnecting devices from networks), and network scanning (discovering nearby networks and clients). The Flipper Zero achieves this through its optional ESP32 WiFi Devboard add-on, while our platform uses the TP-Link Archer T2U PLUS USB adapter with the RTL8821AU chipset running on a full Linux system. The underlying attack concepts are identical — both craft and inject 802.11 management frames — but the implementation environments are very different.

**BLE Reconnaissance & Spam:**
Both platforms can scan for BLE devices and broadcast fake BLE advertisements. The Flipper Zero's built-in Bluetooth module supports BLE spam attacks that trigger pairing popups on iOS and Android devices. Our platform does the same through the bleak library and direct HCI socket manipulation, with support for AirPods spam, Apple device spam, Android device spam, and name spoofing.

**Multi-Attack Capability:**
Both platforms provide a unified interface for accessing multiple attack types. The Flipper Zero uses a physical screen with a D-pad for navigation; our platform uses a color-coded terminal menu system. Both allow users to switch between attack categories without restarting the application.

**Portable Deployment:**
The Flipper Zero is pocket-sized and battery-powered. Our Raspberry Pi platform is larger but still compact enough for field deployment with a portable battery pack. Neither requires a laptop or desktop computer to operate (though our platform benefits from SSH access for development).

---

## 6.2 Features We Went Beyond

Our platform includes several capabilities that the Flipper Zero does not provide:

**Local Network DoS Attack:**
The Flipper Zero has no mechanism for discovering devices on a local network and flooding them with packets. Our platform uses arp-scan to find devices on the WiFi network, then uses hping3 to send continuous SYN packet floods to a selected target. In testing, this attack caused an iPhone to freeze completely within seconds — buttons stopped responding, video and audio stopped, and the screen became unresponsive until the attack was stopped. This attack demonstrates protocol-level DoS at the network layer, which is outside the Flipper's scope.

**HTTP DoS Attack:**
Our platform includes a multi-threaded HTTP flooding tool that sends requests with randomized User-Agent headers to a target web server. The Flipper Zero has no equivalent — it cannot generate HTTP traffic or perform application-layer attacks. While our implementation is not powerful enough to affect production servers (which would require distributed attacks from many sources), it effectively demonstrates the concept of HTTP resource exhaustion.

**Phishing Simulation Suite:**
The Flipper Zero has no phishing capability. Our platform includes complete Facebook and Google login page replicas with credential capture, file-based logging, and Cloudflare Tunnel integration for public access. This demonstrates social engineering attacks — a major category of real-world threats — that the Flipper Zero cannot address.

**Comprehensive BLE Device Scanning:**
While the Flipper Zero can scan for BLE devices, our BLE device scanner provides significantly more detail: real-time RSSI tracking, distance estimation from signal strength, manufacturer identification using a YAML database of company identifiers, first-seen and last-seen timestamps, and color-coded signal strength indicators. The output is a continuously updating table that gives a complete picture of the BLE environment.

**ESSID Bruteforce:**
Our platform can discover hidden WiFi networks by sending probe requests with common network names from a wordlist file and listening for responses. The Flipper Zero does not include this capability in its standard WiFi module.

**Packet Capture for Wireshark:**
Our platform can record all WiFi traffic to .cap files with timestamps, which can be opened and analyzed in Wireshark. This is a fundamental forensics capability that the Flipper Zero's WiFi module does not support in the same way.

**Source Code Transparency:**
Every attack in our platform is a readable Python file that students can inspect, modify, and learn from. The Flipper Zero firmware is not openly modifiable in the same way — while community firmware exists, modifying attack behavior requires understanding the C codebase and reflashing the device.

---

## 6.3 Features Flipper Zero Has That We Don't

The Flipper Zero includes several modules that our platform does not implement:

**Sub-GHz Radio Attacks:**
The Flipper Zero's most distinctive feature is its CC1101 Sub-GHz transceiver, which can transmit and receive on frequencies below 1 GHz. This enables interaction with:
- Garage door openers (300-390 MHz)
- Car key fobs (rolling codes and fixed codes)
- Weather stations and remote sensors
- Wireless doorbells and remote controls

**Why we don't have this:** No affordable Software-Defined Radio (SDR) module was found that works reliably with the Raspberry Pi Zero 2 W. Entry-level SDRs like the HackRF One cost $300+, and the USRP costs $700+ — either would more than triple the platform cost. Additionally, Sub-GHz protocol research would have required 3+ months of additional development time for a bachelor thesis that focuses on WiFi and Bluetooth security. This is a scope decision, not a technical limitation.

**Infrared Control:**
The Flipper Zero includes an IR transmitter and receiver that can learn and replay infrared signals from TV remotes, air conditioners, and other IR-controlled devices.

**Why we don't have this:** Infrared control is not related to cybersecurity education. While the Flipper Zero includes it as a convenience feature, adding IR capability to our platform would require additional hardware (an IR LED and receiver module) and provide no security-relevant educational value.

**NFC Communication:**
The Flipper Zero can read, write, and emulate NFC tags and contactless cards (MIFARE, NTAG, etc.).

**Why we don't have this:** NFC security is a separate domain from WiFi/Bluetooth security. Implementing NFC attacks would require an NFC reader/writer module and extensive research into contactless card protocols. This falls outside the scope of a thesis focused on short-range wireless communication protocols (WiFi and Bluetooth).

**125 kHz RFID:**
The Flipper Zero can read and emulate low-frequency RFID cards used in access control systems.

**Why we don't have this:** Same reasoning as NFC — RFID security is a separate domain. The hardware (125 kHz antenna and reader) would need to be added, and the educational focus would shift away from the core WiFi/Bluetooth theme.

**Proprietary Flipper OS:**
The Flipper Zero runs its own custom operating system optimized for its hardware. This provides a polished user experience with animations, a dolphin mascot, and gamification elements.

**Our approach:** We run on standard Linux (Raspberry Pi OS / Debian), which provides significantly more flexibility and power. Users have access to the full Linux command line, can install additional tools, and can modify the system freely. The trade-off is a more complex setup process versus a more capable platform.

---

## 6.4 Resource Constraints Encountered

**Memory Limitations (512 MB RAM):**
The Raspberry Pi Zero 2 W has only 512 MB of shared RAM (CPU + GPU). This prevented us from implementing:
- hashcat PMKID cracking (requires 2-4 GB of RAM)
- Large-scale packet processing in Python (memory-intensive)
- Running multiple simultaneous attacks with large data buffers

**Solution:** We moved CPU-intensive operations to external tools (aircrack-ng, mdk4, hping3) that are compiled C programs and handle memory efficiently. Python serves as the orchestrator, not the packet processor. For password cracking, we recommend users transfer captured handshakes to a more powerful machine.

**Single WiFi Interface Challenge:**
When the WiFi adapter is in monitor mode (required for packet capture and injection), it cannot simultaneously connect to a WiFi network for internet access. This means:
- The Pi loses internet connectivity during WiFi attacks
- Phishing attacks that need Cloudflare Tunnel must use a separate connection (e.g., Ethernet dongle or built-in WiFi)

**Solution:** We designed the platform so WiFi attacks and phishing attacks are in separate menu categories. Users switch between them as needed. For advanced setups, a USB Ethernet adapter provides persistent connectivity.

**CPU Performance:**
The ARM Cortex-A53 at 1.0 GHz is adequate for most operations but slower than desktop systems for:
- Real-time packet processing
- Multi-threaded HTTP flooding (limited by CPU, not network)
- BLE scanning with rapid advertisement rotation

**Mitigation:** We use pre-built tools for CPU-intensive operations rather than implementing packet processing in Python. The subprocess pattern (Chapter 3, Section 3.5) lets us leverage compiled tools that run efficiently on ARM.

---

## 6.5 Why Certain Features Were Removed

**PMKID Cracking via hashcat:**
Originally planned as part of the WiFi attack suite. After implementation, we found that:
- hashcat cannot run on ARM processors without significant modification
- The Pi's 512 MB RAM is insufficient for wordlist-based cracking
- CPU-only cracking would take days for even simple passwords
- The Flipper Zero also cannot crack passwords for similar resource reasons

**Alternative:** Users can capture handshakes with our packet capture tool and transfer them to a desktop machine with a GPU for cracking. This is actually more realistic — professional penetration testers also capture on portable devices and crack on workstations.

**4-Way Handshake Capture & Cracking:**
Similar to PMKID, the capture works but the cracking is impractical on the Pi. The packet capture tool records handshakes, but offline analysis must happen on more powerful hardware.

**Sub-GHz Implementation:**
Would have required $300+ in SDR hardware plus 3+ months of protocol research. The cost and time investment exceeded what was practical for this project's scope and budget.

---

## 6.6 Comparison Table

| Feature | Flipper Zero | Our Platform | Notes |
|---------|:---:|:---:|-------|
| **WiFi** | | | |
| Beacon Broadcasting | ✅ | ✅ | Both use 802.11 frame injection |
| Deauthentication | ✅ | ✅ | Our version supports SSID, BSSID, and device-level targeting |
| Network Scanning | ✅ | ✅ | Ours uses airodump-ng for comprehensive output |
| AP Network Flood | ❌ | ✅ | Mass fake network broadcasting from wordlist |
| ESSID Bruteforce | ❌ | ✅ | Hidden network discovery |
| Packet Capture | ❌ | ✅ | .cap files for Wireshark analysis |
| HTTP DoS | ❌ | ✅ | Multi-threaded request flooding |
| Local Network DoS | ❌ | ✅ | ARP discovery + SYN flooding via hping3 |
| Password Cracking | ❌ | ❌ | Neither can do this with limited resources |
| **Bluetooth** | | | |
| BLE Device Scanner | ✅ | ✅ | Ours includes company ID lookup, distance estimation |
| BLE Spam (iOS) | ✅ | ✅ | AirPods and Apple device spam |
| BLE Spam (Android) | ✅ | ✅ | Google/Samsung device spam |
| BLE Name Spoofing | ❌ | ✅ | Rapid adapter name rotation |
| L2CAP DoS | ❌ | ✅ | Bluetooth Classic connection flooding |
| **Phishing** | | | |
| Fake Login Pages | ❌ | ✅ | Facebook and Google replicas |
| Credential Capture | ❌ | ✅ | With logging and Cloudflare Tunnel |
| **Other Modules** | | | |
| Sub-GHz Radio | ✅ | ❌ | Requires SDR hardware ($300+) |
| Infrared Control | ✅ | ❌ | Not relevant to cybersecurity education |
| NFC | ✅ | ❌ | Out of scope |
| 125 kHz RFID | ✅ | ❌ | Out of scope |
| **Platform** | | | |
| Source Code Access | ⚠️ Partial | ✅ Full | Community firmware exists for Flipper |
| Cost | $399+ | ~$50 | Raspberry Pi + WiFi adapter |
| Form Factor | Pocket-sized | Compact portable | Pi with adapter and battery |
| OS | Custom FW | Full Linux | Linux provides full flexibility |
| Extensibility | Limited | ✅ Easy | Python modules, simple pattern |
| Educational Value | Medium | High | Code transparency is the key difference |

**Legend:** ✅ = Supported, ❌ = Not supported, ⚠️ = Partially supported

---

## Summary

The Flipper Zero and our platform target different use cases with different trade-offs:

**The Flipper Zero excels at:** Portability, physical-world interaction (Sub-GHz, IR, NFC, RFID), polished user experience, and battery-powered field deployment. It's a great tool for security professionals who need a pocket-sized multi-tool.

**Our platform excels at:** Educational transparency, affordability for classroom deployment, WiFi/Bluetooth attack depth, phishing simulation, and extensibility. It's a better tool for students and educators who need to understand how attacks work at the code level.

The platforms are complementary, not competitive. A cybersecurity curriculum could use our platform for teaching fundamentals (where students need to read code and understand protocols) and the Flipper Zero for advanced demonstrations (where portability and additional modules matter). The key difference is that our platform costs 1/8th the price and provides full source code transparency — making it the clear choice for educational environments where understanding matters more than convenience.
