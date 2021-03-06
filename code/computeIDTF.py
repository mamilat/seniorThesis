# extract IDT features

import numpy as np
import subprocess, os
import sys, avconv

"""
Wrapper library for the IDTF executable.
Implements methods to extract IDTFs.
Seperate methods for extracting IDTF and computing Fisher Vectors.

Assumes existance of tmpDir to store resized videos.


Example usage:

python computeIDTF.py video_list.txt output_directory



Usage: DenseTrackStab video_file [options]
Options:
  -h                        Display this message and exit
  -S [start frame]          The start frame to compute feature (default: S=0 frame)
  -E [end frame]            The end frame for feature computing (default: E=last frame)
  -L [trajectory length]    The length of the trajectory (default: L=15 frames)
  -W [sampling stride]      The stride for dense sampling feature points (default: W=5 pixels)
  -N [neighborhood size]    The neighborhood size for computing the descriptor (default: N=32 pixels)
  -s [spatial cells]        The number of cells in the nxy axis (default: nxy=2 cells)
  -t [temporal cells]       The number of cells in the nt axis (default: nt=3 cells)
  -H [human bounding box]   The human bounding box file to remove outlier matches (default: None)
  

"""
#Path to the video repository
ucf101_path = "/afs/cs.stanford.edu/group/cvgl/rawdata/THUMOS2014/Training/videos/"

# Improved Dense Trajectories binary
dtBin = '/afs/cs.stanford.edu/u/anenberg/code/improved_trajectory_release/release/DenseTrackStab'

# Temp directory to store resized videos
#Should put videos in different location.
tmpDir = './tmp'

SRC="/afs/cs.stanford.edu/u/anenberg/code/snrThesis/src/"


COMPUTE_FV = 'python '+os.path.join(SRC,"computeFVstream.py")



def extract(videoName, outputBase):
    """
    Extracts the IDTFs and stores them in outputBase file.
    """
    if not os.path.exists(videoName):
        print '%s does not exist!' % videoName
        return False
    resizedName=videoName
    resizedName = os.path.join(tmpDir, os.path.basename(videoName))
    if not avconv.resize(videoName, resizedName):
        resizedName = videoName     # resize failed, just use the input video
    subprocess.call('%s %s > %s' % (dtBin, resizedName, outputBase), shell=True)
    #Removes the resized video after using it to extract IDTFs.
    os.remove(resizedName)
    return True



def extractFV(videoName, outputBase,gmm_list):
    """
    Extracts the IDTFs, constructs a Fisher Vector, and saves the Fisher Vector at outputBase
    outputBase: the full path to the newly constructed fisher vector.
    gmm_list: file of the saved list of gmms
    """
    if not os.path.exists(videoName):
        print '%s does not exist!' % videoName
        return False
    resizedName=videoName
    """
    resizedName = os.path.join(tmpDir, os.path.basename(videoName))
    resized_vids = [filename for filename in os.listdir(tmpDir) if filename.endswith('.avi')]
    if os.path.basename(videoName) not in resized_vids:
        if not avconv.resize(videoName, resizedName):
            resizedName = videoName     # resize failed, just use the input video
    """
    subprocess.call('%s %s | %s %s %s' % (dtBin, resizedName, COMPUTE_FV, outputBase, gmm_list), shell=True)
    #Removes the resized video after using it to extract IDTFs.
    #os.remove(resizedName)
    return True


if __name__ == '__main__':
    #Useage: python computeIDTF.py video_list.txt output_directory
    videoList = sys.argv[1]
    outputBase = sys.argv[2]
    try:
        f = open(videoList, 'r')
        videos = f.readlines()
        f.close()
        videos = [video.rstrip() for video in videos]
        for i in range(0, len(videos)):
            outputName = os.path.join(outputBase, os.path.basename(videos[i])[:-4]+".features")
            videoLocation = os.path.join(ucf101_path,videos[i])
            print "generating IDTF for %s" % (videos[i],)
            extract(videoLocation, outputName)
            print "completed."
    except IOError:
        sys.exit(0)