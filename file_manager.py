import datetime
from pathlib import Path
from shutil import copyfile



class DeleteUnpairs():
    '''
    Deletes all files of dst_dir with specific extension that names don't equal to file names in src_dir.
    '''
    def __init__(self, src_dir, dst_dir, src_extension, dst_extension):
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        
        self.src_extension = src_extension
        self.dst_extension = dst_extension
        
        self.src_file_names = self.get_file_names(src_dir, src_extension)
        self.dst_file_names = self.get_file_names(dst_dir, dst_extension)
        
        
    def get_file_names(self, dir_path, extension):
        file_names = set()
        for file in dir_path.glob('*'):
            file_name = file.name.split('.')
            if file_name[-1] == extension:
                file_names.add('.'.join(file_name[:-1]))
                
        return file_names
    
    
    def delete(self):
        for file_name in self.get_delete_candidates_():
            file_path = self.get_path_(file_name, self.dst_dir, self.dst_extension)
            try:
                file_path.unlink()
                self.dst_file_names.remove(file_name)
            except FileNotFoundError as error:
                print(f'Error: file "{file_path}" does not found')
            finally:
                continue

    
    def get_path_(self, file_name, root_dir, extension):
        return root_dir / (file_name + '.' + extension)
    

    # def get_delete_candidates_(self):
    #     '''
    #     Doesnot work when src and dst is the same.
    #     '''
    #     for file_name in self.dst_file_names:
    #         if file_name not in self.src_file_names:
    #             yield file_name

    
    def get_delete_candidates_(self):
        candidates = []
        for file_name in self.dst_file_names:
            if file_name not in self.src_file_names:
                candidates.append(file_name)
        return candidates
                
                
    def random_copy(self, annot_dir, image_dir, ratio=0.2):
        file_names = list(self.src_file_names)
        
        count = math.ceil(ratio * len(file_names))
        indexes = np.random.permutation(len(file_names))
        indexes = indexes[:count]
        for i in indexes:
            annot_file_path = self.get_path_(file_names[i], self.src_dir, self.src_extension)
            img_file_path = self.get_path_(file_names[i], self.dst_dir, self.dst_extension)
            
            copyfile(annot_file_path, annot_dir / annot_file_path.name)
            copyfile(img_file_path, image_dir / img_file_path.name)
