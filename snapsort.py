#!/usr/bin/env python

"""
@date: February 21, 2016
@author: Dominic Philip
"""

import os
import psutil
import shutil
import logging
import time
import calendar
import exifread
import bcolors as bc


class SnapSort:

    def __init__(self, directory, destination):
        if os.path.exists(os.path.expanduser(directory.strip())):
            self.__directory = os.path.expanduser(directory.strip())
        else:
            raise ValueError("Directory is not a valid location")
        if os.path.exists(os.path.expanduser(destination.strip())):
            self.__destination = os.path.expanduser(destination.strip())
        else:
            raise ValueError("Destination is not a valid location")

    def num_of_images(self):
        return len(self.__find_images())

    def total_size(self):
        size = 0
        for path in self.__find_images():
            size += os.path.getsize(path)
        return size * 0.001

    def sort(self):
        self.__check_space()
        for path in self.__find_images():
            try:
                tags = exifread.process_file(open(path, 'rb'))
                date = str(tags['EXIF DateTimeOriginal'])
                base, extension = os.path.splitext(os.path.basename(path))
                core = self.__destination + "/" + str(date[0:4]) + "/" + str(calendar.month_name[int(date[5:7])])
                end = core + "/" + base + extension
                self.__is_zero(date)
                if os.path.exists(self.__destination + "/" + str(date[0:4])):
                    if os.path.exists(core):
                        if os.path.exists(os.path.join(core + "/" + base + extension)):
                            self.__rename(path, core + "/" + base, extension)
                        else:
                            print(bc.BColors.OKGREEN + "Copying path '" + path + "' to '" + end + "'" + bc.BColors.ENDC)
                            shutil.copy(path, os.path.join(end))
                    else:
                        print(bc.BColors.OKBLUE + "Making path '" + core + "'" + bc.BColors.ENDC)
                        os.makedirs(core)
                        print(bc.BColors.OKGREEN + "Copying path '" + path + "' to '" + end + "' " + bc.BColors.ENDC)
                        shutil.copy(path, os.path.join(end))
                else:
                    print(bc.BColors.OKBLUE + "Making path '" + core + "'" + bc.BColors.ENDC)
                    os.makedirs(core)
                    print(bc.BColors.OKGREEN + "Copying path '" + path + "' to '" + end + "' " + bc.BColors.ENDC)
                    shutil.copy(path, os.path.join(end))
            except (KeyError, OSError, DateError):
                print(bc.BColors.FAIL + "Picture '" + path + "' cannot be moved and will be logged." + bc.BColors.ENDC)
                self.__log(path)
                pass

    @staticmethod
    def __rename(old_path, new_path, extension):
        count = 1
        while True:
            rename = os.path.join(new_path + "_" + str(count) + extension)
            if not os.path.exists(rename):
                print(bc.BColors.OKBLUE + "Renaming '" + old_path + "' to '" + rename + "'" + bc.BColors.ENDC)
                print(bc.BColors.OKGREEN + "Copying '" + old_path + "' to '" + rename + "'" + bc.BColors.ENDC)
                shutil.copy(old_path, rename)
                break
            count += 1

    @staticmethod
    def __is_zero(date):
        date = date.replace(':', '').replace(' ', '').strip()
        if date == len(date) * date[0]:
            raise DateError('Date is corrupt, will be logged.')

    def __check_space(self):
        if self.total_size() > psutil.disk_usage(self.__destination).free:
            raise Exception("Destination folder does not have enough space!")

    def __find_images(self):
        extensions = '.jpg', '.jpeg', '.JPG', '.JPEG', '.Jpg', 'TIFF', 'tiff'
        image_list = []
        for (dir_path, dir_names, file_names) in os.walk(self.__directory):
            image_file_names = [image for image in file_names if image.endswith(extensions)]
            for name in image_file_names:
                image_list.append(dir_path + "/" + name)
        return image_list

    def __log(self, path):
        logging.basicConfig()
        text_path = os.path.join(self.__destination, "ImagesNotProcessed.txt")
        log = open(text_path, 'a')
        if str(time.strftime("%d/%m/%Y")) not in open(text_path, 'r').read():
            open(text_path, 'a').write(str(time.strftime("%d/%m/%Y")) + "\n")
        log.write(str(time.strftime("%I:%M:%S")) + "\n")
        log.write(path + "\n")
        log.close()


class DateError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
