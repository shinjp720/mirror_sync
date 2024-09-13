from pathlib import Path


class DirectoryObject:
    '''
    ディレクトリの構造を持つ
    '''
    def __init__(self, base_dir: Path|str) -> None:
        if isinstance(base_dir, str):
            base_dir = Path(base_dir)
        if not base_dir.is_dir():
            raise ValueError(f'{base_dir} Is Not Directory.')

        self.base_dir = base_dir
        self.dirs = []
        self.files = []

        for p in base_dir.rglob('*'):
            if p.is_dir():
                self.dirs.append(p)
            elif p.is_file():
                self.files.append(p)


        