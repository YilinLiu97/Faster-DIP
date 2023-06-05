python super_resolution.py --task sr \
                      --model_type DD \
                      --num_iters 5000 \
                      --folder_path '/mnt/yaplab/data/yilinliu/datasets/Set5' \
                      --save_folder '/mnt/yaplab/data/yilinliu/saves/noise_fitting' \
                      --sr_factor 4 \
                      --sr_kernel_type lanczos2 \
                      --filter_size_down 3 \
                      --filter_size_up 3 \
                      --in_size 16 16 \
                      --progressive True \
                      --num_layers 6 \
                      --num_skips 0 \
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
                      --exp_weight 0 \
                      --noise_type u \
                      --noise_method noise \
                      --n_freqs 8 \
                      --special 5Layers_TransposedConv\
                      --prune_type None \
                      --reg_type 0 \
                      --decay 0 0 \
                      --freq_lbda 0 \
                      --reg_noise_std '0' \
                      --upsample_mode transposed \
                      --act_func ReLU \
                      --pad zero \
                      --dim 128 \
                      --lr 0.01                       
                      
