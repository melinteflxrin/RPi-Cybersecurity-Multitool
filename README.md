# Raspberry Pi Cybersecurity Multitool

> **For educational use only.** Only use on devices and networks you own or have explicit permission to test.

## Setup

On a Raspberry Pi, follow the steps in [SETUP.md](SETUP.md) to install the required packages and configure the Bluetooth and WiFi adapters. Clone the repo and run the app:

```bash
git clone https://github.com/melinteflxrin/RPi-Cybersecurity-Multitool.git
cd RPi-Cybersecurity-Multitool
sudo python3 main.py
```

## Acknowledgements

Inspired by several open-source projects:

- [Jammy](https://github.com/FLOCK4H/Jammy) by FLOCK4H
- [Bluetooth-WOS](https://github.com/skittleson/bluetooth-wos) by Skittleson
- [Shark](https://github.com/Bhaviktutorials/shark) by Bhaviktutorials
- [iBeacon-Scanner](https://github.com/switchdoclabs/iBeacon-Scanner-) by SwitchDoc Labs
- [ESP32 Sour Apple](https://github.com/RapierXbox/ESP32-Sour-Apple) by RapierXbox

Open-source tools and libraries used:

- [aircrack-ng](https://www.aircrack-ng.org/) / [mdk4](https://github.com/aircrack-ng/mdk4) — WiFi scanning and frame injection
- [bleak](https://github.com/hbldh/bleak) — BLE scanning
- [BlueZ](http://www.bluez.org/) — Linux Bluetooth stack
- [hping3](https://github.com/antirez/hping) / [arp-scan](https://github.com/royhills/arp-scan) — network flooding and discovery
- [8821au driver](https://github.com/morrownr/8821au-20210708) — monitor-mode WiFi adapter support
- [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) — public URLs for phishing demos

Full bibliography and references: [docs/thesis.pdf](docs/thesis.pdf).
