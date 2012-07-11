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
    
if __name__ == '__main__':
    

    """Run the following if module is top module"""
    #createTable('TableName', {'FIRSTVAR': 'INT', 'SECONDVAR': 'TEXT'})
    #deleteTable('TableName')
    
    conn = buildMusicDatabaseV1('first.db')