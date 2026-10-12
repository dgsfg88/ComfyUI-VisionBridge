"""Mock camera backend for development and testing without hardware."""


import struct
import sys
from typing import Dict, List, Optional

# Fix imports for top-level package usage
if __name__ == '__main__':
    pass  # This is just a check
else:
    from camera.base import CameraBackend, Capability, CameraError, ConnectionError, ParameterError


class MockCameraDevice:
    """Represents a virtual mock camera device."""
    
    def __init__(self, manufacturer: str = "Mock Manufacturer", 
                 model: str = "Mock GigE Camera", 
                 serial_number: str = "MOCK-001"):
        self.manufacturer = manufacturer
        self.model = model
        self.serial_number = serial_number
        
        # Simulated parameters with realistic ranges for industrial cameras
        self._numeric_params: Dict[str, tuple] = {
            'ExposureTime': (0.0001, 0.0256, 0.0001),  # [min, max, step] seconds
            'Gain': (0, 48, 1),  # dB
            'Width': (640, 4096, 4),  # pixels
            'Height': (480, 2304, 8),  # pixels
        }
        
        self._enum_params: Dict[str, tuple] = {
            'PixelFormat': ('Mono8', 'Mono12', 'Mono16', 'RGB8'),  # enum-like
            'TriggerMode': ('Software', 'Hardware', 'External'),  # enum-like
        }
        
        self._current_values: Dict[str, float] = {
            'ExposureTime': 0.0005,
            'Gain': 12,
            'Width': 640,
            'Height': 480,
            'PixelFormat': 0,  # Index for enum
            'TriggerMode': 0,  # Index for enum
        }


class MockCameraBackend(CameraBackend):
    """Mock implementation of CameraBackend for development without hardware."""
    
    def __init__(self):
        self._devices: List[MockCameraDevice] = []
        self._connected_device: Optional[MockCameraDevice] = None
    
    def add_mock_device(self, manufacturer: str = "Mock Manufacturer", 
                        model: str = "Mock GigE Camera",
                        serial_number: str = "") -> MockCameraDevice:
        """Add a virtual camera device to the mock backend."""
        serial = serial_number or f"MOCK-{len(self._devices) + 1:03d}"
        device = MockCameraDevice(manufacturer, model, serial)
        self._devices.append(device)
        return device
    
    def enumerate_devices(self) -> List[Dict]:
        """Return list of available mock devices."""
        if not self._devices:
            # Add a default mock device if none exist
            device = self.add_mock_device()
        
        result = []
        for i, device in enumerate(self._devices):
            result.append({
                'id': f'gige:{i}',
                'manufacturer': device.manufacturer,
                'model': device.model,
                'serial_number': device.serial_number
            })
        return result
    
    def connect(self, device_id: str) -> None:
        """Connect to a mock device."""
        if not self._devices:
            raise ConnectionError("No devices available")
        
        # Find matching device (simple string match for demo)
        for device in self._devices:
            if device_id == f'gige:{len(self._devices) - 1}':
                self._connected_device = device
                return
        
        raise ConnectionError(f"Device {device_id} not found")
    
    def disconnect(self) -> None:
        """Disconnect from the current device."""
        self._connected_device = None
    
    def get_capabilities(self) -> List[Capability]:
        """Return list of available parameters."""
        if not self._devices:
            return []
        
        device = self._devices[0]
        capabilities = []
        
        # Add numeric parameters
        for name, (min_val, max_val, step) in device._numeric_params.items():
            cap = Capability(
                name=name,
                description=f"Adjusts {name}",
                min_value=min_val,
                max_value=max_val,
                unit='seconds' if 'Time' in name else 'dB' if 'Gain' in name else '',
                supported=True
            )
            capabilities.append(cap)
        
        # Add enum parameters (simplified for mock)
        for name in device._enum_params:
            cap = Capability(
                name=name,
                description=f"Selects {name} mode",
                min_value=0,
                max_value=len(device._enum_params[name]) - 1,
                unit='index',
                supported=True
            )
            capabilities.append(cap)
        
        return capabilities
    
    def get_parameter(self, name: str) -> float:
        """Get current parameter value."""
        if not self._connected_device:
            raise ConnectionError("Not connected to a camera")
        
        if name not in self._connected_device._current_values:
            raise ParameterError(f"Parameter '{name}' is not supported by this device")
        
        return self._connected_device._current_values[name]
    
    def set_parameter(self, name: str, value: float) -> None:
        """Set a parameter value."""
        if not self._connected_device:
            raise ConnectionError("Not connected to a camera")
        
        device = self._connected_device
        
        if name in device._numeric_params:
            params = device._numeric_params[name]
            min_val, max_val, step = params
            value = max(min_val, min(max_val, round(value / step) * step))
            device._current_values[name] = value
            
        elif name in device._enum_params:
            # Convert enum index to float
            valid_values = device._enum_params[name]
            if isinstance(value, int):
                value = float(value)
            value = max(0, min(len(valid_values) - 1, int(round(value))))
            device._current_values[name] = value
            
        else:
            raise ParameterError(f"Parameter '{name}' is not supported by this device")
    
    def capture(self) -> bytes:
        """Capture an image (simulated)."""
        if not self._connected_device:
            raise ConnectionError("Not connected to a camera")
        
        width = int(self._connected_device._current_values['Width'])
        height = int(self._connected_device._current_values['Height'])
        pixel_format = self._connected_device._current_values['PixelFormat']
        
        # Generate simulated image data
        if pixel_format == 'Mono8':
            nbytes = 1  # unsigned char
        elif pixel_format == 'Mono12':
            nbytes = 2  # unsigned short
        elif pixel_format == 'Mono16':
            nbytes = 4  # unsigned int
        else:  # RGB8
            nbytes = 3
        
        size = width * height * nbytes
        image_data = bytearray(size)
        
        # Fill with gradient pattern for visual testing
        for i in range(size):
            val = (i * 255 // size) % 256
            image_data[i] = val
        
        return bytes(image_data)
