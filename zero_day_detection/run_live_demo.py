"""
Live Network Monitoring Demo
Run this to see real-time attack detection
"""

from src.live_monitor import LiveNetworkMonitor
import sys

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   ZERO-DAY ATTACK DETECTION - LIVE MONITORING MODE       ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    print("Options:")
    print("1. Monitor 100 packets (Quick demo)")
    print("2. Monitor 1000 packets (Extended demo)")
    print("3. Continuous monitoring (Until Ctrl+C)")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ")
    
    if choice == '1':
        packet_count = 100
    elif choice == '2':
        packet_count = 1000
    elif choice == '3':
        packet_count = 0
    else:
        print("Exiting...")
        return
    
    # Create monitor
    monitor = LiveNetworkMonitor()
    
    # Start monitoring
    print("\n⚠️  NOTE: This requires administrator privileges!")
    print("If you get permission error, run as administrator.\n")
    
    try:
        monitor.start_monitoring(packet_count=packet_count)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Run PowerShell/Terminal as Administrator")
        print("2. Install Npcap: https://npcap.com/#download")
        print("3. Check firewall settings")

if __name__ == "__main__":
    main()
