"""Color Picker Application for Remote Execution using Globus Compute."""

from typing import Optional

from globus_compute_sdk import Executor
from globus_compute_sdk.serialize import CombinedCode, ComputeSerializer


def run_color_picker_experiment(init: bool = False, iteration: int = 0, inputs: Optional[list[list[float]]] = None) -> list[float]:
    """Run the color picker experiment using Globus Compute."""
    from datetime import datetime

    from madsci.common.types.experiment_types import ExperimentDesign

    from colorpicker_experiment.color_picker_app import (
        ColorPickerConfig,
        ColorPickerExperimentApplication,
    )

    experiment_app = ColorPickerExperimentApplication(
        config=ColorPickerConfig(
            experiment_design=ExperimentDesign(
                experiment_name="Color Picker Globus Compute",
                experiment_description="A demonstration and benchmarking experimental application: mixing colors autonomously. This run is initiated using Globus Compute.",
            )
        )
    )

    with experiment_app.manage_experiment(
        run_name=f"Color Picker Globus Run {datetime.now()}",
        run_description=f"Run for color picker experiment, started using Globus Compute at ~{datetime.now()}",
    ):
        try:
            if init:
                experiment_app.workcell_client.submit_workflow(
                    experiment_app.barty_fill_workflow, await_completion=False
                )
            experiment_app.loop(iteration, inputs)
        except Exception as e:
            experiment_app.workcell_client.submit_workflow(
                experiment_app.barty_cleanup_workflow, await_completion=False
            )
            raise e
        experiment_app.clean_up()



if __name__ == "__main__":
    with Executor(endpoint_id="0de58510-6af5-4731-a924-87bbaa1648fe") as executor:
        executor.serializer = ComputeSerializer(
            strategy_code=CombinedCode()
        )
        future = executor.submit(run_color_picker_experiment, init=True)
        result = future.result()
