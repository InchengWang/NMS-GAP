"""Independent architecture adapters for a proposed matched-input benchmark.

Literature provenance: Hur et al., Scientific Reports 15:5287 (2025),
doi:10.1038/s41598-025-89716-4. Only the published recurrent specification
is used here; this module does not copy or import the authors' implementation.

Changes from the article are explicit: 12 measured input channels instead of
72, task-defined output channels instead of 10, and a caller-specified context
instead of the native 50-frame window. Width 85 is a project capacity control.
No preprocessing, scaler estimation, adaptation, or checkpoint selection is
implemented in this module. Every call starts a new recurrent context.
"""

from __future__ import annotations

import torch
from torch import nn


PAPER_DOI = "10.1038/s41598-025-89716-4"
AUTHOR_CODE_COMMIT = "62af9e446bd52e3ab500c166847d690dc0a944c9"
DEFERRED_BASELINES = {
    "hur_cnn": {
        "status": "not_implemented_unresolved_paper_code_mismatch",
        "paper_convolution_outputs": (24, 8, 10),
        "released_code_convolution_outputs": (24, 8, 3),
        "released_code_temporal_readout": "Linear(50, 50)",
        "reason": "Paper methods do not specify that temporal readout; no guess is made.",
    }
}


class SequenceLSTMBaseline(nn.Module):
    """Map [batch, time, channels] to [batch, time, task_outputs].

    This is a three-layer, unidirectional LSTM followed by the same learned
    affine projection at every time step. No previous state is accepted or
    retained, so trial/window boundaries are owned by the benchmark runner.
    PyTorch initialization is used; no published or project weights are loaded.
    """

    def __init__(self, hidden_size: int, input_channels: int = 12,
                 output_channels: int = 6) -> None:
        super().__init__()
        if min(hidden_size, input_channels, output_channels) < 1:
            raise ValueError("All dimensions must be positive integers.")
        self.input_channels = input_channels
        self.output_channels = output_channels
        self.hidden_size = hidden_size
        self.recurrent = nn.LSTM(
            input_size=input_channels,
            hidden_size=hidden_size,
            num_layers=3,
            dropout=0.2,
            bidirectional=False,
            batch_first=True,
        )
        self.angle_projection = nn.Linear(hidden_size, output_channels)

    def forward(self, measurements: torch.Tensor) -> torch.Tensor:
        if measurements.ndim != 3:
            raise ValueError("Expected [batch, time, measured_channels].")
        if measurements.shape[2] != self.input_channels:
            raise ValueError("Measured channel count differs from the declared input.")
        if measurements.shape[0] == 0 or measurements.shape[1] == 0:
            raise ValueError("Empty batches or temporal contexts are not supported.")
        frame_features, _ = self.recurrent(measurements)
        return self.angle_projection(frame_features)

    def provenance(self) -> dict:
        return {
            "paper_doi": PAPER_DOI,
            "author_code_commit_inspected": AUTHOR_CODE_COMMIT,
            "implementation": "independently_written_from_architecture_specification",
            "hidden_size": self.hidden_size,
            "layers": 3,
            "dropout": 0.2,
            "bidirectional": False,
            "input_channels": self.input_channels,
            "output_channels": self.output_channels,
            "output_layout": "batch_time_output",
            "recurrent_state": "reset_on_each_forward_call",
            "native_article_input_channels": 72,
            "native_article_output_channels": 10,
            "native_article_window_frames": 50,
            "exact_article_reproduction": False,
            "capacity_control_not_paper_setting": self.hidden_size == 85,
        }


def hur_lstm128_adapted(input_channels: int = 12,
                        output_channels: int = 6) -> SequenceLSTMBaseline:
    """Published-width backbone with explicit input/task adaptation."""
    return SequenceLSTMBaseline(128, input_channels, output_channels)


def hur_lstm85_capacity_control(input_channels: int = 12,
                                output_channels: int = 6) -> SequenceLSTMBaseline:
    """Project width chosen to control parameter count, not a paper setting."""
    return SequenceLSTMBaseline(85, input_channels, output_channels)
