python train_unsup.py --task denoising \
                      --folder_path '../data/denoising' \
                      --save_folder '/mnt/yaplab/data/yilinliu/saves/CBM3D' \
                      --input_image_name 'image_Baboon512rgb.png' \
                      --imsize -1 \
                      --model_type DIP_2_scaled \
                      --progressive False \
                      --num_iters 3000 \
                      --norm_func bn \
                      --noise_sigma 25 \
                      --filter_size_down 3 \
                      --filter_size_up 3 \
                      --num_skips 0 \
                      --num_scales 2 \
                      --need_sigmoid True \
                      --loss_func mse \
                      --freq_loss_func moment_matching \
                      --optimizer adam \
                      --decay_lr False \
                      --step_size 50 \
                      --gamma 0.55 \
                      --morph_lbda 1e-5 \
                      --exp_weight 0.99 \
                      --Lipschitz_constant 0 \
                      --Lipschitz_reg 0 \
                      --verbose False \
                      --num_power_iterations 0 \
                      --noise_type u \
                      --noise_method noise \
                      --special 2levels_0skips_256chns\
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
                      --dim 256 \
                      --lr 0.01              
            
