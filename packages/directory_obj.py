from pathlib import Path


class DirectoryObject:
    '''
    ディレクトリの構造を持つ
    '''
    def __init__(self, base_dir: Path|str) -> None:
        self.base = base_dir
        self.dirs = []
        self.files = []

        if isinstance(self.base, str):
            self.base = Path(self.base)
        if not self.base.is_dir():
            raise ValueError(f'{self.base}')

        for p in self.base.rglob('*'):
            if p.is_dir():
                self.dirs.append(p)
            elif p.is_file():
                self.files.append(p)


        