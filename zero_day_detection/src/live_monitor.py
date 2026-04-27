"""
Live Network Traffic Monitor
Captures real-time network packets and detects attacks
"""

from scapy.all import sniff, IP, TCP, UDP, ICMP
import numpy as np
import pandas as pd
import pickle
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class LiveNetworkMonitor:
    """
    Real-time network monitoring and attack detection
    """
    
    def __init__(self, model_path='models/rf_model.pkl'):
        """
        Initialize monitor with trained model
        
        Args:
            model_path: Path to saved Random Forest model
        """
        self.model = None
        self.load_model(model_path)
        self.packet_count = 0
        self.alert_count = 0
        self.blocked_ips = set()
        
    def load_model(self, model_path):
        """Load pre-trained model"""
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            print(f"✓ Model loaded from {model_path}")
        except FileNotFoundError:
            print(f"⚠ Model not found. Please train and save model first.")
            self.model = None
    
    def extract_features(self, packet):
        """
        Extract 93 features from network packet
        (Same format as NSL-KDD dataset)
        
        Args:
            packet: Scapy packet object
            
        Returns:
            numpy array of 93 features
        """
        features = {}
        
        # Basic packet info
        if IP in packet:
            ip_layer = packet[IP]
            
            # Duration (we'll calculate this over time)
            features['duration'] = 0
            
            # Protocol type
            if TCP in packet:
                features['protocol_type'] = 'tcp'
                tcp_layer = packet[TCP]
                features['src_port'] = tcp_layer.sport
                features['dst_port'] = tcp_layer.dport
                features['flag'] = tcp_layer.flags
            elif UDP in packet:
                features['protocol_type'] = 'udp'
                features['src_port'] = packet[UDP].sport
                features['dst_port'] = packet[UDP].dport
                features['flag'] = 'S0'
            elif ICMP in packet:
                features['protocol_type'] = 'icmp'
                features['src_port'] = 0
                features['dst_port'] = 0
                features['flag'] = 'S0'
            else:
                features['protocol_type'] = 'other'
                features['src_port'] = 0
                features['dst_port'] = 0
                features['flag'] = 'S0'
            
            # Byte counts
            features['src_bytes'] = len(packet)
            features['dst_bytes'] = 0  # We'd need to track connections
            
            # Service (guess from port)
            features['service'] = self.port_to_service(features.get('dst_port', 0))
            
            # IP addresses
            features['src_ip'] = ip_layer.src
            features['dst_ip'] = ip_layer.dst
            
            # Additional features (simplified for demo)
            features['land'] = 1 if ip_layer.src == ip_layer.dst else 0
            features['wrong_fragment'] = 0
            features['urgent'] = 0
            features['hot'] = 0
            features['num_failed_logins'] = 0
            features['logged_in'] = 0
            features['num_compromised'] = 0
            features['root_shell'] = 0
            features['su_attempted'] = 0
            features['num_root'] = 0
            features['num_file_creations'] = 0
            features['num_shells'] = 0
            features['num_access_files'] = 0
            features['num_outbound_cmds'] = 0
            features['is_host_login'] = 0
            features['is_guest_login'] = 0
            features['count'] = 1
            features['srv_count'] = 1
            features['serror_rate'] = 0.0
            features['srv_serror_rate'] = 0.0
            features['rerror_rate'] = 0.0
            features['srv_rerror_rate'] = 0.0
            features['same_srv_rate'] = 1.0
            features['diff_srv_rate'] = 0.0
            features['srv_diff_host_rate'] = 0.0
            features['dst_host_count'] = 1
            features['dst_host_srv_count'] = 1
            features['dst_host_same_srv_rate'] = 1.0
            features['dst_host_diff_srv_rate'] = 0.0
            features['dst_host_same_src_port_rate'] = 1.0
            features['dst_host_srv_diff_host_rate'] = 0.0
            features['dst_host_serror_rate'] = 0.0
            features['dst_host_srv_serror_rate'] = 0.0
            features['dst_host_rerror_rate'] = 0.0
            features['dst_host_srv_rerror_rate'] = 0.0
            
            return features
        else:
            return None
    
    def port_to_service(self, port):
        """Map port number to service name"""
        port_map = {
            20: 'ftp_data', 21: 'ftp', 22: 'ssh', 23: 'telnet',
            25: 'smtp', 53: 'domain', 80: 'http', 110: 'pop3',
            143: 'imap', 443: 'https', 3306: 'mysql', 5432: 'postgres'
        }
        return port_map.get(port, 'other')
    
    def analyze_packet(self, packet):
        """
        Analyze packet and detect if it's an attack
        
        Args:
            packet: Scapy packet object
        """
        self.packet_count += 1
        
        # Extract features
        features = self.extract_features(packet)
        
        if features is None:
            return
        
        # Prepare features for model (simplified - needs proper encoding)
        try:
            # Convert to DataFrame for easier processing
            df = pd.DataFrame([features])
            
            # For demo: just check basic rules
            # In production: use your trained model
            is_suspicious = self.check_suspicious_behavior(features)
            
            if is_suspicious:
                self.handle_attack(features)
        
        except Exception as e:
            print(f"Error analyzing packet: {e}")
    
    def check_suspicious_behavior(self, features):
        """
        Simple rule-based detection (for demonstration)
        In production, use your trained ML model
        """
        suspicious = False
        
        # Rule 1: Large packet size
        if features['src_bytes'] > 10000:
            suspicious = True
        
        # Rule 2: ICMP flood
        if features['protocol_type'] == 'icmp' and features['src_bytes'] > 1000:
            suspicious = True
        
        # Rule 3: Port scanning (multiple ports from same IP)
        # (Would need connection tracking)
        
        # Rule 4: Same source and destination (land attack)
        if features['land'] == 1:
            suspicious = True
        
        return suspicious
    
    def handle_attack(self, features):
        """
        Handle detected attack
        """
        self.alert_count += 1
        
        src_ip = features['src_ip']
        dst_ip = features['dst_ip']
        protocol = features['protocol_type']
        size = features['src_bytes']
        
        # Log alert
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_msg = f"""
        ⚠️  ATTACK DETECTED! ⚠️
        Time: {timestamp}
        Source IP: {src_ip}
        Destination IP: {dst_ip}
        Protocol: {protocol}
        Packet Size: {size} bytes
        Threat Level: HIGH
        """
        
        print(alert_msg)
        
        # Save to log file
        with open('alerts.log', 'a') as f:
            f.write(alert_msg + '\n')
        
        # Block IP (demo - would need firewall integration)
        self.block_ip(src_ip)
    
    def block_ip(self, ip_address):
        """
        Block suspicious IP address
        (Demo only - needs actual firewall integration)
        """
        if ip_address not in self.blocked_ips:
            self.blocked_ips.add(ip_address)
            print(f"🚫 BLOCKED: {ip_address}")
            
            # In production, integrate with firewall:
            # os.system(f"netsh advfirewall firewall add rule name='Block {ip_address}' dir=in action=block remoteip={ip_address}")
    
    def start_monitoring(self, interface=None, packet_count=100):
        """
        Start monitoring network traffic
        
        Args:
            interface: Network interface to monitor (None = all)
            packet_count: Number of packets to capture (0 = infinite)
        """
        print("="*60)
        print("🔒 LIVE NETWORK MONITORING STARTED 🔒")
        print("="*60)
        print(f"Interface: {interface if interface else 'All'}")
        print(f"Capturing {packet_count if packet_count else 'unlimited'} packets...")
        print("Press Ctrl+C to stop\n")
        
        try:
            # Start packet capture
            sniff(
                iface=interface,
                prn=self.analyze_packet,
                count=packet_count,
                store=False  # Don't store packets in memory
            )
        except KeyboardInterrupt:
            print("\n\n⏹  Monitoring stopped by user")
        except PermissionError:
            print("\n❌ Error: Need administrator privileges to capture packets")
            print("Run PowerShell/Terminal as Administrator and try again")
        finally:
            self.print_summary()
    
    def print_summary(self):
        """Print monitoring summary"""
        print("\n" + "="*60)
        print("📊 MONITORING SUMMARY")
        print("="*60)
        print(f"Total packets captured: {self.packet_count}")
        print(f"Attacks detected: {self.alert_count}")
        print(f"IPs blocked: {len(self.blocked_ips)}")
        print(f"Detection rate: {(self.alert_count/self.packet_count*100) if self.packet_count > 0 else 0:.2f}%")
        print("="*60)


# Demo usage
if __name__ == "__main__":
    # Create monitor
    monitor = LiveNetworkMonitor()
    
    # Start monitoring (capture 100 packets)
    monitor.start_monitoring(packet_count=100)
