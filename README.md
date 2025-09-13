# Fermi Fluids: An Interactive Introduction

A comprehensive, interactive tutorial on Fermi fluid theory with visual representations of quantum many-body physics concepts.

## Overview

This tutorial provides an in-depth introduction to Fermi fluid (Fermi liquid) theory, one of the cornerstone concepts in condensed matter physics. Through interactive visualizations and mathematical explanations, learners can explore:

- **Fermi sphere and Fermi surface concepts**
- **Quasiparticle picture and Landau parameters**
- **Interaction effects in quantum many-body systems**
- **Transport properties and experimental signatures**

## Features

### 🎯 Interactive Visualizations
- **Dynamic Fermi-Dirac distribution** with temperature controls
- **Quasiparticle dispersion** showing interaction effects
- **Fermi surface visualization** with interaction arrows
- **Transport property plots** demonstrating T² and linear dependencies

### 📚 Educational Content
- Clear explanations of fundamental concepts
- Mathematical formulations with MathJax rendering
- Progressive complexity from basic to advanced topics
- Real-world applications and experimental relevance

### 🎨 Modern Design
- Responsive layout for desktop and mobile devices
- Smooth animations and transitions
- Accessibility features for inclusive learning
- Clean, professional appearance

## Getting Started

### Prerequisites
- Modern web browser with JavaScript enabled
- Internet connection (for CDN resources)

### Running the Tutorial

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pchj/fermi-fluids-intro.git
   cd fermi-fluids-intro
   ```

2. **Open the tutorial:**
   ```bash
   # Simply open index.html in your browser
   open index.html  # macOS
   xdg-open index.html  # Linux
   start index.html  # Windows
   ```

   Or serve locally:
   ```bash
   # Using Python
   python -m http.server 8000
   # Then navigate to http://localhost:8000

   # Using Node.js
   npx serve .
   ```

3. **Navigate through sections:**
   - Use the navigation menu or scroll through sections
   - Interact with sliders to see real-time parameter changes
   - Explore the mathematical relationships visually

## Content Structure

### 1. Introduction
- What is a Fermi fluid?
- Historical context and importance
- Basic visualization of occupied vs. empty states

### 2. Fermi Sphere and Fermi Surface
- Momentum space representation
- Temperature effects on distribution
- Interactive temperature slider
- Mathematical formulation: E_F = ℏ²k_F²/(2m)

### 3. Quasiparticles and Landau Parameters
- Quasiparticle concept and renormalization
- Effective mass and interaction effects
- Landau interaction function
- Interactive parameter controls

### 4. Interaction Effects
- Landau parameters F_l^{s,a}
- Compressibility and susceptibility modifications
- Visual representation of interactions

### 5. Transport Properties
- Resistivity: ρ(T) = ρ₀ + AT²
- Specific heat: C_V ∝ γT
- Wilson ratio and other observables
- Breakdown of Fermi liquid behavior

## Technical Implementation

### Technologies Used
- **HTML5** for structure and semantic markup
- **CSS3** with modern features (Grid, Flexbox, CSS Variables)
- **JavaScript (ES6+)** for interactivity and calculations
- **D3.js v7** for data visualization and SVG manipulation
- **MathJax v3** for mathematical equation rendering

### Code Organization
- `index.html` - Main HTML structure and content
- `styles.css` - Responsive CSS styling and animations
- `script.js` - Interactive visualization logic and controls

### Browser Compatibility
- Chrome/Chromium 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Educational Applications

### For Students
- **Undergraduate physics:** Introduction to quantum many-body systems
- **Graduate courses:** Advanced condensed matter physics
- **Self-study:** Interactive learning at your own pace

### For Instructors
- **Lecture supplement:** Visual aids for complex concepts
- **Assignment tool:** Interactive exploration exercises
- **Research introduction:** Gateway to advanced topics

### For Researchers
- **Quick reference:** Visual reminder of key relationships
- **Presentation tool:** Clear illustrations for talks
- **Teaching resource:** Ready-to-use educational material

## Key Concepts Covered

### Theoretical Framework
- **Landau's Fermi liquid theory**
- **Quasiparticle picture**
- **Renormalization concepts**
- **Interaction vertex functions**

### Physical Observables
- **Electronic specific heat**
- **Magnetic susceptibility**
- **Electrical resistivity**
- **Optical conductivity**

### Mathematical Tools
- **Fermi-Dirac statistics**
- **Green's functions (basic introduction)**
- **Perturbation theory concepts**
- **Symmetry considerations**

## Contributing

We welcome contributions to improve this educational resource:

1. **Content improvements:** Better explanations, additional examples
2. **Code enhancements:** Performance optimizations, new features
3. **Bug fixes:** Cross-browser compatibility, mobile responsiveness
4. **Educational feedback:** User experience improvements

### Development Setup
```bash
# Clone and setup
git clone https://github.com/pchj/fermi-fluids-intro.git
cd fermi-fluids-intro

# Make changes to HTML, CSS, or JavaScript files
# Test in multiple browsers
# Submit pull request
```

## License

This educational content is provided under the MIT License. See LICENSE file for details.

## Acknowledgments

- **Lev Landau** for the foundational theory
- **David Pines** and **Philippe Nozières** for seminal textbooks
- **D3.js community** for excellent visualization tools
- **MathJax team** for mathematical rendering
- **Educational physics community** for feedback and suggestions

## Further Reading

### Essential Textbooks
- Pines & Nozières: "The Theory of Quantum Liquids"
- Ashcroft & Mermin: "Solid State Physics"
- Kittel: "Introduction to Solid State Physics"

### Advanced References
- Abrikosov, Gorkov & Dzyaloshinski: "Methods of Quantum Field Theory"
- Fetter & Walecka: "Quantum Theory of Many-Particle Systems"
- Coleman: "Introduction to Many-Body Physics"

### Online Resources
- arXiv condensed matter section
- Condensed Matter Physics community
- Quantum many-body theory courses

---

**Happy learning!** 🚀✨

For questions, suggestions, or collaboration opportunities, please open an issue or reach out to the maintainers.