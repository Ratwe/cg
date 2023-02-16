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

    # Расчет площадей треугольников
    a = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    b = ((x3 - x2) ** 2 + (y3 - y2) ** 2) ** 0.5
    c = ((x3 - x1) ** 2 + (y3 - y1) ** 2) ** 0.5
    p = (a + b + c) / 2  # полупериметр
    area = (p * (p - a) * (p - b) * (p - c)) ** 0.5

    # Определение, лежит ли точка внутри треугольника
    a1 = ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
    a2 = ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5
    a3 = ((x - x3) ** 2 + (y - y3) ** 2) ** 0.5
    sum_of_areas = (
        (p - a) * (p - b) * (p - c) - a * (p - a1) * (p - a3) - b * (p - a2) * (p - a1) - c * (p - a2) * (p - a3)
    ) ** 0.5

    return area == sum_of_areas


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
                    elif is_point_in_circle(point, triangle) is not None:
                        count_in_circle += 1
                diff = abs(count_in_triangle - count_in_circle)
                if diff < min_diff:
                    min_diff = diff
                    res = i, j, k
                    p_in = count_in_triangle
                    p_out = count_in_circle

    return min_diff, res, p_in, p_out
