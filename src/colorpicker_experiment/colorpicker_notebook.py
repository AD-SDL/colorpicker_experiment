"""ExperimentNotebook harness for the Color Picker experiment.

Provides ColorPickerNotebook for cell-by-cell Jupyter notebook execution.

Typical notebook usage::

    # Cell 1: Setup
    from colorpicker_experiment import ColorPickerNotebook
    exp = ColorPickerNotebook(lab_server_url="http://...")
    exp.start()
    exp._initialize_run()   # sets target_color, solver, wells, etc.

    # Cell 2..N: run one iteration at a time
    colors = exp.loop(0)
    exp.display(colors, title="Iteration 0 results")

    # Final cell
    exp.end()
"""

from typing import Any, Optional

from madsci.experiment_application import ExperimentNotebook
from madsci.experiment_application.experiment_notebook import ExperimentNotebookConfig

from colorpicker_experiment.colorpicker_core import (
    COLORPICKER_DESIGN,
    ColorPickerConfigMixin,
    ColorPickerMixin,
)


class ColorPickerNotebookConfig(ColorPickerConfigMixin, ExperimentNotebookConfig):
    """ColorPicker config with notebook-specific fields (rich_output, etc.)."""


class ColorPickerNotebook(ColorPickerMixin, ExperimentNotebook):
    """Notebook-mode harness for the Color Picker experiment.

    Combines ColorPickerMixin (core logic) with ExperimentNotebook
    (cell-by-cell execution with Rich display helpers).

    Unlike the Script modality, this class exposes loop() and
    _initialize_run() for direct cell-by-cell control. The notebook
    pattern uses start()/end() rather than run_experiment().
    """

    config_model = ColorPickerNotebookConfig
    experiment_design = COLORPICKER_DESIGN

    def run_experiment(  # type: ignore[override]
        self,
        opentron: Optional[str] = None,
        pipette_side: Optional[str] = None,
        iterations: Optional[int] = None,
    ) -> dict[str, Any]:
        """Run the full experiment in a single notebook cell.

        For cell-by-cell control (recommended for notebooks), use
        start() → _initialize_run() → loop() → end() instead.

        Args:
            opentron: OT-2 node name override. Falls back to config.opentron.
            pipette_side: Pipette side override. Falls back to config.pipette_side.
            iterations: Number of rounds override. Falls back to config.iterations.

        Returns:
            Experiment results dict with target_color, best_color, and iterations.
        """
        return super().run_experiment(
            opentron=opentron,
            pipette_side=pipette_side,
            iterations=iterations,
        )
