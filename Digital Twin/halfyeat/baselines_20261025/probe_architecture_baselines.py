"""Synthetic-only interface/gradient probe; no optimizer or real-data access."""
from pathlib import Path
import hashlib
import json
import platform
import torch

from architecture_baselines import (
    hur_lstm128_adapted,
    hur_lstm85_capacity_control,
    DEFERRED_BASELINES,
)


def main():
    root = Path(__file__).resolve().parent
    torch.set_num_threads(2)
    torch.manual_seed(20261025)
    constructors = {
        "hur_lstm128_adapted": hur_lstm128_adapted,
        "hur_lstm85_capacity_control": hur_lstm85_capacity_control,
    }
    counts = {(128, 6): 337670, (128, 2): 337154,
              (85, 6): 151136, (85, 2): 150792}
    rows = []
    for name, constructor in constructors.items():
        for outputs in (6, 2):
            model = constructor(output_channels=outputs)
            total = sum(p.numel() for p in model.parameters())
            assert total == counts[model.hidden_size, outputs]
            checked_shapes = []
            model.eval()
            with torch.no_grad():
                for length in (50, 120, 200):
                    result = model(torch.randn(3, length, 12))
                    assert tuple(result.shape) == (3, length, outputs)
                    assert torch.isfinite(result).all()
                    checked_shapes.append(list(result.shape))
                x = torch.randn(2, 120, 12)
                first = model(x)
                model(torch.randn_like(x))
                second = model(x)
                reset_difference = (first - second).abs().max().item()
                assert reset_difference == 0
                prefix = model(x[:, :60])
                prefix_difference = (first[:, :60] - prefix).abs().max().item()
                assert prefix_difference < 1e-6
            model.train()
            synthetic_input = torch.randn(2, 120, 12, requires_grad=True)
            synthetic_target = torch.randn(2, 120, outputs)
            loss = (model(synthetic_input) - synthetic_target).square().mean()
            loss.backward()
            assert synthetic_input.grad is not None
            assert torch.isfinite(synthetic_input.grad).all()
            checked_gradients = 0
            for p in model.parameters():
                assert p.grad is not None and torch.isfinite(p.grad).all()
                assert p.grad.abs().sum() > 0
                checked_gradients += 1
            rows.append({
                "name": name,
                "provenance": model.provenance(),
                "parameters": total,
                "checked_output_shapes": checked_shapes,
                "parameter_tensors_with_finite_nonzero_gradient": checked_gradients,
                "synthetic_input_gradient_finite": True,
                "repeated_call_after_unrelated_call_max_difference": reset_difference,
                "prefix_max_difference_eval_mode": prefix_difference,
            })
    receipt = {
        "status": "passed_synthetic_only_architecture_interface_probe",
        "date": "2026-10-25",
        "seed": 20261025,
        "python": platform.python_version(),
        "torch": torch.__version__,
        "threads": torch.get_num_threads(),
        "models_and_heads": rows,
        "deferred_not_implemented": DEFERRED_BASELINES,
        "shape_cases": 12,
        "gradient_cases": 4,
        "optimizer_steps": 0,
        "real_data_arrays_or_old_weights_opened": False,
        "neural_training_fits": 0,
        "benchmark_protocol_frozen": False,
        "meaning": "interface readiness only, not training correctness or performance evidence",
        "source_sha256": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [root / "architecture_baselines.py", Path(__file__).resolve()]
        },
    }
    (root / "probe_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "shape_cases": 12,
                      "gradient_cases": 4, "optimizer_steps": 0,
                      "receipt_sha256": hashlib.sha256((root / "probe_receipt.json").read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
