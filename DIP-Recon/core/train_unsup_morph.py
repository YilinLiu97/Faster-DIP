from __future__ import print_function
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

import numpy as np
import os
import h5py
import time
import copy
import argparse
from fractions import Fraction

import torch
import torch.nn as nn
import torch.optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
from pytorch_model_summary import summary

from models import getModel
from datasets import getDataset
import configs as cfg
from fit import fit
from losses import getLoss
from visualize import *
from pruning.morphnet import *
from utils import getForwardm
from utils.mri_utils import *
from utils.common_utils import *
from utils.pruning_utils import *
from fit import eval_mri, eval_general

from skimage.metrics import structural_similarity as compare_ssim
from skimage.metrics import peak_signal_noise_ratio as compare_psnr

torch.backends.cudnn.enabled = True
torch.backends.cudnn.benchmark = True
dtype = torch.cuda.FloatTensor
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
print("num GPUs", torch.cuda.device_count())


def main(args):
    loss_func = getLoss(args.loss_func)
    forwardm = getForwardm(args)
    rec2_available = False

    dataset = getDataset(args)
    train_data = DataLoader(dataset, batch_size=1, shuffle=False, num_workers=14, pin_memory=True)
    print(len(train_data))

    if args.task == 'mri_knee' or args.task == 'mri_brain':

       for iter, sample in enumerate(train_data):
           print('Sample ', (iter+1))
           masked_kspace = sample['slice_ksp'].type(dtype)
           orig = sample['orig'].type(dtype)
           slice_ksp_torchtensor = sample['slice_ksp_torchtensor']
           csm = sample['csm'].type(dtype)
           mask1d = sample['mask1d'].type(dtype)
           mask2d = sample['mask2d'].type(dtype)
           filename_full = ' '.join(map(str, sample['filename']))
           filename = filename_full.split(".")[0]
           print(filename_full)
         
           if orig.shape[-2:] != (320,320):
             continue

           # initialize a net for each input instance
           if not args.progressive:
              args.in_size = mask2d.shape[-2:]
           args.out_size = mask2d.shape[-2:]
           args.out_chns = masked_kspace.shape[1]*2
           net = getModel(args).type(dtype)
                
           args.exp_name = args.save_path + '/' + args.model_type + '_' + filename
           # ni generation and scaling factor
           scaling_factor, ni = get_scale_factor(net,
                                args.dim,
                                args.in_size,
                                masked_kspace,
                                ni = None)
           print(ni.shape)
           if iter == 0:
              network_info(net)
              with open(args.log_filename, 'at') as log_file:
                 log_file.write('---------- Networks initialized -------------\n')
                 print(summary(net, torch.zeros(ni.shape).cuda(), show_input=True, show_hierarchical=False))
                 log_file.write(summary(net, torch.zeros(ni.shape).cuda(), show_input=True, show_hierarchical=True))
                 log_file.write('-----------------------------------------------\n')


           masked_kspace *= scaling_factor

           unders_measurement = Variable(masked_kspace)


           ### reconstruct ###
           start = time.time()

           trained_net, psnr_score, ssim_score = fit(args,
                              copy.deepcopy(net),
                              unders_measurement.type(dtype),
                              net_input = ni,
                              mask = Variable(mask2d),
                              orig = orig[0].data.cpu().numpy(),
                              apply_f = forwardm,
                              experiment_name = args.exp_name,
                              snapshots_save_path = args.save_path + '/figures/',
                              csm = csm,
                              loss_func = loss_func,
                              )

           ### data consistency ###
           rec = data_consistency(trained_net, ni, mask1d, scaling_factor*slice_ksp_torchtensor.data.cpu(), orig.shape[-2:], csm)
           print('\nfinished after %.1f minutes.'%((time.time()-start)/60))

           metrics = eval_mri(torch_to_np(orig), rec)
           print('PSNR: %.4f  SSIM: %.4f'%(metrics['psnr'], metrics['ssim']))

           ### pruning
           if args.decay or args.reg_type:
               net2 = copy.deepcopy(trained_net)
               print("Pruning...")
               net2 = pruning(args, net2, args.pruning_sensitivity)
               rec2 = data_consistency(net2, ni, mask1d, scaling_factor*slice_ksp_torchtensor.data.cpu(), orig.shape[-2:], csm)
               print((rec!=rec2).sum())
               metrics2 = eval_mri(torch_to_np(orig), rec2)
               print('(After pruning) PSNR: %.4f  SSIM: %.4f'%(metrics2['psnr'], metrics2['ssim']))
               stat = print_nonzeros(args, net2)
               rec2_available = True

           # Analysis
           info = {'rec': rec, 'orig': orig[0].data.cpu().numpy(), 'p_score': metrics['psnr'], 's_score': metrics['ssim'],
                   'filename': filename_full, 'savename': (args.exp_name + '_results')}
           visualize(info)

           if rec2_available:
              info2 = {'rec': rec2, 'orig': orig[0].data.cpu().numpy(), 'p_score': metrics2['psnr'], 's_score': metrics2['ssim'],
                        'filename': filename_full, 'savename': (args.exp_name + '_pruning_results')}
              visualize(info2)

           plot_metrics(f"{args.exp_name}_{args.num_iters}th_epoch.pt", f"{args.exp_name}_metric_plots")

    else:

        for iter, sample in enumerate(train_data):
      
            noisy_target = sample['target_img'].type(dtype)
            orig = sample['gt'].type(dtype)
            mask = sample['mask'].type(dtype) if 'mask' in sample.keys() else None
            filename_full = ' '.join(map(str, sample['filename']))
            filename = filename_full.split("/")[-1]
      
            print('Sample %d %s' % ((iter+1), filename))    

            # initialize a net for each input instance
            if not args.progressive:
                args.in_size = orig.shape[-2:]
            args.out_size = orig.shape[-2:]         
            args.out_chns = 3
            net = getModel(args).type(dtype)

            args.exp_name = args.save_path + '/' + args.model_type + '_' + filename.split(".")[0]
            ### reconstruct ###
            ni_shape = [1] + [args.dim] + list(args.in_size)
            ni = get_noise(args.dim, 'noise', args.in_size)

            if iter == 0:
               print(net)
               with open(args.log_filename, 'at') as log_file:
                    log_file.write('---------- Networks initialized -------------\n')
                    print(summary(net, torch.zeros(ni.shape).cuda(), show_input=True, show_hierarchical=False))
                    log_file.write(summary(net, torch.zeros(ni.shape).cuda(), show_input=True, show_hierarchical=True))
                    log_file.write('-----------------------------------------------\n')

      
            start = time.time()

            trained_net, psnr_score, ssim_score = fit(args,
                                                      copy.deepcopy(net),
                                                      Variable(noisy_target),
                                                      net_input=ni,
                                                      mask=mask,
                                                      orig=orig[0].data.cpu().numpy(),
                                                      apply_f=forwardm,
                                                      experiment_name=args.exp_name,
                                                      snapshots_save_path = args.save_path + '/figures/',
                                                      csm=None,
                                                      loss_func=loss_func,
                                                      )

            if args.morph_lbda:
                ## auxilary pruning
                aux_net = copy.deepcopy(trained_net)
                rec_orig = aux_net(ni)[0].data.cpu().numpy()
                metrics = eval_general(torch_to_np(orig), rec_orig)
                s = compare_ssim(torch_to_np(orig).transpose(1,2,0), rec_orig.transpose(1,2,0), multichannel=True)
                print(f"After the original training | ssim: {s}")
                aux_net = pruning(args, aux_net, args.pruning_sensitivity)
                stat = print_nonzeros(args, aux_net)
                param_size = measure_model(aux_net)
                target = noisy_target.numel() # the final model size < the image size
                print(f"After 1st pruning | prams: {param_size} | target: {target} | ssim: {s}")
                iter = 1
                while iter < 3:
                    
                    ratio = 1.5 #np.round(int(512/args.dim)) #get_uniform_ratio(param_size, target)
                    print(f"Growing the net with the ratio: {ratio}")
                    uniform_grow(args, aux_net, ratio)
                    params = measure_model(aux_net, actual_size=True)
                    print(f"After growth | prams: {params}")
                    trained_net, psnr_score, ssim_score = fit(args,
                                                              aux_net,
                                                              Variable(noisy_target),
                                                              net_input=ni,
                                                              mask=mask,
                                                              orig=orig[0].data.cpu().numpy(),
                                                              apply_f=forwardm,
                                                              experiment_name=args.exp_name,
                                                              snapshots_save_path=args.save_path + '/figures/',
                                                              csm=None,
                                                              loss_func=loss_func,
                                                              )
                    aux_net = pruning(args, trained_net, args.pruning_sensitivity)
                    param_size = measure_model(aux_net)
                    iter += 1
                    # eval
                    aux_rec = aux_net(ni)[0].data.cpu().numpy()
                    metrics = eval_general(torch_to_np(orig), aux_rec)
                    s = compare_ssim(torch_to_np(orig).transpose(1,2,0), aux_rec.transpose(1,2,0), multichannel=True)
                    print(f"After the {iter}th pruning | prams: {param_size} | target: {target} | ssim: {s}")

            print('\nfinished after %.1f minutes.' % ((time.time() - start) / 60))

            print('PSNR: %.4f  SSIM: %.4f' % (psnr_score, ssim_score))
            rec = trained_net(ni)[0].data.cpu().numpy()

            metrics = eval_general(torch_to_np(orig), rec)
            print(compare_ssim(torch_to_np(orig).transpose(1,2,0), rec.transpose(1,2,0), multichannel=True))
#            print(compare_psnr(torch_to_np(orig).transpose(1,2,0), torch_to_np(rec).transpose(1,2,0))

            ### pruning
            if args.decay and args.reg_type or args.sr:
                net2 = copy.deepcopy(trained_net)
                print("Pruning...")
                pruning(args, net2, args.pruning_sensitivity)
                rec2 = net2(ni)[0].data.cpu().numpy()
                metrics2 = eval_general(torch_to_np(orig), rec2)
                stat = print_nonzeros(args, net2)
                rec2_available = True


            # Analysis
            info = {'rec': rec, 'orig': orig[0].data.cpu().numpy(), 'p_score': metrics['psnr'], 's_score': metrics['ssim'],
                   'filename': filename_full, 'savename': (args.exp_name + '_results')}
            visualize(info)

            if rec2_available:
               info2 = {'rec': rec2, 'orig': orig[0].data.cpu().numpy(), 'p_score': metrics2['psnr'], 's_score': metrics2['ssim'],
                        'filename': filename_full, 'savename': (args.exp_name + '_pruning_results')}
               visualize(info2)

            plot_metrics(f"{args.exp_name}_{args.num_iters}th_epoch.pt", f"{args.exp_name}_metric_plots")


if __name__ == '__main__':

    def str2bool(v):
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')
   
    def str2float(v):
        return float(sum(Fraction(s) for s in v.split()))
 
    def str2int(v):
        return int(v)

    def str2none(v):
        if v == None or v == 'None' or v == 'none':
           return None
        else:
           v
      #  else:
      #     return int(v)

    parser = argparse.ArgumentParser()   

    parser.add_argument('--exp_name', default='saves/')
    parser.add_argument('--special', default=None, type=str)
    parser.add_argument('--folder_path', default='/shenlab/lab_stor/yilinliu/multicoil_val/')
    parser.add_argument('--save_path', default=None, type=str)
    parser.add_argument('--log_filename', default='', type=str)
    parser.add_argument('--prepruning', default=None, type=str, help='avg | multi | none')

    # task related
    parser.add_argument('--task', default='mri_knee',
                        help='mri_knee | mri_brain | sr | denoising | inpainting')

    # mri data related
    parser.add_argument('--ac_factor', default=4, type=str2int,
                        help='acceleration factor')
    parser.add_argument('--center_frac', default=0.07, type=str2float,
                        help='percentage of the preserved center portion of the k-space')

    # natural data related
    parser.add_argument('--noise_sigma', default=25, type=str2int)

    # pruning related
    parser.add_argument('--prune_type', default=None, type=str2none, help='HS')
    parser.add_argument('--pruning_sensitivity', default=0.01, type=str2float, help='ConvDecoder:0.03 | DIP:0.01')
    parser.add_argument('--dam_lambda', default=0.0, type=str2float, help='lambda=0.001 for DAM')
    parser.add_argument('--meta_img_idx', default=[0,2,4,6,8], nargs='+', type=int, help='the image idexes used for pre-pruning')

    # model related
    parser.add_argument('--reg_noise_std', default=0, type=str2float, help='add noise at each iteration')
    parser.add_argument('--progressive', default=False, type=str2bool, help='whether the image is gradually upsampled')
    parser.add_argument('--model_type', default='ConvDecoder', type=str)
    parser.add_argument('--noise_type', default='u', type=str, help='u | n, uniform or normal')
    parser.add_argument('--patch_size', default=16, type=str2int,
                        help='dividing images into tokens')
    parser.add_argument('--num_layers', default=7, type=str2int,
                        help='default:7 in ConvDecoder')
    parser.add_argument('--out_chns', default=3, type=str2int)
    parser.add_argument('--dim', default=256, type=str2int,
                        help='number of channels per layer except for the last one')
    parser.add_argument('--in_size', default=[8, 4], nargs='+', type=int)
    parser.add_argument('--out_size', default=[512, 512], nargs='+', type=int)
    parser.add_argument('--filter_size_up', default=3, type=str2int, help='filter size for the decoder')
    parser.add_argument('--filter_size_down', default=5, type=str2int, help='filter size for the encoder')
    parser.add_argument('--num_skips', default=2, type=str2int, help='number of skip connections')
    parser.add_argument('--norm_func', default='bn', type=str, help='bn | instance')
    parser.add_argument('--need_dropout', default=False, type=str2bool)
    parser.add_argument('--need_sigmoid', default=False, type=str2bool)
    parser.add_argument('--num_scales', default=5, type=str2int, help='for DIP setup')
    parser.add_argument('--act_func', default='ReLU', type=str, help='ReLU|LeakyReLU|Swish|ELU|GELU')
    parser.add_argument('--upsample_mode', default='nearest', help='nearest|bilinear')
    parser.add_argument('--downsample_mode', default='stride', help='stride|avg|max|lanczos2')
    parser.add_argument('--pad', default='zero', help='zero|reflection')

    # optimization related
    parser.add_argument('--optimizer', default='adam', type=str, help='rmsprop | adam | sgd')
    parser.add_argument('--decay_lr', default=False, type=str2bool, help='decay the learning rate, linear | cosine')
    parser.add_argument('--morph_lbda', default=0, type=str2float, help='decay for morph net')
    parser.add_argument('--freq_lbda', default=0, type=str2float, help='weight for the spectral loss')
    parser.add_argument('--step_size', default=50, type=str2int, help='the step size for linearly decayed learning rate')
    parser.add_argument('--gamma', default=0.75, type=str2float, help='the decayed rate for linearly decayed learning rate')
    parser.add_argument('--T_max', default=1, type=str2int, help='# of changes')
    parser.add_argument('--loss_func', default='l1', type=str)
    parser.add_argument('--freq_loss_func', default='ehm', type=str)
    parser.add_argument('--every_n_iter', default=200, type=str2int, help='print every n iterations')
    parser.add_argument('--num_iters', default=2500, type=str2int)
    parser.add_argument('--reg_type', default=0, type=str2int,
                        help='regularization type: 0:None 1:L1 2:Hoyer 3:HS 4:Transformed L1')
    parser.add_argument('--decay', default=[0.0, 0.0], nargs='+', type=str2float, help='0.0000001 for element-wise HS, 0.00001 for struc-wise')
    parser.add_argument('--sr', default=0.0, type=str2float, help='sparsity rate for network slimming')
    parser.add_argument('--lr', type=str2float, default=0.008)
    parser.add_argument('--param_idx', default=[], nargs='+', type=int, help='the layer index for printing out the learning rate, [0,8,16,28]')

    args = parser.parse_args()

    args.save_path = f"saves/{args.task}/{args.model_type}_{args.special}" if args.special is not None \
        else f"saves/{args.task}/{args.model_type}"
    print(args.save_path)
    os.makedirs(args.save_path, exist_ok=True)
 
    args.log_filename = os.path.join(args.save_path, 'log.txt')

    print("------------ Input arguments: ------------")
    for key, val in vars(args).items():
        print(f"{key} {val}")
    print("---------------- End ----------------")

    with open(args.log_filename, 'wt') as log_file:
       log_file.write('------------ Options -------------\n')
       for k, v in sorted(vars(args).items()):
           log_file.write('%s: %s\n' % (str(k), str(v)))
       log_file.write('-------------- End ----------------\n')

    main(args)