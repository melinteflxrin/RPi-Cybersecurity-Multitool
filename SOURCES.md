# Sources of Inspiration & Attribution

This document details the specific sources of inspiration used in this project.

## Project Overview

This is an **independent work** developed as a bachelor thesis project. The code is **original**, developed with educational inspiration from select open-source projects listed below.

---

## Specific Inspirations

### 1. **Jammy** (https://github.com/FLOCK4H/Jammy)
**Author:** FLOCK4H  
**Inspiration Type:** Main framework and WiFi attack implementations

**What was inspired:**
- Concepts for certain WiFi attack implementations
- Project structure and attack orchestration approach
- Attack menu system architecture

**What is original:**
- All attack modules are completely new implementations
- Different attack selection and parameters
- Custom Raspberry Pi optimizations
- Integration with BLE and Phishing modules
- Unique code structure and error handling

**Status:** Original code, educational inspiration only

**Note:** Jammy itself credits several projects (see below) which have also influenced this work

---

### 2. **Bluetooth-WOS** (https://github.com/skittleson/bluetooth-wos)
**Author:** Skittleson  
**Inspiration Type:** BLE device scanner implementation

**What was inspired:**
- BLE device scanning approach patterns
- Advertisement data handling concepts

**What is original:**
- Complete reimplementation using bleak library
- Company identifier database (YAML format)
- Distance calculation from RSSI
- Real-time device table display
- Integration with main menu system

**Files inspired:**
- `personal_project/ble/device_scanner.py`

**Status:** Original implementation, pattern-inspired

---

### 3. **Shark** (https://github.com/Bhaviktutorials/shark)
**Author:** Bhaviktutorials  
**License:** BSD 3-Clause License  
**Inspiration Type:** Phishing server approach

**What was inspired:**
- Phishing server hosting concepts
- Credential capture methodology

**What is original:**
- Complete custom implementation using http.server
- Fake HTML pages (Facebook and Google)
- File-based credential logging
- Redirect functionality
- Menu integration

**Files inspired:**
- `personal_project/phishing/facebook_phish.py`
- `personal_project/phishing/google_phish.py`

**Status:** Original implementation, approach-inspired

---

---

### 4. **iBeacon-Scanner-** (https://github.com/switchdoclabs/iBeacon-Scanner-/blob/master/blescan.py)
**Author:** SwitchDoc Labs  
**Inspiration Type:** BLE scanning and advertisement parsing patterns

**What was inspired:**
- HCI command structures for BLE operations
- Advertisement packet parsing logic
- Bluetooth device interaction patterns

**What is original:**
- Reimplementation adapted for this project
- Integration with company identifier database
- Real-time BLE table display

**Files inspired:**
- `personal_project/ble/bluetooth_utils.py`

**Status:** Original implementation, pattern-inspired

---

### 5. **Bluez Sources** (http://www.bluez.org/)
**Type:** Linux Bluetooth Stack Documentation & Source Code  
**Inspiration Type:** Bluetooth protocol implementation patterns

**What was inspired:**
- HCI command structures and ioctl patterns
- Bluetooth device control methodology
- Low-level BLE advertising techniques

**What is original:**
- Adaptation for Python and this specific project
- Custom advertisement data structures
- Real-time monitoring implementation

**Files inspired:**
- `personal_project/ble/bluetooth_utils.py`
- `personal_project/ble/ad_spam.py`

**Status:** Original implementation, pattern-inspired

---

### 6. **Sour Apple Attack by RapierXbox** (https://github.com/RapierXbox)
**Author:** RapierXbox  
**Inspiration Type:** Apple BLE advertisement spoofing technique

**What was inspired:**
- Apple device advertisement format and types
- Proximity notification trigger mechanisms
- BLE manufacturer data structures for Apple devices

**What is original:**
- Python implementation using bleak/PyBluez
- Integration with attack menu system
- Real-time advertisement broadcasting
- Educational wrapper and documentation

**Files inspired:**
- `personal_project/ble/ad_spam.py`

**Status:** Original implementation, technique-inspired

---

### 7. **BlueDucky** (by saad0x1 and pentestfunctions)
**Authors:** saad0x1 (https://github.com/saad0x1) and pentestfunctions (https://github.com/pentestfunctions)  
**Source:** https://github.com/saad0x1/BlueDucky  
**Inspiration Type:** Bluetooth HID keyboard exploitation

**What was inspired:**
- Bluetooth HID device emulation concepts
- Keyboard input simulation over Bluetooth

**What is original:**
- Architecture adapted to project structure
- Specific payload implementations
- Menu integration

**Status:** Referenced from Jammy project, original implementations

---

### 8. **Shark by Bhaviktutorials** (covered above in main inspirations)
Also credits:
- **mdk4** - WiFi pentesting tool
- **eaphammer** - Evil Twin WiFi framework
- **wifite2** - WiFi cracking framework
- **hashcat** - Password hash cracking

These tools are used within the Shark framework and indirectly influence our WiFi module design.

## External Tools & Libraries

All external tools and libraries are properly integrated and attributed:

- **aircrack-ng** - WiFi security testing suite (GPL-2.0)
- **mdk4** - WiFi DoS tool (GPL-2.0)
- **hping3** - Packet crafting tool
- **bluez** - Bluetooth stack (GPL-2.0)
- **Scapy** - Packet manipulation (GPL-2.0)
- **bleak** - BLE library (MIT)
- **PyYAML** - YAML parsing (MIT)
- **Wireshark** - Network analysis (GPL-2.0)

---

## Attribution Standards

This project follows academic integrity standards:
- All inspirational sources are cited
- All implementations are original code
- External tools are properly attributed
- Clear distinction between inspiration and plagiarism

---

## Summary

| Component | Source | Type |
|-----------|--------|------|
| Some WiFi Attacks | Jammy | Educational inspiration |
| BLE Scanner | Bluetooth-WOS | Educational inspiration |
| Phishing Modules | Shark | Educational inspiration |
| Other Attacks | Original | Completely original |
| UI System | Original | Completely original |
| Architecture | Original | Completely original |

All code is 100% written from scratch with educational inspiration from these projects.
