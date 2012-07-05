import wx
import wx.media


class Example(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(id=wx.ID_ANY, *args, **kwargs) 
            
        self.song_path = r'C:\Programming\Python\Project\MusicPlayer\10.mp3'
            
        self.InitUI()
        #self.initButtons()
        
    def InitUI(self):    
        
        #create labels for music picking
        self.lbl_cursong = wx.StaticText(self, label='Current Song:')
        try:
            lbl = self.song_path
        except AttributeError as e:
            lbl = '--SONG NOT SET--'
        self.lbl_setsong = wx.StaticText(self, label=lbl)
        self.lbl_setsong.SetBackgroundColour((100, 90, 70))
        self.btn_chooseSong = wx.Button(self, label='Choose Song to play')
        self.Bind(wx.EVT_BUTTON, self.onClick, self.btn_chooseSong)
        
        #sizers 
        self.siz_songInfo = wx.BoxSizer(wx.HORIZONTAL)
        self.siz_songInfo.AddMany([self.lbl_cursong, self.lbl_setsong])
        
        self.siz_songChoose = wx.BoxSizer(wx.HORIZONTAL)
        self.siz_songChoose.Add(self.btn_chooseSong)
        
        #main sizers for this section
        self.sizer_main = wx.BoxSizer(wx.VERTICAL)
        self.sizer_main.AddMany([self.siz_songInfo, self.siz_songChoose])
        
        self.SetSizer(self.sizer_main)
        
        #music player change the back end to WMP10, and catch the event for playback
        self.mediaPlayer = wx.media.MediaCtrl(self,  
                                        szBackend=wx.media.MEDIABACKEND_WMP10, )
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.lay)
        self.sizer_main.Add(self.mediaPlayer)
        
        #play button
        self.btn_play = wx.Button(self, label='Play Song')
        self.sizer_main.Add(self.btn_play)
        self.Bind(wx.EVT_BUTTON,
                  lambda e: self.play2(self.song_path, e),
                  self.btn_play)
        
        #pause button
        self.btn_pause = wx.Button(self, label='Pause')
        self.Bind(wx.EVT_BUTTON, self.pause2, self.btn_pause)
        self.sizer_main.Add(self.btn_pause)
        
        #progress slider
        self.sldr_prog = wx.Slider(self)
        self.Bind(wx.EVT_SLIDER, self.SetProg, self.sldr_prog)
        self.sizer_main.Add(self.sldr_prog)
        
        #volume slider
        self.sldr_vol = wx.Slider(self, style=wx.VERTICAL | wx.SL_INVERSE)
        self.Bind(wx.EVT_SLIDER, self.SetVol, self.sldr_vol)
        self.sizer_main.Add(self.sldr_vol)
        
        #self.sizer_main.Layout()
        self.Show()
        
        
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
        
    def lay(self, e):
        print 'caught EVT_MEDIA_LOADED'
        self.mediaPlayer.Play()
        
        #progress slider
        maxLen = self.mediaPlayer.Length()
        print 'maxlen', maxLen
        self.sldr_prog.SetRange(0, maxLen)        
        
        #volume slider
        self.sldr_vol.SetRange(0, 100)        
        
    #----------------------------------------------------------------------
    def onClick(self, e):
        """"""
        print 'Gotcha bitch'
        dlg = wx.FileDialog(self, )
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            
            print 'path chosen:', path
            
            self.lbl_setsong.SetLabel(path)
            self.Layout()
        
            self.song_path = path
        
    def play2(self, path, event):
        
        print 'load:', self.mediaPlayer.Load(path), path
        #import time
        #time.sleep(1)
        self.mediaPlayer.SetInitialSize()
        
        
        
        #self.mediaPlayer.g
        
        #print 'play:', self.mediaPlayer.Play()
        self.mediaPlayer.SetVolume(1)
        self.mediaPlayer.SetPlaybackRate(1)
        print 'music playing'
        
        #event.Skip()
        
    def pause2(self, event):
        
        if not self.mediaPlayer.GetState() == 1:
            
            self.mediaPlayer.Pause()
        else:
            self.mediaPlayer.Play()

def main():
    
    ex = wx.App(redirect=False)  #redirect to wxStdOut 
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()
