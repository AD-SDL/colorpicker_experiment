"""Core colorpicker experiment logic shared across all modalities.

Provides ColorPickerConfig, COLORPICKER_DESIGN, and ColorPickerMixin,
which are combined with a modality-specific base class (ExperimentScript,
ExperimentTUI, ExperimentNode, or ExperimentNotebook) to create the full
experiment harness.
"""

from pathlib import Path
from random import randint
from string import ascii_uppercase
from typing import TYPE_CHECKING, Any, Optional

import numpy as np
from madsci.common.types.base_types import PathLike
from madsci.common.types.experiment_types import ExperimentDesign
from madsci.common.types.workflow_types import StepDefinition, WorkflowDefinition
from madsci.experiment_application.experiment_base import ExperimentBaseConfig
from pydantic import Field

from colorpicker_experiment.bayes_solver import BayesColorSolver
from colorpicker_experiment.utils import get_colors_from_file

if TYPE_CHECKING:
    pass


class ColorPickerConfigMixin:
    """Mixin providing colorpicker-specific configuration fields.

    Combined with a modality-specific config base class
    (ExperimentScriptConfig, ExperimentNotebookConfig, etc.) to produce the
    final config for each harness.
    """

    opentron: str = Field(
        default="ot2_gamma",
        title="OT-2 Node Name",
        description="Name of the OT-2 node to use for color mixing.",
    )
    pipette_side: str = Field(
        default="left",
        title="Pipette Side",
        description="Side of the pipette to use (left or right).",
    )
    image_directory: PathLike = Field(
        default=Path("./images").resolve(),
        title="Image Directory",
        description="Directory where plate photos are saved.",
    )
    pop_size: int = Field(
        default=4,
        gt=0,
        title="Population Size",
        description="Number of colors to mix per iteration.",
    )
    well_volume: float = Field(
        default=275.0,
        gt=0,
        title="Well Volume",
        description="Volume in microliters to fill each well.",
    )
    iterations: int = Field(
        default=4,
        gt=0,
        title="Iterations",
        description="Number of optimization rounds to run.",
    )
    workflow_directory: PathLike = Field(
        default=(Path(__file__).parent / "workflows").resolve(),
        title="Workflow Directory",
        description="Directory containing workflow definition files.",
    )
    protocol_directory: PathLike = Field(
        default=(Path(__file__).parent / "protocols").resolve(),
        title="Protocol Directory",
        description="Directory containing OT-2 protocol files.",
    )
    reservoir_fill_level: float = Field(
        default=100.0,
        gt=0,
        title="Reservoir Fill Level",
        description="Target fill level for ink reservoirs before mixing.",
    )


class ColorPickerConfig(ColorPickerConfigMixin, ExperimentBaseConfig):
    """Generic colorpicker configuration (base modality)."""


COLORPICKER_DESIGN = ExperimentDesign(
    experiment_name="Color Picker",
    experiment_description="Autonomous color mixing via Bayesian optimization.",
)


class ColorPickerMixin:
    """Mixin providing core color picker experiment logic.

    Available to all harness classes (Script, TUI, Node, Notebook) via MRO.
    Requires the inheriting class to also inherit from ExperimentBase (or a
    subclass) to provide self.config, self.logger, self.workcell_client,
    self.data_client, and self.check_experiment_status().
    """

    config: ColorPickerConfig

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the mixin and set up colorpicker state."""
        super().__init__(*args, **kwargs)
        self._setup_colorpicker()

    def _setup_colorpicker(self) -> None:
        """Initialize non-run-specific state: wells list and workflow definitions."""
        self.wells: list[str] = [
            ascii_uppercase[i] + str(j) for i in range(9) for j in range(1, 13)
        ]
        self.mix_colors_workflow: WorkflowDefinition = WorkflowDefinition.from_yaml(
            self.config.workflow_directory / "mix_colors.workflow.yaml"
        )
        self.rinse_plate_workflow: WorkflowDefinition = WorkflowDefinition.from_yaml(
            self.config.workflow_directory / "rinse_plate.workflow.yaml"
        )

    def _initialize_run(
        self,
        opentron: Optional[str] = None,
        pipette_side: Optional[str] = None,
    ) -> None:
        """Initialize per-run state. Called at the start of each run_experiment()."""
        self.opentron: str = opentron or self.config.opentron
        self.pipette_side: str = pipette_side or self.config.pipette_side
        self.target_color: list[int] = [
            randint(0, 255),  # noqa: S311
            randint(0, 255),  # noqa: S311
            randint(0, 255),  # noqa: S311
        ]
        self.solver: BayesColorSolver = BayesColorSolver(
            self.config.pop_size, self.target_color
        )
        self.previous_ratios: Optional[list[list[float]]] = None
        self.previous_colors: Optional[list[list[float]]] = None
        self.total_wells: list[str] = []

    def _ensure_reservoirs_filled(self, target_level: float) -> None:
        """Fill target reservoirs to the desired level. Skips if not using ot2_gamma."""
        if self.opentron != "ot2_gamma":
            return
        workflow = WorkflowDefinition(
            name="Fill All Reservoirs to Target",
            steps=[
                StepDefinition(
                    name="Fill All Reservoirs to Target",
                    node="barty",
                    action="fill_all_to_target",
                    args={"target_level": target_level},
                )
            ],
        )
        self.workcell_client.start_workflow(workflow, await_completion=True)  # type: ignore[attr-defined]

    def _drain_all_reservoirs(self) -> None:
        """Drain all target reservoirs completely. Skips if not using ot2_gamma."""
        if self.opentron != "ot2_gamma":
            return
        workflow = WorkflowDefinition(
            name="Drain All Reservoirs",
            steps=[
                StepDefinition(
                    name="Drain All Reservoirs",
                    node="barty",
                    action="drain_all_to_empty",
                    args={},
                )
            ],
        )
        self.workcell_client.start_workflow(workflow, await_completion=False)  # type: ignore[attr-defined]

    def loop(
        self,
        iteration: int,
        inputs: Optional[list[list[float]]] = None,
    ) -> list[Any]:
        """Run one iteration: get ratios from solver, mix, image, measure colors.

        Args:
            iteration: Zero-based iteration index, used to select plate wells.
            inputs: Pre-computed volumes (µL) for each color channel. If None,
                volumes are generated by the Bayesian solver.

        Returns:
            List of measured RGB colors for the current batch of wells.
        """
        self.logger.info(  # type: ignore[attr-defined]
            "Running iteration",
            iteration=iteration,
        )
        if inputs is None:
            ratios = self.solver.run_iteration(
                self.previous_ratios, self.previous_colors
            )
            inputs = (np.array(ratios) * self.config.well_volume).round(3).tolist()
            self.previous_ratios = ratios

        start = iteration * self.config.pop_size
        end = (iteration + 1) * self.config.pop_size
        current_wells = self.wells[start:end]

        opentron_location = f"{self.opentron}.deck_2"
        workflow = self.workcell_client.start_workflow(  # type: ignore[attr-defined]
            workflow_definition=self.mix_colors_workflow,
            json_inputs={
                "opentron_name": self.opentron,
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
        self.data_client.save_datapoint_value(  # type: ignore[attr-defined]
            workflow.get_datapoint_id(step_key="take_picture"),
            self.config.image_directory / "plate_image.jpg",
        )

        colors = get_colors_from_file(self.config.image_directory / "plate_image.jpg")
        reference_colors = [colors[well] for well in current_wells]
        self.previous_colors = reference_colors
        return reference_colors

    def run_experiment(
        self,
        opentron: Optional[str] = None,
        pipette_side: Optional[str] = None,
        iterations: Optional[int] = None,
    ) -> dict[str, Any]:
        """Run the full experiment: initialize state, iterate, return results.

        Args:
            opentron: OT-2 node name override. Falls back to config.opentron.
            pipette_side: Pipette side override. Falls back to config.pipette_side.
            iterations: Number of rounds override. Falls back to config.iterations.

        Returns:
            Dictionary with target_color, best_color, and iterations count.
        """
        self._initialize_run(opentron, pipette_side)
        n = iterations or self.config.iterations
        try:
            for iteration in range(n):
                self.check_experiment_status()  # type: ignore[attr-defined]
                self._ensure_reservoirs_filled(self.config.reservoir_fill_level)
                self.loop(iteration)
        finally:
            self._drain_all_reservoirs()
        best_idx = int(
            np.argmin(
                self.solver._grade_population(self.previous_colors, self.target_color)
            )
        )
        return {
            "target_color": self.target_color,
            "best_color": self.previous_colors[best_idx],  # type: ignore[index]
            "iterations": n,
        }
