# fluid_gui.py
# Interactive GUI for fluid simulation using pygame
import pygame
import numpy as np
import sys
import time
from fluid_core import FluidSim
from colormaps import (
    dye_colormap, viridis_colormap, divergence_colormap, 
    velocity_arrows, grayscale_colormap, create_colorbar
)


class FluidGUI:
    """Interactive GUI for 2D fluid simulation."""
    
    def __init__(self, N=128, window_width=1000, window_height=700):
        """Initialize the GUI."""
        pygame.init()
        
        self.N = N
        self.window_width = window_width
        self.window_height = window_height
        self.panel_width = 250
        self.sim_size = min(window_width - self.panel_width, window_height)
        
        # Create window
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Interactive Fluid Simulation")
        
        # Initialize simulation
        self.sim = FluidSim(N=N)
        self._seed_initial_state()
        
        # GUI state
        self.running = True
        self.paused = False
        self.show_help = False
        self.visualization_mode = 0  # 0: dye, 1: vorticity, 2: divergence, 3: velocity
        self.viz_modes = ["Dye", "Vorticity", "Divergence", "Velocity"]
        
        # Fonts
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)
        
        # Colors
        self.bg_color = (20, 20, 30)
        self.panel_color = (40, 40, 50)
        self.text_color = (220, 220, 220)
        self.button_color = (80, 80, 100)
        self.button_hover_color = (100, 100, 120)
        
        # UI elements
        self.buttons = {}
        self.sliders = {}
        self._create_ui_elements()
        
        # Mouse state
        self.mouse_down = False
        self.last_mouse_pos = None
        
        # Performance tracking
        self.last_time = time.time()
        self.fps_history = []
        
        # Educational info
        self.help_text = [
            "CONTROLS:",
            "Left drag: Add dye + velocity",
            "Right click: Add velocity vortex",
            "Space: Pause/Resume",
            "S: Single step",
            "R: Reset simulation",
            "C: Clear dye",
            "H: Toggle this help",
            "1-4: Change visualization",
            "",
            "CONCEPTS:",
            "Semi-Lagrangian advection:",
            "- Unconditionally stable",
            "- Adds numerical diffusion",
            "",
            "Pressure projection:",
            "- Enforces incompressibility",
            "- Makes velocity divergence-free",
            "",
            "Vorticity confinement:",
            "- Restores small-scale turbulence",
            "- Counteracts numerical dissipation"
        ]
    
    def _seed_initial_state(self):
        """Add some initial dye and velocity to make it interesting."""
        rng = np.random.default_rng(42)
        for _ in range(3):
            x, y = rng.random(), rng.random()
            angle = rng.random() * 2 * np.pi
            fx, fy = np.cos(angle) * 0.5, np.sin(angle) * 0.5
            self.sim.add_splat(x, y, dye_amount=0.8, fx=fx, fy=fy, radius=0.08)
    
    def _create_ui_elements(self):
        """Create UI buttons and sliders."""
        panel_x = self.window_width - self.panel_width + 10
        y = 10
        
        # Visualization mode button
        self.buttons['viz_mode'] = pygame.Rect(panel_x, y, 180, 30)
        y += 40
        
        # Control buttons
        button_width = 80
        button_spacing = 90
        self.buttons['pause'] = pygame.Rect(panel_x, y, button_width, 30)
        self.buttons['step'] = pygame.Rect(panel_x + button_spacing, y, button_width, 30)
        y += 40
        
        self.buttons['reset'] = pygame.Rect(panel_x, y, button_width, 30)
        self.buttons['clear'] = pygame.Rect(panel_x + button_spacing, y, button_width, 30)
        y += 50
        
        # Parameter sliders (simplified for now - just show text)
        self.slider_y_start = y
    
    def _draw_text(self, text, x, y, font=None, color=None):
        """Draw text on screen."""
        if font is None:
            font = self.font_small
        if color is None:
            color = self.text_color
        
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))
        return surface.get_height()
    
    def _draw_button(self, name, text, mouse_pos):
        """Draw a button and return if it's hovered."""
        rect = self.buttons[name]
        hovered = rect.collidepoint(mouse_pos)
        
        color = self.button_hover_color if hovered else self.button_color
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, self.text_color, rect, 2)
        
        # Center text in button
        text_surface = self.font_small.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return hovered
    
    def _draw_panel(self, mouse_pos):
        """Draw the control panel."""
        panel_rect = pygame.Rect(self.window_width - self.panel_width, 0, self.panel_width, self.window_height)
        pygame.draw.rect(self.screen, self.panel_color, panel_rect)
        
        panel_x = self.window_width - self.panel_width + 10
        y = 10
        
        # Title
        self._draw_text("Fluid Simulation", panel_x, y, self.font_medium)
        y += 30
        
        # Visualization mode
        viz_text = f"Mode: {self.viz_modes[self.visualization_mode]}"
        self._draw_button('viz_mode', viz_text, mouse_pos)
        y += 40
        
        # Control buttons
        self._draw_button('pause', "Pause" if not self.paused else "Resume", mouse_pos)
        self._draw_button('step', "Step", mouse_pos)
        y += 40
        
        self._draw_button('reset', "Reset", mouse_pos)
        self._draw_button('clear', "Clear Dye", mouse_pos)
        y += 50
        
        # Parameters
        self._draw_text("Parameters:", panel_x, y, self.font_small)
        y += 25
        
        params = [
            f"dt: {self.sim.dt:.3f}",
            f"vel_diss: {self.sim.vel_diss:.3f}",
            f"dye_diss: {self.sim.dye_diss:.3f}",
            f"vort_str: {self.sim.vort_strength:.1f}",
            f"proj_iters: {self.sim.iters}",
        ]
        
        for param in params:
            self._draw_text(param, panel_x, y, self.font_small)
            y += 20
        
        y += 10
        
        # Statistics
        self._draw_text("Statistics:", panel_x, y, self.font_small)
        y += 25
        
        stats = self.sim.get_stats()
        stat_lines = [
            f"Step: {stats['step']}",
            f"L2(div): {stats['divergence_l2']:.6f}",
            f"Max |v|: {stats['max_velocity']:.3f}",
            f"CFL: {stats['cfl_estimate']:.3f}",
        ]
        
        # Add FPS
        current_time = time.time()
        dt = current_time - self.last_time
        if dt > 0:
            fps = 1.0 / dt
            self.fps_history.append(fps)
            if len(self.fps_history) > 10:
                self.fps_history.pop(0)
            avg_fps = sum(self.fps_history) / len(self.fps_history)
            stat_lines.append(f"FPS: {avg_fps:.1f}")
        self.last_time = current_time
        
        for stat in stat_lines:
            self._draw_text(stat, panel_x, y, self.font_small)
            y += 20
        
        y += 10
        
        # Divergence history (simple sparkline)
        if len(self.sim.divergence_history) > 1:
            self._draw_text("Divergence History:", panel_x, y, self.font_small)
            y += 20
            
            # Draw simple line chart
            chart_width = 200
            chart_height = 40
            chart_rect = pygame.Rect(panel_x, y, chart_width, chart_height)
            pygame.draw.rect(self.screen, (30, 30, 40), chart_rect)
            pygame.draw.rect(self.screen, self.text_color, chart_rect, 1)
            
            if len(self.sim.divergence_history) > 1:
                history = self.sim.divergence_history[-50:]  # Last 50 points
                max_div = max(history) if max(history) > 0 else 1.0
                
                points = []
                for i, div_val in enumerate(history):
                    x = panel_x + (i / (len(history) - 1)) * chart_width
                    y_val = y + chart_height - (div_val / max_div) * chart_height
                    points.append((x, y_val))
                
                if len(points) > 1:
                    pygame.draw.lines(self.screen, (100, 200, 100), False, points, 2)
            
            y += chart_height + 10
        
        # Instructions
        y += 10
        self._draw_text("Controls:", panel_x, y, self.font_small)
        y += 20
        instructions = [
            "Left drag: Add dye+velocity",
            "Right click: Add vortex",
            "Space: Pause  S: Step",
            "R: Reset  C: Clear dye",
            "H: Help  1-4: Viz mode"
        ]
        for instruction in instructions:
            self._draw_text(instruction, panel_x, y, self.font_small, (180, 180, 180))
            y += 15
    
    def _draw_help(self):
        """Draw help overlay."""
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Draw help text
        x = 50
        y = 50
        for line in self.help_text:
            if line == "":
                y += 10
            else:
                font = self.font_medium if line.endswith(":") else self.font_small
                self._draw_text(line, x, y, font, (255, 255, 255))
                y += 25 if line.endswith(":") else 20
    
    def _field_to_surface(self, field, colormap_func):
        """Convert a field to a pygame surface."""
        rgb_array = colormap_func(field)
        
        # Ensure rgb_array is the right shape
        if len(rgb_array.shape) != 3 or rgb_array.shape[2] != 3:
            raise ValueError(f"Expected RGB array of shape (H, W, 3), got {rgb_array.shape}")
        
        # Resize to simulation display size if needed
        if rgb_array.shape[0] != self.sim_size:
            # Simple nearest neighbor resize
            scale_factor = self.sim_size / self.N
            new_shape = (self.sim_size, self.sim_size, 3)
            resized = np.zeros(new_shape, dtype=np.uint8)
            
            for i in range(self.sim_size):
                for j in range(self.sim_size):
                    orig_i = int(i / scale_factor)
                    orig_j = int(j / scale_factor)
                    orig_i = min(orig_i, self.N - 1)
                    orig_j = min(orig_j, self.N - 1)
                    resized[i, j] = rgb_array[orig_i, orig_j]
            
            rgb_array = resized
        
        # Transpose for pygame (pygame expects width, height order)
        rgb_array = np.transpose(rgb_array, (1, 0, 2))
        
        return pygame.surfarray.make_surface(rgb_array)
    
    def _draw_simulation(self):
        """Draw the main simulation area."""
        fields = self.sim.get_fields()
        
        if self.visualization_mode == 0:  # Dye
            surface = self._field_to_surface(fields['dye'], dye_colormap)
        elif self.visualization_mode == 1:  # Vorticity
            surface = self._field_to_surface(fields['vorticity'], viridis_colormap)
        elif self.visualization_mode == 2:  # Divergence
            surface = self._field_to_surface(fields['divergence'], divergence_colormap)
        elif self.visualization_mode == 3:  # Velocity magnitude
            surface = self._field_to_surface(fields['velocity_mag'], viridis_colormap)
        
        self.screen.blit(surface, (0, 0))
        
        # Draw velocity arrows if in velocity mode
        if self.visualization_mode == 3:
            arrows = velocity_arrows(fields['u'], fields['v'], downsample=max(1, self.N // 16), scale=10)
            for x1, y1, x2, y2 in arrows:
                # Scale to display coordinates
                scale = self.sim_size / self.N
                x1, y1, x2, y2 = x1 * scale, y1 * scale, x2 * scale, y2 * scale
                if 0 <= x2 < self.sim_size and 0 <= y2 < self.sim_size:
                    pygame.draw.line(self.screen, (255, 255, 255), (x1, y1), (x2, y2), 2)
    
    def _handle_mouse_input(self, mouse_pos, mouse_buttons):
        """Handle mouse input for adding splats."""
        if mouse_pos[0] < self.sim_size:  # Only in simulation area
            # Convert to normalized coordinates
            x = mouse_pos[0] / self.sim_size
            y = mouse_pos[1] / self.sim_size
            
            if mouse_buttons[0]:  # Left button: dye + velocity
                if self.last_mouse_pos is not None:
                    # Calculate velocity from mouse movement
                    last_x = self.last_mouse_pos[0] / self.sim_size
                    last_y = self.last_mouse_pos[1] / self.sim_size
                    fx = (x - last_x) * 20  # Scale factor for velocity
                    fy = (y - last_y) * 20
                else:
                    fx = fy = 0
                
                self.sim.add_splat(x, y, dye_amount=0.5, fx=fx, fy=fy, radius=0.03)
            
            elif mouse_buttons[2]:  # Right button: velocity vortex
                # Add a small vortex
                angle = np.random.random() * 2 * np.pi
                strength = 0.8
                fx = np.cos(angle) * strength
                fy = np.sin(angle) * strength
                self.sim.add_splat(x, y, dye_amount=0.0, fx=fx, fy=fy, radius=0.04)
        
        self.last_mouse_pos = mouse_pos if any(mouse_buttons) else None
    
    def _handle_button_click(self, mouse_pos):
        """Handle button clicks."""
        for name, rect in self.buttons.items():
            if rect.collidepoint(mouse_pos):
                if name == 'viz_mode':
                    self.visualization_mode = (self.visualization_mode + 1) % len(self.viz_modes)
                elif name == 'pause':
                    self.paused = not self.paused
                elif name == 'step':
                    if self.paused:
                        self.sim.step()
                elif name == 'reset':
                    self.sim.reset()
                    self._seed_initial_state()
                elif name == 'clear':
                    self.sim.dye.fill(0.0)
                break
    
    def _handle_keyboard(self, key):
        """Handle keyboard input."""
        if key == pygame.K_SPACE:
            self.paused = not self.paused
        elif key == pygame.K_s:
            if self.paused:
                self.sim.step()
        elif key == pygame.K_r:
            self.sim.reset()
            self._seed_initial_state()
        elif key == pygame.K_c:
            self.sim.dye.fill(0.0)
        elif key == pygame.K_h:
            self.show_help = not self.show_help
        elif key == pygame.K_1:
            self.visualization_mode = 0
        elif key == pygame.K_2:
            self.visualization_mode = 1
        elif key == pygame.K_3:
            self.visualization_mode = 2
        elif key == pygame.K_4:
            self.visualization_mode = 3
    
    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self._handle_keyboard(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_button_click(mouse_pos)
            
            # Handle continuous mouse input
            self._handle_mouse_input(mouse_pos, mouse_buttons)
            
            # Update simulation
            if not self.paused:
                self.sim.step()
            
            # Draw everything
            self.screen.fill(self.bg_color)
            self._draw_simulation()
            self._draw_panel(mouse_pos)
            
            if self.show_help:
                self._draw_help()
            
            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS
        
        pygame.quit()


def main():
    """Main entry point."""
    # Parse command line arguments
    N = 128
    if len(sys.argv) > 1:
        try:
            N = int(sys.argv[1])
            N = max(32, min(512, N))  # Clamp to reasonable range
        except ValueError:
            print(f"Invalid grid size: {sys.argv[1]}. Using default N=128.")
    
    print(f"Starting fluid simulation with {N}x{N} grid")
    print("Controls:")
    print("  Left drag: Add dye + velocity")
    print("  Right click: Add velocity vortex")
    print("  Space: Pause/Resume")
    print("  S: Single step when paused")
    print("  R: Reset simulation")
    print("  C: Clear dye")
    print("  H: Toggle help overlay")
    print("  1-4: Change visualization mode")
    
    gui = FluidGUI(N=N)
    gui.run()


if __name__ == "__main__":
    main()