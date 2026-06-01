model_type = "UNETP"
model_path = "./aae_model_ne_27_03_22_128_fl_next" #"./aae_model_ne_27_03_22_128_fl" #"./aae_model_ne_27_03_22_128_fl_next" 
patch_size = (32,64,64,1) ## 2D: (1,*,*,1) , 3D: (*,*,*,1)
latent_dim = 128 #128 #64 #1024
number_epochs = 100 #10000
batch_size = 4
batch_norm = True

input = "channel_signal"
target = "channel_target"
