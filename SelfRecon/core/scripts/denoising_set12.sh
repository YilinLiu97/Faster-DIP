python denoising.py --task denoising \
                      --folder_path '/mnt/yaplab/data/yilinliu/datasets/Set12' \
                      --save_folder '/mnt/yaplab/data/yilinliu/saves/Fig1_10000iters' \
                      --input_image_name 'image_F16_512rgb.png' \
                      --imsize -1 \
                      --model_type DIP_2_scaled \
                      --progressive False \
                      --num_iters 10000 \
                      --norm_func bn \
                      --noise_sigma 50 \
                      --filter_size_down 3 \
                      --filter_size_up 3 \
                      --num_layers 7 \
                      --num_skips 0 \
                      --need_sigmoid True \
                      --loss_func mse \
                      --freq_loss_func moment_matching \
                      --num_scales 2 \
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
                      --special 2levels_0skips_64chns_Set12_sigma50_10000iters\
                      --prune_type None \
                      --reg_type 0 \
                      --decay 1e-5 0 \
                      --freq_lbda 0 \
                      --prune_type None \
                      --reg_type 0 \
                      --decay 1e-7 0 \
                      --freq_lbda 0 \
                      --reg_noise_std '1/20'\
                      --act_func ReLU \
                      --upsample_mode 'bilinear' \
                      --pad zero \
                      --dim 64 \
                      --lr 0.01              
            
