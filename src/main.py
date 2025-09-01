import math
import matplotlib.pyplot as plt
import numpy as np
import random
from argparse import ArgumentParser, Namespace
from typing import List, Literal, Tuple, Union


ANALYTICAL_SOLUTION = 2 / 3


def sample_triangle_points(point_a: Tuple[float, float],
                           point_b: Tuple[float, float],
                           point_c: Tuple[float, float]) -> Tuple[float, float]:
    """
    Sample a single random point uniformly within the triangle
    defined by vertices `point_a`, `point_b`, and `point_c`.

    This uses the method of barycentric coordinates for uniform sampling.

    Args:
        point_a: The first vertex of the triangle (x, y).
        point_b: The second vertex of the triangle (x, y).
        point_c: The third vertex of the triangle (x, y).

    Returns:
        A tuple `(x, y)` representing a point uniformly sampled inside the triangle.
    """
    r1: float = random.random()
    r2: float = random.random()

    s1: float = math.sqrt(r1)

    x: float = point_a[0] * (1.0 - s1) + point_b[0] * (1.0 - r2) * s1 + point_c[0] * r2 * s1
    y: float = point_a[1] * (1.0 - s1) + point_b[1] * (1.0 - r2) * s1 + point_c[1] * r2 * s1

    return x, y


def sign(num: float | int) -> Literal[-1, 0, 1]:
    """
    Return the sign of a finite number.

    Args:
        num (Union[float, int]): The number to sign.

    Returns:
        The sign of the number.
    """
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0


def ccw(point_a: Tuple[float, float], point_b: Tuple[float, float], point_c: Tuple[float, float]) -> int:
    """
    Args:
        point_a (Tuple[float, float]): The first point.
        point_b (Tuple[float, float]): The second point.
        point_c (Tuple[float, float]): The third point.

    Returns:
        1 if A-B-C is a counterclockwise turn,
        -1 for clockwise,
        0 if the points are collinear (or not all distinct).
    """
    disc: Union[float, int] = (
        (point_a[0] - point_c[0]) *
        (point_b[1] - point_c[1]) - (point_a[1] - point_c[1]) *
        (point_b[0] - point_c[0])
    )
    return sign(disc)


def classify_points(point_a: Tuple[float, float],
                    point_b: Tuple[float, float],
                    point_c: Tuple[float, float],
                    point_d: Tuple[float, float]) -> int:
    """
    Returns:
        1 if a convex hull of A, B, C and D is a quadrilateral,
        -1 if a triangle,
        0 if any three of A, B, C and D are collinear (or if not all points are distinct).
    """
    return (
        ccw(point_a, point_b, point_c) *
        ccw(point_a, point_b, point_d) *
        ccw(point_a, point_c, point_d) *
        ccw(point_b, point_c, point_d)
    )


def simulate(args: Namespace) -> List[float]:
    """
    Start the simulation.

    Args:
        args (Namespace): Arguments parsed from the command line.

    Returns:
        The simulation results.
    """

    # Define the points of the triangle
    point_a: tuple[float, float] = (0, 0)
    point_b: tuple[float, float] = (0.5, math.sqrt(.75))
    point_c: tuple[float, float] = (1, 0)

    # Generate N points within the triangle
    results: List[float] = []
    points: List[Tuple[float, float]] = [
        sample_triangle_points(point_a, point_b, point_c) for _ in range(args.num)
    ]

    quad_cnt: int = 0
    total_cnt: int = 0

    for _ in range(1, args.num + 1):
        quad_points = random.sample(points, k=4)

        point_a: tuple[float, float] = quad_points[0]
        point_b: tuple[float, float] = quad_points[1]
        point_c: tuple[float, float] = quad_points[2]
        point_d: tuple[float, float] = quad_points[3]

        total_cnt += 1

        if classify_points(point_a, point_b, point_c, point_d) == 1:
            quad_cnt += 1

        results.append(quad_cnt / total_cnt)

    return results


def plot_results(args: Namespace, res: List[float]) -> None:
    XX = np.linspace(1, args.num, args.num)
    YY = res

    plt.figure(figsize=(8, 4))
    plt.scatter(XX, YY, s=0.3, color="blue", label="Monte-Carlo simulation")
    plt.hlines(ANALYTICAL_SOLUTION, 100, args.num, colors="red", label="Analytical solution")
    plt.ylim(0.6, 0.8)
    plt.xlabel("$N$")
    plt.ylabel("$P$")
    plt.legend()
    plt.show()


def main(args: Namespace) -> None:
    res = simulate(args)
    plot_results(args, res)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--num", "-n", default=10_000, type=int)
    args = parser.parse_args()

    main(args)
