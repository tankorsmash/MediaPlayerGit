import wx
import wx.media
from pprint import pprint as pp2
import datetime




from MediaPlayerBrowserStartSupportv2 import ID3
from MediaPlayerLibrary import findMP3s


class MediaPlayerApp(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(MediaPlayerApp, self).__init__(id=wx.ID_ANY, *args, **kwargs) 
            
        #self.song_path = r'e:\music'
        self.song_path = r'C:\Programming\Python\Project\MusicPlayer\10.mp3'
            
        self.sizer_main = wx.GridBagSizer()
        self.sizer_main.SetRows(3)
        self.SetSizer(self.sizer_main)
            
            
        #sets the frame's favico
        self.setFavicon()
            
        #sets up the main screen
        self.initPlayer()
        self.initSongList()
        self.initSongInfoPane()
        
        #self.setSizerMainColors()
        
        self.Layout()
        #self.Show()
        self.Fit()
        
        #self.Bind(wx., lambda e:self.snglst_panel.Layout)
        
        
    #----------------------------------------------------------------------
    def initSongInfoPane(self):
        """fills the song info grid with title, band, album,
        length, size etc"""
        
        self.info_pnl = wx.Panel(self)
        self.info_szr = wx.BoxSizer()
        
        self.info_trk = wx.TextCtrl(self.info_pnl, value='Track Name')
        self.info_szr.Add(self.info_trk)
        
        self.info_alb = wx.TextCtrl(self.info_pnl, value='Album Name')
        self.info_szr.Add(self.info_alb)
        
        self.info_bnd = wx.TextCtrl(self.info_pnl, value='Artist Name')
        self.info_szr.Add(self.info_bnd)
        
        self.info_pnl.SetSizer(self.info_szr)
        
        self.info_szr.Layout()
        
        self.sizer_main.Add(self.info_pnl, (1, 1),
                            flag=wx.EXPAND)
        
        self.sizer_main.Layout()
        self.Fit()
        
        self.info_pnl.Show()


        
    #----------------------------------------------------------------------
    def setFavicon(self, path=None):
        '''Sets the favicon for the app'''
        
        if not path:
            name = r'.\favicon1.ico'
            type = wx.BITMAP_TYPE_ICO
            favicon = wx.Icon(name, type, )  # 16, 16)
            self.SetIcon(favicon)
            
        
    #----------------------------------------------------------------------
    def setSizerMainColors(self):
        """sets colors of the grids so I can debug a bit easier
        row/column"""
        
        
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.RED)
        panel.Show()
        self.sizer_main.Add(panel, (1, 1), flag=wx.EXPAND)
        
        
        panel = wx.Panel(self)
        #panel.SetBackgroundColour(wx.BLUE)
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
        #self.player_panel.SetBackgroundColour(wx.BLUE)
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
        self.btn_chooseSong.SetBackgroundColour(wx.GREEN)
        self.Bind(wx.EVT_BUTTON, self.media_path, self.btn_chooseSong)
        
        #sizers 
        self.siz_songInfo = wx.BoxSizer(wx.HORIZONTAL)
        self.siz_songInfo.AddMany([self.lbl_cursong, self.lbl_setsong])
        
        self.siz_songChoose = wx.BoxSizer(wx.HORIZONTAL)
        #self.siz_songChoose.Add(self.btn_chooseSong)
        
        #main sizers for this section
        self.player_sizer.AddMany([self.siz_songInfo, self.siz_songChoose])
        
        self.btn_sizer = wx.GridBagSizer()
        self.btn_sizer.Add(self.btn_chooseSong, (0, 1))
        
        self.player_sizer.Add(self.btn_sizer)
        #music player change the back end to WMP10, and catch the event for playback
        self.mediaPlayer = wx.media.MediaCtrl(self.player_panel,  
                                        szBackend=wx.media.MEDIABACKEND_WMP10, )
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.media_loaded)
        self.btn_sizer.Add(self.mediaPlayer, (0, 0))
        self.mediaPlayer.SetVolume(1)
        
        #play button
        self.btn_play = wx.Button(self.player_panel, label='Play Song')
        self.btn_play.SetBackgroundColour(wx.RED)
        self.btn_sizer.Add(self.btn_play, (1, 0))
        self.Bind(wx.EVT_BUTTON,
                  lambda e: self.media_play(self.song_path, e),
                  self.btn_play)
        
        #pause button
        self.btn_pause = wx.Button(self.player_panel, label='Pause')
        self.btn_pause.SetBackgroundColour(wx.RED)
        self.Bind(wx.EVT_BUTTON, self.media_pause, self.btn_pause)
        self.btn_sizer.Add(self.btn_pause, (1, 1))
        
        #progress slider
        self.sldr_prog = wx.Slider(self.player_panel)
        self.Bind(wx.EVT_SLIDER, self.SetProg, self.sldr_prog)
        self.sldr_prog.SetMinSize((200, -1))
        self.btn_sizer.Add(self.sldr_prog, (3, 0), span=(3, 3))
        
        #volume slider
        self.sldr_vol = wx.Slider(self.player_panel, style=wx.VERTICAL | wx.SL_INVERSE)
        self.sldr_vol.SetMin(0)
        self.sldr_vol.SetMax(100)
        volume = self.mediaPlayer.GetVolume()
        self.sldr_vol.SetValue(1000)
        self.Bind(wx.EVT_SLIDER, self.SetVol, self.sldr_vol)
        self.btn_sizer.Add(self.sldr_vol, (2, 0))
        
        self.sizer_main.Add(self.player_panel, (0, 1),
                            flag=wx.EXPAND)
        
        self.btn_sizer.Layout()
        self.player_sizer.Layout()
        self.player_panel.Fit()
        self.Show()
        self.Layout()
        
        #slider updater
        print 'timer created'
        #self.player_timer = NewTimer(owner=self)
        self.player_timer = wx.Timer(owner=self)
        print 'timer set ?:', self.player_timer.Start(1000)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        print 'timer done binded'
        
    #----------------------------------------------------------------------
    def onTimer(self, e):
        """Gets called when the player_timer goes off every second, in order
        to move the progress slider"""
        
        #start, end value of the song
        #print 'min', self.sldr_prog.GetMin(), 
        #print 'max', self.sldr_prog.GetMax(),
        #print 'len', self.mediaPlayer.Length()
        
        #current value of the song's progress
        current = self.mediaPlayer.Tell()
        #print 'current', current
        self.sldr_prog.SetValue(current)
        
        #current volue
        volume = self.mediaPlayer.GetVolume()
        self.SetVol(100)
        
        #resize progress slider
        xsize = self.player_panel.Size[0]
        ysize = -1
        self.sldr_prog.SetSize((xsize, ysize))
    #----------------------------------------------------------------------
    def SetVol(self, e):
        """sets the volume of the song, in percentage of 100"""
        
        vol = self.sldr_vol.GetValue()
        #print 'cur vol val:', vol
        #print 'volume to be set:', vol
        vol /= 100.0
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
        
        #set column widths manually
        self.sngLst.SetColumnWidth(0, 150)
        self.sngLst.SetColumnWidth(1, 150)
        self.sngLst.SetColumnWidth(2, 150)
 
        #set col widths automatically
        #self.sngLst.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        #self.sngLst.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        #self.sngLst.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
        
        #create the sizer for the song list
        self.snglst_sizer.Add(self.sngLst)
        self.snglst_sizer.Layout()
        self.snglst_panel.Show()
        
        #add the songist to the main sizer
        self.sizer_main.Add(self.snglst_panel, (0, 0),
                             #span=wx.GBSpan(3, 1),
                             flag=wx.EXPAND)
        
        
        #make a list of songs
        #list_of_songs = ['C:\\Programming\\Python\\Project\\MusicPlayer\\10.mp3',
                         #'C:\\Programming\\Python\\Project\\MusicPlayer\\1.mp3']
        #list_of_songs = findMP3s(r'./songs')
        list_of_songs = findMP3s(r"E:\Music\as i lay dying")
        
        self.rowData = {}
        for i, song in enumerate(list_of_songs):
            
            songTag = ID3(song)
        
            try:
                title = songTag.tags['TIT2']['data']['cont']
                album = songTag.tags['TALB']['data']['cont']
                band = songTag.tags['TPE1']['data']['cont']
            except (KeyError, TypeError):
                print 'No title, album and/or band found'
                title, album, band = 'ERROR', 'ERROR', 'ERROR'
            
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
        
        index = e.m_itemIndex
        song = self.rowData[self.sngLst.GetItemData(index)]
        
        try:
                
            self.info_trk.SetValue(song.title)
            self.info_alb.SetValue(song.album)
            self.info_bnd.SetValue(song.band)
        except AttributeError:
            pass
        
########################################################################
class NewTimer(wx.Timer):
    """override wx.timer"""

    #----------------------------------------------------------------------
    def __init__(self, owner, *args, **kwargs):
        """Constructor"""
        super(wx.Timer, self).__init__(owner=owner, *args, **kwargs)
        
        self.Start(1000)
        
        print self.IsRunning()
    #----------------------------------------------------------------------
    def Notify(self):
        """updates slider progress"""
        
        print 'caught notify'
    
    

        
def main():
    
    ex = wx.App(redirect=False)  #redirect to wxStdOut 
    MediaPlayerApp(None, title='TEST')
    ex.MainLoop()    


if __name__ == '__main__':
    main()
