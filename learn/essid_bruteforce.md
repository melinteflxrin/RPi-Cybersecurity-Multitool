# ESSID Bruteforce Attack — How It Works

## What is it?

A hidden network (also called a closed network) is a WiFi access point that has **SSID broadcast disabled**. Instead of including its name in beacon frames, it broadcasts an empty SSID field (`<length: 0>`). The network still exists and accepts connections — it just doesn't announce itself.

The ESSID bruteforce attack **discovers the hidden SSID** by exploiting how the 802.11 probe request/response mechanism works.

---

## 802.11 Background: Probes

The WiFi standard (IEEE 802.11) defines two ways a device finds a network:

| Method | How it works |
|---|---|
| **Passive scan** | Device listens for beacon frames. Hidden APs send beacons with empty SSID — so the network appears nameless or not at all. |
| **Active scan** | Device sends a **probe request** frame containing a specific SSID. If an AP has that SSID, it replies with a **probe response** containing the SSID in plaintext. |

The attack exploits the **active scan** path.

---

## Frame Structure

### Probe Request (sent by us)
```
RadioTap → Dot11 → Dot11Elt (SSID) → Dot11Elt (Supported Rates)
```

Key fields in the Dot11 header:
- `type = 0` — management frame
- `subtype = 4` — probe request
- `addr1` — destination MAC. Set to the **target router's BSSID** (unicast/directed)
- `addr2` — source MAC (our station MAC, randomised per probe)
- `addr3` — BSSID of the target AP

Setting `addr1 = BSSID` makes this a **directed probe request**, sent only to that specific AP. This is essential — broadcast probes (`addr1 = ff:ff:ff:ff:ff:ff`) are ignored by hidden APs.

### Probe Response (sent by the router)
```
RadioTap → Dot11 → Dot11ProbeResp → Dot11Elt (SSID) → ...
```

Key fields:
- `type = 0, subtype = 5` — probe response (management)
- `addr2` — the AP's BSSID (source)
- SSID element (ID=0) contains the **actual SSID in plaintext**

---

## How the Attack Works (Step by Step)

1. Put the WiFi adapter into **monitor mode** so it can send and receive raw 802.11 frames
2. Start an `AsyncSniffer` to capture all probe response frames from the target BSSID
3. For each SSID in the wordlist:
   - Build a directed probe request with that SSID
   - Send it to the target router's BSSID
   - Wait 300ms
   - Check if the sniffer captured a probe response from the target
4. If a probe response arrives — its SSID element reveals the hidden network name

---

## Problems Encountered and How They Were Fixed

### Problem 1: Wrong tool (mdk4 + `-t` flag)
The original code used `mdk4 p -t <bssid> -f <wordlist>`. When targeting a hidden AP with `-t`, mdk4 reads the SSID length from the beacon (`length: 0`) and uses it to filter the wordlist — only probing SSIDs of length 0. Since no wordlist entry has 0 characters, only 1 packet was sent and mdk4 exited immediately.

**Fix:** Replaced mdk4 entirely with a scapy-based implementation that crafts raw 802.11 frames directly, bypassing any length filtering.

### Problem 2: Router ignores broadcast probes
Without the `-t` flag, mdk4 sent probes to `ff:ff:ff:ff:ff:ff` (broadcast). Hidden APs do not respond to broadcast probe requests — they only respond to directed (unicast) probes where `addr1` equals their BSSID.

**Fix:** Set `addr1 = bssid` in every probe request to make them directed/unicast.

### Problem 3: Race condition — sniff misses the response
The first scapy attempt sent the probe then called `sniff()` to wait for a response. The router responded within ~2ms, but `sniff()` takes a few ms to open its raw socket — so the response arrived before the capture socket existed and was dropped by the kernel.

**Fix:** Start `AsyncSniffer` **before** sending any probe. The capture socket is already open when the probe goes out, so the fast response is buffered and caught.

### Problem 4: `AsyncSniffer.results` is None during capture
`AsyncSniffer.results` is only populated after `sniffer.stop()` is called. Checking it inside the probe loop always returned `None`.

**Fix:** Use the `prn` callback parameter to append matched packets into a plain Python list (`captured = []`) that is updated in real-time by the sniffer's background thread.

### Problem 5: Wrong SSID in the wordlist
The router model is `TL-WR740N` but its default SSID was `TP-LINK_9A39A4` (TP-Link's naming convention: `TP-LINK_` + last 6 hex digits of the MAC address). The wordlist had the model name, not the actual SSID.

**Fix:** Identify the correct SSID from the router admin page and add it to the wordlist. For the demo, the SSID was renamed to `test_demo_wifi`.

---

## Final Implementation (essid_bruteforce.py)

```python
# 1. AsyncSniffer started BEFORE probe loop — socket is open before first probe
captured = []

def on_response(p):
    if (p.haslayer(Dot11) and
        p[Dot11].type == 0 and p[Dot11].subtype == 5 and   # probe response
        p[Dot11].addr2 and p[Dot11].addr2.lower() == bssid_lower):
        captured.append(p)

sniffer = AsyncSniffer(iface=interface, prn=on_response, store=False)
sniffer.start()
time.sleep(0.2)  # brief warmup

# 2. Probe loop
for ssid in wordlist:
    # Build directed probe request
    pkt = (RadioTap() /
           Dot11(type=0, subtype=4,
                 addr1=bssid,      # unicast to target AP
                 addr2=RandMAC(),  # randomised station MAC
                 addr3=bssid) /
           Dot11Elt(ID='SSID', info=ssid) /
           Dot11Elt(ID='Rates', info=b'\x82\x84\x8b\x96\x24\x30\x48\x6c'))

    sendp(pkt, iface=interface, verbose=False)
    time.sleep(0.3)

    # 3. Check if sniffer caught a response
    if captured:
        ssid_elt = captured[0].getlayer(Dot11Elt)
        # Walk information elements to find SSID (ID=0)
        while ssid_elt:
            if ssid_elt.ID == 0 and ssid_elt.info:
                print(f"Found: {ssid_elt.info.decode()}")
                break
            ssid_elt = ssid_elt.payload.getlayer(Dot11Elt)
        break
```

---

## Key Concepts to Know for the Presentation

| Concept | What to say |
|---|---|
| **Monitor mode** | The adapter's mode that allows it to capture and inject raw 802.11 frames, bypassing the normal association process |
| **BSSID** | Basic Service Set Identifier — the MAC address of the access point radio |
| **SSID** | Service Set Identifier — the human-readable network name |
| **Directed probe** | A probe request sent to a specific BSSID (`addr1 = bssid`), as opposed to a broadcast probe (`addr1 = ff:ff:ff:ff:ff:ff`) |
| **Information Elements** | Variable-length fields in 802.11 management frames. Each has an ID, length, and value. ID=0 is always the SSID |
| **Scapy** | Python library for crafting and capturing raw network packets at any layer |
| **AsyncSniffer** | Scapy class that runs packet capture in a background thread, keeping the capture socket open while your main code runs |
| **RadioTap** | A pseudo-header added by the WiFi driver in monitor mode. Required for packet injection with scapy |

---

## Why Hidden SSIDs Are Not a Security Measure

This attack demonstrates that hiding an SSID provides **security through obscurity only**:
- The AP still transmits beacon frames (just with an empty SSID field)
- It still responds to directed probe requests containing the correct SSID
- Tools like this can discover the SSID in seconds if it appears in a wordlist
- Connected clients actively probe for the hidden network, revealing the SSID in plaintext

Hidden SSID should never be relied upon as a security control — it is at best a minor inconvenience.
