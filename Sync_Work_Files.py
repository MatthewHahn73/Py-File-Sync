import filecmp
import argparse
import os.path
from dirsync import sync

class Sync():
    Host_Dir = ''
    Dest_Dir = ''

    def __init__(self, Args):
        self.Host_Dir = Args.hostdir
        self.Dest_Dir = Args.destdir

    def Require_Syncing(self, Host, Dest):
        dirs_cmp = filecmp.dircmp(Host, Dest)
        if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0 or len(dirs_cmp.funny_files) > 0:
            return True
        (_, mismatch, errors) =  filecmp.cmpfiles(Host
                                , Dest
                                , dirs_cmp.common_files
                                , shallow = False)
        if len(mismatch) > 0 or len(errors) > 0:
            return True
        for common_dir in dirs_cmp.common_dirs:
            new_dir1 = os.path.join(Host, common_dir)
            new_dir2 = os.path.join(Dest, common_dir)
            if not self.Require_Syncing(new_dir1, new_dir2):
                return False
        return False
    
    def Sync_Files(self): 
        try:
            (sync(self.Host_Dir, self.Dest_Dir, 'sync') 
            if self.Require_Syncing(self.Host_Dir, self.Dest_Dir) 
            else print('No action required\n'))
        except FileNotFoundError as e:
            print(e)
            
if __name__ == '__main__':
    P = argparse.ArgumentParser(description='File Sync v0.1')
    P.add_argument('-syncall', help='<Required> Syncs all files in given host directory', required=True, action='store_true')
    P.add_argument('-hostdir', help='<Required> Path to host directory', required=True)
    P.add_argument('-destdir', help='<Required> Path to destination directory', required=True)

    Sync_Object = Sync(P.parse_args())
    Sync_Object.Sync_Files()