import os
import os.path
import random
import shutil


#gets the names of the files from both processed and preprocessed files
processed_data_dir1=[os.path.splitext(filename.lower())[0] for filename in os.listdir("MultipleTTSConverted")]
print(type(processed_data_dir1))
print(processed_data_dir1[0])
random.shuffle(processed_data_dir1)
print(processed_data_dir1[0])
for value in range(75000):
    #+processed_data_dir1[value]+".jpg
    shutil.move("/mnt/c/Users/bryan/OneDrive/Documents/SharedFolderUbuntu/scalableComputing/Assignment3MultipleTTS/MultipleTTSConverted/"+processed_data_dir1[value]+".jpg", "/mnt/c/Users/bryan/OneDrive/Documents/SharedFolderUbuntu/scalableComputing/Assignment3MultipleTTS/MixedDataTrain/"+processed_data_dir1[value]+".jpg")
