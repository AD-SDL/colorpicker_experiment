"""A Bayesian optimization solver for color mixing."""

from typing import List, Optional, Union

import numpy as np


# https://python-colormath.readthedocs.io/en/latest/color_objects.html
from colormath.color_objects import sRGBColor
from skopt import Optimizer


class BayesColorSolver:
    """A Bayesian optimization solver for color mixing."""

    def __init__(self, pop_size, target_color) -> None:
        self.optimizer = Optimizer(
            dimensions=[(0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0)],
            # base_estimator='GP',
            n_initial_points=4,
            initial_point_generator="random",
            # acq_func='EI',
            # acq_optimizer='sampling',
        )
        self.pop_size = pop_size
        self.target_color = target_color

    def _augment(
        self,
        prev_pop: List[sRGBColor],
        prev_grades: int,
    ) -> List[float]:
        self.optimizer.tell(prev_pop, prev_grades)
        new_pop = self.optimizer.ask(self.pop_size)
        new_pop = [(x / np.sum(x)).round(3).tolist() for x in new_pop]
        return new_pop

    def run_iteration(
        self,
        previous_ratios: Optional[List[List[float]]] = None,
        prev_colors: Optional[List[List[float]]] = None,
    ) -> List[List[float]]:
        if previous_ratios is None:
            ratios = []
            for j in range(0, self.pop_size):
                random_ratios = np.random.rand(1, 4).tolist()[0]
                random_sum = sum(random_ratios)
                random_ratios = [x / random_sum for x in random_ratios]
                random_ratios = np.round(random_ratios, 3)
                ratios.append(random_ratios.tolist())
            return ratios
        prev_diffs = self._grade_population(prev_colors, self.target_color)

        # Augment
        new_population = self._augment(previous_ratios, prev_diffs)

        # Convert to volumes
        return new_population

    @staticmethod
    def _grade_population(
        cls,
        pop_colors: List[Union[sRGBColor, List[float]]],
        target: Union[sRGBColor, List[float]],
    ):
        if not isinstance(target, sRGBColor):
            target = sRGBColor(*target, is_upscaled=True if max(target) > 1 else False)
        if not all([isinstance(exp_color, sRGBColor) for exp_color in pop_colors]):
            pop_colors = [
                sRGBColor(
                    *exp_color,
                    is_upscaled=True if max(exp_color) > 1 else False,
                )
                for exp_color in pop_colors
            ]

        diffs = []
        for color in pop_colors:
            diff = cls._color_diff(target, color)
            diffs.append(diff)

        return diffs
