# VoIPScope v1.0 - Core Edition

**Professional VoIP Diagnostic & Analysis Tool**

*"See beyond the call"*

---

## 🎯 Overview

VoIPScope is an automated VoIP troubleshooting tool that analyzes PCAP files and generates comprehensive diagnostic reports. It detects common VoIP issues like one-way audio, NAT problems, TAG mismatches, and call quality degradation.

### Key Features

✅ **Automatic SIP/RTP Analysis**
- Parses SIP signaling and RTP media streams
- Correlates SIP calls with RTP flows using SDP

✅ **MOS Score Calculation**
- ITU-T E-Model based quality scoring
- Real-time quality assessment (1.0 - 4.5 scale)

✅ **Advanced Diagnostics**
- One-Way Audio detection
- NAT/Routing issue identification
- SIP TAG validation
- SDP vs Actual RTP comparison

✅ **Comprehensive Excel Reports**
- 6-sheet detailed analysis
- Color-coded quality indicators
- Actionable recommendations

---

## 📦 Installation

### Requirements

- Python 3.8+
- TShark (Wireshark command-line tool)

### Install Dependencies

```bash
pip install pyshark pandas openpyxl scapy
```

### Verify TShark Installation

```bash
tshark --version
```

If TShark is not found, install Wireshark from: https://www.wireshark.org/download.html

---

## 🚀 Quick Start

### 1. Generate Test PCAPs (Optional)

```bash
python generate_test_pcaps.py
```

This creates 5 test scenarios:
- Normal call (baseline)
- One-way audio
- NAT routing issue
- Missing TAG
- Poor quality (high jitter + packet loss)

### 2. Run VoIPScope

```bash
python voipscope.py
```

VoIPScope will:
1. Scan current directory for `.pcap` or `.pcapng` files
2. Analyze SIP signaling and RTP media
3. Detect issues automatically
4. Generate Excel report: `VoIPScope_Report_YYYYMMDD_HHMMSS.xlsx`

---

## 📊 Excel Report Structure

### Sheet 1: Call Summary
Overview of all calls with MOS scores and issue counts.

**Columns:**
- Call-ID
- From/To numbers
- Start/End time
- Duration
- RTP stream count
- Average MOS
- Quality rating
- Issue count

### Sheet 2: RTP Streams
Detailed metrics for each RTP stream.

**Columns:**
- Stream (IP:port → IP:port)
- Direction (Caller→Callee / Callee→Caller)
- SSRC
- Codec (G.711, G.729, etc.)
- Packet count
- Duration
- **Jitter (ms)** - Packet timing variance
- **Loss (%)** - Packet loss percentage
- **Delay (ms)** - One-way delay
- **MOS** - Call quality score
- Quality rating

### Sheet 3: SDP Analysis
SDP content from SIP INVITE and 200 OK messages.

**Shows:**
- Expected RTP IP/port from SDP
- Codec negotiations
- NAT warnings (private IP detection)

### Sheet 4: TAG Analysis
SIP dialog validation using From-Tag and To-Tag.

**Detects:**
- Missing TAGs
- TAG mismatches
- Dialog continuity issues

### Sheet 5: Issues & Recommendations ⭐
**Most Important Sheet!**

Lists all detected issues with:
- Severity (CRITICAL, HIGH, MEDIUM, LOW)
- Issue type
- Description
- Root cause analysis
- **Actionable recommendations**

### Sheet 6: Quality Report
Summary statistics and interpretation guides.

**Includes:**
- MOS score interpretation
- Issue severity levels
- Overall health assessment

---

## 🔍 Issue Detection

### 1. One-Way Audio (CRITICAL)

**Symptoms:**
- RTP packets only in one direction
- Severe packet imbalance (>90% difference)

**Causes:**
- Firewall blocking RTP
- NAT traversal failure
- Asymmetric routing

**VoIPScope Detection:**
Compares packet counts in both directions. If one direction has 0 packets or <10% of expected, flags as one-way audio.

---

### 2. NAT/Routing Issues (HIGH)

**Symptoms:**
- SDP advertises private IP (192.168.x.x, 10.x.x.x)
- Actual RTP comes from different public IP
- No RTP received at advertised IP

**Causes:**
- NAT device not updating SDP
- Missing STUN/TURN configuration
- SIP ALG disabled

**VoIPScope Detection:**
Compares SDP `c=` line IP with actual RTP source IP. Flags mismatches and private IPs.

---

### 3. TAG Validation (MEDIUM)

**Symptoms:**
- Missing From-Tag or To-Tag
- Inconsistent TAG values across messages

**Causes:**
- Non-compliant SIP client
- Proxy/B2BUA bug
- Configuration error

**VoIPScope Detection:**
Extracts TAGs from From/To headers. Validates presence in INVITE, 180 RINGING, and 200 OK.

---

### 4. Call Quality Issues (HIGH/MEDIUM)

**Metrics:**

**Jitter:**
- Good: < 10ms
- Acceptable: 10-30ms
- Poor: > 30ms

**Packet Loss:**
- Good: < 1%
- Acceptable: 1-3%
- Poor: > 3%

**MOS Score:**
- Excellent: 4.3-4.5
- Good: 4.0-4.2
- Fair: 3.0-3.9
- Poor: < 3.0

**VoIPScope Detection:**
Calculates real-time jitter, packet loss, and MOS using ITU-T E-Model.

---

## 📖 Understanding MOS Scores

**MOS (Mean Opinion Score)** predicts perceived call quality on a scale of 1.0 to 4.5.

### MOS Formula (Simplified E-Model)

```
R-factor = 93.2 - Delay_Penalty - Loss_Penalty - Jitter_Penalty
MOS = 1 + 0.035*R + 0.000007*R*(R-60)*(100-R)
```

### Real-World Interpretation

| MOS   | Quality   | User Experience                          |
|-------|-----------|------------------------------------------|
| 4.3+  | Excellent | Crystal clear, like face-to-face         |
| 4.0   | Good      | Minor artifacts, barely noticeable       |
| 3.5   | Fair      | Some choppy audio, still understandable  |
| 3.0   | Poor      | Frequent drops, frustrating              |
| <3.0  | Bad       | Unusable, call should be dropped         |

---

## 🛠️ Troubleshooting Guide

### Issue: "No PCAP files found"
**Solution:** Place `.pcap` or `.pcapng` files in the same directory as `voipscope.py`

### Issue: "tshark: command not found"
**Solution:** Install Wireshark (includes TShark):
- Windows: https://www.wireshark.org/download.html
- Linux: `sudo apt-get install tshark`
- macOS: `brew install wireshark`

### Issue: "SDP Analysis sheet is empty"
**Causes:**
1. PCAP doesn't contain SIP INVITE or 200 OK with SDP
2. TShark version too old
3. Capture filter excluded SDP content

**Solution:**
- Ensure capture includes full SIP dialog
- Update Wireshark/TShark to latest version
- Use capture filter: `port 5060 or port 5061`

### Issue: "ModuleNotFoundError: No module named 'pyshark'"
**Solution:**
```bash
pip install pyshark pandas openpyxl
```

---

## 📈 Use Cases

### 1. Troubleshooting Customer Issues
**Before:**
- Manual Wireshark analysis: 15 minutes
- Hard to explain technical details to customers

**After:**
- Automated analysis: 5 seconds
- Excel report with clear recommendations
- Customer sees color-coded quality: Green = Good, Red = Problem

### 2. Network Optimization
**Scenario:** ISP wants to monitor VoIP quality across network

**Solution:**
- Capture PCAP at multiple points
- Run VoIPScope batch analysis
- Identify problematic routes/devices
- Prioritize fixes based on issue severity

### 3. Compliance & SLA Monitoring
**Scenario:** VoIP provider guarantees MOS > 4.0

**Solution:**
- Periodic PCAP capture
- VoIPScope generates quality reports
- Track MOS trends over time
- Prove SLA compliance with Excel reports

---

## 🧪 Testing & Validation

### Run Test Suite

```bash
# Generate test PCAPs
python generate_test_pcaps.py

# Analyze test scenarios
python voipscope.py
```

### Expected Results

**test_normal_call.pcap:**
- ✅ No issues detected
- MOS: 4.3+
- All metrics healthy

**test_oneway_audio.pcap:**
- 🔴 CRITICAL: One-Way Audio
- Only caller sends RTP
- Recommendation: Check firewall on callee side

**test_nat_routing_issue.pcap:**
- 🟠 HIGH: NAT Routing Issue
- SDP has private IP (192.168.1.100)
- RTP from public IP (203.0.113.52)
- Recommendation: Enable STUN/TURN

**test_missing_tag.pcap:**
- 🟡 MEDIUM: TAG Missing
- To-Tag absent in 200 OK
- Recommendation: Check SIP server config

**test_poor_quality.pcap:**
- 🟠 HIGH: Poor Call Quality
- Jitter: 40-60ms
- Loss: ~10%
- MOS: < 3.0
- Recommendation: Enable QoS

---

## 🔐 Privacy & Security

- VoIPScope processes PCAP files **locally**
- No data sent to external servers
- Excel reports stored on your machine
- Safe for analyzing customer data (no cloud dependency)

---

## 🚧 Roadmap

### v1.1 (Planned)
- [ ] DTMF detection (RFC2833)
- [ ] Codec mismatch warnings
- [ ] Call setup delay analysis
- [ ] Silent call detection

### v2.0 (Future)
- [ ] WebRTC support
- [ ] Real-time monitoring mode
- [ ] Multi-file comparison
- [ ] Graphical dashboard
- [ ] PDF report generation

---

## 📄 License

MIT License

Copyright (c) 2025 Emre Karayazgan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.

---

## 👤 Author

**Emre Karayazgan**
- VoIP/Network Engineer
- LinkedIn: [[Your LinkedIn Profile](https://www.linkedin.com/in/emre-karayazgan/)]
- GitHub: [[Your GitHub Profile](https://github.com/emrekarayazgan)]

---

## 🙏 Acknowledgments

- ITU-T for E-Model standardization
- Wireshark/TShark for packet analysis capabilities
- Python community for excellent libraries

---

## 📞 Support

For bug reports, feature requests, or questions:
- Open an issue on GitHub
- Email: [emre.karayazgan@gmail.com]
- LinkedIn: [[Your LinkedIn](https://www.linkedin.com/in/emre-karayazgan/)]

---

**VoIPScope v1.0 - Core Edition**

*Making VoIP troubleshooting simple, fast, and accurate.*

"See beyond the call" 🚀
