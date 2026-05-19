"""
Laboratory Work No. 4 - Task 4
Title: Geometric Figures - Triangle Inscribed in a Circle
Version: 1.0
Developer: Maleeva Kira 453501
Date: 2026-05-06
"""

from triangle_circle import InscribedTriangle
from color import FigureColor
from visualizer import FigureVisualizer
import math

def validate_positive_float(value: str) -> float:
    """Validate positive float input"""
    try:
        num = float(value)
        if num <= 0:
            raise ValueError("Value must be positive")
        return num
    except ValueError as e:
        raise ValueError(f"Invalid input: {e}")

def get_user_input():
    """Get user input for triangle parameters"""
    # Get radius
    while True:
        try:
            radius_str = input("Enter circle radius (positive number): ")
            radius = validate_positive_float(radius_str)
            break
        except ValueError as e:
            print(f"Error: {e}")
    
    # Get color (any string is accepted)
    color = input("Enter color: ").strip()
    if not color:
        color = "blue"
    
    return radius, color

def demonstrate_polymorphism():
    """Demonstrate polymorphism with different figures"""   
    triangles = [
        InscribedTriangle(0.5, 'red'),
        InscribedTriangle(1.0, 'blue'),
        InscribedTriangle(1.5, 'green')
    ]
    
    print("\nDifferent triangles (polymorphism in action):")
    for i, triangle in enumerate(triangles, 1):
        print(f"\nTriangle {i}:")
        print(f"  {triangle}")
        print(f"  Area: {triangle.calculate_area():.2f}")
        print(f"  Perimeter: {triangle.calculate_perimeter():.2f}")

def demonstrate_super_and_static():
    """Demonstrate super() and static attributes"""   
    from shapes import GeometricFigure
    
    # Reset counter for clean demonstration (optional)
    GeometricFigure.figure_count = 0
    
    print(f"Total figures created: {GeometricFigure.get_figure_count()}")
    
    t1 = InscribedTriangle(0.8, 'purple')
    t2 = InscribedTriangle(1.2, 'orange')
    
    print(f"After creating 2 more: {GeometricFigure.get_figure_count()}")
    print(f"\nTriangle figure type: {InscribedTriangle.figure_type}")
    print(f"Triangle class representation: {t1}")

def demonstrate_magic_methods():
    """Demonstrate magic/dunder methods"""  
    t1 = InscribedTriangle(1.0, 'red')
    t2 = InscribedTriangle(1.5, 'blue')
    
    print(f"__str__: {t1}")
    print(f"__repr__: {repr(t2)}")
    
    color_obj = FigureColor('red')
    print(f"\nColor getter: {color_obj.color}")

def draw_triangle_visualization(radius: float, color: str):
    """Draw triangle with circumscribed circle"""
    triangle = InscribedTriangle(radius, color)
    
    print(triangle.get_info())
    
    visualizer = FigureVisualizer()
    visualizer.setup_canvas(title=f"Triangle inscribed in circle (R={radius})")
    
    visualizer.draw_circle(triangle.get_center(), radius, color='gray')
    
    vertices = triangle.get_vertices_for_drawing()
    visualizer.draw_triangle(vertices, color=color, alpha=0.6)
    
    margin = radius * 1.2
    visualizer.ax.set_xlim(-margin, margin)
    visualizer.ax.set_ylim(-margin, margin)
    
    visualizer.add_text_label(f"R = {radius}", (0, radius + 0.1), fontsize=10)
    visualizer.add_text_label(f"Area = {triangle.calculate_area():.2f}", 
                             (0, -radius - 0.15), fontsize=9)
    
    explanation = (
        f"Equilateral triangle\n"
        f"Side = {triangle._side_length:.2f}\n"
        f"Color: {color}"
    )
    visualizer.ax.text(-margin + 0.1, margin - 0.3, explanation, 
                       fontsize=8, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    filename = f"triangle_R{radius}_{color}.png"
    visualizer.save_figure(filename)
    visualizer.show_figure()
    visualizer.close()

def interactive_mode():
    """Interactive mode for creating triangles"""   
    while True:
        print("\nOptions:")
        print("1. Create and draw new triangle")
        print("2. Show demonstrations")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            radius, color = get_user_input()
            try:
                draw_triangle_visualization(radius, color)
            except Exception as e:
                print(f"Error drawing triangle: {e}")
        
        elif choice == '2':
            demonstrate_polymorphism()
            demonstrate_super_and_static()
            demonstrate_magic_methods()
        
        elif choice == '3':
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3")

def main():
    """Main function"""    
    demonstrate_polymorphism()
    demonstrate_super_and_static()
    demonstrate_magic_methods()
    
    interactive_mode()

if __name__ == "__main__":
    main()