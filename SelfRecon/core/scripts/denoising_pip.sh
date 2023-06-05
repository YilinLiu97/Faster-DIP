python train_unsup.py --task denoising \
                      --folder_path '../data/denoising' \
                      --save_folder '/mnt/yaplab/data/yilinliu/saves/PIP_CBM3D' \
                      --imsize -1 \
                      --model_type multiscale_mlp \
                      --progressive False \
                      --num_iters 3000 \
                      --norm_func bn \
                      --noise_sigma 25 \
                      --filter_size_down 1 \
                      --filter_size_up 1 \
                      --num_layers 7 \
                      --num_skips 5 \
                      --need_sigmoid True \
                      --loss_func mse \
                      --freq_loss_func moment_matching \
                      --num_scales 5 \
                      --optimizer adam \
                      --decay_lr False \
                      --step_size 50 \
                      --gamma 0.55 \
                      --morph_lbda 1e-5 \
                      --exit_layer_idx_prior 0.5 \
                      --min_tau 0.4 \
                      --exp_weight 0.99 \
                      --Lipschitz_constant 0 \
                      --Lipschitz_reg 0 \
                      --verbose False \
                      --num_power_iterations 0 \
                      --noise_type u \
                      --noise_method noise \
                      --n_freqs 10 \
                      --cosine_only False \
                      --iters_print_acc 100 \
                      --special UnformInput_withReg\
                      --prune_type None \
                      --reg_type 0 \
                      --decay 1e-5 0 \
                      --freq_lbda 0 \
                      --prune_type None \
                      --reg_type 0 \
                      --decay 1e-7 0 \
                      --freq_lbda 0 \
                      --reg_noise_std '1/30'\
                      --act_func ReLU \
                      --upsample_mode 'bilinear' \
                      --pad zero \
                      --dim 64 \
                      --lr 0.01              
            
