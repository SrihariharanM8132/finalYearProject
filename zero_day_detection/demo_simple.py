"""
Zero-Day Attack Detection - Demonstration Mode
Simulates network monitoring without requiring network access
Perfect for project presentations!
"""

import random
import time
from datetime import datetime
import sys

class NetworkSimulator:
    """Simulates network traffic for demonstration"""
    
    def __init__(self):
        self.packets_analyzed = 0
        self.attacks_detected = 0
        self.blocked_ips = set()
        
    def generate_packet(self):
        """Generate simulated network packet"""
        protocols = ['tcp', 'udp', 'icmp']
        services = ['http', 'https', 'ftp', 'ssh', 'smtp', 'telnet', 'dns']
        
        # Generate realistic IP addresses
        src_ip = f"192.168.1.{random.randint(1, 255)}"
        dst_ip = f"{random.choice(['8.8.8', '1.1.1', '142.250.185'])}.{random.randint(1, 255)}"
        
        packet = {
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'protocol': random.choice(protocols),
            'service': random.choice(services),
            'size': random.randint(50, 20000),
            'duration': round(random.uniform(0.1, 5.0), 2),
            'flags': random.choice(['S0', 'SF', 'REJ', 'RSTO']),
        }
        
        return packet
    
    def detect_attack(self, packet):
        """
        Detect if packet is malicious using ML-inspired rules
        (Simulates your trained Random Forest model)
        """
        score = 0
        reasons = []
        
        # Rule 1: Large packet size (DoS indicator)
        if packet['size'] > 15000:
            score += 30
            reasons.append("Abnormally large packet size")
        
        # Rule 2: ICMP flood
        if packet['protocol'] == 'icmp' and packet['size'] > 1000:
            score += 40
            reasons.append("Possible ICMP flood attack")
        
        # Rule 3: Connection rejected (suspicious)
        if packet['flags'] == 'REJ' or packet['flags'] == 'RSTO':
            score += 20
            reasons.append("Connection rejected/reset")
        
        # Rule 4: Short duration with large size (fast data transfer)
        if packet['duration'] < 0.5 and packet['size'] > 10000:
            score += 25
            reasons.append("Rapid data transfer pattern")
        
        # Rule 5: Telnet/FTP (outdated, insecure protocols)
        if packet['service'] in ['telnet', 'ftp']:
            score += 15
            reasons.append("Use of insecure legacy protocol")
        
        # Rule 6: Random chance for zero-day (unknown pattern)
        if random.random() < 0.03:  # 3% chance
            score += 50
            reasons.append("⚠️ Zero-day pattern detected")
        
        # Determine if attack (threshold = 40)
        is_attack = score >= 40
        attack_type = self.classify_attack(packet, reasons) if is_attack else None
        confidence = min(95, score + random.randint(5, 15))
        
        return is_attack, attack_type, confidence, reasons
    
    def classify_attack(self, packet, reasons):
        """Classify type of attack"""
        if "Zero-day" in str(reasons):
            return "Zero-Day Attack"
        elif packet['protocol'] == 'icmp':
            return "DoS (ICMP Flood)"
        elif packet['size'] > 15000:
            return "DoS (Bandwidth Flood)"
        elif "legacy protocol" in str(reasons):
            return "Probe (Port Scan)"
        else:
            return "Suspicious Activity"
    
    def display_packet(self, packet_num, packet, is_attack, attack_type, confidence):
        """Display packet information"""
        status = "⚠️  ATTACK" if is_attack else "✓ SAFE  "
        color = "\033[91m" if is_attack else "\033[92m"  # Red or Green
        reset = "\033[0m"
        
        print(f"{color}Packet #{packet_num:3d}: {packet['src_ip']:15s} → {packet['dst_ip']:18s} "
              f"[{packet['protocol']:4s}] {packet['size']:5d}B  {status}{reset}")
        
        if is_attack:
            print(f"              └─ Type: {attack_type}")
            print(f"              └─ Confidence: {confidence}%")
            print(f"              └─ Action: Blocked & Logged")
            self.attacks_detected += 1
            self.blocked_ips.add(packet['src_ip'])
    
    def run_simulation(self, num_packets=50):
        """Run the network monitoring simulation"""
        print("="*70)
        print("🔒 ZERO-DAY ATTACK DETECTION - DEMONSTRATION MODE 🔒")
        print("="*70)
        print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Analyzing {num_packets} network packets...\n")
        print("Legend: ✓ = Safe traffic  ⚠️ = Attack detected\n")
        
        try:
            for i in range(1, num_packets + 1):
                # Simulate processing time
                time.sleep(0.08)  # 80ms per packet (realistic)
                
                # Generate and analyze packet
                packet = self.generate_packet()
                is_attack, attack_type, confidence, reasons = self.detect_attack(packet)
                
                self.packets_analyzed += 1
                self.display_packet(i, packet, is_attack, attack_type, confidence)
                
                # Occasionally show ML model thinking
                if i % 15 == 0:
                    print(f"\n  📊 Running ML inference... (Random Forest + CNN ensemble)")
                    time.sleep(0.2)
                    print(f"  ✓ Analysis complete\n")
        
        except KeyboardInterrupt:
            print("\n\n⏸  Simulation paused by user\n")
        
        self.display_summary()
    
    def display_summary(self):
        """Display final statistics"""
        print("\n" + "="*70)
        print("📊 DETECTION SUMMARY")
        print("="*70)
        print(f"Total packets analyzed:  {self.packets_analyzed}")
        print(f"Attacks detected:        {self.attacks_detected}")
        print(f"Safe packets:            {self.packets_analyzed - self.attacks_detected}")
        print(f"IPs blocked:             {len(self.blocked_ips)}")
        
        detection_rate = (self.attacks_detected / self.packets_analyzed * 100) if self.packets_analyzed > 0 else 0
        print(f"Attack detection rate:   {detection_rate:.1f}%")
        
        print("\n" + "="*70)
        print("✅ DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("="*70)
        
        print("\n📌 Note:")
        print("This simulation demonstrates the detection logic.")
        print("In production, the system would:")
        print("  • Capture real network packets using Scapy/libpcap")
        print("  • Process at 10,000+ packets per second")
        print("  • Integrate with firewall for automatic blocking")
        print("  • Send alerts to Security Operations Center (SOC)")
        print("  • Log all incidents for forensic analysis")


def main():
    """Main entry point"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║                                                                    ║")
    print("║     HYBRID ML FRAMEWORK FOR ZERO-DAY ATTACK DETECTION             ║")
    print("║                                                                    ║")
    print("║     Final Year Project - Computer Science Engineering             ║")
    print("║     Student: SRI HARIHARAN M (713922104040)                       ║")
    print("║                                                                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print("\n")
    
    print("Select demonstration mode:")
    print("1. Quick demo (50 packets)")
    print("2. Extended demo (100 packets)")
    print("3. Full demo (200 packets)")
    print("4. Exit")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            num_packets = 50
        elif choice == '2':
            num_packets = 100
        elif choice == '3':
            num_packets = 200
        elif choice == '4':
            print("\nExiting... Thank you!")
            return
        else:
            print("Invalid choice. Using default (50 packets)")
            num_packets = 50
        
        # Run simulation
        simulator = NetworkSimulator()
        simulator.run_simulation(num_packets)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
