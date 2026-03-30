import sys
import os

sys.path.append('/app/geometric_lib')

try:
    from circle import area as circle_area, perimeter as circle_perimeter
    from square import area as square_area, perimeter as square_perimeter
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    sys.exit(1)

def calculate_figure(figure, value):
    """Вычисляет площадь и периметр для одной фигуры"""
    figure = figure.lower()
    try:
        val = float(value)
    except ValueError:
        return f"Ошибка: '{value}' не является числом"
    
    if figure == "circle":
        return (f"Круг радиусом {val}\n"
                f"  Площадь: {circle_area(val)}\n"
                f"  Периметр: {circle_perimeter(val)}")
    elif figure == "square":
        return (f"Квадрат со стороной {val}\n"
                f"  Площадь: {square_area(val)}\n"
                f"  Периметр: {square_perimeter(val)}")
    else:
        return f"Неизвестная фигура: {figure}"

def main():
    if len(sys.argv) < 3:
        print("Использование: python script.py <фигура1> <значение1> [<фигура2> <значение2> ...]")
        print("Пример: python script.py circle 5 square 7 circle 3")
        sys.exit(1)
    
    # Проверяем, что аргументов четное количество (пары фигура-значение)
    if len(sys.argv) % 2 != 1:  # +1 потому что sys.argv[0] - имя скрипта
        print("Ошибка: аргументы должны быть парами 'фигура значение'")
        sys.exit(1)
    
    print("Результаты вычислений:")
    print("-" * 30)
    
    # Обрабатываем пары аргументов
    for i in range(1, len(sys.argv), 2):
        figure = sys.argv[i]
        value = sys.argv[i+1]
        result = calculate_figure(figure, value)
        print(result)
        print("-" * 30)

if __name__ == "__main__":
    main()