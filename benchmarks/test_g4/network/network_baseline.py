# network_baseline.py
import time

def generate_packet_stream():
    print("Generating 15,000,000 network packets... Please wait.", flush=True)
    packets = []
    for i in range(25_000_000):
        # Healthy secure packet
        if i % 3 == 0:
            packets.append({"ip": "10.0.0.1", "payload_len": 512, "flags": 0x02})
        # Malformed packet (missing fields/None)
        elif i % 3 == 1:
            packets.append(None)
        # Empty/dropped heartbeat frame
        else:
            packets.append({"ip": "0.0.0.0", "payload_len": 0, "flags": 0x00})
    return packets

def process_stream_baseline(stream):
    allowed_count = 0
    start_time = time.time()
    
    for packet in stream:
        # Deeply nested indentation structures
        if packet is not None:
            if packet["payload_len"] > 0:
                if packet["ip"] != "0.0.0.0":
                    # Simulated complex checksum math
                    heavy_calc = (packet["payload_len"] ** 7) % 9999991
                    if heavy_calc > 0:
                        allowed_count += 1
                        
    return allowed_count

if __name__ == "__main__":
    traffic_stream = generate_packet_stream()
    allowed = process_stream_baseline(traffic_stream)
    print(f"\nPassed Packets: {allowed:,}")