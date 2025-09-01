#!/usr/bin/env python3
"""
DXF File Generator

A Python program to generate DXF files with various geometric shapes.
Uses the ezdxf library for DXF file creation.

Copyright 2025

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import ezdxf
from ezdxf import colors
from typing import List, Tuple, Optional
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon, Arc
import numpy as np


class DXFGenerator:
    def __init__(self):
        self.doc = ezdxf.new('R2010')
        self.msp = self.doc.modelspace()
        self.drawing_elements = []
        
    def add_line(self, start: Tuple[float, float], end: Tuple[float, float], color: int = colors.WHITE):
        """Add a line to the DXF document."""
        line = self.msp.add_line(start, end)
        line.dxf.color = color
        self.drawing_elements.append({'type': 'line', 'start': start, 'end': end, 'color': color})
        return line
    
    def add_circle(self, center: Tuple[float, float], radius: float, color: int = colors.WHITE):
        """Add a circle to the DXF document."""
        circle = self.msp.add_circle(center, radius)
        circle.dxf.color = color
        self.drawing_elements.append({'type': 'circle', 'center': center, 'radius': radius, 'color': color})
        return circle
    
    def add_rectangle(self, corner1: Tuple[float, float], corner2: Tuple[float, float], color: int = colors.WHITE):
        """Add a rectangle to the DXF document."""
        x1, y1 = corner1
        x2, y2 = corner2
        
        points = [
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2),
            (x1, y1)  # Close the rectangle
        ]
        
        lwpolyline = self.msp.add_lwpolyline(points)
        lwpolyline.dxf.color = color
        self.drawing_elements.append({'type': 'rectangle', 'corner1': corner1, 'corner2': corner2, 'color': color})
        return lwpolyline
    
    def add_polygon(self, points: List[Tuple[float, float]], closed: bool = True, color: int = colors.WHITE):
        """Add a polygon to the DXF document."""
        original_points = points.copy()
        if closed and points[0] != points[-1]:
            points = points + [points[0]]
        
        lwpolyline = self.msp.add_lwpolyline(points)
        lwpolyline.dxf.color = color
        self.drawing_elements.append({'type': 'polygon', 'points': original_points, 'closed': closed, 'color': color})
        return lwpolyline
    
    def add_arc(self, center: Tuple[float, float], radius: float, start_angle: float, 
                end_angle: float, color: int = colors.WHITE):
        """Add an arc to the DXF document. Angles in degrees."""
        arc = self.msp.add_arc(center, radius, start_angle, end_angle)
        arc.dxf.color = color
        self.drawing_elements.append({'type': 'arc', 'center': center, 'radius': radius, 
                                    'start_angle': start_angle, 'end_angle': end_angle, 'color': color})
        return arc
    
    def add_text(self, text: str, position: Tuple[float, float], height: float = 1.0, 
                 color: int = colors.WHITE):
        """Add text to the DXF document."""
        text_entity = self.msp.add_text(text, dxfattribs={
            'height': height,
            'insert': position,
            'color': color
        })
        self.drawing_elements.append({'type': 'text', 'text': text, 'position': position, 
                                    'height': height, 'color': color})
        return text_entity
    
    def add_spline(self, control_points: List[Tuple[float, float]], color: int = colors.WHITE):
        """Add a spline curve to the DXF document."""
        spline = self.msp.add_spline(control_points)
        spline.dxf.color = color
        self.drawing_elements.append({'type': 'spline', 'control_points': control_points, 'color': color})
        return spline
    
    def create_grid(self, width: float, height: float, spacing: float, 
                    origin: Tuple[float, float] = (0, 0), color: int = colors.GRAY,
                    show_coordinates: bool = True, text_height: float = 0.8):
        """Create a grid pattern with optional coordinate labels at intersections."""
        x_origin, y_origin = origin
        
        # Vertical lines
        x = x_origin
        while x <= x_origin + width:
            self.add_line((x, y_origin), (x, y_origin + height), color)
            x += spacing
            
        # Horizontal lines
        y = y_origin
        while y <= y_origin + height:
            self.add_line((x_origin, y), (x_origin + width, y), color)
            y += spacing
            
        # Add coordinate labels at intersections (only within grid boundaries)
        if show_coordinates:
            x = x_origin
            while x <= x_origin + width:
                y = y_origin
                while y <= y_origin + height:
                    # Offset text slightly to avoid overlapping with grid lines
                    text_x = x + spacing * 0.05
                    text_y = y + spacing * 0.05
                    
                    # Only add text if it falls within the grid boundaries
                    if (text_x <= x_origin + width and text_y <= y_origin + height):
                        # Format coordinates to remove unnecessary decimals
                        x_str = f"{x:g}"
                        y_str = f"{y:g}"
                        coord_text = f"({x_str},{y_str})"
                        
                        self.add_text(coord_text, (text_x, text_y), 
                                    height=text_height, color=colors.RED)
                    y += spacing
                x += spacing
    
    def create_star(self, center: Tuple[float, float], outer_radius: float, 
                    inner_radius: float, points: int = 5, color: int = colors.WHITE):
        """Create a star shape."""
        cx, cy = center
        angle_step = 2 * math.pi / (points * 2)
        star_points = []
        
        for i in range(points * 2):
            angle = i * angle_step - math.pi / 2  # Start from top
            if i % 2 == 0:  # Outer point
                radius = outer_radius
            else:  # Inner point
                radius = inner_radius
            
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            star_points.append((x, y))
        
        return self.add_polygon(star_points, closed=True, color=color)
    
    def _color_to_matplotlib(self, dxf_color: int) -> str:
        """Convert DXF color to matplotlib color."""
        color_map = {
            colors.WHITE: 'black',  # White elements show as black on white background
            colors.RED: 'red',
            colors.YELLOW: 'orange',  # Better contrast on white background
            colors.GREEN: 'green',
            colors.CYAN: 'cyan',
            colors.BLUE: 'blue',
            colors.MAGENTA: 'magenta',
            colors.BLACK: 'black',
            colors.GRAY: 'black'  # Gray elements show as black for grid lines
        }
        return color_map.get(dxf_color, 'black')
    
    def save_png(self, filename: str, width: int = 12, height: int = 8, dpi: int = 300):
        """Save the drawing as a PNG file."""
        if not filename.endswith('.png'):
            filename += '.png'
        
        fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
        ax.set_aspect('equal')
        
        for element in self.drawing_elements:
            color = self._color_to_matplotlib(element['color'])
            
            if element['type'] == 'line':
                start, end = element['start'], element['end']
                ax.plot([start[0], end[0]], [start[1], end[1]], color=color, linewidth=1)
                
            elif element['type'] == 'circle':
                center, radius = element['center'], element['radius']
                circle = plt.Circle(center, radius, fill=False, color=color, linewidth=1)
                ax.add_patch(circle)
                
            elif element['type'] == 'rectangle':
                corner1, corner2 = element['corner1'], element['corner2']
                x1, y1 = corner1
                x2, y2 = corner2
                width = abs(x2 - x1)
                height = abs(y2 - y1)
                rect = patches.Rectangle((min(x1, x2), min(y1, y2)), width, height, 
                                       fill=False, color=color, linewidth=1)
                ax.add_patch(rect)
                
            elif element['type'] == 'polygon':
                points = element['points']
                if element['closed'] and points[0] != points[-1]:
                    points = points + [points[0]]
                polygon = Polygon(points, fill=False, edgecolor=color, linewidth=1)
                ax.add_patch(polygon)
                
            elif element['type'] == 'arc':
                center = element['center']
                radius = element['radius']
                start_angle = element['start_angle']
                end_angle = element['end_angle']
                arc = patches.Arc(center, 2*radius, 2*radius, angle=0, 
                                theta1=start_angle, theta2=end_angle, color=color, linewidth=1)
                ax.add_patch(arc)
                
            elif element['type'] == 'text':
                position = element['position']
                text = element['text']
                height = element['height']
                # Use smaller font size for coordinate text, normal for other text
                if text.startswith('(') and ',' in text and text.endswith(')'):
                    fontsize = height * 2.4  # Triple the coordinate font size
                else:
                    fontsize = height * 4    # Reasonable size for titles and labels
                ax.text(position[0], position[1], text, fontsize=fontsize, color=color)
                
            elif element['type'] == 'spline':
                points = element['control_points']
                if len(points) > 1:
                    x_coords = [p[0] for p in points]
                    y_coords = [p[1] for p in points]
                    ax.plot(x_coords, y_coords, color=color, linewidth=1)
        
        ax.set_facecolor('white')
        ax.grid(True, alpha=0.3, color='lightgray')
        ax.autoscale()
        plt.tight_layout()
        plt.savefig(filename, facecolor='white', edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"PNG file saved as: {filename}")
    
    def save(self, filename: str, save_png: bool = False, png_width: int = 12, png_height: int = 8, png_dpi: int = 300):
        """Save the DXF document to a file and optionally save as PNG."""
        if not filename.endswith('.dxf'):
            filename += '.dxf'
        self.doc.saveas(filename)
        print(f"DXF file saved as: {filename}")
        
        if save_png:
            png_filename = filename.replace('.dxf', '.png')
            self.save_png(png_filename, png_width, png_height, png_dpi)


def create_sample_drawing():
    """Create a sample DXF file with various shapes."""
    generator = DXFGenerator()
    
    # Add title
    generator.add_text("Sample DXF Drawing", (10, 90), height=3, color=colors.RED)
    
    # Add some basic shapes
    generator.add_rectangle((10, 10), (30, 20), color=colors.BLUE)
    generator.add_circle((50, 15), 8, color=colors.GREEN)
    generator.add_line((70, 10), (90, 20), color=colors.YELLOW)
    
    # Add a polygon (triangle)
    triangle_points = [(100, 10), (110, 25), (120, 10)]
    generator.add_polygon(triangle_points, color=colors.MAGENTA)
    
    # Add an arc
    generator.add_arc((140, 15), 10, 0, 180, color=colors.CYAN)
    
    # Add a star
    generator.create_star((50, 50), 15, 8, points=6, color=colors.RED)
    
    # Add a grid in the background
    generator.create_grid(200, 100, 5, origin=(0, 0), color=colors.GRAY)
    
    # Add some text labels
    generator.add_text("Rectangle", (10, 5), height=1.5)
    generator.add_text("Circle", (45, 5), height=1.5)
    generator.add_text("Line", (75, 5), height=1.5)
    generator.add_text("Triangle", (100, 5), height=1.5)
    generator.add_text("Arc", (135, 5), height=1.5)
    generator.add_text("Star", (40, 35), height=1.5)
    
    return generator


if __name__ == "__main__":
    # Create and save a sample drawing with PNG
    sample = create_sample_drawing()
    sample.save("sample_drawing.dxf", save_png=True)
    
    # Example of creating a custom drawing with PNG
    custom = DXFGenerator()
    
    # Create a simple house
    # Base
    custom.add_rectangle((0, 0), (20, 15), color=colors.BLUE)
    
    # Roof (triangle)
    roof_points = [(0, 15), (10, 25), (20, 15)]
    custom.add_polygon(roof_points, color=colors.RED)
    
    # Door
    custom.add_rectangle((8, 0), (12, 8), color=colors.YELLOW)
    
    # Windows
    custom.add_rectangle((2, 8), (6, 12), color=colors.CYAN)
    custom.add_rectangle((14, 8), (18, 12), color=colors.CYAN)
    
    # Door handle
    custom.add_circle((11, 4), 0.3, color=colors.BLACK)
    
    # Add title
    custom.add_text("Simple House", (2, 30), height=2, color=colors.BLACK)
    
    custom.save("house.dxf", save_png=True)
    
    # Create spoil board grid with PNG
    spoil_board = DXFGenerator()
    spoil_board.add_text("Spoil Board - 300x800 Grid (50mm spacing)", (10, 820), height=4, color=colors.BLACK)
    spoil_board.create_grid(300, 800, 50, origin=(0, 0), color=colors.GRAY, show_coordinates=True, text_height=2.5)
    spoil_board.save("spoil_board.dxf", save_png=True, png_width=16, png_height=12)
    
    print("DXF and PNG generation complete!")
    print("Files created:")
    print("- sample_drawing.dxf + sample_drawing.png (various shapes demo)")
    print("- house.dxf + house.png (simple house example)")
    print("- spoil_board.dxf + spoil_board.png (300x800 grid with 50mm spacing and coordinates)")