from pathlib import Path
from packages.directory_obj import DirectoryObject


class MirrorSync:
    '''
    sync_sourceとsync_destinationを同期させる
    '''
    def __init__(self, sync_source:str|Path , sync_destination: str|Path) -> None:
        self.sync_source = DirectoryObject(sync_source) # DirectoryObjectを合成
        self.sync_destination = DirectoryObject(sync_destination) # DirectoryObjectを合成

    def sync_exec(self):
        '''
        sync_sourceとsync_destinationをシンクさせる
        '''


    def create_fo(self):
        '''
        sourceとdestinationからFileObjectを生成
        '''