import config
import os
import subprocess
import shutil
from app_init import app
def run_command(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f'Error occurred: {stderr.decode()}')
    else:
        print(stdout.decode())


def testModelSwinIR(input, output):
    cmd = f"""{config.PYTHONCOMMAND} {config.SWINIR_CONFIG['SCRIPT_PATH']} --task {config.SWINIR_CONFIG['TASK']} --noise {config.SWINIR_CONFIG['NOISE']} --model_path {config.SWINIR_CONFIG['MODEL_PATH']} --folder_gt {config.SWINIR_CONFIG['INPUT_DIR']} --save_dir {config.SWINIR_CONFIG['SAVE_DIR']}"""
    run_command(cmd)

def testModelPix2Pix(input, output):
    cmd =f"""{config.PYTHONCOMMAND} {config.PIX2PIX_CONFIG['TEST_PY']} --dataroot {config.PIX2PIX_CONFIG['DATAROOT']}{input} --name {config.PIX2PIX_CONFIG['MODEL_NAME']} --model test --direction {config.PIX2PIX_CONFIG['DIRECTION']} --preprocess {config.PIX2PIX_CONFIG['PREPROCESS']} --num_test {config.PIX2PIX_CONFIG['NUM_TEST']} --dataset_mode {config.PIX2PIX_CONFIG['DATASET_MODE']} --netG {config.PIX2PIX_CONFIG['NETG']} --norm {config.PIX2PIX_CONFIG['NORM']} --crop_size {config.PIX2PIX_CONFIG['CROP_SIZE']} --load_size {config.PIX2PIX_CONFIG['LOAD_SIZE']} --results_dir {config.PIX2PIX_CONFIG['RESULTS_DIR']} --checkpoints_dir {config.PIX2PIX_CONFIG['CHECKPOINTS_DIR']}"""
    run_command(cmd)
    # testModelSwinIR(input, output)

def runModel(input, output):
    delete_directory_if_exists('finalResults')
    delete_directory_if_exists('resultsPix2Pix')
    delete_directory_if_exists(app.config['ENHANCED_FOLDER'])
    testModelPix2Pix(input, output)
    delete_files_with_word(config.SWINIR_CONFIG["INPUT_DIR"], "_real")
    remove_suffix_from_all_files(config.SWINIR_CONFIG["INPUT_DIR"],"_fake")
    testModelSwinIR(input, output)
    copy_to_image_directory(config.SWINIR_CONFIG["INPUT_DIR"], app.config['ENHANCED_FOLDER'])
    # copy_to_image_directory( input ,output)


def delete_files_with_word(directory, word):
    try:
        for filename in os.listdir(directory):
            basename, extension = os.path.splitext(filename)
            extension = extension[1:]  # remove the dot from the extension

            if extension in config.ALLOWED_EXTENSIONS and basename.endswith(word):
                os.remove(os.path.join(directory, filename))
        print(f"Deleted files ending with {word} from {directory}.")
    except Exception as e:
        print(f"An error occurred while deleting files: {e}")



def remove_suffix_from_all_files(directory, suffix):

    for filename in os.listdir(directory):
        _, file_extension = os.path.splitext(filename)
        file_extension = file_extension[1:]  # remove the dot from the extension

        if file_extension.lower() in config.ALLOWED_EXTENSIONS and filename.endswith(suffix + '.' + file_extension):
            new_name = filename[:-(len(suffix + '.' + file_extension))] + '.' + file_extension
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))

def delete_directory_if_exists(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f"Directory {directory} has been deleted.")
    else:
        print(f"Directory {directory} does not exist.")

def copy_to_image_directory(src, dst):
    # Ensure destination directory exists
    os.makedirs(dst, exist_ok=True)
    try:
        # Copy all files in the source to the destination directory
        for filename in os.listdir(src):
            shutil.copy(os.path.join(src, filename), dst)
        print(f"Copied files from {src} to {dst}.")
    except Exception as e:
        print(f"An error occurred while copying files: {e}")


