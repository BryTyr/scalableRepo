

import os
import os.path
import pandas as pd
from glob import glob
import numpy as np
import librosa
import threading
import librosa.display
import pylab
import matplotlib.pyplot as plt
from multiprocessing import Pool
from matplotlib import figure
import gc
#from path import Path

# creates a spectrogram from an mp3 file
def create_spectrogram(names):

        plt.interactive(False)
        clip, sample_rate = librosa.load('/mnt/c/Users/bryan/OneDrive/Documents/SharedFolderUbuntu/scalableComputing/Assignment3CleanWorkflow/rawData/' + names + '.mp3', sr=24000)
        fig = plt.figure(figsize=[1.28,0.64])
        ax = fig.add_subplot(111)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.set_frame_on(False)
        S = librosa.feature.melspectrogram(y=clip, sr=sample_rate)
        s_db=librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
        filename_out  = '/mnt/c/Users/bryan/OneDrive/Documents/SharedFolderUbuntu/scalableComputing/Assignment3CleanWorkflow/DataConverted/' + names.lower() + '.jpg'
        plt.savefig(filename_out,dpi=170, bbox_inches='tight',pad_inches=0)
        plt.close()
        fig.clf()
        plt.close(fig)
        plt.close('all')
        # deletes reference to variables garbage collection
        del filename_out,clip,sample_rate,fig,ax,S,s_db


#gets the names of the files from both processed and preprocessed files
Data_dir1=[os.path.splitext(filename.lower())[0] for filename in os.listdir("rawData")]
processed_data_dir1=[os.path.splitext(filename.lower())[0] for filename in os.listdir("ConvertedData")]

#sorts them into a unique list of files for preprocessing
unique_list = set(Data_dir1) - set(processed_data_dir1)
unique_list=sorted(unique_list)
print(len(unique_list))

#12 hreads to speed up the preprocessing
with Pool(12) as p:
       p.map(create_spectrogram, list(unique_list))
