"""A Bayesian optimization solver for color mixing."""

from typing import Optional, Union

import numpy as np

# https://python-colormath.readthedocs.io/en/latest/color_objects.html
from colormath.color_objects import sRGBColor
from skopt import Optimizer


class BayesColorSolver:
    """A Bayesian optimization solver for color mixing."""

    def __init__(self, pop_size: int, target_color: list[float]) -> None:
        """
        Initialize the Bayesian color solver.
        Args:
            pop_size (int): The size of the population to generate.
            target_color (list[float]): The target color to match, in RGB format.
        """
        self.optimizer = Optimizer(
            dimensions=[(0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0)],
            n_initial_points=4,
            initial_point_generator="random",
        )
        self.pop_size = pop_size
        self.target_color = target_color

    def _augment(
        self,
        prev_pop: list[list[float]],
        prev_grades: list[float],
    ) -> list[list[float]]:
        self.optimizer.tell(prev_pop, prev_grades)
        new_pop = self.optimizer.ask(self.pop_size)
        return [(x / np.sum(x)).round(3).tolist() for x in new_pop]

    def run_iteration(
        self,
        previous_ratios: Optional[list[list[float]]] = None,
        prev_colors: Optional[list[list[float]]] = None,
    ) -> list[list[float]]:
        """
        Run one iteration of the Bayesian optimization algorithm.

        If previous_ratios is None, generate random ratios.
        If previous_ratios is provided, use it to augment the population.
        If prev_colors is None, use the target color as the previous colors.
        If prev_colors is provided, grade the population based on the target color.

        Returns a list of ratios for the next population.
        """
        if previous_ratios is None:
            ratios = []
            for _ in range(self.pop_size):
                random_ratios = np.random.rand(1, 4).tolist()[0]
                random_sum = sum(random_ratios)
                random_ratios = [x / random_sum for x in random_ratios]
                random_ratios = np.round(random_ratios, 3)
                ratios.append(random_ratios.tolist())
            return ratios
        prev_diffs = self._grade_population(prev_colors, self.target_color)

        # Augment
        return self._augment(previous_ratios, prev_diffs)

    @staticmethod
    def _grade_population(
        pop_colors: list[Union[sRGBColor, list[float]]],
        target: Union[sRGBColor, list[float]],
    ) -> list[float]:
        if not isinstance(target, sRGBColor):
            target = sRGBColor(*target, is_upscaled=bool(max(target) > 1))
        if not all(isinstance(exp_color, sRGBColor) for exp_color in pop_colors):
            pop_colors = [
                sRGBColor(
                    *exp_color,
                    is_upscaled=bool(max(exp_color) > 1),
                )
                for exp_color in pop_colors
            ]

        diffs = []
        for color in pop_colors:
            diff = BayesColorSolver._color_diff(target, color)
            diffs.append(diff)

        return diffs

    @staticmethod
    def _color_diff(color1: sRGBColor, color2: sRGBColor) -> float:
        # Simple Euclidean distance in RGB space
        arr1 = np.array([color1.rgb_r, color1.rgb_g, color1.rgb_b])
        arr2 = np.array([color2.rgb_r, color2.rgb_g, color2.rgb_b])
        return float(np.linalg.norm(arr1 - arr2))
