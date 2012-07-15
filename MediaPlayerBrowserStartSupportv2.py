from pprint import pprint as pp2
import datetime
import struct, binascii

from ID3_tag_list import ID3v2, ID3v3 

import wx
import wx.media

from configurer import UTF16_BE_BOM, UTF16_LE_BOM

class ID3(object):
    
    def __init__(self, fp):

        try:  #try to find the raw file
            with open(fp, 'rb') as f:
                self.song = f.read()
        except IOError as e:
            print e, 'couldnt open the song'
    
    
        #sets an id
        self.id = id(self)
        #saves the file path
        self.fp = fp
        #load the regular ID3v2 header.
        self.id3_header = self.song[:10]
        #get the id3 string
        self.headerID3 = struct.unpack('>3s', self.id3_header[0:3])[0]
        #get the ID3version ie 3.0 
        self.headerVER = struct.unpack('>2B', self.id3_header[3:5])
        #get the flag enabled, see docs. Extended header etc.
        self.headerFLAGS = struct.unpack('>B', self.id3_header[5])[0]
        #get song size
        self.headerSIZE = struct.unpack('>i', self.id3_header[6:])
        
        if self.headerVER == (3, 0):
            
            self.tags = self.getAllFramesV3()
            self.title = self.tags['TIT2']['data']['cont']
            self.album = self.tags['TALB']['data']['cont']
            self.artist = self.tags['TPE1']['data']['cont']
        elif self.headerVER == (2, 0):
            
            self.tags = self.getAllFramesV2()
            self.title = self.tags['TT2']['data']['cont']
            self.album = self.tags['TAL']['data']['cont']
            self.artist = self.tags['TP1']['data']['cont']
            
        else:
            print 'ERROR ON INIT'
            raise Exception('Unrecognized ID3 version')
    #----------------------------------------------------------------------
    def __str__(self):
        """prints a human readable info:
        band - title"""
        
        return '{} - {}'.format(self.artist, self.title)
    
    #----------------------------------------------------------------------
    def getAllFramesV2(self):
        """gets the tags for ID3.v2.0"""
        
        #print 'OH GOD, v2'
        #True when end of frames found
        done = False
        next_byte = 10 
        all_frames = []
        while not done:
            frame = self.getFrameDataV2(next_byte)
            
            if frame != None :
                next_byte = frame['data']['byte']
                if '\x00' not in frame['id']:
                    all_frames.append(frame)
                    
                else:
                    done = True                
            else:
                'frames None, so setting done to True'
                done = True
                
        all_frames_dict = {}
        for frame in all_frames:
            all_frames_dict[frame['id']]= frame
        
        return all_frames_dict
     
    #----------------------------------------------------------------------
    def getFrameDataV2(self, pos):
        """"""
        
        #header frame
        frm_header = self.song[pos:pos+6]
    
        ID = struct.unpack('>3s', frm_header[:3])[0]
        if ID not in ID3v2.keys() and ID != 'CM1':
            print 'ID3v2 tag error', ID, '############'
            return None
        #LEN = struct.unpack('>i', frm_header[3:7])[0]
        LEN = int(binascii.hexlify(frm_header[3:6]), 16)
        #FLAG = struct.unpack('>cc', frm_header[8:])
        
        #content of tag
        # if it's a text info frame
        if ID.startswith('T'):
            ENC = self.song[pos+6]
            content = self.song[pos+6 +1 : pos+6 + LEN]
        else:
            ENC = 'Not Text tag'
            content = self.song[pos+6 : pos+6 + LEN]
        #last byte in tag
        BYTE = pos + 6 + LEN
        
        headerInner = {  #'id': ID,
                       'len': LEN,
                       #'flags': FLAG,
                       'cont': content,
                       'enc': ENC,
                       'byte': BYTE,}
        headerOuter = {'id': ID,
                       'data': headerInner}
        
        return headerOuter
        #print 'done reading v2 header'    
    
    def getFrameDataV3(self, pos):
        '''gets the ID, Size and Flags for the given frame,
         as well as frame's content
         
         returns a dict with the {ID {len,flags,content}}'''
        
        #if ID3v3
        try:
            #frame's header
            frm_header = self.song[pos:pos+10]
            
            ID = struct.unpack('>4s', frm_header[:4])[0]
            LEN = struct.unpack('>i', frm_header[4:8])[0]
            FLAG = struct.unpack('>cc', frm_header[8:])
            
            #print 'ID:', ID
            #print 'LEN:', LEN
            #print 'flag:', FLAG
    
            #frames content
            if ID.startswith('T') or ID.startswith('WXXX') or \
               ID.startswith('IPLS'): 
                ENC = struct.unpack('>c', self.song[pos+10])[0]
                
                #if is unicode:
                if ENC != '\x00':
                    #endianness
                    end = self.song[pos+11:pos+11+2]
                    if end == UTF16_LE_BOM:
                        content = self.song[pos+11+2:pos+10+LEN].decode('UTF-16LE')
                    elif end == UTF16_BE_BOM:
                        content = self.song[pos+11+2:pos+10+LEN].decode('UTF-16BE')
                    else:
                        print 'Endianness isn\'t understood'
                        
                #If it's string                
                else:
                    content = self.song[pos+11:pos+10+LEN]
                    end = 'string'
             
            else:
                content = self.song[pos+10:pos+10+LEN]
                ENC = r'N/A'
            
            #ending
            BYTE =   pos + 10 + LEN
            
            headerInner = {  #'id': ID,
                           'len': LEN,
                           'flags': FLAG,
                           'cont': content,
                           'enc': ENC,
                           'byte': BYTE,}
            headerOuter = {'id': ID,
                           'data': headerInner}
            
            return headerOuter
        
        except struct.error as e:
            print e, self.song
            
    #----------------------------------------------------------------------
    def getAllFramesV3(self):
        """loads an mp3 and finds all ID3v3 tags and returns them in a dict"""
        
        #True when end of frames found
        done = False
        next_byte = 10
        all_frames = []
        while not done:
            frame = self.getFrameDataV3(next_byte)
            
            if frame != None :
                next_byte = frame['data']['byte']
                if '\x00' not in frame['id']:
                    all_frames.append(frame)
                    
                else:
                    done = True                
            else:
                'frames None, so setting done to True'
                done = True
                
        all_frames_dict = {}
        for frame in all_frames:
            all_frames_dict[frame['id']]=frame
        
        return all_frames_dict

########################################################################
class SongList(wx.Frame):
    """This is going to be the main frame where you can choose a bunch of
    songs to play, on the left of the screen."""

    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        super(SongList, self).__init__(id=wx.ID_ANY, *args, **kwargs)
        
        self.lstCtrl = wx.ListCtrl(self, style=wx.BORDER_RAISED|
                                                wx.LC_REPORT|
                                                wx.EXPAND,
                                                
                                        size=(-1, 50))
        self.lstCtrl.InsertColumn(0, 'Head1')
        self.lstCtrl.InsertColumn(1, 'Head2')
        self.lstCtrl.InsertColumn(2, 'Head3')
        
        self.lstCtrl.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.lstCtrl.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        self.lstCtrl.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)        
        
        #self.lstCtrl.SetStringItem(0, 0, 'asd')
        self.lstCtrl.InsertStringItem(0, 'Line 0')
        #self.lstCtrl.SetStringItem(0, 1, 'col1')
        #self.lstCtrl.SetStringItem(0, 2, 'col2')
        
        self.lstCtrl.SetItemState(5, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        #self.lbl = wx.TextCtrl(self, value='hel')
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.lstCtrl, 0, wx.ALL|wx.EXPAND)
        
        self.SetSizer(sizer)
        
        self.Show()

    
    
if __name__ == '__main__':
    """Run the following if module is top module"""
    
    path = '../1.mp3'
    songTag = ID3(path)
    
    #pp2(songTag.headerSIZE)
    #songTag.getAllFramesV2()
    
    app = wx.App(redirect=False)
    
    slist = SongList(parent=None)
    
    app.MainLoop()
