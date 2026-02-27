"""The main colorpicker experiment application."""

import datetime
from pathlib import Path
from random import randint
from string import ascii_uppercase
from typing import Optional, Union

import numpy as np
from madsci.common.types.base_types import PathLike
from madsci.common.types.experiment_types import ExperimentDesign
from madsci.common.types.step_types import StepDefinition
from madsci.common.types.workflow_types import WorkflowDefinition
from madsci.experiment_application import ExperimentApplication
from madsci.experiment_application.experiment_application import (
    ExperimentApplicationConfig,
)
from threading import Thread
from pydantic import Field
from rich.console import Console

from colorpicker_experiment.bayes_solver import BayesColorSolver
from colorpicker_experiment.utils import get_colors_from_file
from madsci.client import WorkcellClient, DataClient
console = Console()


class ColorPickerConfig(ExperimentApplicationConfig):
    """Configuration for the color picker experiment application."""

    workflow_directory: PathLike = (Path(__file__).parent / "workflows").resolve()
    """The directory where the workflows are stored."""
    protocol_directory: PathLike = (Path(__file__).parent / "protocols").resolve()
    """The directory where the protocols are stored."""
    image_directory: PathLike = Path("./images").resolve()
    """The directory where the images are stored."""
    experiment_design: Union[ExperimentDesign, PathLike] = Path(
        "./experiment_design.yaml"
    ).resolve()
    """The path to the experiment design file."""
    pop_size: int = 4
    """The population size for the experiment (i.e. number of colors to mix per iteration)."""
    well_volume: Union[int, float] = Field(gt=0, default=275)
    """The volume to fill each well in microliters."""
    iterations: int = Field(default=4, gt=0)
    """The number of iterations to run the experiment for."""


class ColorPickerExperimentApplication(ExperimentApplication):
    """A demonstration and benchmarking experimental application: mixing colors autonomously."""

    config = ColorPickerConfig()
    """The configuration for the color picker experiment application."""

    previous_ratios = None
    previous_colors = None

    

    def __init__(
        self, opentron: str, pipette_side: str, config: Optional[ColorPickerConfig] = None
    ) -> "ColorPickerExperimentApplication":
        """Initialize the color picker experiment application."""
        if config:
            self.config = config
        self.experiment_design = self.config.experiment_design
        super().__init__()
        self.target_color = [randint(0, 255), randint(0, 255), randint(0, 255)]  # noqa: S311
        self.solver = BayesColorSolver(self.config.pop_size, self.target_color)
        self.pipette_side = "left"
        self.total_wells = []
        self.wells = []
        self.opentron = opentron
        self.pipette_side = pipette_side
        self.workcell_client = WorkcellClient("http://parker.cels.anl.gov:8005")
        self.data_client = DataClient("http://parker.cels.anl.gov:8003")
        for i in range(9):
            for j in range(1, 13):
                self.wells.append(ascii_uppercase[i] + str(j))
        self.mix_colors_workflow = WorkflowDefinition.from_yaml(
            self.config.workflow_directory / "mix_colors.workflow.yaml"
        )
        self.rinse_plate_workflow = WorkflowDefinition.from_yaml(
            self.config.workflow_directory / "rinse_plate.workflow.yaml"
        )

    def loop(self, opentron: str, iteration: int, inputs: Optional[list[list[float]]] = None) -> None:
        """Run one iteration of the main experiment loop."""
        self.logger.info(f"Running iteration {iteration}")
        # * Get the input volumes for the ot2 to mix in the plate from the bayesian solver, if not provided
        if inputs is None:
            inputs = self.solver.run_iteration(
                self.previous_ratios, self.previous_colors
            )
            inputs = (np.array(inputs) * self.config.well_volume).round(3).tolist()

        # Track which wells in the plate to create samples in
        start = iteration * self.config.pop_size
        end = (iteration + 1) * self.config.pop_size
        current_wells = self.wells[start:end]

        opentron_location = f"{opentron}.deck_2"
        # Run the color mixing workflow
        workflow = self.workcell_client.start_workflow(
            workflow_definition=self.mix_colors_workflow,
            json_inputs={
                "opentron_name": opentron,
                "opentron_location": opentron_location,
                "mixing_protocol_parameters": {
                    "wells": current_wells,
                    "amounts": inputs,
                    "pipette_side": self.pipette_side,
                },
            },
            file_inputs={
                "protocol_path": str(self.config.protocol_directory / "mix_colors.py"),
            },
        )

        self.total_wells = self.total_wells + current_wells
        # Retrieve the data generated by the workflow and save it as "image.jpg"
        self.data_client.save_datapoint_value(
            workflow.get_datapoint_id(step_key="take_picture"),
            self.config.image_directory / "plate_image.jpg",
        )

        # Calculate all the colors on the plate and save the neccessary ones to submit to the solver
        colors = get_colors_from_file(self.config.image_directory / "plate_image.jpg")
        reference_colors = []
        for well in current_wells:
            reference_colors.append(colors[well])
        self.previous_colors = reference_colors
        return reference_colors

    def run_experiment(self) -> None:
        """Run the color picker experiment."""
        for iteration in range(self.config.iterations):
            self.loop(self.opentron, iteration)
        console.print(
            f"[bold green]Target Color:[/bold green] {self.target_color} | [bold blue]Final Mixed Color:[/bold blue] {self.previous_colors[np.argmin(self.previous_ratios)]}"
        )


if __name__ == "__main__":
    app1 = ColorPickerExperimentApplication(opentron="ot2_gamma", pipette_side='"left"')
    app2 = ColorPickerExperimentApplication(opentron="ot2_beta", pipette_side='"right"')
    thread1 = Thread(target=app1.run_experiment)
    thread2 = Thread(target=app2.run_experiment)
    thread1.start()
    thread2.start()