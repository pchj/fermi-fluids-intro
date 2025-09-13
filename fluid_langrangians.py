# pure_numpy_fluid.py
# 2D incompressible flow with semi-Lagrangian advection, vorticity confinement, Jacobi projection.
#
# NOTE: For an interactive GUI version of this simulation, see:
#   python fluid_gui.py
#
# This file contains the original headless implementation for reference and comparison.
import numpy as np, math

# ---------- boundaries ----------
def enforce_no_through(u, v):
    u[:, 0] = 0.0; u[:, -1] = 0.0
    v[0, :] = 0.0; v[-1, :] = 0.0

# ---------- operators ----------
def divergence(u, v):
    div = np.zeros_like(u)
    div[1:-1,1:-1] = 0.5*((u[1:-1,2:]-u[1:-1,:-2]) + (v[2:,1:-1]-v[:-2,1:-1]))
    div[:,0]   = u[:,1]-u[:,0]
    div[:,-1]  = u[:,-1]-u[:,-2]
    div[0,:]  += v[1,:]-v[0,:]
    div[-1,:] += v[-1,:]-v[-2,:]
    return div

def jacobi_pressure(div, iters=60):
    p = np.zeros_like(div)
    for _ in range(iters):
        p_new = np.zeros_like(p)
        p_new[1:-1,1:-1] = 0.25*(p[1:-1,2:]+p[1:-1,:-2]+p[2:,1:-1]+p[:-2,1:-1]-div[1:-1,1:-1])
        p_new[:,0]  = p_new[:,1]
        p_new[:,-1] = p_new[:,-2]
        p_new[0,:]  = p_new[1,:]
        p_new[-1,:] = p_new[-2,:]
        p = p_new
    return p

def project(u, v, iters=60):
    enforce_no_through(u, v)
    div = divergence(u, v)
    p = jacobi_pressure(div, iters)
    u[:,1:-1] -= 0.5*(p[:,2:]-p[:,:-2])
    v[1:-1,:] -= 0.5*(p[2:,:]-p[:-2,:])
    enforce_no_through(u, v)
    return u, v

def curl_scalar(u, v):
    w = np.zeros_like(u)
    w[1:-1,1:-1] = 0.5*((v[1:-1,2:]-v[1:-1,:-2]) - (u[2:,1:-1]-u[:-2,1:-1]))
    w[:,0]  = v[:,1]-v[:,0];   w[:, -1] = v[:,-1]-v[:,-2]
    w[0,:] -= u[1,:]-u[0,:];   w[-1,:] -= u[-1,:]-u[-2,:]
    return w

def vorticity_confinement(u, v, strength, dt, eps0=1e-5):
    if strength <= 0: return u, v
    w = curl_scalar(u, v); mag = np.abs(w)
    gx = np.zeros_like(mag); gy = np.zeros_like(mag)
    gx[1:-1,1:-1] = 0.5*(mag[1:-1,2:]-mag[1:-1,:-2])
    gy[1:-1,1:-1] = 0.5*(mag[2:,1:-1]-mag[:-2,1:-1])
    norm = np.sqrt(gx*gx+gy*gy)+eps0
    Nx, Ny = gx/norm, gy/norm
    fx = strength * Ny * w
    fy = -strength * Nx * w
    u = u + dt*fx; v = v + dt*fy
    enforce_no_through(u, v)
    return u, v

# ---------- semi-Lagrangian sampling ----------
def _bilinear_sample(F, x, y):
    N = F.shape[0]
    x = np.clip(x, 0.0, N-1.001); y = np.clip(y, 0.0, N-1.001)
    x0 = np.floor(x).astype(np.int32); y0 = np.floor(y).astype(np.int32)
    x1 = np.clip(x0+1, 0, N-1);        y1 = np.clip(y0+1, 0, N-1)
    wx = x - x0; wy = y - y0
    f00 = F[y0, x0]; f10 = F[y0, x1]; f01 = F[y1, x0]; f11 = F[y1, x1]
    return (1-wx)*(1-wy)*f00 + wx*(1-wy)*f10 + (1-wx)*wy*f01 + wx*wy*f11

def advect_scalar(c, u, v, dt, diss=0.0):
    N = c.shape[0]
    Y, X = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    xb = X - dt*u; yb = Y - dt*v
    out = _bilinear_sample(c, xb, yb)
    if diss>0: out *= math.exp(-diss*dt)
    return out

def advect_vector(u, v, dt, diss=0.0):
    N = u.shape[0]
    Y, X = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    xb = X - dt*u; yb = Y - dt*v
    u2 = _bilinear_sample(u, xb, yb)
    v2 = _bilinear_sample(v, xb, yb)
    if diss>0:
        decay = math.exp(-diss*dt); u2 *= decay; v2 *= decay
    enforce_no_through(u2, v2)
    return u2, v2

# ---------- splats ----------
def splat_scalar(c, x, y, radius, amount):
    N = c.shape[0]; Y, X = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    cx, cy = x*(N-1), y*(N-1); r = radius*(N-1)
    w = np.exp(-((X-cx)**2+(Y-cy)**2)/(r*r+1e-6))
    return c + amount*w

def splat_vector(u, v, x, y, radius, fx, fy):
    N = u.shape[0]; Y, X = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    cx, cy = x*(N-1), y*(N-1); r = radius*(N-1)
    w = np.exp(-((X-cx)**2+(Y-cy)**2)/(r*r+1e-6))
    u2, v2 = u + fx*w, v + fy*w
    enforce_no_through(u2, v2); return u2, v2

# ---------- main ----------
if __name__ == "__main__":
    N = 128
    rng = np.random.default_rng(7)
    u = np.zeros((N,N), np.float32); v = np.zeros((N,N), np.float32)
    dye = np.zeros((N,N), np.float32)

    # seed
    for _ in range(6):
        x, y = rng.random(), rng.random()
        ang = rng.random()*2*np.pi
        u, v = splat_vector(u, v, x, y, radius=0.07, fx=np.cos(ang)*0.6, fy=np.sin(ang)*0.6)
        dye = splat_scalar(dye, x, y, radius=0.07, amount=1.0)

    # quick projection sanity
    u_rand = rng.standard_normal((N,N))*0.1; v_rand = rng.standard_normal((N,N))*0.1
    enforce_no_through(u_rand, v_rand)
    d0 = np.linalg.norm(divergence(u_rand, v_rand))
    ur, vr = project(u_rand.copy(), v_rand.copy(), iters=60)
    d1 = np.linalg.norm(divergence(ur, vr))
    print(f"[projection test] L2(div) before={d0:.6f}, after={d1:.6f}")

    # simulate
    steps, dt = 120, 0.08
    vel_diss, dye_diss = 0.08, 0.12
    vort_strength, iters = 6.0, 60

    for s in range(steps):
        u, v = advect_vector(u, v, dt, diss=vel_diss)
        u, v = vorticity_confinement(u, v, strength=vort_strength, dt=dt)

        # assert local decrease in divergence across projection
        pre = np.linalg.norm(divergence(u, v))
        u, v = project(u, v, iters=iters)
        post = np.linalg.norm(divergence(u, v))
        assert post < pre + 1e-6, "Projection did not reduce divergence"

        dye = advect_scalar(dye, u, v, dt, diss=dye_diss)
        if s % 10 == 0 or s == steps-1:
            print(f"step {s:03d}  L2(div)≈ {post:.6f}")
