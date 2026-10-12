"""Camera Backend Interface - Common API for all camera backends."""


class CameraError(Exception):
    """Base exception for camera-related errors."""
    pass


class ConnectionError(CameraError):
    """Raised when camera connection fails."""
    pass


class ParameterError(CameraError):
    """Raised when parameter is invalid or unsupported."""
    pass


class Capability:
    """Represents a camera capability/parameter."""
    
    def __init__(self, name: str, description: str = "", min_value: float = None, 
                 max_value: float = None, unit: str = "", supported: bool = True):
        self.name = name
        self.description = description
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.supported = supported
    
    def __repr__(self) -> str:
        return f"Capability({self.name}, supported={self.supported})"


class CameraBackend:
    """Abstract base class for camera backends.
    
    All backends must implement these methods to be compatible with the ComfyUI nodes.
    """
    
    def enumerate_devices(self) -> list[dict]:
        """Enumerate available cameras and return device information.
        
        Returns:
            List of dictionaries with keys: id, manufacturer, model, serial_number
        """
        raise NotImplementedError
    
    def connect(self, device_id: str) -> None:
        """Connect to the specified camera device.
        
        Args:
            device_id: The ID returned from enumerate_devices()
            
        Raises:
            ConnectionError: If connection fails
        """
        raise NotImplementedError
    
    def disconnect(self) -> None:
        """Disconnect from the camera."""
        raise NotImplementedError
    
    def get_capabilities(self) -> list[Capability]:
        """Get list of available capabilities/parameters.
        
        Returns:
            List of Capability objects for supported parameters
        """
        raise NotImplementedError
    
    def get_parameter(self, name: str) -> float:
        """Get current value of a parameter.
        
        Args:
            name: Parameter name (e.g., 'ExposureTime', 'Gain')
            
        Returns:
            Current parameter value
            
        Raises:
            ParameterError: If parameter doesn't exist or is not supported
        """
        raise NotImplementedError
    
    def set_parameter(self, name: str, value: float) -> None:
        """Set a parameter value.
        
        Args:
            name: Parameter name
            value: New parameter value
            
        Raises:
            ParameterError: If parameter is invalid or not supported
        """
        raise NotImplementedError
    
    def capture(self) -> bytes:
        """Capture an image from the camera.
        
        Returns:
            Raw image data as bytes (format depends on backend)
            
        Raises:
            CameraError: If capture fails
        """
        raise NotImplementedError
