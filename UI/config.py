# py
import os
import subprocess
import shutil

PYTHONCOMMAND = "py"
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Configurations for the Pix2Pix model.
PIX2PIX_CONFIG = {
    'MODEL_NAME': "pix2pix_NewData_Both",  # Name of the Pix2Pix model.
    'CHECKPOINTS_DIR': "..\\pytorch-CycleGAN-and-pix2pix\\checkpoints\\",  # Checkpoints directory for the Pix2Pix model.
    'DATAROOT': '..\\UI\\',  # Root directory for the dataset.
    'TEST_PY': '../pytorch-CycleGAN-and-pix2pix/test.py',  # Path to the Pix2Pix test script.
    'DIRECTION': 'AtoB',
    'PREPROCESS': 'scale_width_and_crop',
    'NUM_TEST': 10,
    'DATASET_MODE': 'single',
    'NETG': 'unet_256',
    'NORM': 'batch',
    'CROP_SIZE': 512,
    'LOAD_SIZE': 512,
    'RESULTS_DIR':'../UI/resultsPix2Pix'
}

# Configurations for the SwinIR model.
SWINIR_CONFIG = {
    'MODEL_PATH': "..\KAIR\denoising\swinir_denoising_gray_15\models\latest_G.pth",  # Path to the SwinIR model.
    'SAVE_DIR': "../UI/finalResults",  # Directory to save the SwinIR results.
    'SCRIPT_PATH': '../KAIR/main_test_swinir.py',  # Path to the script for running the SwinIR model.
    'TASK': 'gray_dn',
    'NOISE': 15,
    'INPUT_DIR' : "..//UI//resultsPix2Pix//" + PIX2PIX_CONFIG['MODEL_NAME'] + "//test_latest//images"
}