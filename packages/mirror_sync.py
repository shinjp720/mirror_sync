from pathlib import Path
from packages.directory_obj import DirectoryObject
from shutil import copy2, move


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
        delete_ok=Trueで、dest内のsrcに無いファイルと重複を削除する
        この順番で実行しないと予期しない挙動となる恐れがあります
        '''
        if delete_ok == True:
            self._delete_duplicate()
        self._make_dir()
        self._copy_file()
        if delete_ok == True:
            self._remove_items()
        self._move_files()


    def _delete_duplicate(self):
        '''
        dest内に重複があれば削除する
        '''

    def _make_dir(self):
        '''
        destに無いディレクトリを作成する
        '''
        for dir in self.src.dirs:
            p = self.__substitute(dir)
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
                copy2(p, self.__substitute(p))
                print(f'[copied] {str(p)}')
            

    def _remove_items(self):
        '''
        srcに無いfileとdirの削除
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
        source_dirs = set(self.__substitute(dir) for dir in self.src.dirs)
        for p in self.dest.dirs:
            if p not in source_dirs:
                p.rmdir()
                self.dest.dirs.remove(p)
                print(f'[deleted] {str(p)}')


    def _move_files(self):
        '''
        ファイルを移動する
        '''
        self.src = DirectoryObject(self.src.base) # DirectoryObjectを再生成
        self.dest = DirectoryObject(self.dest.base) # DirectoryObjectを再生成

        files_to_move = [] # moveへの引数として(src, dest)で格納

        for src in self.src.files:
            for dest in self.dest.files:
                sub = self.__substitute(src)
                if (src.stem == dest.stem) and (sub != dest):
                    files_to_move.append((dest, sub))

        for arg in files_to_move:
            move(*arg)
            print(f'[moved] {arg[1]}')


    def __substitute(self, source_dir: Path) -> Path:
        '''
        渡したsourceのbase部分をdestinationのbaseに書き換えて返す
        '''
        return Path(str(source_dir).replace(str(self.src.base)+'/',
                                       str(self.dest.base)+'/'))