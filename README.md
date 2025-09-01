# DXF Generator

A Python tool for generating DXF (Drawing Exchange Format) files with PNG output capability. Create technical drawings, grids, and geometric shapes programmatically.

## Features

- 🎯 **Dual Output**: Generate both DXF and PNG files from the same drawing
- 📐 **Geometric Shapes**: Lines, circles, rectangles, polygons, arcs, splines, and stars
- 📊 **Grid Generation**: Create coordinate grids with customizable spacing and labels
- 🎨 **Color Support**: Multiple colors with automatic PNG conversion
- 📝 **Text Support**: Add labels and annotations with custom sizing
- ⚙️ **Customizable**: Flexible parameters for all drawing elements

## Installation

### Requirements

- Python 3.6+
- Required packages:
  ```bash
  pip install ezdxf matplotlib numpy
  ```

### Quick Setup

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the generator:
   ```bash
   python dxf_generator.py
   ```

## Usage

### Basic Example

```python
from dxf_generator import DXFGenerator
from ezdxf import colors

# Create a new generator
generator = DXFGenerator()

# Add shapes
generator.add_rectangle((0, 0), (10, 5), color=colors.BLUE)
generator.add_circle((15, 2.5), 3, color=colors.RED)
generator.add_text("My Drawing", (0, 8), height=1.5)

# Save as DXF and PNG
generator.save("my_drawing.dxf", save_png=True)
```

### Grid Generation

```python
# Create a coordinate grid
generator = DXFGenerator()
generator.create_grid(
    width=300,           # Grid width
    height=200,          # Grid height  
    spacing=25,          # Grid spacing
    origin=(0, 0),       # Starting point
    show_coordinates=True, # Show coordinate labels
    text_height=1.0      # Coordinate text size
)
generator.save("grid.dxf", save_png=True)
```

## Available Methods

### Basic Shapes

| Method | Description | Parameters |
|--------|-------------|------------|
| `add_line()` | Draw a line | `start, end, color` |
| `add_circle()` | Draw a circle | `center, radius, color` |
| `add_rectangle()` | Draw a rectangle | `corner1, corner2, color` |
| `add_polygon()` | Draw a polygon | `points, closed, color` |
| `add_arc()` | Draw an arc | `center, radius, start_angle, end_angle, color` |
| `add_text()` | Add text | `text, position, height, color` |
| `add_spline()` | Draw a spline curve | `control_points, color` |

### Advanced Shapes

| Method | Description | Parameters |
|--------|-------------|------------|
| `create_star()` | Create a star shape | `center, outer_radius, inner_radius, points, color` |
| `create_grid()` | Create coordinate grid | `width, height, spacing, origin, color, show_coordinates, text_height` |

### Output

| Method | Description | Parameters |
|--------|-------------|------------|
| `save()` | Save DXF file | `filename, save_png, png_width, png_height, png_dpi` |
| `save_png()` | Save PNG file only | `filename, width, height, dpi` |

## Color Support

The generator supports standard DXF colors:

```python
from ezdxf import colors

# Available colors
colors.WHITE    # Shows as black in PNG (white background)
colors.RED      # Red
colors.YELLOW   # Orange in PNG (better contrast)
colors.GREEN    # Green
colors.CYAN     # Cyan
colors.BLUE     # Blue  
colors.MAGENTA  # Magenta
colors.BLACK    # Black
colors.GRAY     # Black in PNG (for grid lines)
```

## PNG Output Features

- **White background** with black grid lines and text
- **High resolution** output (300 DPI default)
- **Scalable fonts** with intelligent sizing for coordinates vs labels
- **Color preservation** with automatic contrast adjustment
- **Professional appearance** suitable for documentation

## Example Files

Run the script to generate example files:

```bash
python dxf_generator.py
```

This creates:

1. **sample_drawing.dxf/.png** - Various shapes demonstration
2. **house.dxf/.png** - Simple house example  
3. **spoil_board.dxf/.png** - 300×800mm grid with 50mm spacing

## Advanced Configuration

### Custom PNG Settings

```python
generator.save("drawing.dxf", 
    save_png=True,
    png_width=16,      # Figure width in inches
    png_height=12,     # Figure height in inches  
    png_dpi=300        # Resolution
)
```

### Grid with Custom Coordinates

```python
generator.create_grid(
    width=100,
    height=80, 
    spacing=10,
    origin=(50, 25),        # Start grid at (50,25)
    color=colors.GRAY,
    show_coordinates=True,
    text_height=0.8         # Smaller coordinate text
)
```

### Complex Shapes

```python
# Create a 6-pointed star
generator.create_star(
    center=(50, 50),
    outer_radius=20,
    inner_radius=10,
    points=6,
    color=colors.RED
)

# Create a custom polygon
triangle = [(0, 0), (10, 0), (5, 8.66)]
generator.add_polygon(triangle, closed=True, color=colors.BLUE)
```

## File Structure

```
dxfgen/
├── dxf_generator.py    # Main generator class
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── examples/          # Generated example files
    ├── sample_drawing.dxf
    ├── sample_drawing.png
    ├── house.dxf
    ├── house.png
    ├── spoil_board.dxf
    └── spoil_board.png
```

## Use Cases

- **CNC Programming**: Generate spoil board grids and work coordinates
- **Technical Documentation**: Create clean diagrams and schematics  
- **Architectural Drawing**: Basic floor plans and layouts
- **Engineering**: Mechanical parts and assemblies
- **Education**: Geometry and drafting exercises
- **Prototyping**: Quick concept visualization

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

### License Summary

- ✅ **Commercial use** - Use for commercial purposes
- ✅ **Modification** - Modify and distribute modified versions
- ✅ **Distribution** - Distribute original or modified versions
- ✅ **Patent use** - Use any patent claims in the project
- ✅ **Private use** - Use privately without restrictions

**Requirements:**
- Include license and copyright notice
- State changes made to the code
- Include original license in derivative works

---

**Generated with DXF Generator** - Create precise technical drawings with Python!

*NOTE: Much of this code was written with the help of Claude Code*