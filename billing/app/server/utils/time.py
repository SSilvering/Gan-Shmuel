import os
import glob
import datetime


class TimeUtils:
    @staticmethod
    def get_now():
        return datetime.datetime.now()

    @staticmethod
    def set_file_last_modified(file_path, dt):
        dt_epoch = dt.timestamp()
        os.utime(file_path, (dt_epoch, dt_epoch))

    @staticmethod
    def get_latest_file_in_dir(dir, ext):
        list_of_files = glob.glob(dir + '/*' + ext)  # get all *.ext files in the specified dir
        return max(list_of_files, key=os.path.getctime)
