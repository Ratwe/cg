import random
from typing import List
import math

from numpy import fabs


class Point:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num


def is_point_in_circle(point: Point, triangle: List[Point]):
    a = triangle[0]
    b = triangle[1]
    c = triangle[2]
    center = get_circle_center(a, b, c)
    if center is None:
        return None
    radius = get_circle_radius(a, b, c)
    return math.sqrt((point.x - center.x) ** 2 + (point.y - center.y) ** 2) < radius


def get_circle_center(a: Point, b: Point, c: Point):
    d = 2 * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y))
    if d == 0:
        return None
    x = ((a.x ** 2 + a.y ** 2) * (b.y - c.y) + (b.x ** 2 + b.y ** 2) * (c.y - a.y) + (c.x ** 2 + c.y ** 2) * (
            a.y - b.y)) / d
    y = ((a.x ** 2 + a.y ** 2) * (c.x - b.x) + (b.x ** 2 + b.y ** 2) * (a.x - c.x) + (c.x ** 2 + c.y ** 2) * (
            b.x - a.x)) / d
    return Point(x, y, None)


def get_circle_radius(a: Point, b: Point, c: Point):
    center = get_circle_center(a, b, c)
    return math.sqrt((center.x - a.x) ** 2 + (center.y - a.y) ** 2)


def is_point_in_triangle(point: Point, triangle: List[Point]):
    x1, y1 = triangle[0].x, triangle[0].y
    x2, y2 = triangle[1].x, triangle[1].y
    x3, y3 = triangle[2].x, triangle[2].y
    x, y = point.x, point.y

    # Расчет площадей треугольников
    a = fabs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2
    b = fabs(x * (y2 - y3) + x2 * (y3 - y) + x3 * (y - y2)) / 2
    c = fabs(x1 * (y - y3) + x * (y3 - y1) + x3 * (y1 - y)) / 2
    d = fabs(x1 * (y2 - y) + x2 * (y - y1) + x * (y1 - y2)) / 2

    # Сравнение площадей
    return a == b + c + d


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


def generate_points(n):
    points = []
    pnum = 0
    for i in range(n):
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        points.append(Point(x, y, pnum))
    return points

