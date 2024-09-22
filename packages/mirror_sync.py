from pathlib import Path
from packages.directory_obj import DirectoryObject
from shutil import copy2


class MirrorSync:
    '''
    sync_sourceとsync_destinationを同期させる
    ファイル名のみで差分同期する
    '''
    def __init__(self, source: str|Path , destination: str|Path) -> None:
        self.source = DirectoryObject(source) # DirectoryObjectを合成
        self.destination = DirectoryObject(destination) # DirectoryObjectを合成


    def sync_exec(self, *, delete_ok=False):
        '''
        sourceとdestinationをシンクさせる
        delete_ok=Trueでsourceにないファイルを削除する
        '''
        self._make_dir()
        self._copy_file()
        if delete_ok == True:
            self._remove_items()


    def _make_dir(self):
        '''
        sourceのディレクトリをdestinationに作成する
        '''
        for dir in self.source.dirs:
            p = self._dir_sub(dir)
            if not p.exists(): # destinationにdirが存在しない場合
                p.mkdir(parents=True, exist_ok=True) # dirを作成
                print(f'[created] {str(p)}')


    def _copy_file(self):
        '''
        fileのコピー
        '''
        destination_files = set(file.stem for file in self.destination.files)
        for p in self.source.files:
            if p.stem in destination_files:
                continue
            else:
                copy2(p, self._dir_sub(p))
                print(f'[copied] {str(p)}')


    def _remove_items(self):
        '''
        fileとdirの削除
        '''
        # fileの削除
        source_files_stem = set(file.stem for file in self.source.files)
        for p in self.destination.files:
            if p.stem not in source_files_stem:
                p.unlink()
                self.destination.files.remove(p)
                print(f'[deleted] {str(p)}')
        
        # dirの削除
        source_dirs = set(self._dir_sub(dir) for dir in self.source.dirs)
        for p in self.destination.dirs:
            if p not in source_dirs:
                p.rmdir()
                self.destination.dirs.remove(p)
                print(f'[deleted] {str(p)}')


    def _dir_sub(self, source_dir: Path) -> Path:
        '''
        渡したsourceのbase部分をdestinationのbaseに書き換えて返す
        '''
        return Path(str(source_dir).replace(str(self.source.base_dir)+'/',
                                       str(self.destination.base_dir)+'/'))