import wx
import wx.media
from pprint import pprint as pp2
import datetime

from MediaPlayerBrowser import ID3


class MediaPlayerApp(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(MediaPlayerApp, self).__init__(id=wx.ID_ANY, *args, **kwargs) 
            
        self.song_path = r'C:\Programming\Python\Project\MusicPlayer\10.mp3'
            
        self.sizer_main = wx.GridBagSizer()
        self.sizer_main.SetRows(3)
        self.SetSizer(self.sizer_main)
            
        self.initPlayer()
        #self.initButtons()
        
        self.initSongList()
        
        #self.SetBackgroundColour(wx.GREEN)
        
        self.setSizerMainColors()
        
        self.Layout()
        #self.Show()
        self.Fit()
    #----------------------------------------------------------------------
    def setSizerMainColors(self):
        """sets colors of the grids so I can debug a bit easier
        row/column"""
        
        
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.RED)
        panel.Show()
        self.sizer_main.Add(panel, (1, 1), flag=wx.EXPAND)
        
        
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.BLUE)
        panel.Show()
        self.sizer_main.Add(panel, (2, 1), flag=wx.EXPAND)
        
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.GREEN)
        panel.Show()
        self.sizer_main.Add(panel, (1, 0), flag=wx.EXPAND)
        
        
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.WHITE)
        panel.Show()
        self.sizer_main.Add(panel, (2, 0), flag=wx.EXPAND)
        
        
    def initPlayer(self):    

        #create panel
        self.player_panel = wx.Panel(self)
        self.player_panel.SetBackgroundColour(wx.BLUE)
        #sizer for the panel
        self.player_sizer = wx.BoxSizer(wx.VERTICAL)
        self.player_panel.SetSizer(self.player_sizer)
        
        #create labels for music picking
        self.lbl_cursong = wx.StaticText(self.player_panel, label='Current Song:')
        try:
            lbl = self.song_path
        except AttributeError as e:
            lbl = '--SONG NOT SET--'
        self.lbl_setsong = wx.StaticText(self.player_panel, label=lbl)
        self.lbl_setsong.SetBackgroundColour((100, 90, 70))
        self.btn_chooseSong = wx.Button(self.player_panel, label='Choose Song to play')
        self.Bind(wx.EVT_BUTTON, self.media_path, self.btn_chooseSong)
        
        #sizers 
        self.siz_songInfo = wx.BoxSizer(wx.HORIZONTAL)
        self.siz_songInfo.AddMany([self.lbl_cursong, self.lbl_setsong])
        
        self.siz_songChoose = wx.BoxSizer(wx.HORIZONTAL)
        self.siz_songChoose.Add(self.btn_chooseSong)
        
        #main sizers for this section
        self.player_sizer.AddMany([self.siz_songInfo, self.siz_songChoose])
        
        
        
        #music player change the back end to WMP10, and catch the event for playback
        self.mediaPlayer = wx.media.MediaCtrl(self.player_panel,  
                                        szBackend=wx.media.MEDIABACKEND_WMP10, )
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.media_loaded)
        self.player_sizer.Add(self.mediaPlayer)
        
        #play button
        self.btn_play = wx.Button(self.player_panel, label='Play Song')
        self.player_sizer.Add(self.btn_play)
        self.Bind(wx.EVT_BUTTON,
                  lambda e: self.media_play(self.song_path, e),
                  self.btn_play)
        
        #pause button
        self.btn_pause = wx.Button(self.player_panel, label='Pause')
        self.Bind(wx.EVT_BUTTON, self.media_pause, self.btn_pause)
        self.player_sizer.Add(self.btn_pause)
        
        #progress slider
        self.sldr_prog = wx.Slider(self.player_panel)
        self.Bind(wx.EVT_SLIDER, self.SetProg, self.sldr_prog)
        self.player_sizer.Add(self.sldr_prog)
        
        #volume slider
        self.sldr_vol = wx.Slider(self.player_panel, style=wx.VERTICAL | wx.SL_INVERSE)
        self.Bind(wx.EVT_SLIDER, self.SetVol, self.sldr_vol)
        self.player_sizer.Add(self.sldr_vol)
        
        self.sizer_main.Add(self.player_panel, (0, 1))
        
        self.player_sizer.Layout()
        self.player_panel.Fit()
        self.Show()
        self.Layout()
        
    #----------------------------------------------------------------------
    def SetVol(self, e):
        """sets the volume of the song"""
        
        vol = self.sldr_vol.GetValue()
        print 'cur vol val:', vol
        vol /= 100.0
        print 'volume to be set:', vol
        self.mediaPlayer.SetVolume(vol)
        
    #----------------------------------------------------------------------
    def SetProg(self, e):
        """seeks the song to wherever the slider stops"""
        
        prog = self.sldr_prog.GetValue()
        print 'prog to seek to:', prog
        self.mediaPlayer.Seek(prog)
        
    def media_loaded(self, e):
        #print 'caught EVT_MEDIA_LOADED'
        self.mediaPlayer.Play()
        
        #progress slider
        maxLen = self.mediaPlayer.Length()
        #print 'maxlen', maxLen, 'sec'
        self.sldr_prog.SetRange(0, maxLen)        
        
        #volume slider
        self.sldr_vol.SetRange(0, 100)        
        
    #----------------------------------------------------------------------
    def media_path(self, e):
        """"""
        print 'Gotcha bitch'
        dlg = wx.FileDialog(self, )
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            
            print 'path chosen:', path
            
            self.lbl_setsong.SetLabel(path)
            self.Layout()
        
            self.song_path = path
        
    def media_play(self, path, event=None):
        '''Plays the media, at path'''
        
        print 'load:',  path
        self.mediaPlayer.Load(path)
        self.mediaPlayer.SetInitialSize()
        
        self.mediaPlayer.SetVolume(1)
        self.mediaPlayer.SetPlaybackRate(1)
        print 'music playing'
        
        
    def media_pause(self, event):
        '''Pauses the media. If it's already paused, it'll start it up'''
        
        if not self.mediaPlayer.GetState() == 1:
            
            self.mediaPlayer.Pause()
        else:
            self.mediaPlayer.Play()

    #----------------------------------------------------------------------
    def initSongList(self):
        """builds a list of songs in the current dir"""
        
        self.snglst_sizer = wx.BoxSizer()
        self.snglst_panel = wx.Panel(self)
        
        self.sngLst = wx.ListCtrl(self.snglst_panel, style=wx.LC_REPORT,
                                  size=(500, 300))

        #create col headers
        self.sngLst.InsertColumn(0, 'Track')
        self.sngLst.InsertColumn(1, 'Album')
        self.sngLst.InsertColumn(2, 'Band')

        #set col widths
        self.sngLst.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.sngLst.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        self.sngLst.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
        
        #create the sizer for the song list
        self.snglst_sizer.Add(self.sngLst)
        self.snglst_sizer.Layout()
        self.snglst_panel.Show()
        
        #add the songist to the main sizer
        self.sizer_main.Add(self.snglst_panel, (0, 0),
                             #span=wx.GBSpan(3, 1),
                             flag=wx.EXPAND)
        
        
        #make a list of songs
        list_of_songs = ['C:\\Programming\\Python\\Project\\MusicPlayer\\10.mp3',
                         'C:\\Programming\\Python\\Project\\MusicPlayer\\1.mp3']
        
        
        self.rowData = {}
        for i, song in enumerate(list_of_songs):
            
            songTag = ID3(song)
        
            title = songTag.tags['TIT2']['data']['cont']
            album = songTag.tags['TALB']['data']['cont']
            band = songTag.tags['TPE1']['data']['cont']
        
            
            self.sngLst.InsertStringItem(i, title)
            self.sngLst.SetStringItem(i, 1, album.decode(errors='ignore'))
            self.sngLst.SetStringItem(i, 2, band.decode(errors='ignore'))
            self.sngLst.SetItemData(i, songTag.id)
            
            ##for each tag in a song
            #for i, tag in enumerate(songTag.tags):
                
                #title = songTag.tags[tag]['data']
                #title = songTag.tags[tag]['data']
                #title = songTag.tags[tag]['data']
                
                #self.sngLst.InsertStringItem(i, tag)
                #self.sngLst.SetStringItem(i, 1, songTag.tags[tag]['data']['cont'].decode(errors='ignore'))
        
            self.rowData[songTag.id] = songTag
                
        #bind item select to play a song
        self.sngLst.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSongSelect)
        self.sngLst.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onSongActive)
        
            
        self.Fit()
        self.Layout()
        
    #----------------------------------------------------------------------
    def onSongActive(self, e):
        """print the song info"""
        
        
        
        index = e.m_itemIndex
        song = self.rowData[self.sngLst.GetItemData(index)]
        print song.fp
        print 'playing {}'.format(song)
        self.media_play(song.fp)
        
    #----------------------------------------------------------------------
    def onSongSelect(self, e):
        """print the song info"""
        
        pass
        #print 'Selected: {}!'.format(song)
        
        index = e.m_itemIndex
        song = self.rowData[self.sngLst.GetItemData(index)]
        #print song.fp
        
        
def main():
    
    ex = wx.App(redirect=False)  #redirect to wxStdOut 
    MediaPlayerApp(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()
