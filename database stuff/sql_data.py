style = '''
*ID3tag table 
  * ID3Id int Primary Key
  * ID3Tag nvarchar(25) NOT NULL -- Might be able to get away with shorter.  Also, you can ditch the 'n' if you don't expect to have non-english characters
* Song table
  * SongId int Primary Key
  * SongName nvarchar(255) NOT NULL
  * FilePath nvarchar(255) NOT NULL  -- Might consider nulls if you want a wishlist type function
  * TimesPlayed int NOT NULL DEFAULT 0
* Album table
  * AlbumId int Primary Key
  * AlbumName nvarchar(255) NOT NULL
  * CoverArtPath nvarchar(255) NULL  -- Could also be a BLOB and store the image directly
* Artist table
  * ArtistId int Primary Key
  * ArtistName nvarchar(255) NOT NULL

And, of course, you need your linkage tables so:  

* SongId3Link
  * SongId int
  * ID3Id int
* SongAlbum
  * SongId
  * AlbumId
* SongArtist
  * SongId
  * ArtistId'''

from collections import OrderedDict as odict
import sqlite3 as sql

#----------------------------------------------------------------------
def createTable(conn, name, vars = {}):
    """create a new table, with the vars, as a columnname : datatype dict"""
    
    pairs = []
    for colname, datatype in vars.items():
        pairs.append('{} {}'.format(colname, datatype))
    values = ', '.join(pairs)
    
    cmd = r'CREATE TABLE {} ({})'.format(name, values)
    print 'The command sent', `cmd`
    
    curs = conn.cursor()
    try:
        curs.execute(cmd)
    except sql.OperationalError as e:
    #except IndexError:
        print e

#----------------------------------------------------------------------
def deleteTable(table):
    """Deletes table entirely"""
    
    curs = conn.cursor()
    
    cmd = r'DROP TABLE {}'.format(table)
    try:
        curs.execute(cmd)
        print table, 'deleted successfully'
    except sql.OperationalError as e:    
        print e
        
    

#----------------------------------------------------------------------
def buildMusicDatabaseV1(name):
    """builds the preset database named name"""
    print 'Starting to create new database:', name
    conn = sql.connect(name)
    
    #table name : vars(in a dict)
    tables = {'ID3tag': {'ID3id': 'int PRIMARY KEY',
                         'ID3tag': 'nvarchar(25) NOT NULL'},
              
              'Song': {'SONGid': 'int PRIMARY KEY',
                       'SONGname': 'nvarchar(255) NOT NULL', 
                       'FILEpath': 'nvarchar(255)NOT NULL', 
                       'PLAYcount': 'int NOT NULL DEFAULT 0',},
              
              'Album': {'ALBUMid': 'int PRIMARY KEY',
                        'ALBUMname': 'nvarchar(255) NOT NULL',
                        'ARTcover': 'BLOB', },
              
              'Artist': {'ARTISTid': 'int PRIMARY KEY',
                         'ARTISTname': 'nvarchar(255) NOT NULL', }
              }
    
    numTables = len(tables.keys())
    print '#-- creating {} tables --#'.format(numTables)
    for name, variables in tables.items():
        createTable(conn, name, variables,)
    print '#-- done creating {} tables --#'.format(numTables)
    
    return conn
    
#----------------------------------------------------------------------
def insertData(conn, table, data, ):
    """inserts data into the table on row"""
    
    cmd = r'INSERT into {tbl} VALUES ({data})'.format(tbl=table, data=data)
    print cmd
    
    cur = conn.cursor()
    res = cur.execute(cmd)
    
    print res
      
    print 'done'
    
    
#----------------------------------------------------------------------
def buildMusicDatabaseV2(name):
    """builds the preset database this time without ID3 tags, just
    taking straight data. Will use more complex data later because right now
    I just need to get my head around SQL"""
    print 'Starting to create new database:', name
    conn = sql.connect(name)
    
    #table name : vars(in a dict)
    tables = {'Song': {'SONGid': 'integer PRIMARY KEY ',
                       'SONGname': 'nvarchar(255) NOT NULL', 
                       'FILEpath': 'nvarchar(255)NOT NULL', 
                       'PLAYcount': 'int NOT NULL DEFAULT 0',},
              
              'Album': {'ALBUMid': 'integer PRIMARY KEY ',
                        'ALBUMname': 'nvarchar(255) NOT NULL',
                        'ARTISTid': 'int', 
                        'FOREIGN KEY': '(ARTISTid) REFERENCES Artist(ARTISTid)'},
              
              'Artist': {'ARTISTid': 'integer PRIMARY KEY ',
                         'ARTISTname': 'nvarchar(255) NOT NULL', }
              }
    
    numTables = len(tables.keys())
    print '#-- creating {} tables --#'.format(numTables)
    for name, variables in tables.items():
        createTable(conn, name, variables,)
    print '#-- done creating {} tables --#'.format(numTables)
    #----------------------------------------------------------------------
def buildMusicDatabaseV3(name):
    """builds the preset database this time without ID3 tags, just
    taking straight data. Will use more complex data later because right now
    I just need to get my head around SQL
    
    In this v3, I changed the INT to INTEGER, and will make it use ordered dicts"""
    print 'Starting to create new database:', name
    conn = sql.connect(name)
    
    #table name : vars(in a dict)
    tables = odict()
    {'Song': {'SONGid': 'integer PRIMARY KEY ',
                       'SONGname': 'nvarchar(255) NOT NULL', 
                       'FILEpath': 'nvarchar(255)NOT NULL', 
                       'PLAYcount': 'int NOT NULL DEFAULT 0',},
              
              'Album': {'ALBUMid': 'integer PRIMARY KEY ',
                        'ALBUMname': 'nvarchar(255) NOT NULL',
                        'ARTISTid': 'int', 
                        'FOREIGN KEY': '(ARTISTid) REFERENCES Artist(ARTISTid)'},
              
              'Artist': {'ARTISTid': 'integer PRIMARY KEY ',
                         'ARTISTname': 'nvarchar(255) NOT NULL', }
              }
    
    numTables = len(tables.keys())
    print '#-- creating {} tables --#'.format(numTables)
    for name, variables in tables.items():
        createTable(conn, name, variables,)
    print '#-- done creating {} tables --#'.format(numTables)
    

    return conn
if __name__ == '__main__':
    

    """Run the following if module is top module"""
    #createTable('TableName', {'FIRSTVAR': 'INT', 'SECONDVAR': 'TEXT'})
    #deleteTable('TableName')
    
    db = 'first4.db' 
    conn = buildMusicDatabaseV2(db)
    #conn = sql.connect(db)    
    #insertData(conn, 'Artist', '1121, "August Burns Red"')    
        
    conn.commit()
    conn.close()