// Fermi Fluids Tutorial JavaScript
// Interactive visualizations using Canvas API

class FermiFluidsVisualization {
    constructor() {
        this.initializeConstants();
        this.setupEventListeners();
        this.createVisualizationsSafely();
    }

    initializeConstants() {
        this.kF = 1.0; // Fermi momentum (normalized)
        this.EF = 1.0; // Fermi energy (normalized)
        this.temperature = 0.0; // Temperature in units of EF/kB
        this.interactionStrength = 0.0; // Landau parameter F0s
    }

    setupEventListeners() {
        // Temperature slider
        const tempSlider = document.getElementById('temperature-slider');
        const tempValue = document.getElementById('temperature-value');
        if (tempSlider && tempValue) {
            tempSlider.addEventListener('input', (e) => {
                this.temperature = parseFloat(e.target.value);
                tempValue.textContent = this.temperature.toFixed(2);
                this.updateFermiSphereViz();
            });
        }

        // Interaction strength slider
        const intSlider = document.getElementById('interaction-slider');
        const intValue = document.getElementById('interaction-value');
        if (intSlider && intValue) {
            intSlider.addEventListener('input', (e) => {
                this.interactionStrength = parseFloat(e.target.value);
                intValue.textContent = this.interactionStrength.toFixed(1);
                this.updateQuasiparticleViz();
            });
        }

        // Smooth scrolling for navigation
        document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    createVisualizationsSafely() {
        // Delay creation to ensure DOM is ready
        setTimeout(() => {
            this.createIntroVisualization();
            this.createFermiSphereVisualization();
            this.createQuasiparticleVisualization();
            this.createInteractionVisualization();
            this.createTransportVisualization();
        }, 100);
    }

    // Utility function to get canvas and context
    getCanvasContext(id) {
        const canvas = document.getElementById(id);
        if (!canvas) return null;
        
        const ctx = canvas.getContext('2d');
        
        // Set actual canvas size
        canvas.width = 500;
        canvas.height = 400;
        
        return { canvas, ctx };
    }

    // Utility function to draw axes
    drawAxes(ctx, width, height, margin, xLabel, yLabel, xMax = 3, yMax = 1.2) {
        const plotWidth = width - margin.left - margin.right;
        const plotHeight = height - margin.top - margin.bottom;
        
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2;
        
        // X-axis
        ctx.beginPath();
        ctx.moveTo(margin.left, height - margin.bottom);
        ctx.lineTo(width - margin.right, height - margin.bottom);
        ctx.stroke();
        
        // Y-axis
        ctx.beginPath();
        ctx.moveTo(margin.left, margin.top);
        ctx.lineTo(margin.left, height - margin.bottom);
        ctx.stroke();
        
        // Axis labels
        ctx.fillStyle = '#333';
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(xLabel, width / 2, height - 10);
        
        ctx.save();
        ctx.translate(15, height / 2);
        ctx.rotate(-Math.PI / 2);
        ctx.fillText(yLabel, 0, 0);
        ctx.restore();
        
        // Tick marks and grid
        ctx.strokeStyle = '#ddd';
        ctx.lineWidth = 1;
        
        // X-axis ticks
        for (let i = 0; i <= 5; i++) {
            const x = margin.left + (i / 5) * plotWidth;
            ctx.beginPath();
            ctx.moveTo(x, height - margin.bottom);
            ctx.lineTo(x, height - margin.bottom + 5);
            ctx.stroke();
            
            // Grid lines
            if (i > 0 && i < 5) {
                ctx.beginPath();
                ctx.moveTo(x, margin.top);
                ctx.lineTo(x, height - margin.bottom);
                ctx.stroke();
            }
            
            // Labels
            ctx.fillStyle = '#666';
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText((i / 5 * xMax).toFixed(1), x, height - margin.bottom + 20);
        }
        
        // Y-axis ticks
        for (let i = 0; i <= 5; i++) {
            const y = height - margin.bottom - (i / 5) * plotHeight;
            ctx.beginPath();
            ctx.moveTo(margin.left - 5, y);
            ctx.lineTo(margin.left, y);
            ctx.stroke();
            
            // Grid lines
            if (i > 0 && i < 5) {
                ctx.beginPath();
                ctx.moveTo(margin.left, y);
                ctx.lineTo(width - margin.right, y);
                ctx.stroke();
            }
            
            // Labels
            ctx.fillStyle = '#666';
            ctx.font = '12px Arial';
            ctx.textAlign = 'right';
            ctx.fillText((i / 5 * yMax).toFixed(1), margin.left - 10, y + 4);
        }
        
        return { plotWidth, plotHeight };
    }

    createIntroVisualization() {
        const result = this.getCanvasContext('intro-viz');
        if (!result) return;
        
        const { canvas, ctx } = result;
        const width = canvas.width;
        const height = canvas.height;
        const margin = { top: 20, right: 20, bottom: 60, left: 60 };
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        const { plotWidth, plotHeight } = this.drawAxes(ctx, width, height, margin, 'k/kF', 'n(k)', 2, 1);
        
        // Draw Fermi step function
        ctx.strokeStyle = '#3498db';
        ctx.lineWidth = 3;
        ctx.beginPath();
        
        const steps = 200;
        for (let i = 0; i <= steps; i++) {
            const k = (i / steps) * 2;
            const n = k <= 1 ? 1 : 0;
            
            const x = margin.left + (k / 2) * plotWidth;
            const y = height - margin.bottom - n * plotHeight;
            
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        ctx.stroke();
        
        // Fermi surface line
        const kFx = margin.left + (1 / 2) * plotWidth;
        ctx.strokeStyle = '#e74c3c';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.moveTo(kFx, margin.top);
        ctx.lineTo(kFx, height - margin.bottom);
        ctx.stroke();
        ctx.setLineDash([]);
        
        // Labels
        ctx.fillStyle = '#3498db';
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Filled states', margin.left + plotWidth * 0.25, height / 2);
        
        ctx.fillStyle = '#e74c3c';
        ctx.fillText('Empty states', margin.left + plotWidth * 0.75, height / 2);
        
        ctx.fillStyle = '#e74c3c';
        ctx.font = '14px Arial';
        ctx.fillText('Fermi surface', kFx + 20, margin.top + 30);
    }

    createFermiSphereVisualization() {
        this.updateFermiSphereViz();
    }

    updateFermiSphereViz() {
        const result = this.getCanvasContext('fermi-sphere-viz');
        if (!result) return;
        
        const { canvas, ctx } = result;
        const width = canvas.width;
        const height = canvas.height;
        const margin = { top: 20, right: 20, bottom: 60, left: 60 };
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        const { plotWidth, plotHeight } = this.drawAxes(ctx, width, height, margin, 'Energy (E/EF)', 'f(E)', 3, 1.2);
        
        // Draw Fermi-Dirac distribution
        ctx.strokeStyle = '#3498db';
        ctx.lineWidth = 3;
        ctx.beginPath();
        
        const steps = 300;
        for (let i = 0; i <= steps; i++) {
            const E = (i / steps) * 3;
            const f = this.fermiDirac(E, 1, this.temperature);
            
            const x = margin.left + (E / 3) * plotWidth;
            const y = height - margin.bottom - (f / 1.2) * plotHeight;
            
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        ctx.stroke();
        
        // Fermi energy line
        const EFx = margin.left + (1 / 3) * plotWidth;
        ctx.strokeStyle = '#e74c3c';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.moveTo(EFx, margin.top);
        ctx.lineTo(EFx, height - margin.bottom);
        ctx.stroke();
        ctx.setLineDash([]);
        
        // Labels
        ctx.fillStyle = '#e74c3c';
        ctx.font = '14px Arial';
        ctx.textAlign = 'left';
        ctx.fillText('EF', EFx + 5, margin.top + 20);
        
        if (this.temperature > 0) {
            ctx.fillStyle = '#3498db';
            ctx.font = '14px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(`kBT/EF = ${this.temperature.toFixed(2)}`, margin.left + plotWidth * 0.7, margin.top + 40);
        }
    }

    createQuasiparticleVisualization() {
        this.updateQuasiparticleViz();
    }

    updateQuasiparticleViz() {
        const result = this.getCanvasContext('quasiparticle-viz');
        if (!result) return;
        
        const { canvas, ctx } = result;
        const width = canvas.width;
        const height = canvas.height;
        const margin = { top: 20, right: 20, bottom: 60, left: 60 };
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Custom scale for this plot
        const kMin = 0.5, kMax = 1.5;
        const EMin = 0.5, EMax = 1.5;
        
        // Draw custom axes
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2;
        
        // X-axis
        ctx.beginPath();
        ctx.moveTo(margin.left, height - margin.bottom);
        ctx.lineTo(width - margin.right, height - margin.bottom);
        ctx.stroke();
        
        // Y-axis
        ctx.beginPath();
        ctx.moveTo(margin.left, margin.top);
        ctx.lineTo(margin.left, height - margin.bottom);
        ctx.stroke();
        
        const plotWidth = width - margin.left - margin.right;
        const plotHeight = height - margin.top - margin.bottom;
        
        // Free particle dispersion (dashed)
        ctx.strokeStyle = '#95a5a6';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        
        const steps = 100;
        for (let i = 0; i <= steps; i++) {
            const k = kMin + (i / steps) * (kMax - kMin);
            const E = k * k; // Free particle: E ∝ k²
            
            const x = margin.left + ((k - kMin) / (kMax - kMin)) * plotWidth;
            const y = height - margin.bottom - ((E - EMin) / (EMax - EMin)) * plotHeight;
            
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        ctx.stroke();
        ctx.setLineDash([]);
        
        // Quasiparticle dispersion with interactions
        const effectiveMass = 1 + this.interactionStrength / 3;
        ctx.strokeStyle = '#27ae60';
        ctx.lineWidth = 3;
        ctx.beginPath();
        
        for (let i = 0; i <= steps; i++) {
            const k = kMin + (i / steps) * (kMax - kMin);
            const E = 1 + (k - 1) / effectiveMass; // Linear near Fermi surface
            
            const x = margin.left + ((k - kMin) / (kMax - kMin)) * plotWidth;
            const y = height - margin.bottom - ((E - EMin) / (EMax - EMin)) * plotHeight;
            
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        ctx.stroke();
        
        // Fermi surface lines
        const kFx = margin.left + ((1 - kMin) / (kMax - kMin)) * plotWidth;
        const EFy = height - margin.bottom - ((1 - EMin) / (EMax - EMin)) * plotHeight;
        
        ctx.strokeStyle = '#e74c3c';
        ctx.lineWidth = 2;
        
        // Vertical line at kF
        ctx.beginPath();
        ctx.moveTo(kFx, margin.top);
        ctx.lineTo(kFx, height - margin.bottom);
        ctx.stroke();
        
        // Horizontal line at EF
        ctx.beginPath();
        ctx.moveTo(margin.left, EFy);
        ctx.lineTo(width - margin.right, EFy);
        ctx.stroke();
        
        // Labels
        ctx.fillStyle = '#95a5a6';
        ctx.font = '14px Arial';
        ctx.textAlign = 'left';
        ctx.fillText('Free particles', margin.left + plotWidth * 0.6, margin.top + 30);
        
        ctx.fillStyle = '#27ae60';
        ctx.fillText('Quasiparticles', margin.left + plotWidth * 0.6, margin.top + 50);
        
        ctx.fillStyle = '#e74c3c';
        ctx.textAlign = 'center';
        ctx.fillText('(kF, EF)', kFx + 20, EFy - 10);
        
        ctx.fillStyle = '#2c3e50';
        ctx.textAlign = 'left';
        ctx.fillText(`m*/m = ${effectiveMass.toFixed(2)}`, margin.left + 20, height - margin.bottom - 20);
        
        // Axis labels
        ctx.fillStyle = '#333';
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('k/kF', width / 2, height - 10);
        
        ctx.save();
        ctx.translate(15, height / 2);
        ctx.rotate(-Math.PI / 2);
        ctx.fillText('E/EF', 0, 0);
        ctx.restore();
    }

    createInteractionVisualization() {
        const result = this.getCanvasContext('interaction-viz');
        if (!result) return;
        
        const { canvas, ctx } = result;
        const width = canvas.width;
        const height = canvas.height;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = 120;
        
        // Fermi sphere (circle in 2D projection)
        ctx.strokeStyle = '#3498db';
        ctx.fillStyle = 'rgba(52, 152, 219, 0.2)';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
        
        // Quasiparticle interactions (arrows)
        const angleStep = Math.PI / 8;
        for (let angle = 0; angle < 2 * Math.PI; angle += angleStep) {
            const x1 = centerX + radius * Math.cos(angle);
            const y1 = centerY + radius * Math.sin(angle);
            const x2 = centerX + (radius + 30) * Math.cos(angle);
            const y2 = centerY + (radius + 30) * Math.sin(angle);
            
            // Interaction arrows
            ctx.strokeStyle = '#8e44ad';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
            
            // Simple arrowhead
            const headLength = 8;
            const headAngle = Math.PI / 6;
            ctx.beginPath();
            ctx.moveTo(x2, y2);
            ctx.lineTo(x2 - headLength * Math.cos(angle - headAngle), y2 - headLength * Math.sin(angle - headAngle));
            ctx.moveTo(x2, y2);
            ctx.lineTo(x2 - headLength * Math.cos(angle + headAngle), y2 - headLength * Math.sin(angle + headAngle));
            ctx.stroke();
        }
        
        // Labels
        ctx.fillStyle = '#2c3e50';
        ctx.font = '18px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Fermi Surface with Interactions', centerX, 40);
        
        ctx.fillStyle = '#8e44ad';
        ctx.font = '14px Arial';
        ctx.fillText('Quasiparticle interactions', centerX, height - 20);
    }

    createTransportVisualization() {
        const result = this.getCanvasContext('transport-viz');
        if (!result) return;
        
        const { canvas, ctx } = result;
        const width = canvas.width;
        const height = canvas.height;
        const margin = { top: 20, right: 20, bottom: 60, left: 60 };
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        const { plotWidth, plotHeight } = this.drawAxes(ctx, width, height, margin, 'Temperature (T/TF)', 'Normalized Value', 1, 1);
        
        // T² resistivity
        ctx.strokeStyle = '#e74c3c';
        ctx.lineWidth = 3;
        ctx.beginPath();
        
        const steps = 100;
        for (let i = 0; i <= steps; i++) {
            const T = (i / steps) * 1;
            const rho = 0.1 + T * T; // ρ = ρ₀ + AT²
            
            const x = margin.left + T * plotWidth;
            const y = height - margin.bottom - rho * plotHeight;
            
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        ctx.stroke();
        
        // Linear specific heat
        ctx.strokeStyle = '#27ae60';
        ctx.lineWidth = 3;
        ctx.beginPath();
        
        for (let i = 0; i <= steps; i++) {
            const T = (i / steps) * 1;
            const cv = T; // CV ∝ T
            
            const x = margin.left + T * plotWidth;
            const y = height - margin.bottom - cv * plotHeight;
            
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        ctx.stroke();
        
        // Legend
        ctx.fillStyle = '#e74c3c';
        ctx.font = '16px Arial';
        ctx.textAlign = 'left';
        ctx.fillText('ρ ∝ T²', margin.left + plotWidth * 0.6, margin.top + 40);
        
        ctx.fillStyle = '#27ae60';
        ctx.fillText('CV ∝ T', margin.left + plotWidth * 0.6, margin.top + 60);
    }

    // Utility function for Fermi-Dirac distribution
    fermiDirac(energy, mu, temperature) {
        if (temperature === 0) {
            return energy <= mu ? 1 : 0;
        }
        return 1 / (Math.exp((energy - mu) / temperature) + 1);
    }
}

// Initialize the visualization when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const visualization = new FermiFluidsVisualization();
    
    // Add some interactivity feedback
    console.log('Fermi Fluids Tutorial loaded successfully!');
    
    // Smooth reveal animation for sections
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all sections
    document.querySelectorAll('.section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
});