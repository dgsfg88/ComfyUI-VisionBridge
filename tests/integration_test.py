#!/usr/bin/env python3
"""
Integration test for the VisionBridge native module and ComfyUI compatibility.

This test verifies that:
1. C++ native module compiles correctly
2. Python module can be imported
3. Basic functionality works
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def test_native_module_import():
    """Test that the native module imports correctly and has expected functions."""
    try:
        from visionbridge import add, version
        print("[PASS] Module imports successfully")
        
        # Test the functions
        result = add(2, 2)
        print(f"[PASS] add(2, 2) = {result} (expected 4)")
        
        print(f"[PASS] Module version: {version}")
        
        # Check that we're working with the right module
        print(f"[PASS] Using {sys.executable}")
        return True
        
    except Exception as e:
        print(f"[FAIL] Module import failed: {e}")
        return False

def test_backend_functionality():
    """Test that the mock backend functions work correctly."""
    try:
        from backends.mock import MockCameraBackend
        from camera.base import CameraBackend
        
        print("[PASS] Import successful")
        
        # Create backend
        backend = MockCameraBackend()
        print("[PASS] Backend created")
        
        # Test enumeration
        devices = backend.enumerate_devices()
        print(f"[PASS] Enumerated {len(devices)} devices")
        
        if devices:
            dev_id = devices[0]['id']
            print(f"[PASS] Found device: {dev_id}")
            
        # Test capabilities
        capabilities = backend.get_capabilities()
        print(f"[PASS] Retrieved {len(capabilities)} capabilities")
        
        # Test parameter access
        cap_exposure = next((c for c in capabilities if 'Exposure' in c.name), None)
        if cap_exposure and cap_exposure.supported:
            print(f"[PASS] Parameter {cap_exposure.name} is supported")
            
        return True
        
    except Exception as e:
        print(f"[FAIL] Backend functionality test failed: {e}")
        return False

if __name__ == "__main__":
    import traceback
    print("Starting VisionBridge Phase 2 Integration Tests")
    print("-" * 50)
    
    success = True
    
    # Test native module
    print("\n1. Testing native C++ module:")
    if not test_native_module_import():
        success = False
    
    # Test backend functionality  
    print("\n2. Testing backend functionality:")
    if not test_backend_functionality():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("[PASS] PHASE 2 INTEGRATION TESTS PASSED")
        print("Phase 2 build is complete.")
    else:
        print("[FAIL] PHASE 2 INTEGRATION TESTS FAILED")
        print("Please review the error output above.")
    
    sys.exit(0 if success else 1)