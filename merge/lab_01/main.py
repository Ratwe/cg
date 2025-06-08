from typing import List
import math

from numpy import fabs


class Point:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num


# Функция, определяющая, находится ли точка внутри описанной окружности треугольника
def is_point_in_circle(point: Point, triangle: List[Point]):
    a = triangle[0]
    b = triangle[1]
    c = triangle[2]
    center = get_circle_center(a, b, c)
    if center is None:
        return None
    radius = get_circle_radius(a, b, c)

    if math.sqrt((point.x - center.x) ** 2 + (point.y - center.y) ** 2) <= radius:
        print(f"L = {math.sqrt((point.x - center.x) ** 2 + (point.y - center.y) ** 2)} <= {radius}")

    return math.sqrt((point.x - center.x) ** 2 + (point.y - center.y) ** 2) <= radius


# Функция, находящая центр описанной окружности треугольника
# Формула для нахождения координат центра описанной окружности треугольника через координаты вершин треугольника
def get_circle_center(a: Point, b: Point, c: Point):
    x1, y1 = a.x, a.y
    x2, y2 = b.x, b.y
    x3, y3 = c.x, c.y

    denominator = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if denominator == 0:
        return None
    x = ((x1 ** 2 + y1 ** 2) * (y2 - y3) + (x2 ** 2 + y2 ** 2) * (y3 - y1) + (x3 ** 2 + y3 ** 2) * (
                y1 - y2)) / denominator
    y = ((x1 ** 2 + y1 ** 2) * (x3 - x2) + (x2 ** 2 + y2 ** 2) * (x1 - x3) + (x3 ** 2 + y3 ** 2) * (
                x2 - x1)) / denominator
    return Point(x, y, None)


# Функция, находящая радиус описанной окружности треугольника
def get_circle_radius(a: Point, b: Point, c: Point):
    center = get_circle_center(a, b, c)
    return math.sqrt((center.x - a.x) ** 2 + (center.y - a.y) ** 2)


def distance(p1, p2):
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def is_point_in_triangle(point: Point, triangle: List[Point]):
    x1, y1 = triangle[0].x, triangle[0].y
    x2, y2 = triangle[1].x, triangle[1].y
    x3, y3 = triangle[2].x, triangle[2].y
    x, y = point.x, point.y

    # if (x, y) == (x1, y1) or (x, y) == (x2, y2) or (x, y) == (x3, y3):
    #     return True

    print(f"nums: {triangle[0].num}, {triangle[1].num}, {triangle[2].num}")
    print("x....y")
    print(x1, y1)
    print(x2, y2)
    print(x3, y3)

    # Расчет площадей треугольников
    a = fabs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2
    b = fabs(x * (y2 - y3) + x2 * (y3 - y) + x3 * (y - y2)) / 2
    c = fabs(x1 * (y - y3) + x * (y3 - y1) + x3 * (y1 - y)) / 2
    d = fabs(x1 * (y2 - y) + x2 * (y - y1) + x * (y1 - y2)) / 2

    print("S =", a, b + c + d)
    if abs(a - (b + c + d)) < 1e-6:
        print(f"Point {point.num} ({x}, {y}) -> IN")
    else:
        print(f"Point {point.num} ({x}, {y}) -> OUT")

    print("----------\n")

    # Сравнение площадей
    return abs(a - (b + c + d)) < 1e-6


# def is_point_in_triangle(point: Point, triangle: List[Point]):
#     x1, y1 = triangle[0].x, triangle[0].y
#     x2, y2 = triangle[1].x, triangle[1].y
#     x3, y3 = triangle[2].x, triangle[2].y
#     x, y = point.x, point.y
#
#     print(f"x = {x}, y = {y}, x3 = {x3}, y3 = {y3}")
#
#     # Расчет площадей треугольников
#     a = fabs((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
#     b = fabs((x3 - x2) ** 2 + (y3 - y2) ** 2) ** 0.5
#     c = fabs((x3 - x1) ** 2 + (y3 - y1) ** 2) ** 0.5
#     p = (a + b + c) / 2  # полупериметр
#     print(f"p * (p - aa) * (p - b) * (p - c) = {p} * ({p - a}) * ({p - b}) * ({p - c})")
#     area = (p * (p - a) * (p - b) * (p - c)) ** 0.5
#
#     # Определение, лежит ли точка внутри треугольника
#     ad = fabs((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
#     bd = fabs((x - x2) ** 2 + (y - y2) ** 2) ** 0.5
#     cd = fabs((x - x3) ** 2 + (y - y3) ** 2) ** 0.5
#     p = (ad + bd + cd) / 2  # полупериметр
#     dot_area = fabs(p * (p - ad) * (p - bd) * (p - cd))
#     print(f"p * (p - ad) * (p - bd) * (p - cd) = {p} * ({p - ad}) * ({p - bd}) * ({p - cd})")
#
#     print("area, dot_area", area, dot_area)
#     print(f"a = {a}, b = {b}, c = {c}")
#     print(f"ad = {ad}, bd = {bd}, cd = {cd}")
#     print("res =", area - dot_area)
#
#     return abs(area - dot_area) < 1e-6


def get_min_difference(points: List[Point]):
    n = len(points)
    min_diff = float("inf")
    res = None
    p_in = 0
    p_out = 0

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                triangle = [points[i], points[j], points[k]]
                count_in_triangle = 0
                count_in_circle = 0
                for point in points:
                    if is_point_in_triangle(point, triangle):
                        count_in_triangle += 1
                    elif is_point_in_circle(point, triangle) is True:
                        count_in_circle += 1
                        print(f"point {point.num} in circle")
                diff = abs(count_in_triangle - count_in_circle)
                if diff < min_diff:
                    min_diff = diff
                    res = i, j, k
                    p_in = count_in_triangle
                    p_out = count_in_circle

    return min_diff, res, p_in, p_out
