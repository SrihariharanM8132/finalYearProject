"""
Interactive Dashboard Demo Script
Run this to show an impressive live demonstration to your guide
"""

import os
import webbrowser
import time

def show_project_demo():
    """Launch interactive demonstration"""
    
    print("\n" + "="*70)
    print(" " * 15 + "PROJECT DEMONSTRATION LAUNCHER")
    print("="*70)
    
    print("\n🎯 Dual-Phase Intrusion Detection System")
    print("   NSL-KDD Dataset | 72.81% Accuracy | 3.54% FPR")
    
    print("\n" + "="*70)
    print("DEMONSTRATION OPTIONS")
    print("="*70)
    
    print("\n1. 📊 Open Interactive Dashboard (HTML)")
    print("2. 📈 Show Evaluation Summary (Markdown)")
    print("3. 🖼️  Display All Visualizations")
    print("4. 🚀 Run Live Evaluation (takes ~30 seconds)")
    print("5. 📁 Open Results Folder")
    print("6. 📖 Show Project Documentation")
    print("7. ✅ Quick Summary (for fast demo)")
    
    choice = input("\nSelect option (1-7): ").strip()
    
    if choice == "1":
        print("\n📊 Opening interactive dashboard...")
        dashboard_path = os.path.abspath("results/dashboard.html")
        if os.path.exists(dashboard_path):
            webbrowser.open(f"file://{dashboard_path}")
            print(f"✓ Dashboard opened: {dashboard_path}")
        else:
            print("❌ Dashboard not found. Run: python dashboard.py")
    
    elif choice == "2":
        print("\n📈 Displaying evaluation summary...")
        summary_path = "results/EVALUATION_SUMMARY.md"
        if os.path.exists(summary_path):
            with open(summary_path, 'r') as f:
                print(f.read())
        else:
            print("❌ Summary not found. Run: python evaluate_system.py")
    
    elif choice == "3":
        print("\n🖼️  Opening all visualizations...")
        viz_files = [
            "results/confusion_matrix.png",
            "results/detection_rates.png",
            "results/classification_report.png",
            "results/phase2_feature_importance.png"
        ]
        for viz in viz_files:
            if os.path.exists(viz):
                os.startfile(viz)
                print(f"✓ Opened: {viz}")
                time.sleep(0.5)
            else:
                print(f"❌ Not found: {viz}")
    
    elif choice == "4":
        print("\n🚀 Running live evaluation...")
        print("This will take approximately 30 seconds...\n")
        os.system("python evaluate_system.py")
    
    elif choice == "5":
        print("\n📁 Opening results folder...")
        os.startfile("results")
    
    elif choice == "6":
        print("\n📖 Opening project documentation...")
        docs = [
            "PRESENTATION_GUIDE.md",
            "MISSION_CONTROL.md",
            "TWO_PHASE_README.md"
        ]
        for doc in docs:
            if os.path.exists(doc):
                os.startfile(doc)
                print(f"✓ Opened: {doc}")
                time.sleep(0.3)
    
    elif choice == "7":
        print("\n" + "="*70)
        print("QUICK PROJECT SUMMARY")
        print("="*70)
        print("\n📌 Project: Dual-Phase Zero-Day Intrusion Detection System")
        print("📊 Dataset: NSL-KDD (125,973 train, 22,544 test)")
        print("\n🤖 Phase 1: Autoencoder (Zero-Day Detection)")
        print("   - Trained on: 67,343 normal samples only")
        print("   - Threshold: 28.119")
        print("   - Flags: 445 samples (1.97%) as zero-day")
        print("\n🌲 Phase 2: Random Forest (Attack Classification)")
        print("   - Classes: DoS, Probe, R2L, U2R, Normal")
        print("   - Trees: 100, Max Depth: 20")
        print("\n📈 RESULTS:")
        print("   ✓ Overall Accuracy: 72.81%")
        print("   ✓ False Positive Rate: 3.54%")
        print("   ✓ DoS Detection: 75.30%")
        print("   ✓ Probe Detection: 57.54%")
        print("\n📁 Generated:")
        print("   - 6 trained models")
        print("   - 22,544 predictions")
        print("   - 8+ visualizations")
        print("   - Complete documentation")
        print("\n" + "="*70)
        
        input("\nPress Enter to open key visualizations...")
        os.startfile("results/confusion_matrix.png")
        time.sleep(0.3)
        os.startfile("results/detection_rates.png")
    
    else:
        print("\n❌ Invalid option")
    
    print("\n" + "="*70)
    print("Demo launcher ready for next action")
    print("="*70)


if __name__ == "__main__":
    show_project_demo()
