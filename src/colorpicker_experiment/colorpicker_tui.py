"""ExperimentTUI harness for the Color Picker experiment.

Provides ColorPickerTUI for interactive terminal UI execution with
pause/cancel/resume controls via a Textual-based TUI.

CLI usage:
    colorpicker-tui [--mode single|dual] [--opentron NAME] [--pipette-side SIDE]

Note: Dual mode in TUI is not recommended because two separate TUI instances
cannot share a single terminal. Dual mode here runs experiments sequentially.
For true parallel dual-OT-2 operation, use colorpicker-script --mode dual.
"""

import argparse
import threading
from typing import Any

from madsci.experiment_application import ExperimentTUI
from madsci.experiment_application.experiment_tui import ExperimentTUIConfig

from colorpicker_experiment.colorpicker_core import (
    COLORPICKER_DESIGN,
    ColorPickerConfigMixin,
    ColorPickerMixin,
)


class ColorPickerTUIConfig(ColorPickerConfigMixin, ExperimentTUIConfig):
    """ColorPicker config with TUI-specific fields (refresh_interval, etc.)."""


class ColorPickerTUI(ColorPickerMixin, ExperimentTUI):
    """TUI-mode harness for the Color Picker experiment.

    Combines ColorPickerMixin (core logic) with ExperimentTUI (interactive
    terminal UI with pause/cancel/resume support).

    The check_experiment_status() method is overridden by ExperimentTUI to
    use thread-safe events, so pause/cancel requests from the TUI are
    respected between iterations.
    """

    config_model = ColorPickerTUIConfig
    experiment_design = COLORPICKER_DESIGN

    def run_experiment(  # type: ignore[override]
        self,
        opentron: str | None = None,
        pipette_side: str | None = None,
        iterations: int | None = None,
    ) -> dict[str, Any]:
        """Run the full experiment under TUI lifecycle management.

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


def main() -> None:
    """Entry point for the colorpicker-tui CLI command.

    Supports single-OT-2 and dual-OT-2 (sequential) modes.
    For parallel dual-OT-2, use colorpicker-script --mode dual instead.
    """
    parser = argparse.ArgumentParser(
        description="Run the Color Picker experiment with an interactive TUI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["single", "dual"],
        default="single",
        help=(
            "Run on a single OT-2 (recommended) or two OT-2s sequentially. "
            "For true parallel dual-OT-2, use colorpicker-script --mode dual."
        ),
    )
    parser.add_argument(
        "--opentron",
        default=None,
        help="OT-2 node name. Overrides config.",
    )
    parser.add_argument(
        "--pipette-side",
        default=None,
        dest="pipette_side",
        help="Pipette side. Overrides config.",
    )
    args = parser.parse_args()

    if args.mode == "dual":
        app1 = ColorPickerTUI(opentron="ot2_gamma", pipette_side="left")
        app2 = ColorPickerTUI(opentron="ot2_beta", pipette_side="right")
        t1 = threading.Thread(target=app1.run_tui)
        t2 = threading.Thread(target=app2.run_tui)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    else:
        kwargs: dict[str, Any] = {}
        if args.opentron:
            kwargs["opentron"] = args.opentron
        if args.pipette_side:
            kwargs["pipette_side"] = args.pipette_side
        ColorPickerTUI(**kwargs).run_tui()


if __name__ == "__main__":
    main()
