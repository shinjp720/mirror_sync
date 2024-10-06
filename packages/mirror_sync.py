from pathlib import Path
from packages.directory_obj import DirectoryObject
from shutil import copy2, move
from pprint import pprint

class MirrorSync:
    '''
    sync_sourceとsync_destinationを同期させる
    ファイル名のみで差分同期する
    '''
    def __init__(self, source: str|Path , destination: str|Path) -> None:
        self.src = DirectoryObject(source) # DirectoryObjectを合成
        self.dest = DirectoryObject(destination) # DirectoryObjectを合成


    def sync_exec(self, *, delete_ok=False):
        '''
        sourceとdestinationをシンクさせる
        delete_ok=Trueでsourceにないファイルを削除する
        '''
        self._make_dir()
        self._copy_file()
        if delete_ok == True:
            self._remove_items()
        self._move_file()


    def _make_dir(self):
        '''
        sourceのディレクトリをdestinationに作成する
        '''
        for dir in self.src.dirs:
            p = self._substitute(dir)
            if not p.exists(): # destinationにdirが存在しない場合
                p.mkdir(parents=True, exist_ok=True) # dirを作成
                print(f'[created] {str(p)}')


    def _copy_file(self):
        '''
        fileのコピー
        '''
        destination_files = set(file.stem for file in self.dest.files)
        for p in self.src.files:
            if p.stem in destination_files:
                continue
            else:
                copy2(p, self._substitute(p))
                print(f'[copied] {str(p)}')


    def _move_file(self):
        '''
        fileの移動
        '''
        self.src = DirectoryObject(self.src.base) # DirectoryObjectを再生成
        self.dest = DirectoryObject(self.dest.base) # DirectoryObjectを再生成

        src_files = set(self._substitute(file) for file in self.src.files)
        dest_files = set(self.dest.files)

        diff1 = src_files - dest_files
        diff2 = dest_files - src_files

        for d1 in diff1:
            for d2 in diff2:
                if d1.stem == d2.stem:
                    move(d2, d1)
                    print(f'[moved] {str(d1)}')
            

    def _remove_items(self):
        '''
        fileとdirの削除
        '''
        # fileの削除
        source_files_stem = set(file.stem for file in self.src.files)
        files_to_delete = []
        for p in self.dest.files:
            if p.stem not in source_files_stem:
                files_to_delete.append(p)
        for p in files_to_delete:
                p.unlink()
                self.dest.files.remove(p)
                print(f'[deleted] {str(p)}')
        
        # dirの削除
        source_dirs = set(self._substitute(dir) for dir in self.src.dirs)
        for p in self.dest.dirs:
            if p not in source_dirs:
                p.rmdir()
                self.dest.dirs.remove(p)
                print(f'[deleted] {str(p)}')


    def _substitute(self, source_dir: Path) -> Path:
        '''
        渡したsourceのbase部分をdestinationのbaseに書き換えて返す
        '''
        return Path(str(source_dir).replace(str(self.src.base)+'/',
                                       str(self.dest.base)+'/'))