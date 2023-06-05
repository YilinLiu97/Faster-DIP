python inpainting.py --task inpainting \
                      --model_type DIP_2_scaled \
                      --progressive False \
                      --num_iters 3000 \
                      --folder_path '../data/inpainting' \
                      --save_folder '/mnt/yaplab/data/yilinliu/saves/noise_fitting' \
                      --mask_type 'kate_mask' \
                      --zero_fraction 0.5 \
                      --filter_size_down 5 \
                      --filter_size_up 3 \
                      --in_size 512 512 \
                      --num_layers 4 \
                      --num_skips 2 \
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
                      --special kate_mask_2_2_256\
                      --prune_type None \
                      --reg_type 0 \
                      --decay 0 0 \
                      --freq_lbda 0 \
                      --reg_noise_std '0' \
                      --upsample_mode 'bilinear' \
                      --act_func ReLU \
                      --pad zero \
                      --dim 256 \
                      --lr 0.01                       
                      
