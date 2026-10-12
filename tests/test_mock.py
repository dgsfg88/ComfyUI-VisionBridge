#!/usr/bin/env python3
"""
Test suite for mock camera backend.

Tests:
1. MockCameraBackend can enumerate devices and return devices list
2. MockCameraBackend can connect to devices
3. MockCameraBackend can get capabilities
4. MockCameraBackend can get and set parameters
5. Capture function returns bytes with correct size
6. Unit tests using pytest
"""

import unittest
from backends.mock import MockCameraBackend
from camera.base import CameraBackend


class TestMockCameraBackend(unittest.TestCase):
    
    def test_enumerate_devices(self):
        """Test that enumerate_devices returns correct device information."""
        backend = MockCameraBackend()
        devices = backend.enumerate_devices()
        
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]['id'], 'gige:0')
        self.assertIn('GigE Camera', devices[0]['model'])
        self.assertTrue(devices[0]['manufacturer'].startswith('Mock'))

    def test_connect_device(self):
        """Test that connecting to a device works.""" 
        backend = MockCameraBackend()
        device_id = backend.enumerate_devices()[0]['id']
        backend.connect(device_id)
        
        # Should now be connected
        self.assertNotEqual(backend._connected_device, None)
        self.assertEqual(backend._connected_device.serial_number, 'MOCK-001')

    def test_disconnect_device(self):
        """Test that disconnecting from a device works."""
        backend = MockCameraBackend()
        device_id = backend.enumerate_devices()[0]['id']
        backend.connect(device_id)
        backend.disconnect()
        
        # Should be disconnected
        self.assertEqual(backend._connected_device, None)

    def test_get_capabilities(self):
        """Test that get_capabilities returns all expected capabilities."""
        backend = MockCameraBackend()
        device_id = backend.enumerate_devices()[0]['id']
        backend.connect(device_id)
        
        capabilities = backend.get_capabilities()
        
        self.assertEqual(len(capabilities), 6)  # ExposureTime, Gain, Width, Height, PixelFormat, TriggerMode
        
        capDesc = map(lambda x: x.name, capabilities)

        # Check specific capabilities
        self.assertIn("ExposureTime", capDesc, "ExposureTime")
        self.assertIn("Gain", capDesc, "Gain")
        self.assertIn("Width", capDesc, "Width")
        self.assertIn("Height", capDesc, "Height")
        self.assertIn("PixelFormat", capDesc, "PixelFormat")
        self.assertIn("TriggerMode", capDesc, "TriggerMode")

    def test_get_parameter(self):
        """Test getting parameters works correctly."""
        backend = MockCameraBackend()
        device_id = backend.enumerate_devices()[0]['id']
        backend.connect(device_id)
                
        # Default values should be within reasonable ranges
        self.assertAlmostEqual(backend.get_parameter('ExposureTime'), 0.0005)
        self.assertAlmostEqual(backend.get_parameter('Gain'), 12.0)
        self.assertEqual(backend.get_parameter('Width'), 640)
        self.assertEqual(backend.get_parameter('Height'), 480)

    def test_set_parameter(self):
        """Test setting parameters works correctly."""
        backend = MockCameraBackend()
        device_id = backend.enumerate_devices()[0]['id']
        backend.connect(device_id)
        
        # Set a new value
        backend.set_parameter('ExposureTime', 0.002)
        self.assertAlmostEqual(backend.get_parameter('ExposureTime'), 0.002)
        
        # Test numeric parameter clamps
        backend.set_parameter('Width', 720)
        self.assertEqual(backend.get_parameter('Width'), 720)
        
        backend.set_parameter('Height', 488)
        self.assertEqual(backend.get_parameter('Height'), 488)

    def test_capture(self):
        """Test capture function returns correct size bytes."""
        backend = MockCameraBackend()
        device_id = backend.enumerate_devices()[0]['id']
        backend.connect(device_id)
        
        raw_data = backend.capture()
        
        # Calculate expected size (640x480x3 bytes for RGB)
        self.assertEqual(len(raw_data), 640 * 480 * 3)
        self.assertGreater(len(raw_data), 0)


if __name__ == '__main__':
    unittest.main()