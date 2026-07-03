#!/usr/bin/env python3
"""
Attack Suite - Entry Point

A menu-driven application for BLE, Bluetooth, and WiFi attacks and security
research tools. Run from the repository root with: sudo python main.py

ATTRIBUTION: inspired by concepts from Jammy (https://github.com/FLOCK4H/Jammy)
"""

import os
import sys
from ui import eprint, wprint
from ui.app import AttackSuite


def check_requirements():
    """Check if required dependencies are installed."""
    try:
        import bluetooth._bluetooth as bluez
    except ImportError:
        eprint("PyBluez library not found!")
        eprint("Install it with: pip install pybluez")
        eprint("\nOn Linux, you may also need:")
        eprint("  sudo apt-get install python3-dev libbluetooth-dev")
        return False

    # Check if running on Linux
    if os.name != 'posix':
        wprint("This tool is designed for Linux systems.")
        wprint("Some features may not work on other platforms.")

    # Check if running as root
    if os.geteuid() != 0:
        wprint("Not running as root!")
        wprint("Some BLE operations require sudo/root privileges.")
        wprint("Run with: sudo python3 main.py")

    return True


def main():
    """Entry point for the application."""
    if not check_requirements():
        sys.exit(1)

    app = AttackSuite()
    app.run()


if __name__ == '__main__':
    main()
