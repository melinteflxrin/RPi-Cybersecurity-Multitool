# Chapter 1: Introduction

## 1.1 Context & Motivation

Security tools in the cybersecurity industry often run as "black boxes." Students and junior professionals execute attacks using tools like aircrack-ng, Metasploit, or the Flipper Zero, but they rarely understand how those attacks actually work underneath. They press a button, something happens, and they move on. This is efficient for professionals but terrible for learning.

The Flipper Zero portable hacking device was a key inspiration for this project. It demonstrated that a small, affordable device could perform meaningful WiFi, Bluetooth, and radio-frequency attacks. But it also revealed a critical limitation: the Flipper Zero is closed source and costs $399 or more. Students can execute attacks, but they cannot read the code that constructs a deauthentication frame, spoofs a BLE advertisement, or crafts a phishing page. For an educational tool, this is a significant drawback.

At the same time, university cybersecurity courses face a persistent theory-practice disconnect. Lectures cover WiFi protocol layers, Bluetooth pairing mechanisms, and encryption algorithms in detail — but students rarely get hands-on practice with real attacks in a controlled environment. Lab equipment is expensive, tools require expert-level knowledge to combine, and the learning curve for setting up a security testing environment is steep.

This project addresses these problems by building an open-source, affordable security research platform that runs on a Raspberry Pi Zero 2 W (~$15) with a TP-Link WiFi adapter (~$35). For approximately $50 per station — compared to $5,000+ for professional security platforms or $399 per Flipper Zero — universities can deploy practical cybersecurity labs where students see exactly how every attack works at the code level.

The platform is entirely self-contained: everything needed to learn, set up, and execute 15 different attacks across WiFi, Bluetooth Low Energy, Bluetooth Classic, and phishing domains is in a single repository. Setup instructions, driver installation guides, working code for all attacks, and this documentation are all included. Students don't need to gather information from multiple sources or navigate complex framework documentation — they clone one repository and start learning.

## 1.2 Problem Statement: Why This Tool?

Five interconnected problems motivated this project:

**Learning Gap.** Students learn WiFi and Bluetooth security theory in lectures but lack practical, hands-on experience with real attacks. They understand that deauthentication frames exploit unprotected WiFi management frames, but they've never actually sent one and watched a device disconnect. This gap between knowing *about* an attack and understanding *how* it works limits the depth of their education.

**Integration Challenge.** Performing even a simple WiFi security test requires combining multiple tools: `airmon-ng` to enable monitor mode, `airodump-ng` to scan networks, `aireplay-ng` or `mdk4` to inject packets, and potentially `wireshark` to analyze captures. Each tool has its own command-line interface, parameters, and output format. Students who want to learn about WiFi security often spend more time learning tool syntax than understanding the underlying vulnerabilities. Our platform wraps these tools behind a unified menu system, so students can focus on what the attack does rather than how to invoke the tool.

**Transparency.** Proprietary security tools and closed-source devices hide their implementation details. A student using the Flipper Zero sees that a deauthentication attack works, but they can't inspect the code that constructs the frame, choose how many frames to send, or modify the attack behavior. Commercial platforms like Metasploit Pro provide powerful automation but offer limited insight into how individual exploits are implemented. Our platform makes every line of code available for inspection, modification, and learning.

**Accessibility.** Professional security testing requires specialized knowledge, expensive equipment, and significant experience. The barrier to entry for a student who wants to practice WiFi security testing is high: they need a compatible WiFi adapter, a Linux system with the right drivers, knowledge of 5-10 different command-line tools, and an understanding of which tools to use in which order. Our platform reduces this barrier to a $50 hardware investment and a single `sudo python3 main.py` command.

**Customization Limitations.** Existing tools are difficult to modify for specific educational or research needs. Adding a new attack to aircrack-ng requires understanding its C codebase. Extending Metasploit requires learning Ruby and the framework's module system. Our platform uses Python — the most widely taught programming language in computer science — with a simple, documented pattern for adding new attacks. A student with basic Python knowledge can read, modify, and extend any attack module.

## 1.3 Target Users & Applications

The platform is designed for five primary audiences:

**Cybersecurity Students.** The primary target audience. Students taking network security, ethical hacking, or cybersecurity courses can use the platform for hands-on lab exercises. The transparent codebase allows them to learn both security concepts and software engineering patterns (modular design, subprocess integration, async programming) simultaneously. The affordable hardware means each student can have their own testing station.

**Educators & Instructors.** The unified interface and menu-driven workflow make it easy to demonstrate attack concepts in a classroom setting without spending time on tool setup. An instructor can show a deauthentication attack, a BLE spam attack, and a phishing demonstration in a single lecture using the same platform. The modular architecture also makes it easy to create focused lab exercises around specific attack categories.

**Security Researchers.** The open-source implementation enables vulnerability research and documentation. Researchers can modify attack modules, add measurement instrumentation, automate testing across different configurations, and publish findings with a fully reproducible methodology. The consistent attack interface (validate → execute → display) simplifies the process of adding new attacks or modifying existing ones for research purposes.

**Network Administrators.** Administrators who want to understand the security implications of their network configurations can use the platform to test their own defenses. The network scanner shows what an attacker can see, the deauthentication attack tests whether WPA3 Protected Management Frames are enabled, and the BLE scanner reveals which devices are broadcasting in the environment.

**Penetration Testers.** Junior security professionals preparing for certifications like CEH (Certified Ethical Hacker) or OSCP (Offensive Security Certified Professional) can use the platform as an affordable practice environment. Understanding how attacks work at the code level builds deeper knowledge than simply memorizing which tool to run for each test case.

## 1.4 Project Objectives

This thesis set out to achieve six objectives:

1. **Create a unified platform** that abstracts the complexity of individual security tools behind a single, menu-driven interface. Users should be able to execute WiFi, Bluetooth, and phishing attacks without learning the command-line syntax of 10+ different tools.

2. **Demonstrate practical vulnerabilities** through executable code. Each attack in the platform targets a real protocol vulnerability — unprotected WiFi management frames, unauthenticated BLE advertisements, L2CAP connection handling, and user trust in login pages — and produces real, observable effects.

3. **Design an intuitive interface** that enables beginners to execute and understand attacks. The color-coded terminal UI with clear message types (info in blue, warnings in yellow, errors in red, success in green) provides immediate visual feedback, and the three-level menu system (category → attack → parameters) guides users through each step.

4. **Implement a modular architecture** that teaches software design principles through practical example. Each attack is an independent Python module following the same pattern (validate → execute → display). Adding a new attack is straightforward: write one class, add one menu entry. This demonstrates separation of concerns, single responsibility, and the strategy pattern.

5. **Provide a complete, transparent codebase** that enables educational inspection, modification, and research extension. Every attack module is a readable Python file with comments explaining not just what the code does, but why specific design decisions were made.

6. **Document the implementation** thoroughly enough for reproducible science and community contribution. This thesis, combined with the setup instructions and source code, enables anyone with the same hardware to build the platform, run the attacks, and verify the results independently.

## 1.5 Key Achievements & Scope

The completed platform includes 15 security attacks across four domains:

**WiFi Attacks (8):**
- Network Scanner — passive discovery of nearby WiFi networks and connected devices using airodump-ng
- Beacon Broadcast — creation of fake WiFi networks using mdk4 beacon frame injection
- AP Network Flood — mass broadcasting of fake networks from a wordlist
- Deauthentication — client disconnection by sending forged deauthentication frames
- ESSID Bruteforce — hidden network discovery through probe request enumeration
- Packet Capture — recording WiFi traffic to .cap files for Wireshark analysis
- HTTP DoS — multi-threaded HTTP request flooding with randomized User-Agent headers
- Local Network DoS — ARP device discovery followed by SYN packet flooding via hping3

**BLE Attacks (5):**
- Device Scanner — real-time BLE device discovery with company identification, signal strength, and distance estimation
- AirPods Spam — fake Apple AirPods advertisement broadcasting to trigger iOS pairing popups
- Android Spam — fake Google/Samsung device advertisement broadcasting
- Apple Ad Spam — fake Apple device (AirTag, Apple TV, etc.) advertisement spoofing
- Name Spoofer — rapid Bluetooth adapter name rotation to create device name confusion

**Bluetooth Classic (1):**
- L2CAP DoS — connection flooding attack using rapid L2CAP echo requests

**Phishing (2):**
- Facebook Phishing — fake Facebook login page with credential capture and Cloudflare Tunnel support
- Google Phishing — fake Google login page with credential capture and Cloudflare Tunnel support

**Platform Characteristics:**
- Runs on Raspberry Pi Zero 2 W (~$15) with TP-Link Archer T2U PLUS WiFi adapter (~$35)
- Total deployment cost: approximately $50 per station
- Cross-platform Linux support (optimized for Raspberry Pi OS, also works on x86 Debian/Ubuntu)
- Unified command-line interface with color-coded output
- Open-source codebase with complete setup and installation documentation
- Modular Python architecture enabling easy extension and modification

**Intentional Scope Limitations:**
Some features were deliberately excluded to maintain focus and feasibility:
- **PMKID password cracking** was removed because the Raspberry Pi's 512 MB RAM cannot run hashcat effectively (see Section 5.1.3)
- **Sub-GHz radio attacks** were excluded because affordable SDR hardware compatible with the Pi was not available (see Section 2.1.4)
- **NFC and infrared modules** were excluded as they fall outside the project's WiFi/Bluetooth security focus
- The platform targets **education and learning**, not comprehensive penetration testing — it prioritizes transparency and simplicity over feature completeness

---

The remainder of this thesis is organized as follows: Chapter 2 provides domain analysis covering WiFi and Bluetooth security fundamentals, the Flipper Zero inspiration, and the educational gap this tool fills. Chapter 3 details the technologies, tools, and methods used. Chapter 4 describes the solution architecture and design. Chapter 5 covers implementation details and challenges. Chapter 6 presents a feature comparison between the Flipper Zero and our implementation. Chapter 7 concludes with a summary, limitations, and future work.
