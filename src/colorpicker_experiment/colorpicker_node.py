"""ExperimentNode harness for the Color Picker experiment.

Provides ColorPickerNode for REST server mode, exposing run_experiment()
as a POST /actions/run_experiment endpoint callable by the workcell manager.

CLI usage:
    colorpicker-node
"""

from typing import Any

from madsci.experiment_application import ExperimentNode
from madsci.experiment_application.experiment_node import ExperimentNodeConfig

from colorpicker_experiment.colorpicker_core import (
    COLORPICKER_DESIGN,
    ColorPickerConfigMixin,
    ColorPickerMixin,
)


class ColorPickerNodeConfig(ColorPickerConfigMixin, ExperimentNodeConfig):
    """ColorPicker config with node-specific fields (server host/port, etc.)."""


class ColorPickerNode(ColorPickerMixin, ExperimentNode):
    """REST node harness for the Color Picker experiment.

    Combines ColorPickerMixin (core logic) with ExperimentNode (REST server).
    Exposes run_experiment() as POST /actions/run_experiment, allowing the
    workcell manager to trigger experiments remotely.
    """

    config_model = ColorPickerNodeConfig
    experiment_design = COLORPICKER_DESIGN

    def run_experiment(  # type: ignore[override]
        self,
        opentron: str,
        pipette_side: str,
        iterations: int = 4,
    ) -> dict[str, Any]:
        """Run a full experiment. Exposed as POST /actions/run_experiment.

        Args:
            opentron: OT-2 node name to use for this run (e.g., "ot2_gamma").
            pipette_side: Pipette side to use ("left" or "right").
            iterations: Number of optimization rounds. Defaults to 4.

        Returns:
            Experiment results dict with target_color, best_color, and iterations.
        """
        return super().run_experiment(
            opentron=opentron,
            pipette_side=pipette_side,
            iterations=iterations,
        )


def main() -> None:
    """Entry point for the colorpicker-node CLI command.

    Starts the Color Picker REST node server.
    """
    ColorPickerNode().start_server()


if __name__ == "__main__":
    main()
