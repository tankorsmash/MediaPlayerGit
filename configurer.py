import ConfigParser 
import string

#set decoding vals
UTF16_LE_BOM = "\xff\xfe"
UTF16_BE_BOM = "\xfe\xff"


if __name__ == '__main__':
    """Run the following if module is top module"""
    
    cfg = ConfigParser.ConfigParser()
    print cfg.read(r'mediaplayer.cfg')
    print cfg.get('library', 'top')
    #cfg.add_section('test1')
    #cfg.write(open(r'mediaplayer.cfg', 'w'))
    
    
    print 'done'