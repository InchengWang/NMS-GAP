"""Independent staged sparse-IMU reconstruction models for a new experiment.

No data, source checkpoint, scaler or ground-truth intermediate is read here.
The caller supplies TRAIN-standardized observed shank ACC/GYRO [B,T,12].
All predicted channels are in their declared TRAIN-standardized target spaces.
The TCN encoder follows the existing project family: causal kernel-7 residual
blocks with dilations 1/2/4 and per-frame LayerNorm, giving RF=85 frames.
The decoder is framewise, so it adds no temporal receptive field.

Sensor targets: S3 waist, S4 left foot, S5 right foot, each ACC xyz/GYRO xyz.
Position targets: eight declared skeletal landmarks relative to a declared
root in an inherited engineering frame. They are not physical sensor locations.
Latent-bottleneck channels are unstructured and must not be called reconstructed
sensor measurements or skeletal positions.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping, Any

import torch
from torch import nn
from torch.nn import functional as F

MODES = ('direct', 'auxiliary_only', 'latent_bottleneck',
         'strict_staged', 'residual_staged')
SEMANTIC_MODES = ('auxiliary_only', 'strict_staged', 'residual_staged')
SIGNAL_GROUPS = ('S3_ACC', 'S3_GYRO', 'S4_ACC', 'S4_GYRO', 'S5_ACC', 'S5_GYRO')


class LeftPaddedConv(nn.Module):
    def __init__(self, channels_in: int, channels_out: int, dilation: int):
        super().__init__()
        self.padding_left = 6 * dilation
        self.operation = nn.Conv1d(channels_in, channels_out, 7,
                                   dilation=dilation)

    def forward(self, sequence: torch.Tensor) -> torch.Tensor:
        return self.operation(F.pad(sequence, (self.padding_left, 0)))


class TemporalResidual(nn.Module):
    def __init__(self, channels_in: int, width: int, dilation: int,
                 dropout: float):
        super().__init__()
        self.conv_first = LeftPaddedConv(channels_in, width, dilation)
        self.conv_second = LeftPaddedConv(width, width, dilation)
        self.norm_first = nn.LayerNorm(width)
        self.norm_second = nn.LayerNorm(width)
        self.dropout = nn.Dropout(dropout)
        self.residual = (nn.Conv1d(channels_in, width, 1)
                         if channels_in != width else nn.Identity())

    def forward(self, sequence: torch.Tensor) -> torch.Tensor:
        hidden = self.conv_first(sequence).transpose(1, 2)
        hidden = self.dropout(F.relu(self.norm_first(hidden))).transpose(1, 2)
        hidden = self.conv_second(hidden).transpose(1, 2)
        hidden = self.dropout(self.norm_second(hidden)).transpose(1, 2)
        return F.relu(hidden + self.residual(sequence))


class TCNEncoder(nn.Module):
    receptive_field_frames = 85

    def __init__(self, width: int = 64, dropout: float = 0.15):
        super().__init__()
        self.blocks = nn.Sequential(*[
            TemporalResidual(12 if level == 0 else width, width, dilation,
                             dropout)
            for level, dilation in enumerate((1, 2, 4))
        ])

    def forward(self, observations: torch.Tensor) -> torch.Tensor:
        return self.blocks(observations.transpose(1, 2)).transpose(1, 2)


class GRUEncoder(nn.Module):
    """Two-layer unidirectional alternative; every call resets hidden state."""
    receptive_field_frames = None

    def __init__(self, width: int = 64, dropout: float = 0.15):
        super().__init__()
        self.recurrent = nn.GRU(12, width, num_layers=2, batch_first=True,
                                dropout=dropout, bidirectional=False)

    def forward(self, observations: torch.Tensor) -> torch.Tensor:
        return self.recurrent(observations)[0]


class StagedReconstruction(nn.Module):
    """Five explicitly different motion pathways; forward accepts observations only.

    direct and auxiliary_only share encoder/decoder dimensions and initialization
    for a common seed, since optional heads are constructed afterwards.
    latent_bottleneck and strict_staged have identical state_dict structure,
    parameter count and initialization for a common seed. Only intermediate
    interpretation and auxiliary-loss eligibility differ.
    """
    def __init__(self, mode: str, *, encoder: str = 'tcn', width: int = 64,
                 decoder_width: int = 64, dropout: float = 0.15,
                 angle_channels: int = 6):
        super().__init__()
        if mode not in MODES:
            raise ValueError('Unknown declared model mode.')
        if encoder not in ('tcn', 'gru'):
            raise ValueError('Encoder must be tcn or gru.')
        if min(width, decoder_width, angle_channels) < 1:
            raise ValueError('Channel dimensions must be positive.')
        if not math.isfinite(dropout) or not 0 <= dropout < 1:
            raise ValueError('Dropout must be finite and in [0,1).')
        self.mode, self.encoder_kind = mode, encoder
        self.width, self.angle_channels = width, angle_channels
        self.encoder = (TCNEncoder(width, dropout) if encoder == 'tcn'
                        else GRUEncoder(width, dropout))
        self.motion_input_channels = (width if mode in ('direct', 'auxiliary_only')
                                      else 54 if mode == 'residual_staged'
                                      else 42)
        self.motion_decoder = nn.Sequential(
            nn.Linear(self.motion_input_channels, decoder_width), nn.ReLU(),
            nn.Dropout(dropout), nn.Linear(decoder_width, angle_channels))
        # Neutral parameter names preserve exact latent/semantic network identity.
        if mode != 'direct':
            self.bottleneck_first = nn.Linear(width, 18)
            self.bottleneck_second = nn.Linear(width, 24)

    def forward(self, observations: torch.Tensor) -> dict[str, Any]:
        if observations.ndim != 3 or observations.shape[-1] != 12:
            raise ValueError('Expected observed shank input [batch,time,12].')
        if observations.shape[0] == 0 or observations.shape[1] == 0:
            raise ValueError('Empty batches or contexts are not supported.')
        hidden = self.encoder(observations)
        result: dict[str, Any] = {'mode': self.mode}
        if self.mode == 'direct':
            decoder_input = hidden
        else:
            first = self.bottleneck_first(hidden)
            second = self.bottleneck_second(hidden)
            intermediate = torch.cat((first, second), dim=-1)
            if self.mode == 'latent_bottleneck':
                result['latent_hat'] = intermediate
            else:
                result['signals_hat'] = first
                result['positions_hat'] = second
            if self.mode == 'auxiliary_only':
                decoder_input = hidden
            elif self.mode == 'residual_staged':
                decoder_input = torch.cat((observations, intermediate), dim=-1)
            else:
                decoder_input = intermediate
        result['angles_hat'] = self.motion_decoder(decoder_input)
        return result

    def parameter_report(self) -> dict[str, Any]:
        count = lambda module: sum(p.numel() for p in module.parameters())
        enc, dec = count(self.encoder), count(self.motion_decoder)
        heads = (0 if self.mode == 'direct' else
                 count(self.bottleneck_first) + count(self.bottleneck_second))
        active = enc + dec + (heads if self.mode in (
            'latent_bottleneck', 'strict_staged', 'residual_staged') else 0)
        return {'mode': self.mode, 'encoder': self.encoder_kind,
                'encoder_parameters': enc, 'motion_decoder_parameters': dec,
                'intermediate_head_parameters': heads,
                'total_trainable_parameters': count(self),
                'parameters_on_motion_path': active,
                'motion_decoder_input_channels': self.motion_input_channels,
                'semantic_auxiliary_supervision': self.mode in SEMANTIC_MODES,
                'observed_input_skip_to_motion_decoder': self.mode == 'residual_staged',
                'receptive_field_frames': self.encoder.receptive_field_frames,
                'decoder_temporal_context_added': 0,
                'all_channels_TRAIN_standardized': True,
                'clinical_JCS_or_sensor_position_claim': False,
                'forward_accepts_ground_truth': False}


@dataclass(frozen=True)
class LossWeights:
    angles: float = 1.0
    signals: float = 0.25
    positions: float = 0.25

    def __post_init__(self):
        if any(not math.isfinite(v) or v < 0 for v in (
                self.angles, self.signals, self.positions)):
            raise ValueError('Loss weights must be finite and nonnegative.')


def _connected_zero(prediction: torch.Tensor) -> torch.Tensor:
    clean = torch.where(torch.isfinite(prediction), prediction,
                        torch.zeros_like(prediction))
    return clean.sum() * 0.0


def _masked_mse(prediction: torch.Tensor, target: torch.Tensor | None,
                mask: torch.Tensor | None) -> tuple[torch.Tensor, torch.Tensor]:
    if target is None:
        if mask is not None:
            raise ValueError('A mask without its target is ambiguous.')
        return _connected_zero(prediction), prediction.new_zeros((), dtype=torch.long)
    if prediction.shape != target.shape:
        raise ValueError('Prediction and target shapes must match.')
    if target.device != prediction.device:
        raise ValueError('Targets must share the prediction device.')
    if mask is None:
        valid = torch.ones_like(prediction, dtype=torch.bool)
    else:
        if mask.dtype != torch.bool or mask.device != prediction.device:
            raise ValueError('Masks must be boolean on the prediction device.')
        if mask.ndim == prediction.ndim - 1 and mask.shape == prediction.shape[:-1]:
            mask = mask.unsqueeze(-1)
        try:
            valid = torch.broadcast_to(mask, prediction.shape)
        except RuntimeError as exc:
            raise ValueError('Mask cannot broadcast to target.') from exc
    if not torch.isfinite(target[valid]).all():
        raise ValueError('Nonfinite unmasked target.')
    if not torch.isfinite(prediction[valid]).all():
        raise ValueError('Nonfinite unmasked prediction.')
    # Mask BEFORE subtraction. Multiplication by zero would not remove NaNs.
    clean_prediction = torch.where(valid, prediction, torch.zeros_like(prediction))
    clean_target = torch.where(valid, target.to(dtype=prediction.dtype),
                               torch.zeros_like(prediction))
    count = valid.sum()
    mse = (clean_prediction - clean_target).square().sum() / count.clamp_min(1)
    return mse, count


def reconstruction_losses(
    predictions: Mapping[str, Any], *,
    angle_target: torch.Tensor | None = None,
    signal_target: torch.Tensor | None = None,
    position_target: torch.Tensor | None = None,
    angle_mask: torch.Tensor | None = None,
    signal_mask: torch.Tensor | None = None,
    position_mask: torch.Tensor | None = None,
    weights: LossWeights = LossWeights(),
) -> dict[str, Any]:
    """Independent losses; targets/masks never enter model.forward.

    All targets are already standardized using their allowed unique TRAIN
    support. Sensor loss averages six sensor×modality group MSEs equally,
    omitting groups with no valid elements. Position/angle losses each average
    their own valid coordinates. No supervision yields a differentiable zero.
    Targets with masked-out NaNs are permitted; unmasked NaNs fail explicitly.
    direct/latent modes never consume semantic auxiliary targets in the loss.
    """
    mode = predictions.get('mode')
    if mode not in MODES or 'angles_hat' not in predictions:
        raise ValueError('Predictions lack a declared mode or angle output.')
    angle_loss, angle_count = _masked_mse(
        predictions['angles_hat'], angle_target, angle_mask)
    anchor = predictions['angles_hat']
    group_losses = []
    group_counts = []
    if mode in SEMANTIC_MODES:
        signals = predictions['signals_hat']
        positions = predictions['positions_hat']
        if signals.shape[-1] != 18 or positions.shape[-1] != 24:
            raise ValueError('Semantic head dimensions differ from the contract.')
        if signal_target is not None and signal_target.shape != signals.shape:
            raise ValueError('Sensor target shape differs from the contract.')
        # Validate mask layout before slicing groups; accept [B,T] or [B,T,18].
        if signal_mask is not None:
            if signal_mask.ndim == signals.ndim-1 and signal_mask.shape == signals.shape[:-1]:
                signal_mask = signal_mask.unsqueeze(-1).expand_as(signals)
            if signal_mask.shape != signals.shape:
                raise ValueError('Sensor mask must be [B,T] or [B,T,18].')
        for group in range(6):
            sl = slice(3*group, 3*group+3)
            value, count = _masked_mse(
                signals[..., sl],
                None if signal_target is None else signal_target[..., sl],
                None if signal_mask is None else signal_mask[..., sl])
            group_losses.append(value); group_counts.append(count)
        grouped = torch.stack(group_losses)
        counts = torch.stack(group_counts)
        active = (counts > 0).to(dtype=grouped.dtype)
        signal_loss = (grouped * active).sum() / active.sum().clamp_min(1)
        position_loss, position_count = _masked_mse(
            positions, position_target, position_mask)
    else:
        signal_loss = _connected_zero(anchor)
        position_loss = _connected_zero(anchor)
        position_count = anchor.new_zeros((), dtype=torch.long)
        counts = anchor.new_zeros((6,), dtype=torch.long)
        grouped = torch.stack([_connected_zero(anchor) for _ in range(6)])
    total = (weights.angles * angle_loss + weights.signals * signal_loss
             + weights.positions * position_loss)
    return {'total': total, 'angles': angle_loss, 'signals': signal_loss,
            'positions': position_loss, 'signal_group_losses': grouped,
            'signal_group_valid_counts': counts,
            'angle_valid_count': angle_count,
            'position_valid_count': position_count,
            'weights': {'angles': weights.angles, 'signals': weights.signals,
                        'positions': weights.positions},
            'semantic_auxiliary_supervision_applied': mode in SEMANTIC_MODES}


def build_model(mode: str, *, encoder: str = 'tcn', width: int = 64,
                decoder_width: int = 64, dropout: float = .15,
                angle_channels: int = 6) -> StagedReconstruction:
    return StagedReconstruction(mode, encoder=encoder, width=width,
                                decoder_width=decoder_width, dropout=dropout,
                                angle_channels=angle_channels)
