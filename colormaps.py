# colormaps.py
# Simple colormap utilities for fluid visualization
import numpy as np


def normalize_field(field, vmin=None, vmax=None):
    """
    Normalize a field to [0, 1] range.
    
    Args:
        field: Input field array
        vmin: Minimum value (auto-detected if None)
        vmax: Maximum value (auto-detected if None)
        
    Returns:
        Normalized field in [0, 1] range
    """
    if vmin is None:
        vmin = np.min(field)
    if vmax is None:
        vmax = np.max(field)
    
    if vmax == vmin:
        return np.zeros_like(field)
    
    return np.clip((field - vmin) / (vmax - vmin), 0.0, 1.0)


def grayscale_colormap(field, vmin=None, vmax=None):
    """
    Convert scalar field to grayscale RGB.
    
    Args:
        field: Input scalar field
        vmin: Minimum value for normalization
        vmax: Maximum value for normalization
        
    Returns:
        RGB array of shape (H, W, 3) with values in [0, 255]
    """
    normalized = normalize_field(field, vmin, vmax)
    gray = (normalized * 255).astype(np.uint8)
    return np.stack([gray, gray, gray], axis=-1)


def viridis_colormap(field, vmin=None, vmax=None):
    """
    Apply a viridis-like colormap to scalar field.
    
    Args:
        field: Input scalar field
        vmin: Minimum value for normalization
        vmax: Maximum value for normalization
        
    Returns:
        RGB array of shape (H, W, 3) with values in [0, 255]
    """
    normalized = normalize_field(field, vmin, vmax)
    
    # Simple viridis-like colormap
    r = np.interp(normalized, [0, 0.25, 0.5, 0.75, 1.0], [0.267, 0.127, 0.0, 0.349, 0.993])
    g = np.interp(normalized, [0, 0.25, 0.5, 0.75, 1.0], [0.004, 0.566, 0.713, 0.906, 0.906])
    b = np.interp(normalized, [0, 0.25, 0.5, 0.75, 1.0], [0.329, 0.550, 0.517, 0.180, 0.144])
    
    rgb = np.stack([r, g, b], axis=-1)
    return (rgb * 255).astype(np.uint8)


def divergence_colormap(field, symmetric=True):
    """
    Blue-red colormap for divergence (blue=negative, red=positive).
    
    Args:
        field: Divergence field
        symmetric: If True, use symmetric range around zero
        
    Returns:
        RGB array of shape (H, W, 3) with values in [0, 255]
    """
    if symmetric:
        max_abs = np.max(np.abs(field))
        vmin, vmax = -max_abs, max_abs
    else:
        vmin, vmax = np.min(field), np.max(field)
    
    normalized = normalize_field(field, vmin, vmax)
    
    # Blue for negative (diverging), red for positive (converging)
    r = np.where(normalized > 0.5, (normalized - 0.5) * 2, 0)
    g = np.zeros_like(normalized)
    b = np.where(normalized < 0.5, (0.5 - normalized) * 2, 0)
    
    rgb = np.stack([r, g, b], axis=-1)
    return (rgb * 255).astype(np.uint8)


def velocity_arrows(u, v, downsample=8, scale=1.0):
    """
    Generate downsampled velocity arrow data for visualization.
    
    Args:
        u, v: Velocity components
        downsample: Factor to downsample the grid
        scale: Scaling factor for arrow length
        
    Returns:
        List of (x1, y1, x2, y2) tuples for drawing arrows
    """
    N = u.shape[0]
    arrows = []
    
    for i in range(0, N, downsample):
        for j in range(0, N, downsample):
            if i < N and j < N:
                x1, y1 = j, i
                dx, dy = u[i, j] * scale, v[i, j] * scale
                x2, y2 = x1 + dx, y1 + dy
                arrows.append((x1, y1, x2, y2))
    
    return arrows


def dye_colormap(field, vmin=None, vmax=None, color=(255, 100, 100)):
    """
    Colormap for dye visualization with custom color.
    
    Args:
        field: Dye concentration field
        vmin: Minimum value for normalization
        vmax: Maximum value for normalization
        color: RGB color tuple for maximum concentration
        
    Returns:
        RGB array of shape (H, W, 3) with values in [0, 255]
    """
    normalized = normalize_field(field, vmin, vmax)
    
    # Blend from black to the specified color
    r = normalized * color[0]
    g = normalized * color[1]
    b = normalized * color[2]
    
    rgb = np.stack([r, g, b], axis=-1)
    return rgb.astype(np.uint8)


def create_colorbar(colormap_func, width=20, height=200):
    """
    Create a colorbar for a given colormap function.
    
    Args:
        colormap_func: Function that takes a field and returns RGB
        width: Width of colorbar in pixels
        height: Height of colorbar in pixels
        
    Returns:
        RGB array representing the colorbar
    """
    # Create a vertical gradient from 0 to 1
    gradient = np.linspace(1, 0, height).reshape(-1, 1)
    gradient = np.tile(gradient, (1, width))
    
    # Apply the colormap
    return colormap_func(gradient, vmin=0, vmax=1)