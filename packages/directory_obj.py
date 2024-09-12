from pathlib import Path


class DirectoryObject:
    '''
    ディレクトリの構造を持つ
    '''
    def __init__(self, parent_dir: Path|str) -> None:
        if isinstance(parent_dir, str):
            parent_dir = Path(parent_dir)
        if not p.is_dir():
            raise ValueError(f'{p} Is Not Directory.')

        self.dirs = []
        self.files = []

        for p in parent_dir.rglob('*'):
            if p.is_dir():
                self.dirs.append(p)
            elif p.is_file():
                self.files.append(p)


        
