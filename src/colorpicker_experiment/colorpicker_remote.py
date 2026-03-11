"""Color Picker Application for Remote Execution using Globus Compute."""

from typing import Any, Optional

from globus_compute_sdk import Executor
from globus_compute_sdk.serialize import CombinedCode, ComputeSerializer


def run_color_picker_experiment(
    opentron: str = "ot2_gamma",
    pipette_side: str = "left",
    iterations: int = 4,
    lab_server_url: Optional[str] = None,
) -> dict[str, Any]:
    """Run the color picker experiment via Globus Compute.

    Args:
        opentron: OT-2 node name to use for color mixing.
        pipette_side: Pipette side to use ("left" or "right").
        iterations: Number of optimization rounds to run.
        lab_server_url: URL of the MADSci lab server for service discovery.

    Returns:
        Experiment results dict with target_color, best_color, and iterations.
    """
    from colorpicker_experiment.colorpicker_script import (  # noqa: PLC0415
        ColorPickerScript,
    )

    app = ColorPickerScript(
        opentron=opentron,
        pipette_side=pipette_side,
        iterations=iterations,
        lab_server_url=lab_server_url,
    )
    return app.run()


if __name__ == "__main__":
    with Executor(endpoint_id="0de58510-6af5-4731-a924-87bbaa1648fe") as executor:
        executor.serializer = ComputeSerializer(strategy_code=CombinedCode())
        future = executor.submit(run_color_picker_experiment)
        result = future.result()
        print(result)  # noqa: T201
