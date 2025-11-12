#!/usr/bin/env python3
"""
generate_test_pcaps.py
Generate test PCAP files with various VoIP issues for VoIPScope testing

Requirements:
    pip install scapy

Usage:
    python generate_test_pcaps.py
"""

from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.layers.rtp import RTP
import random
import time

def create_sip_packet(src_ip, dst_ip, src_port, dst_port, sip_msg):
    pkt = IP(src=src_ip, dst=dst_ip) / UDP(sport=src_port, dport=dst_port) / Raw(load=sip_msg.encode())
    return pkt

def create_rtp_packet(src_ip, dst_ip, src_port, dst_port, seq, timestamp, ssrc, payload_type=0):
    rtp = RTP(
        version=2,
        padding=0,
        extension=0,
        numsync=0,
        marker=0,
        payload_type=payload_type,
        sequence=seq,
        timestamp=timestamp,
        sourcesync=ssrc
    )
    payload = bytes([random.randint(0, 255) for _ in range(160)])
    pkt = IP(src=src_ip, dst=dst_ip) / UDP(sport=src_port, dport=dst_port) / rtp / Raw(load=payload)
    return pkt

def generate_normal_call():
    print("📋 Scenario 1: Normal Call")
    
    packets = []
    caller_pub_ip = "203.0.113.50"
    callee_ip = "198.51.100.20"
    caller_rtp_port = 10000
    callee_rtp_port = 20000
    
    base_time = time.time()
    current_time = base_time
    
    def add_pkt(pkt, delta=0.0):
        nonlocal current_time
        current_time += delta
        pkt.time = current_time
        packets.append(pkt)
    
    # Simple SIP flow
    invite = "INVITE sip:user@example.com SIP/2.0\r\nFrom: <sip:caller@test.com>;tag=abc\r\nTo: <sip:callee@test.com>\r\nCall-ID: normal-call-123\r\n\r\n"
    add_pkt(create_sip_packet("192.168.1.100", "198.51.100.10", 5060, 5060, invite))
    
    trying = "SIP/2.0 100 Trying\r\n\r\n"
    add_pkt(create_sip_packet("198.51.100.10", "192.168.1.100", 5060, 5060, trying), 0.05)
    
    ok = "SIP/2.0 200 OK\r\nFrom: <sip:caller@test.com>;tag=abc\r\nTo: <sip:callee@test.com>;tag=xyz\r\nCall-ID: normal-call-123\r\n\r\n"
    add_pkt(create_sip_packet("198.51.100.10", "192.168.1.100", 5060, 5060, ok), 0.5)
    
    # RTP bidirectional
    ssrc_caller = 0x11111111
    ssrc_callee = 0x22222222
    seq_c = 1000
    seq_d = 2000
    ts_c = 0
    ts_d = 0
    
    for i in range(100):
        add_pkt(create_rtp_packet(caller_pub_ip, callee_ip, caller_rtp_port, callee_rtp_port, seq_c, ts_c, ssrc_caller), 0.020)
        seq_c += 1
        ts_c += 160
        
        add_pkt(create_rtp_packet(callee_ip, caller_pub_ip, callee_rtp_port, caller_rtp_port, seq_d, ts_d, ssrc_callee), 0.020)
        seq_d += 1
        ts_d += 160
    
    wrpcap("test_normal_call.pcap", packets)
    print(f"  ✅ Generated: test_normal_call.pcap ({len(packets)} packets)")
    print(f"  📊 Expected: Healthy call, MOS ~4.3\n")

def generate_oneway_audio():
    print("📋 Scenario 2: One-Way Audio")
    
    packets = []
    caller_pub_ip = "203.0.113.51"
    callee_ip = "198.51.100.21"
    caller_rtp_port = 10001
    callee_rtp_port = 20001
    
    base_time = time.time()
    current_time = base_time
    
    def add_pkt(pkt, delta=0.0):
        nonlocal current_time
        current_time += delta
        pkt.time = current_time
        packets.append(pkt)
    
    invite = "INVITE sip:user@example.com SIP/2.0\r\nCall-ID: oneway-call-456\r\n\r\n"
    add_pkt(create_sip_packet("192.168.1.100", "198.51.100.10", 5060, 5060, invite))
    
    ok = "SIP/2.0 200 OK\r\nCall-ID: oneway-call-456\r\n\r\n"
    add_pkt(create_sip_packet("198.51.100.10", "192.168.1.100", 5060, 5060, ok), 0.5)
    
    # RTP ONLY from caller (one-way!)
    ssrc_caller = 0x33333333
    seq_c = 3000
    ts_c = 0
    
    for i in range(100):
        add_pkt(create_rtp_packet(caller_pub_ip, callee_ip, caller_rtp_port, callee_rtp_port, seq_c, ts_c, ssrc_caller), 0.020)
        seq_c += 1
        ts_c += 160
    
    wrpcap("test_oneway_audio.pcap", packets)
    print(f"  ✅ Generated: test_oneway_audio.pcap ({len(packets)} packets)")
    print(f"  📊 Expected: CRITICAL - One-Way Audio\n")

def generate_poor_quality():
    print("📋 Scenario 3: Poor Quality")
    
    packets = []
    caller_pub_ip = "203.0.113.54"
    callee_ip = "198.51.100.24"
    caller_rtp_port = 10004
    callee_rtp_port = 20004
    
    base_time = time.time()
    current_time = base_time
    
    def add_pkt(pkt, delta=0.0):
        nonlocal current_time
        current_time += delta
        pkt.time = current_time
        packets.append(pkt)
    
    invite = "INVITE sip:user@example.com SIP/2.0\r\nCall-ID: poor-quality-789\r\n\r\n"
    add_pkt(create_sip_packet("192.168.1.100", "198.51.100.10", 5060, 5060, invite))
    
    ok = "SIP/2.0 200 OK\r\nCall-ID: poor-quality-789\r\n\r\n"
    add_pkt(create_sip_packet("198.51.100.10", "192.168.1.100", 5060, 5060, ok), 0.5)
    
    # RTP with high jitter and packet loss
    ssrc_caller = 0x88888888
    ssrc_callee = 0x99999999
    seq_c = 8000
    seq_d = 9000
    ts_c = 0
    ts_d = 0
    
    for i in range(150):
        jitter = random.uniform(0, 0.060)  # High jitter
        
        # 10% packet loss
        if random.random() > 0.10:
            add_pkt(create_rtp_packet(caller_pub_ip, callee_ip, caller_rtp_port, callee_rtp_port, seq_c, ts_c, ssrc_caller), 0.020 + jitter)
        
        seq_c += 1
        ts_c += 160
        
        if random.random() > 0.10:
            add_pkt(create_rtp_packet(callee_ip, caller_pub_ip, callee_rtp_port, caller_rtp_port, seq_d, ts_d, ssrc_callee), 0.020 + jitter)
        
        seq_d += 1
        ts_d += 160
    
    wrpcap("test_poor_quality.pcap", packets)
    print(f"  ✅ Generated: test_poor_quality.pcap ({len(packets)} packets)")
    print(f"  📊 Expected: HIGH - Poor quality (jitter, packet loss)\n")

def main():
    print("\n" + "="*60)
    print("VoIPScope Test PCAP Generator")
    print("="*60 + "\n")
    
    try:
        generate_normal_call()
        generate_oneway_audio()
        generate_poor_quality()
        
        print("="*60)
        print("✅ All test PCAPs generated!")
        print("="*60)
        print("\nGenerated files:")
        print("  • test_normal_call.pcap - Baseline")
        print("  • test_oneway_audio.pcap - One-way issue")
        print("  • test_poor_quality.pcap - Quality problems")
        print("\nRun VoIPScope to analyze:")
        print("  python voipscope.py")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
