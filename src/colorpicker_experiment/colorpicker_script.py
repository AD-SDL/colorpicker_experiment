"""ExperimentScript harness for the Color Picker experiment.

Provides ColorPickerScript for run-once script execution, including
single-OT-2 and dual-OT-2 parallel modes via CLI.

All config fields (--opentron, --pipette-side, --iterations, etc.) are
automatically available as CLI arguments via pydantic-settings.

CLI usage:
    colorpicker-script [--mode single|dual] [--opentron NAME] [--pipette-side SIDE]
"""

import threading
from typing import Any, Literal

from madsci.experiment_application import ExperimentScript
from madsci.experiment_application.experiment_script import ExperimentScriptConfig
from pydantic import Field

from colorpicker_experiment.colorpicker_core import (
    COLORPICKER_DESIGN,
    ColorPickerConfigMixin,
    ColorPickerMixin,
)


class ColorPickerScriptConfig(ColorPickerConfigMixin, ExperimentScriptConfig):
    """ColorPicker config with script-specific fields."""

    mode: Literal["single", "dual"] = Field(
        default="single",
        description="Run on a single OT-2 or two OT-2s in parallel threads.",
    )


class ColorPickerScript(ColorPickerMixin, ExperimentScript):
    """Script-mode harness for the Color Picker experiment.

    Combines ColorPickerMixin (core logic) with ExperimentScript (run-once
    lifecycle management). The experiment_design and config_model class
    attributes wire up the MADSci experiment framework automatically.
    """

    config_model = ColorPickerScriptConfig
    experiment_design = COLORPICKER_DESIGN

    def run(self) -> dict[str, Any]:  # type: ignore[override]
        """Execute the experiment with automatic lifecycle management.

        Overrides ExperimentScript.run() to avoid requiring run_args/run_kwargs
        (not present in ColorPickerConfig). Experiment parameters come from
        self.config (opentron, pipette_side, iterations).

        Returns:
            Experiment results dict with target_color, best_color, and iterations.
        """
        with self.manage_experiment():
            return self.run_experiment()


def main() -> None:
    """Entry point for the colorpicker-script CLI command.

    Supports single-OT-2 and dual-OT-2 (parallel threads) modes.
    All config fields are parsed from CLI args, env vars, and config files
    automatically via pydantic-settings.
    """
    app = ColorPickerScript()
    if app.config.mode == "dual":
        app1 = ColorPickerScript(opentron="ot2_gamma", pipette_side="left")
        app2 = ColorPickerScript(opentron="ot2_beta", pipette_side="right")
        t1 = threading.Thread(target=app1.run)
        t2 = threading.Thread(target=app2.run)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    else:
        app.run()


if __name__ == "__main__":
    main()
