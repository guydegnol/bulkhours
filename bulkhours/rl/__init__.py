import sys
import matplotlib.pyplot as plt
from .hugs import PPOHugs  # noqa
from ..core import runrealcmd


def init_env(verbose=True):
    """Use pip from the current kernel"""
    import tensorflow as tf
    import IPython as ip

    if "google.colab" in sys.modules:
        # runrealcmd("sudo apt-get update", verbose=verbose)
        runrealcmd("sudo apt install swig cmake", verbose=verbose)
        runrealcmd("sudo apt-get install -y python-opengl ffmpeg", verbose=verbose)
        runrealcmd("pip install gym", verbose=verbose)
        runrealcmd("apt update && apt install xvfb && pip3 install pyvirtualdisplay && pip install pyvirtualdisplay")
        # runrealcmd("pip install gymnasium ", verbose=True)
        runrealcmd("pip install stable-baselines3[extra] box2d box2d-kengz array2gif", verbose=verbose)
        # runrealcmd("pip install gymnasium[atari,toy_text,box2d,classic_control,accept-rom-license]", verbose=True)
        runrealcmd("pip install huggingface_sb3 pyglet==1.5.1", verbose=verbose)

    if not tf.config.list_physical_devices("GPU"):
        print("No GPU was detected. Neural nets can be very slow without a GPU.")
        if "google.colab" in sys.modules:
            print("Go to Runtime > Change runtime and select a GPU hardware accelerator.")
        if "kaggle_secrets" in sys.modules:
            print("Go to Settings > Accelerator and select GPU.")

    plt.rc("font", size=14)
    plt.rc("axes", labelsize=14, titlesize=14)
    plt.rc("legend", fontsize=14)
    plt.rc("xtick", labelsize=10)
    plt.rc("ytick", labelsize=10)
    plt.rc("animation", html="jshtml")


def plot_environment(env, figsize=(5, 4)):
    plt.figure(figsize=figsize)
    img = env.render()
    if type(img) == list:
        img = img[0]
    plt.imshow(img)
    plt.axis("off")
    plt.show()
    return img
