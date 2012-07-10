from pprint import pprint as pp2
import datetime
import os, sys
import glob, fnmatch


#----------------------------------------------------------------------
def findMP3s(path=None):
    """finds all MP3s below the path given and returns a list of all the
    file paths"""
    
    if not path:
    
        lib_path = r'.\songs'
    else:
        lib_path = path
        
    
    all_songs = []
    
    #folder from os.walk is: root, dirnames, filenames
    for rt, dirs, files in os.walk(lib_path):
    
        for fp in files:
            if fnmatch.fnmatch(fp, '*.mp3'):
                fullpath = r'{}\{}'.format(rt, fp)
                all_songs.append(fullpath)
                
    #pp2(all_songs)
    print 'found {} songs'.format(len(all_songs))
     
    return all_songs   