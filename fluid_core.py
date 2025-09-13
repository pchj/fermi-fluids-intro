# fluid_core.py
# Extracted and refactored core fluid simulation from fluid_langrangians.py
# 2D incompressible flow with semi-Lagrangian advection, vorticity confinement, Jacobi projection.
import numpy as np
import math


# ---------- boundaries ----------
def enforce_no_through(u, v):
    """Enforce no-slip boundary conditions on velocity field."""
    u[:, 0] = 0.0
    u[:, -1] = 0.0
    v[0, :] = 0.0
    v[-1, :] = 0.0


# ---------- operators ----------
def divergence(u, v):
    """Compute divergence of velocity field."""
    div = np.zeros_like(u)
    div[1:-1, 1:-1] = 0.5 * ((u[1:-1, 2:] - u[1:-1, :-2]) + (v[2:, 1:-1] - v[:-2, 1:-1]))
    div[:, 0] = u[:, 1] - u[:, 0]
    div[:, -1] = u[:, -1] - u[:, -2]
    div[0, :] += v[1, :] - v[0, :]
    div[-1, :] += v[-1, :] - v[-2, :]
    return div


def jacobi_pressure(div, iters=60):
    """Solve for pressure using Jacobi iteration."""
    p = np.zeros_like(div)
    for _ in range(iters):
        p_new = np.zeros_like(p)
        p_new[1:-1, 1:-1] = 0.25 * (p[1:-1, 2:] + p[1:-1, :-2] + p[2:, 1:-1] + p[:-2, 1:-1] - div[1:-1, 1:-1])
        p_new[:, 0] = p_new[:, 1]
        p_new[:, -1] = p_new[:, -2]
        p_new[0, :] = p_new[1, :]
        p_new[-1, :] = p_new[-2, :]
        p = p_new
    return p


def project(u, v, iters=60):
    """Project velocity field to be divergence-free using pressure correction."""
    enforce_no_through(u, v)
    div = divergence(u, v)
    p = jacobi_pressure(div, iters)
    u[:, 1:-1] -= 0.5 * (p[:, 2:] - p[:, :-2])
    v[1:-1, :] -= 0.5 * (p[2:, :] - p[:-2, :])
    enforce_no_through(u, v)
    return u, v


def curl_scalar(u, v):
    """Compute scalar curl (vorticity) of velocity field."""
    w = np.zeros_like(u)
    w[1:-1, 1:-1] = 0.5 * ((v[1:-1, 2:] - v[1:-1, :-2]) - (u[2:, 1:-1] - u[:-2, 1:-1]))
    w[:, 0] = v[:, 1] - v[:, 0]
    w[:, -1] = v[:, -1] - v[:, -2]
    w[0, :] -= u[1, :] - u[0, :]
    w[-1, :] -= u[-1, :] - u[-2, :]
    return w


def vorticity_confinement(u, v, strength, dt, eps0=1e-5):
    """Apply vorticity confinement to restore small-scale rotational energy."""
    if strength <= 0:
        return u, v
    w = curl_scalar(u, v)
    mag = np.abs(w)
    gx = np.zeros_like(mag)
    gy = np.zeros_like(mag)
    gx[1:-1, 1:-1] = 0.5 * (mag[1:-1, 2:] - mag[1:-1, :-2])
    gy[1:-1, 1:-1] = 0.5 * (mag[2:, 1:-1] - mag[:-2, 1:-1])
    norm = np.sqrt(gx * gx + gy * gy) + eps0
    Nx, Ny = gx / norm, gy / norm
    fx = strength * Ny * w
    fy = -strength * Nx * w
    u = u + dt * fx
    v = v + dt * fy
    enforce_no_through(u, v)
    return u, v


# ---------- semi-Lagrangian sampling ----------
def _bilinear_sample(F, x, y):
    """Bilinear interpolation for semi-Lagrangian advection."""
    N = F.shape[0]
    x = np.clip(x, 0.0, N - 1.001)
    y = np.clip(y, 0.0, N - 1.001)
    x0 = np.floor(x).astype(np.int32)
    y0 = np.floor(y).astype(np.int32)
    x1 = np.clip(x0 + 1, 0, N - 1)
    y1 = np.clip(y0 + 1, 0, N - 1)
    wx = x - x0
    wy = y - y0
    f00 = F[y0, x0]
    f10 = F[y0, x1]
    f01 = F[y1, x0]
    f11 = F[y1, x1]
    return (1 - wx) * (1 - wy) * f00 + wx * (1 - wy) * f10 + (1 - wx) * wy * f01 + wx * wy * f11


def advect_scalar(c, u, v, dt, diss=0.0):
    """Semi-Lagrangian advection of scalar field with optional dissipation."""
    N = c.shape[0]
    Y, X = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    xb = X - dt * u
    yb = Y - dt * v
    out = _bilinear_sample(c, xb, yb)
    if diss > 0:
        out *= math.exp(-diss * dt)
    return out


def advect_vector(u, v, dt, diss=0.0):
    """Semi-Lagrangian advection of velocity field with optional dissipation."""
    N = u.shape[0]
    Y, X = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    xb = X - dt * u
    yb = Y - dt * v
    u2 = _bilinear_sample(u, xb, yb)
    v2 = _bilinear_sample(v, xb, yb)
    if diss > 0:
        decay = math.exp(-diss * dt)
        u2 *= decay
        v2 *= decay
    enforce_no_through(u2, v2)
    return u2, v2


# ---------- splats ----------
def splat_scalar(c, x, y, radius, amount):
    """Add a Gaussian splat to scalar field."""
    N = c.shape[0]
    Y, X = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    cx, cy = x * (N - 1), y * (N - 1)
    r = radius * (N - 1)
    w = np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (r * r + 1e-6))
    return c + amount * w


def splat_vector(u, v, x, y, radius, fx, fy):
    """Add a Gaussian splat to velocity field."""
    N = u.shape[0]
    Y, X = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    cx, cy = x * (N - 1), y * (N - 1)
    r = radius * (N - 1)
    w = np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (r * r + 1e-6))
    u2, v2 = u + fx * w, v + fy * w
    enforce_no_through(u2, v2)
    return u2, v2


# ---------- utility functions ----------
def vorticity_magnitude(u, v):
    """Compute magnitude of vorticity field."""
    return np.abs(curl_scalar(u, v))


def velocity_magnitude(u, v):
    """Compute magnitude of velocity field."""
    return np.sqrt(u * u + v * v)


class FluidSim:
    """
    2D incompressible fluid simulation with semi-Lagrangian advection.
    
    This class encapsulates the fluid dynamics simulation including:
    - Semi-Lagrangian advection (unconditionally stable)
    - Pressure projection (enforces incompressibility)
    - Vorticity confinement (restores small-scale turbulence)
    - Scalar transport (dye advection)
    """
    
    def __init__(self, N=128, dt=0.08, vel_diss=0.08, dye_diss=0.12, vort_strength=6.0, iters=60):
        """
        Initialize fluid simulation.
        
        Args:
            N: Grid resolution (NxN)
            dt: Time step size
            vel_diss: Velocity dissipation rate
            dye_diss: Dye dissipation rate
            vort_strength: Vorticity confinement strength
            iters: Number of pressure projection iterations
        """
        self.N = N
        self.dt = dt
        self.vel_diss = vel_diss
        self.dye_diss = dye_diss
        self.vort_strength = vort_strength
        self.iters = iters
        
        # Initialize fields
        self.u = np.zeros((N, N), np.float32)
        self.v = np.zeros((N, N), np.float32)
        self.dye = np.zeros((N, N), np.float32)
        
        # Statistics
        self.step_count = 0
        self.divergence_history = []
        
    def reset(self):
        """Reset simulation to initial state."""
        self.u.fill(0.0)
        self.v.fill(0.0)
        self.dye.fill(0.0)
        self.step_count = 0
        self.divergence_history.clear()
    
    def add_splat(self, x, y, dye_amount=0.0, fx=0.0, fy=0.0, radius=0.05):
        """
        Add a splat of dye and/or velocity at normalized coordinates.
        
        Args:
            x, y: Normalized coordinates (0-1)
            dye_amount: Amount of dye to add
            fx, fy: Velocity force components
            radius: Normalized radius of the splat
        """
        if dye_amount != 0.0:
            self.dye = splat_scalar(self.dye, x, y, radius, dye_amount)
        if fx != 0.0 or fy != 0.0:
            self.u, self.v = splat_vector(self.u, self.v, x, y, radius, fx, fy)
    
    def step(self):
        """Advance simulation by one time step."""
        # Advect velocity field
        self.u, self.v = advect_vector(self.u, self.v, self.dt, diss=self.vel_diss)
        
        # Apply vorticity confinement
        self.u, self.v = vorticity_confinement(self.u, self.v, self.vort_strength, self.dt)
        
        # Project to enforce incompressibility
        pre_div = np.linalg.norm(divergence(self.u, self.v))
        self.u, self.v = project(self.u, self.v, iters=self.iters)
        post_div = np.linalg.norm(divergence(self.u, self.v))
        
        # Store divergence for statistics
        self.divergence_history.append(post_div)
        if len(self.divergence_history) > 100:  # Keep only recent history
            self.divergence_history.pop(0)
        
        # Advect dye
        self.dye = advect_scalar(self.dye, self.u, self.v, self.dt, diss=self.dye_diss)
        
        self.step_count += 1
        
        # Assert divergence reduction (for debugging)
        assert post_div < pre_div + 1e-6, f"Projection did not reduce divergence: {pre_div:.6f} -> {post_div:.6f}"
    
    def get_fields(self):
        """
        Get current simulation fields.
        
        Returns:
            dict: Dictionary containing all simulation fields
        """
        return {
            'dye': self.dye,
            'u': self.u,
            'v': self.v,
            'vorticity': vorticity_magnitude(self.u, self.v),
            'divergence': divergence(self.u, self.v),
            'velocity_mag': velocity_magnitude(self.u, self.v)
        }
    
    def get_stats(self):
        """
        Get current simulation statistics.
        
        Returns:
            dict: Dictionary containing simulation statistics
        """
        fields = self.get_fields()
        return {
            'step': self.step_count,
            'divergence_l2': self.divergence_history[-1] if self.divergence_history else 0.0,
            'max_velocity': np.max(fields['velocity_mag']),
            'cfl_estimate': np.max(fields['velocity_mag']) * self.dt,
            'max_dye': np.max(self.dye)
        }
    
    def set_params(self, **kwargs):
        """Update simulation parameters."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)