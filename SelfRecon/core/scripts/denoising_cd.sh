python train_unsup.py --task denoising \
                      --folder_path '/mnt/yaplab/data/yilinliu/datasets/Set12' \
                      --save_folder '/mnt/yaplab/data/yilinliu/saves/PoissonNoise/Set12/0_01' \
                      --imsize -1 \
                      --model_type ConvDecoder \
                      --progressive True \
                      --in_size 16 16 \
                      --out_chns 1 \
                      --num_iters 3000 \
                      --norm_func bn \
                      --noise_sigma 25 \
                      --poisson_scale 0.01 \
                      --filter_size_down 3 \
                      --filter_size_up 3 \
                      --num_layers 6 \
                      --num_skips 0 \
                      --need_sigmoid False \
                      --loss_func mse \
                      --freq_loss_func moment_matching \
                      --num_scales 2 \
                      --optimizer adam \
                      --decay_lr False \
                      --step_size 50 \
                      --gamma 0.55 \
                      --special 3000iters_NoSigmoid_NoReg \
                      --reg_type 0 \
                      --decay 1e-8 0 \
                      --freq_lbda 0 \
                      --reg_noise_std '0' \
                      --dim 128 \
                      --upsample_mode bilinear \
                      --act_func ReLU \
                      --pad zero \
                      --lr 0.01                       
            
