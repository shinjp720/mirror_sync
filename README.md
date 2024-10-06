ファイル名のみで差分同期します
ms = MirrorSync(src, dest)で生成して
sync_exec()を実行します
sync_exec(delete_ok=True)でsrcにないファイルとディレクトリは削除されます
