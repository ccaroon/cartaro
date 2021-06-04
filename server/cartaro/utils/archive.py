import arrow
import os
import shutil

class Archive:
    def __init__(self, path):
        if not os.path.isdir(path):
            raise ValueError("Path must be a directory and must exist.")

        self.path = path

    def add(self, src):
        """Add a new file or directory to the Archive"""
        if os.path.isdir(src):
            self._add_dir(src)
        elif os.path.isfile(src):
            self._add_file(src)
        else:
            raise ValueError("Unsupported Src Type or Invalid Path")

    def __build_dst_path(self, src):
        ds = arrow.get().to('local').format("YYYYMMDD_HHmm")
        src_file = os.path.basename(src)
        parts = os.path.splitext(src_file)
        dest = F"{self.path}/{parts[0]}-{ds}"

        # Add ext
        if parts[1]:
            dest += F"{parts[1]}"

        return dest

    def _add_dir(self, src):
        dst = self.__build_dst_path(src)
        shutil.make_archive(dst, 'zip', src)

    def _add_file(self, src):
        dst = self.__build_dst_path(src)
        shutil.copyfile(src, dst)

    def files(self):
        return os.listdir(self.path)

    def remove(self, filename):
        os.remove(os.path.join(self.path, filename))

    def remove_all(self):
        for file in self.files():
            self.remove(file)

    def clean(self, **kwargs):
        """Clean up the Archive"""
        older_than = kwargs.get('older_than', 7)
        cut_off_date = arrow.get().to('local').shift(days=older_than*-1)

        for file in self.files():
            mtime = os.path.getmtime(os.path.join(self.path, file))
            file_date = arrow.get(mtime)
            if file_date < cut_off_date:
                self.remove(file)
