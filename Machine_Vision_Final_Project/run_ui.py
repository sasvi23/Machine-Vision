#!/usr/bin/env python3
"""
Quick Start Script for Factory Operator UI
Run this script to set up and launch the Streamlit application
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def check_calibration():
    """Check if calibration.json exists"""
    if os.path.exists("calibration.json"):
        print("✓ Calibration file found (calibration.json)")
        try:
            with open("calibration.json", "r") as f:
                data = json.load(f)
                print(f"  - Resolution: {data.get('image_width', '?')}x{data.get('image_height', '?')}")
                print(f"  - Date: {data.get('calibration_date', 'Unknown')}")
            return True
        except Exception as e:
            print(f"✗ Error reading calibration: {e}")
            return False
    else:
        print("✗ Calibration file NOT found!")
        print("  Run calibration first: python main.py calibrate")
        return False


def check_dependencies():
    """Check if required packages are installed"""
    required = {"streamlit": "streamlit", "cv2": "opencv-python", "numpy": "numpy"}
    missing = []
    
    for import_name, package_name in required.items():
        try:
            if import_name == "cv2":
                import cv2
            elif import_name == "numpy":
                import numpy
            elif import_name == "streamlit":
                import streamlit
        except ImportError:
            missing.append(f"{package_name}")
    
    if missing:
        print("✗ Missing dependencies:", ", ".join(missing))
        print(f"  Run: python -m pip install -r requirements.txt")
        return False
    
    print("✓ All dependencies installed")
    return True


def main():
    print("\n" + "="*60)
    print("🤖 Factory Operator UI - Quick Start")
    print("="*60 + "\n")
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        print("\nInstall missing packages and try again.")
        sys.exit(1)
    
    print()
    
    # Check calibration
    print("Checking calibration...")
    has_calib = check_calibration()
    
    print()
    
    if not has_calib:
        response = input("\nContinue anyway? (y/n): ").lower()
        if response != 'y':
            print("Aborted.")
            sys.exit(1)
    
    print("\n" + "="*60)
    print("🚀 Launching Streamlit UI...")
    print("="*60)
    print("\nThe app will open in your default browser.")
    print("If it doesn't, visit: http://localhost:8501\n")
    
    # Launch Streamlit with port handling
    def is_port_free(port):
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return True
            except OSError:
                return False

    port = 8501
    if not is_port_free(port):
        print(f"Port {port} is already in use, trying next available port...")
        # find next free port in a reasonable range
        for p in range(port + 1, port + 10):
            if is_port_free(p):
                port = p
                break
        print(f"Using port {port} instead.")

    try:
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app_streamlit.py",
            "--server.port",
            str(port)
        ], check=False)
    except KeyboardInterrupt:
        print("\n\nApplication closed.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError launching Streamlit: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
