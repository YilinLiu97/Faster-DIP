python train_unsup.py --task denoising \
                      --folder_path '/mnt/yaplab/data/yilinliu/datasets/DIV2K_train_HR' \
                      --save_folder '/mnt/yaplab/data/yilinliu/saves/DIV2K' \
                      --imsize 256 256 \
                      --model_type DIP_2_scaled \
                      --progressive False \
                      --num_iters 3000 \
                      --norm_func bn \
                      --noise_sigma 25 \
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
                      --special 2levels_0skips_256chns_Smoothing_Resized256\
                      --prune_type None \
                      --reg_type 0 \
                      --decay 1e-8 0 \
                      --freq_lbda 0 \
                      --reg_noise_std '1/30' \
                      --upsample_mode bilinear \
                      --act_func ReLU \
                      --pad zero \
                      --dim 256 \
                      --lr 0.01                       
            
