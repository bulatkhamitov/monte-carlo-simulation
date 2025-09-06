import math
import matplotlib.pyplot as plt
import numpy as np
import random
from argparse import ArgumentParser, Namespace
from pydantic import BaseModel, Field
from typing import List, Literal

# TODO: Add logging
# TODO: Add output mode flag
# TODO: Remove `Project 1/` folder
# TODO: Add TOML integration
# TODO: Implement triangle plotting function
# TODO: Implement random seed option

ANALYTICAL_SOLUTION = 2 / 3

class Point2D(BaseModel):
    x: float = Field(..., description="x coordinate")
    y: float = Field(..., description="y coordinate")


def sample_triangle_points(point_a: Point2D, point_b: Point2D, point_c: Point2D) -> Point2D:
    """
    Sample a single random point uniformly within the triangle
    defined by vertices `point_a`, `point_b`, and `point_c`.

    This uses the method of barycentric coordinates for uniform sampling.

    Args:
        point_a: The first vertex of the triangle (x, y).
        point_b: The second vertex of the triangle (x, y).
        point_c: The third vertex of the triangle (x, y).

    Returns:
        Point2D: a point uniformly sampled inside the triangle.
    """
    r1: float = random.random()
    r2: float = random.random()

    s1: float = math.sqrt(r1)

    x: float = point_a.x * (1.0 - s1) + point_b.x * (1.0 - r2) * s1 + point_c.x * r2 * s1
    y: float = point_a.y * (1.0 - s1) + point_b.y * (1.0 - r2) * s1 + point_c.y * r2 * s1

    return Point2D(x=x, y=y)


def sign(num: float) -> Literal[-1, 0, 1]:
    """
    Return the sign of a finite number.

    Args:
        num (float): The number to sign.

    Returns:
        The sign of the number.
    """
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0


def orientation(point_a: Point2D, point_b: Point2D, point_c: Point2D) -> Literal[-1, 0, 1]:
    """
    Args:
        point_a (Point2D): The first point.
        point_b (Point2D): The second point.
        point_c (Point2D): The third point.

    Returns:
        1 if A-B-C is a counterclockwise turn,
       -1 for clockwise,
        0 if the points are collinear (or not all distinct).
    """
    disc: float = (
        (point_a.x - point_c.x) *
        (point_b.y - point_c.y) - (point_a.y - point_c.y) *
        (point_b.x - point_c.x)
    )
    return sign(disc)


def classify_points(point_a: Point2D, point_b: Point2D, point_c: Point2D, point_d: Point2D) -> int:
    """
    Returns:
        1 if a convex hull of A, B, C and D is a quadrilateral,
       -1 if a triangle,
        0 if any three of A, B, C and D are collinear (or if not all points are distinct).
    """
    return (
        orientation(point_a, point_b, point_c) *
        orientation(point_a, point_b, point_d) *
        orientation(point_a, point_c, point_d) *
        orientation(point_b, point_c, point_d)
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
    point_a = Point2D(x=0.0, y=0.0)
    point_b = Point2D(x=0.5, y=math.sqrt(0.75))
    point_c = Point2D(x=1.0, y=0.0)

    # Generate N points within the triangle
    results: List[float] = []
    points: List[Point2D] = [sample_triangle_points(point_a, point_b, point_c) for _ in range(args.num)]

    quad_cnt: int = 0
    total_cnt: int = 0

    while total_cnt < args.num:
        quad_points = random.sample(points, k=4)

        point_a: Point2D = quad_points[0]
        point_b: Point2D = quad_points[1]
        point_c: Point2D = quad_points[2]
        point_d: Point2D = quad_points[3]

        total_cnt += 1

        if classify_points(point_a, point_b, point_c, point_d) == 1:
            quad_cnt += 1

        probability: float = quad_cnt / total_cnt
        results.append(probability)

    return results


def plot_results(args: Namespace, res: List[float]) -> None:
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "axes.labelsize": 10,
        "font.size": 10,
        "legend.fontsize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "figure.dpi": 100,
    })

    xx = np.linspace(1, args.num + 1, args.num)
    yy = res

    plt.figure(figsize=(8, 4))
    plt.scatter(xx, yy, s=0.3, color="blue", label="Monte-Carlo simulation")
    plt.hlines(y=ANALYTICAL_SOLUTION, xmin=0, xmax=args.num, colors="red", label="Analytical solution")
    # plt.ylim(0.6, 0.7)
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
    # parser.add_argument("--output", "-o", default="./out/output.png")
    parser.add_argument("--verbose", "-v", action="store_true", required=False)
    parser.add_argument("--seed", "-s", action="store_true", required=False)
    cli_args = parser.parse_args()

    main(cli_args)
