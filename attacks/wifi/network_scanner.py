"""
Live Network Scanner - Real-time WiFi Network Discovery and Monitoring

This module provides continuous live scanning and monitoring of nearby WiFi networks
and connected devices using airodump-ng.
"""

import subprocess
import time
from ui import (cprint, iprint, wprint, eprint, sprint, RED, GREEN, CYAN, 
                YELLOW, MAGENTA, WHITE, RESET, LIGHT_CYAN)


class NetworkScanner:
    def __init__(self, interface):
        self.interface = interface
        self.process = None
    
    def verify_monitor_mode(self):
        try:
            result = subprocess.run(
                ["iwconfig", self.interface],
                capture_output=True,
                text=True,
                timeout=5
            )
            return "Monitor" in result.stdout
        except Exception as e:
            eprint(f"Error checking monitor mode: {e}")
            return False
    
    def start_continuous_scan(self):
        if not self.verify_monitor_mode():
            eprint(f"Interface {self.interface} is not in monitor mode!")
            return
        
        try:
            iprint(f"Starting continuous network scan on {self.interface}...")
            iprint("Press Ctrl+C to stop scanning\n")
            time.sleep(1)
            
            cmd = f"airodump-ng {self.interface}"
            
            self.process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Stream output in real-time
            while self.process:
                output = self.process.stdout.readline()
                if output:
                    cprint(output.rstrip(), CYAN)
                
                if self.process.poll() is not None:
                    break
            
            sprint("\nScan stopped successfully!")
            
        except FileNotFoundError:
            eprint("airodump-ng not found. Install aircrack-ng: sudo apt-get install aircrack-ng")
        except KeyboardInterrupt:
            wprint("\nScan interrupted by user")
        except Exception as e:
            eprint(f"Error during scanning: {e}")
        finally:
            if self.process:
                try:
                    self.process.terminate()
                    self.process.wait(timeout=2)
                except:
                    self.process.kill()
    
    def run(self):
        self.start_continuous_scan()
