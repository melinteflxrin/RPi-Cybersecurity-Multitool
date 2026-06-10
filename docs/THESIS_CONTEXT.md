# Thesis Project Context Document

**Last Updated:** June 2, 2026  
**Project:** Raspberry Pi Platform for Security Analysis of Short-Range Communication Protocols  
**Target Audience:** Bachelor thesis (computer science/cybersecurity)  

---

## 1. Project Overview

This bachelor thesis documents the design, implementation, and evaluation of a unified security research platform running on a Raspberry Pi Zero 2 W. The platform demonstrates 15 attacks across WiFi, Bluetooth Low Energy (BLE), Bluetooth Classic, and phishing domains through a single Python-based orchestrator with a color-coded terminal UI.

**Key Innovation:** Self-contained learning platform where everything needed (setup, configuration, code, documentation) is in one repository—no need to gather information from multiple sources.

**Hardware Target:**
- **Deployment:** Raspberry Pi Zero 2 W (~$15-20)
- **WiFi Adapter:** TP-Link Archer T2U PLUS with RTL8821AU chipset (~$35-40)
- **Total Cost:** ~$50-60 per student station (vs. $5000+ for professional platforms)

**Codebase Location:** `d:\@VSCODE PROJECTS\Jammy\personal_project\`

---

## 2. Completed Work

### ✅ Chapter 3: Technologies, Tools & Methods (COMPLETE)
**File:** `personal_project/docs/chapter3.md` (~4,200 words)

**Sections Completed:**
- 3.1 Operating System & Platform Selection (2 pages)
  - Why Raspberry Pi Zero 2 W (specs: ARM A53 4-core 1.0 GHz, 512 MB RAM)
  - Why x86 Linux for development
  - Why Linux/Debian (monitor mode, package management)
  - Cross-platform challenges

- 3.2 Hardware Components (1.5 pages)
  - Pi Zero 2 W detailed specifications
  - TP-Link Archer T2U PLUS (RTL8821AU chipset, dual-band, monitor mode)
  - System integration (USB hub, power, thermal management)

- 3.3 Core Tools & Libraries (3-4 pages) — **MAIN TECHNICAL SECTION**
  - System packages from SETUP.md (bluez, aircrack-ng, mdk4, hping3, arp-scan, etc.)
  - Python libraries with code examples:
    - **Bleak:** Async BLE scanning (from device_scanner.py)
    - **PyYAML:** Configuration file parsing (company identifiers)
    - **PyBluez:** L2CAP Bluetooth Classic
  - WiFi driver: RTL8821AU with DKMS
  - Optional: Cloudflare Tunnel for remote access

- 3.4 Development Methodology (1 page)
  - OOP approach with base class patterns
  - Modular design (single responsibility)
  - Color-coded console UI
  - Error handling strategy

- 3.5 Tool Integration & Compatibility (1 page)
  - Subprocess pattern with real code examples
  - Dependency management (pip, apt, DKMS)
  - Version pinning for reproducibility

- 3.6 Implementation Patterns (1.5 pages) WITH CODE
  - Attack Module Base Class pattern (validate→execute→display)
  - Deauthentication attack concrete example
  - Async BLE scanning pattern

- 3.7 Technology Stack Summary table

**Code Examples Included:**
- Async BLE scanning with bleak
- YAML company ID loading
- Subprocess with real-time output streaming
- DeauthAttack class implementation
- Network scanner integration

### ✅ Thesis Structure Updates
**File:** `personal_project/docs/THESIS_STRUCTURE_PROPOSAL.md`

**Completed Updates:**
- Section 2.5.2: Added "Self-Contained Learning Platform" subsection with 7 key points
- References & Bibliography: 15 citations (Jammy, Bluetooth-WOS, Shark, iBeacon-Scanner, Bluez, RapierXbox, BlueDucky, plus 8 external tools)
- Fixed critical figure numbering issues:
  - FIGURE 4.4: Main Application Flow (kept)
  - FIGURE 4.9: WiFi Attack Execution Flow (renamed from duplicate 4.4)
- Updated Section 4.3.2: "4 BLE attacks" → "5 BLE attacks" (added AdSpam)

### ✅ Chapter 4: Solution Architecture & Design
**File:** `personal_project/docs/chapter4.md` (~3,800 words, PARTIALLY COMPLETE)

**Completed Sections:**
- 4.1 Application Architecture Overview (component & layered diagrams)
- 4.2 Main Application Structure (menu hierarchy, flow diagrams)
- 4.3 Attack Module Architecture (WiFi 8, BLE 5, Bluetooth Classic 1, Phishing 2)
- 4.4 UI/Console Module Design
- 4.5 Data Flow Diagrams (WiFi execution flow with 10-step process)
- 4.6 Core Implementation Patterns WITH CODE
  - 4.6.1: Attack Module Base Pattern
  - 4.6.2: Subprocess Integration Pattern
  - 4.6.2b: WiFi Packet Crafting with Scapy (NEWLY ADDED)
  - 4.6.3: Async BLE Scanning Pattern
  - 4.6.4: Menu Handler Dispatch Pattern

**Recent Additions:**
- Added FIGURE 4.9 placeholder for WiFi Attack Execution Flow
- Added Scapy code example showing beacon frame construction with RadioTap/Dot11/Dot11Beacon

### ✅ Chapter 5: Implementation Details
**File:** `personal_project/docs/chapter5.md` (~3,500 words, PARTIALLY COMPLETE)

**Completed Sections:**
- 5.1 Development Process & Challenges
- 5.2 WiFi Attack Implementation (8 attacks)
- 5.3 BLE Attack Implementation (5 attacks)
- 5.4 Bluetooth Classic & Phishing Implementation
- 5.5 Main Application Flow
- 5.6 Key Implementation Code Snippets

**Updated Content:**
- Phishing section simplified to Cloudflare-only approach (removed localhost/SSH tunnel complexity)
- Updated Section 5.4.2 to emphasize public HTTPS access via cloudflared tunnel

### ✅ Attribution Documentation
**File:** `personal_project/SOURCES.md`

Comprehensive attribution document detailing 7 sources of inspiration:
1. **Jammy** - WiFi attack implementations and project architecture
2. **Bluetooth-WOS** - BLE device scanner implementation
3. **Shark** - Phishing server implementation
4. **iBeacon-Scanner** - BLE scanning and HCI command patterns
5. **Bluez** - Bluetooth protocol implementation patterns
6. **RapierXbox** - Apple BLE advertisement techniques
7. **BlueDucky** - Bluetooth HID keyboard emulation concepts

Each source documented with:
- What was inspired from this project
- What implementation is original
- Which files affected
- Current status

---

## 3. Pending Work

### ⏳ Chapters 1, 2, 6, 7 (NOT STARTED)

**Chapter 1: Introduction** (3-4 pages)
- 1.1 Context & Motivation
- 1.2 Problem Statement
- 1.3 Target Users & Applications
- 1.4 Project Objectives
- 1.5 Key Achievements & Scope

**Chapter 2: Domain Analysis** (14-18 pages)
- 2.0 Motivation, Use Cases & Problem Analysis
- 2.1 Flipper Zero: Inspiration & Reality
- 2.2 WiFi Security Fundamentals
- 2.3 Bluetooth Security Fundamentals
- 2.4 Application Security & Phishing
- 2.5 Why This Tool Fills an Educational Gap

**Chapter 6: Flipper Zero vs Our Implementation** (5-8 pages)
- Feature parity analysis
- Features we exceeded
- Features Flipper has that we don't (and why)
- Comparison table

**Chapter 7: Conclusions & Future Work** (2-3 pages)
- Project summary
- Achievements
- Limitations & trade-offs
- Future enhancements
- Research opportunities
- Educational impact

### ⏳ Appendices A-F (NOT STARTED)
- **A:** Hardware Setup Guide
- **B:** Installation & Configuration (SETUP.md contents)
- **C:** Source Code (key listings)
- **D:** User Manual (usage guide, screenshots)
- **E:** Test Results & Data (metrics, performance)
- **F:** Configuration Files (examples, outputs)

### ⏳ Figures & Diagrams (PLACEHOLDERS EXIST)
- FIGURE 3.1: Hardware Components (Raspberry Pi + TP-Link adapter)
- FIGURE 4.1: System Component Diagram
- FIGURE 4.2: Layered Architecture Diagram
- FIGURE 4.3: Menu Hierarchy Tree
- FIGURE 4.4: Main Application Flow Diagram
- FIGURE 4.5: WiFi Attack Module Class Hierarchy
- FIGURE 4.6: BLE Attack Module Architecture
- FIGURE 4.7: Phishing Server Architecture
- FIGURE 4.8: UI Color Scheme & Message Types
- FIGURE 4.9: WiFi Attack Execution Flow
- FIGURE 5.1: Application Main Menu (screenshot)

---

## 4. Key Project Details

### Attack Implementation (15 Total)

**WiFi Attacks (8):**
1. Beacon Broadcast - Fake network creation
2. Network Flood - AP DoS via mdk4
3. Network Scanner - Real-time discovery via airodump-ng
4. Deauthentication - Client disconnection
5. ESSID Bruteforce - Hidden network enumeration
6. Packet Capture - pcap file generation for Wireshark
7. HTTP DoS - HTTP request flooding with threading
8. Local Network DoS - ARP + ICMP flooding via hping3

**BLE Attacks (5):**
1. Device Scanner - Real-time BLE device discovery with company ID lookup
2. AirPods Spam - Apple device advertisement spoofing
3. Android Spam - Google Play Services advertisement simulation
4. AdSpam - Apple device (Apple TV, AirTag, etc.) advertisement
5. Name Spoofer - Rapid Bluetooth device name changes via btmgmt

**Bluetooth Classic (1):**
1. L2CAP DoS - L2CAP connection flooding attack

**Phishing (2):**
1. Facebook Phishing - Fake Facebook login with credential capture (Cloudflare Tunnel)
2. Google Phishing - Fake Google login with credential capture (Cloudflare Tunnel)

### Core Technologies

**Python Libraries:**
- `bleak` - Async BLE scanning
- `pyyaml` - Configuration parsing
- `pydbus` - D-Bus for Bluetooth
- `http.server` - Phishing server
- Standard libs: subprocess, asyncio, threading, socket, datetime

**System Tools:**
- `aircrack-ng` - WiFi security suite
- `mdk4` - WiFi DoS
- `hping3` - Packet crafting
- `arp-scan` - ARP discovery
- `bluez` - Bluetooth stack
- `cloudflared` - Tunnel service (optional)

**Platform:**
- OS: Debian Linux (Raspberry Pi OS)
- Python: 3.9+
- Driver: RTL8821AU (8821au-20210708.git)

### File Structure

```
personal_project/
├── main.py                 # Main orchestrator with AttackSuite class
├── SETUP.md               # Complete installation instructions
├── SOURCES.md             # Attribution documentation
├── ble/
│   ├── device_scanner.py  # BLE discovery with company ID lookup
│   ├── ad_spam.py         # Apple device advertisement spoofing
│   ├── airpods_spam.py    # AirPods spam attack
│   ├── android_spam.py    # Android device spam
│   ├── name_spoofer.py    # Device name spoofing
│   ├── bluetooth_utils.py # Low-level HCI utilities
│   └── company_identifiers.yaml  # Vendor database
├── wifi/
│   ├── beacon_broadcast.py
│   ├── deauth_attack.py
│   ├── network_scanner.py
│   ├── packet_capture.py
│   ├── network_flood.py
│   ├── essid_bruteforce.py
│   ├── http_dos.py
│   └── ap_networks.txt
├── bt/
│   └── l2cap_dos_attack.py
├── phishing/
│   ├── facebook_phish.py
│   └── google_phish.py
├── ui/
│   └── console.py         # Color-coded terminal output
└── docs/
    ├── chapter3.md        # COMPLETE: Technologies, Tools & Methods
    ├── chapter4.md        # PARTIAL: Solution Architecture
    ├── chapter5.md        # PARTIAL: Implementation Details
    ├── THESIS_STRUCTURE_PROPOSAL.md  # Complete outline
    └── THESIS_CONTEXT.md  # This file
```

---

## 5. Writing Progress & Page Count

| Chapter | Status | Pages | Words | Notes |
|---------|--------|-------|-------|-------|
| Intro (1) | Not started | 3-4 | - | Framework exists |
| Domain (2) | Not started | 14-18 | - | Framework exists |
| Tech (3) | **COMPLETE** | 10-12 | 4,200 | All tools/libs documented |
| Arch (4) | Partial | 8-12 | 3,800 | Code examples added |
| Impl (5) | Partial | 12-18 | 3,500 | Phishing updated to Cloudflare |
| Comparison (6) | Not started | 5-8 | - | Framework exists |
| Conclusion (7) | Not started | 2-3 | - | Framework exists |
| **TOTAL** | **21% done** | **40-50** | **11,500+** | Target: ~40 pages |

---

## 6. Key Decisions Made

### Thesis Scope
✅ **Intentional Simplifications:**
- Removed PMKID cracking (memory constraints on Pi)
- Removed Sub-GHz attacks (cost of SDR hardware)
- Phishing uses Cloudflare Tunnel only (simpler than localhost/SSH)
- Focused on education over feature completeness

✅ **Hardware Choices:**
- Raspberry Pi Zero 2 W for affordability ($15 vs Flipper $399)
- TP-Link T2U PLUS for WiFi (wide driver support, community-backed)
- Desktop x86 for development (same codebase, better iteration)

✅ **Attribution Approach:**
- Granular (per-file attribution vs blanket)
- Distinguished inspiration vs. original implementation
- Created SOURCES.md for transparency
- Referenced inspirations in Chapter 2.5.2

✅ **Phishing Implementation:**
- Cloudflare Tunnel only (vs dual localhost/SSH approach)
- Emphasizes real-world attack infrastructure
- Simpler pedagogically

### Thesis Structure
✅ **Chapter Order** (for writing):
1. Write implementation chapters first (Chapters 3-5) - write about what you built
2. Then context chapters (Chapters 2, 1) - provide background for decisions
3. Finally comparison/conclusions (Chapters 6, 7)

✅ **Figure Strategy:**
- 11 placeholders for diagrams/screenshots
- Real photos of hardware for Appendix A
- Representative attack outputs for Chapter 5

---

## 7. Code Examples Available

All examples in Chapter 3 and 4 are **directly from your codebase**, not hypothetical:

✅ **In Chapter 3:**
- Async BLE scanning (bleak library)
- YAML config loading (company identifiers)
- Subprocess with real-time streaming (airodump-ng integration)

✅ **In Chapter 4:**
- Attack Module Base Class pattern
- Deauthentication attack implementation
- Scapy beacon frame crafting
- Menu dispatch pattern

**Code is production-ready and explains learning value, not just functionality.**

---

## 8. Next Steps Recommendations

### Immediate (Week 1)
1. **Option A:** Continue with Chapter 1 or 2 (provide context for thesis)
2. **Option B:** Finalize figures for Chapters 3-5 (illustrations are ready for sketching)
3. **Option C:** Review and refine Chapter 3 for clarity/completeness

### Short-term (Week 2-3)
1. Write Chapter 1: Introduction
2. Write Chapter 2: Domain Analysis
3. Create figure assets (diagrams, screenshots)

### Medium-term (Week 4-5)
1. Write Chapter 6: Flipper Zero Comparison
2. Write Chapter 7: Conclusions & Future Work
3. Develop Appendices A-D

### Final (Week 6)
1. Proofread all chapters
2. Finalize figure captions
3. Cross-reference all citations
4. Assemble complete thesis document

---

## 9. Important Context for Next Conversation

When continuing in a new chat, clarify:

**If Working on NEW Chapters:**
- Read Chapter 3 to understand tools used
- Read thesis structure for context
- Maintain consistent tone (educational, technical but accessible)
- Reference actual code files when possible

**If Revising EXISTING Chapters:**
- Chapter 3 is COMPLETE (4,200 words, all tools/libs)
- Chapters 4-5 need REFINEMENT not rewriting
- Watch for figure numbering (4.4 and 4.9 are distinct)
- BLE attacks are now 5, not 4

**If Creating Figures:**
- Use placeholders for guidance
- Include captions explaining educational value
- Reference specific page numbers in text

**If Working on APPENDICES:**
- SETUP.md provides installation script
- Example outputs in ble/device_scanner.py
- Phishing pages in phishing/*.py (HTML templates)
- Color codes defined in ui/console.py

---

## 10. File Locations (Quick Reference)

**Thesis Documents:**
- Main outline: `personal_project/docs/THESIS_STRUCTURE_PROPOSAL.md`
- Chapter 3: `personal_project/docs/chapter3.md` ✅ COMPLETE
- Chapter 4: `personal_project/docs/chapter4.md` (partial)
- Chapter 5: `personal_project/docs/chapter5.md` (partial)
- This context: `personal_project/docs/THESIS_CONTEXT.md`

**Code Base:**
- Main app: `personal_project/main.py`
- Attacks: `personal_project/{wifi,ble,bt,phishing}/*.py`
- UI: `personal_project/ui/console.py`
- Setup: `personal_project/SETUP.md`
- Attribution: `personal_project/SOURCES.md`

**External References:**
- Jammy: https://github.com/FLOCK4H/Jammy
- Bluetooth-WOS: https://github.com/skittleson/bluetooth-wos
- Shark: https://github.com/Bhaviktutorials/shark
- RTL8821AU Driver: https://github.com/morrownr/8821au-20210708.git

---

## 11. Quick Stats

- **Attacks implemented:** 15 (8 WiFi, 5 BLE, 1 Bluetooth, 2 Phishing)
- **Python modules:** 20+ attack + utility modules
- **Thesis chapters drafted:** 3 complete, 2 partial, 2 not started
- **Words written:** ~11,500 across chapters
- **Code examples:** 15+ snippets with explanations
- **Sources cited:** 15 references
- **Hardware cost:** ~$50 per deployment
- **Target platform:** Raspberry Pi Zero 2 W (512 MB RAM, ARM)

---

## 12. Writing Style & Tone

**Established Conventions:**
- **Technical but accessible:** Explain WHY, not just WHAT
- **Educational focus:** Emphasize learning over tool completeness
- **Honest about constraints:** 512 MB RAM is real limitation, not hidden
- **Code-first examples:** Show actual patterns from codebase
- **Modular approach:** Each attack follows validate→execute→display pattern
- **Self-contained:** Everything needed in single repository

**Citation Style:** IEEE (15 references formatted in References section)

**Cross-referencing:** Chapters reference each other with section numbers (4.3.1, 5.2.2, etc.)

---

**This context document is comprehensive enough for a new LLM to understand the full project scope and continue writing effectively. Use it as the primary context when starting a new conversation.**
