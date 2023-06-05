python denoising.py --task real_denoising \
                      --dataset 'polyu' \
                      --save_folder '/mnt/yaplab/data/yilinliu/saves/Real_World_Noise/polyu/test' \
                      --imsize -1 \
                      --model_type DIP_2_scaled \
                      --progressive False \
                      --num_iters 3000 \
                      --filter_size_down 3 \
                      --filter_size_up 3 \
                      --num_layers 7 \
                      --num_skips 0 \
                      --need_sigmoid True \
                      --loss_func mse \
                      --num_scales 5 \
                      --optimizer adam \
                      --decay_lr False \
                      --step_size 50 \
                      --gamma 0.55 \
                      --exp_weight 0.99 \
                      --Lipschitz_constant 0 \
                      --Lipschitz_reg 0 \
                      --verbose False \
                      --num_power_iterations 0 \
                      --noise_type u \
                      --noise_method noise \
                      --special 5levels_0skips_128chns_withReg\
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
                      --dim 128 \
                      --lr 0.01              
            
