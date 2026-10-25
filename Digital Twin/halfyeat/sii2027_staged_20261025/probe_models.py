"""Synthetic-only model/loss interface probes. No training fit or real data read."""
from pathlib import Path
import hashlib, inspect, json

import torch

from models import MODES, SEMANTIC_MODES, LossWeights, build_model, reconstruction_losses

ROOT = Path(__file__).resolve().parent
SEED = 20261025


def fresh(mode, encoder='tcn'):
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(SEED)
        return build_model(mode, encoder=encoder)


def tensors(batch=2, frames=120):
    generator = torch.Generator().manual_seed(SEED+1)
    return (torch.randn(batch, frames, 12, generator=generator),
            torch.randn(batch, frames, 6, generator=generator),
            torch.randn(batch, frames, 18, generator=generator),
            torch.randn(batch, frames, 24, generator=generator))


def main():
    torch.set_num_threads(2)
    x, angle, signal, position = tensors()
    reports = []
    shape_cases = 0
    gradient_cases = 0
    forbidden_gt_calls_blocked = 0
    max_prefix_difference = 0.0
    max_reset_difference = 0.0
    hook_cases = []
    for encoder in ('tcn', 'gru'):
        for mode in MODES:
            model = fresh(mode, encoder).eval()
            assert list(inspect.signature(model.forward).parameters) == ['observations']
            for frames in (31, 120, 200):
                example = tensors(frames=frames)[0]
                with torch.no_grad(): out = model(example)
                assert out['angles_hat'].shape == (2, frames, 6)
                assert torch.isfinite(out['angles_hat']).all()
                if mode in SEMANTIC_MODES:
                    assert out['signals_hat'].shape == (2, frames, 18)
                    assert out['positions_hat'].shape == (2, frames, 24)
                    assert 'latent_hat' not in out
                elif mode == 'latent_bottleneck':
                    assert out['latent_hat'].shape == (2, frames, 42)
                    assert 'signals_hat' not in out and 'positions_hat' not in out
                else:
                    assert set(out) == {'mode', 'angles_hat'}
                shape_cases += 1
            with torch.no_grad():
                full = model(x)['angles_hat']
                prefix = model(x[:, :73])['angles_hat']
                difference = float((full[:, :73]-prefix).abs().max())
                assert difference < 2e-6, (mode, encoder, difference)
                max_prefix_difference = max(max_prefix_difference, difference)
                model(tensors(batch=3, frames=53)[0])
                repeated = model(x)['angles_hat']
                reset_diff = float((repeated-full).abs().max())
                assert reset_diff == 0
                max_reset_difference = max(max_reset_difference, reset_diff)
            try:
                model(x, signal_target=signal)
            except TypeError:
                forbidden_gt_calls_blocked += 1
            else:
                raise AssertionError('Ground truth entered model.forward.')
            # Angle loss must reach semantic heads only when used by motion.
            model.zero_grad(set_to_none=True)
            predictions = model(x)
            loss = reconstruction_losses(predictions, angle_target=angle)
            loss['angles'].backward()
            if mode in ('latent_bottleneck', 'strict_staged', 'residual_staged'):
                assert model.bottleneck_first.weight.grad is not None
                assert model.bottleneck_first.weight.grad.abs().sum() > 0
                assert model.bottleneck_second.weight.grad.abs().sum() > 0
            if mode == 'auxiliary_only':
                assert model.bottleneck_first.weight.grad is None
                assert model.bottleneck_second.weight.grad is None
            model.zero_grad(set_to_none=True)
            predictions = model(x)
            losses = reconstruction_losses(predictions, angle_target=angle,
                signal_target=signal, position_target=position)
            if mode in SEMANTIC_MODES:
                assert losses['semantic_auxiliary_supervision_applied']
            else:
                assert not losses['semantic_auxiliary_supervision_applied']
                assert losses['signals'].item() == losses['positions'].item() == 0
            losses['total'].backward()
            for name, parameter in model.named_parameters():
                assert parameter.grad is not None, (encoder, mode, name)
                assert torch.isfinite(parameter.grad).all(), (encoder, mode, name)
            gradient_cases += 1
            reports.append(model.parameter_report())
        # Exact semantic vs unstructured bottleneck architecture/initialization.
        latent, strict = fresh('latent_bottleneck', encoder).eval(), fresh('strict_staged', encoder).eval()
        assert latent.state_dict().keys() == strict.state_dict().keys()
        assert all(torch.equal(v, strict.state_dict()[k]) for k,v in latent.state_dict().items())
        with torch.no_grad():
            lo, so = latent(x), strict(x)
            assert torch.equal(lo['angles_hat'],so['angles_hat'])
            assert torch.equal(lo['latent_hat'],torch.cat((so['signals_hat'],so['positions_hat']),-1))
        direct, auxiliary = fresh('direct', encoder).eval(), fresh('auxiliary_only', encoder).eval()
        assert all(torch.equal(v,auxiliary.state_dict()[k]) for k,v in direct.state_dict().items())
        with torch.no_grad(): assert torch.equal(direct(x)['angles_hat'],auxiliary(x)['angles_hat'])
        # Observe the actual motion-decoder input, then sever the bottleneck.
        for mode, expected_channels in [('strict_staged',42),('residual_staged',54)]:
            model = fresh(mode,encoder).eval()
            captured=[]
            handle=model.motion_decoder.register_forward_pre_hook(lambda module,args:captured.append(args[0].detach().clone()))
            with torch.no_grad(): out=model(x)
            handle.remove()
            expected=torch.cat((out['signals_hat'],out['positions_hat']),-1)
            if mode=='residual_staged': expected=torch.cat((x,expected),-1)
            assert captured[0].shape[-1]==expected_channels
            assert torch.equal(captured[0],expected)
            with torch.no_grad():
                for head in (model.bottleneck_first,model.bottleneck_second):
                    head.weight.zero_();head.bias.zero_()
                a=model(x)['angles_hat'];b=model(x+1.25)['angles_hat']
            delta=float((a-b).abs().max())
            if mode=='strict_staged':assert delta==0
            else:assert delta>1e-7
            hook_cases.append({'encoder':encoder,'mode':mode,
                               'decoder_channels':expected_channels,
                               'zero_bottleneck_change_when_x_changed':delta})

    # Loss: six group means must receive equal weight regardless of valid count.
    pa=torch.zeros(1,2,6,requires_grad=True)
    ps=torch.zeros(1,2,18,requires_grad=True)
    pp=torch.zeros(1,2,24,requires_grad=True)
    targets_s=torch.full_like(ps,float('nan'))
    mask_s=torch.zeros_like(ps,dtype=torch.bool)
    targets_s[...,0:3]=1;mask_s[...,0:3]=True
    targets_s[:,0,3:6]=3;mask_s[:,0,3:6]=True
    outputs={'mode':'strict_staged','angles_hat':pa,'signals_hat':ps,'positions_hat':pp}
    losses=reconstruction_losses(outputs,angle_target=torch.full_like(pa,2),
        signal_target=targets_s,signal_mask=mask_s,position_target=torch.full_like(pp,3),
        weights=LossWeights(2,.5,.25))
    assert losses['angles'].item()==4
    assert losses['signals'].item()==5
    assert losses['positions'].item()==9
    assert losses['total'].item()==12.75
    assert losses['signal_group_valid_counts'].tolist()==[6,3,0,0,0,0]
    losses['total'].backward()
    assert all(torch.isfinite(p.grad).all() for p in (pa,ps,pp))
    assert ps.grad[...,6:].abs().sum()==0
    # Masked-out NaN predictions as well as targets cannot pollute finite loss.
    pn=torch.full((1,2,18),float('nan'),requires_grad=True)
    pn.data[...,0:3]=0
    mn=torch.zeros_like(pn,dtype=torch.bool);mn[...,0:3]=True
    tn=torch.full_like(pn,float('nan'));tn[...,0:3]=2
    nan_out={'mode':'strict_staged','angles_hat':torch.zeros(1,2,6,requires_grad=True),
             'signals_hat':pn,'positions_hat':torch.zeros(1,2,24,requires_grad=True)}
    nl=reconstruction_losses(nan_out,signal_target=tn,signal_mask=mn)
    assert nl['signals'].item()==4 and torch.isfinite(nl['total'])
    nl['total'].backward();assert torch.isfinite(pn.grad).all()
    # Entirely missing groups/positions/angles yield zero with a valid graph.
    zero_out={k:(v.detach().clone().requires_grad_() if torch.is_tensor(v) else v)
              for k,v in outputs.items()}
    zero=reconstruction_losses(zero_out,
        angle_target=torch.full_like(pa,float('nan')),angle_mask=torch.zeros_like(pa,dtype=torch.bool),
        signal_target=torch.full_like(ps,float('nan')),signal_mask=torch.zeros_like(ps,dtype=torch.bool),
        position_target=torch.full_like(pp,float('nan')),position_mask=torch.zeros_like(pp,dtype=torch.bool))
    assert zero['total'].item()==0 and zero['total'].requires_grad
    zero['total'].backward()
    assert all(v.grad is not None and torch.isfinite(v.grad).all() and v.grad.abs().sum()==0
               for v in zero_out.values() if torch.is_tensor(v))
    invalid=0
    for call in [
        lambda: reconstruction_losses(outputs,signal_target=targets_s),
        lambda: reconstruction_losses(outputs,angle_target=torch.zeros(1,2,5)),
        lambda: reconstruction_losses(outputs,angle_target=torch.zeros_like(pa),angle_mask=torch.zeros_like(pa)),
        lambda: reconstruction_losses(outputs,signal_mask=torch.zeros_like(ps,dtype=torch.bool)),
        lambda: LossWeights(-1,.25,.25),
        lambda: LossWeights(float('nan'),.25,.25),
        lambda: fresh('invalid'),
        lambda: fresh('direct')(torch.zeros(2,120,18)),
    ]:
        try:call()
        except ValueError:invalid+=1
        else:raise AssertionError('Invalid input was silently accepted.')
    receipt={'status':'passed_synthetic_only_staged_model_and_loss_probe',
        'date':'2026-10-25','seed':SEED,'torch':torch.__version__,'threads':2,
        'shape_cases':shape_cases,'gradient_cases':gradient_cases,
        'ground_truth_forward_calls_blocked':forbidden_gt_calls_blocked,
        'maximum_eval_prefix_difference':max_prefix_difference,
        'maximum_state_reset_difference':max_reset_difference,
        'latent_and_strict_state_dict_and_initial_predictions_identical':True,
        'direct_and_auxiliary_common_motion_state_and_initial_predictions_identical':True,
        'decoder_path_checks':hook_cases,
        'masked_nan_loss_and_gradients_finite':True,
        'six_sensor_modality_groups_equally_weighted':True,
        'fully_unsupervised_loss_differentiable_zero':True,
        'invalid_contract_inputs_blocked':invalid,
        'default_loss_weights':{'angles':1.0,'signals':.25,'positions':.25},
        'models':reports,'real_data_or_old_weights_read':False,'optimizer_steps':0,
        'formal_training_fits':0,'TRAIN_role_guard_implemented':False,
        'scaler_or_data_synchronization_verified':False,
        'full_independent_training_or_performance_audit':False,
        'source_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
                         for n in ['models.py','probe_models.py']}}
    (ROOT/'model_probe_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':receipt['status'],'shape_cases':shape_cases,
                      'gradient_cases':gradient_cases,'invalid_inputs_blocked':invalid,
                      'parameters':[m for m in reports if m['encoder']=='tcn'],
                      'optimizer_steps':0}))

if __name__=='__main__':main()
