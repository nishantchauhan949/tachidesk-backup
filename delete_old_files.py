# importing the required modules
import os
from shutil import rmtree
from sys import argv
from time import time

from tachidesk_logger import get_logger

logger = get_logger()


# main function
def main_function(path, extension, days):
    try:
        # initializing the count
        deleted_folders_count = 0
        deleted_files_count = 0

        days = float(days)

        # converting days to seconds
        # time() returns current time in seconds
        seconds = time() - (days * 24 * 60 * 60)

        # checking whether the file is present in path or not
        if os.path.exists(path):
            is_file = True

            # iterating over each and every folder and file in the path
            for root_folder, folders, files in os.walk(path):
                # checking folder from the root_folder
                for folder in folders:

                    # folder path
                    folder_path = os.path.join(root_folder, folder)

                    # comparing with the days
                    if seconds >= get_file_or_folder_age(folder_path):
                        # invoking the remove_folder function
                        remove_folder(folder_path)
                        deleted_folders_count += 1  # incrementing count

                # checking the current directory files
                for file in files:

                    # file path
                    file_path = os.path.join(root_folder, file)

                    # extracting the extension from the filename
                    file_extension = os.path.splitext(file_path)[1]

                    # checking the file_extension
                    if extension == file_extension:
                        # comparing the days
                        if seconds >= get_file_or_folder_age(file_path):
                            # invoking the remove_file function
                            remove_file(file_path)
                            deleted_files_count += 1  # incrementing count

                is_file = False

            if is_file:
                # if the path is not a directory
                # comparing with the days
                if seconds >= get_file_or_folder_age(path):
                    # invoking the file
                    remove_file(path)
                    deleted_files_count += 1  # incrementing count

        else:

            # file/folder is not found
            logger.info(f'delete_old_file.main() :: "{path}" is not found')
            deleted_files_count += 1  # incrementing count

        logger.info(f"delete_old_file.main() :: Total folders deleted: {deleted_folders_count}")
        logger.info(f"delete_old_file.main() :: Total files deleted: {deleted_files_count}")

    except Exception as e:
        logger.error(f'delete_old_file.main() :: Some unexpected error occurred :: {e}')


def remove_folder(path):
    try:
        # removing the folder
        if not rmtree(path):

            # success message
            logger.info(f"delete_old_file.remove_folder() :: {path} is removed successfully")

        else:

            # failure message
            logger.info(f"delete_old_file.remove_folder() :: Unable to delete the {path}")
    except Exception as e:
        logger.error(f'delete_old_file.remove_folder() :: Some unexpected error occurred :: {e}')


def remove_file(path):
    try:
        # removing the file
        if not os.remove(path):

            # success message
            logger.info(f"delete_old_file.remove_file() :: {path} is removed successfully")

        else:

            # failure message
            logger.info(f"delete_old_file.remove_file() :: Unable to delete the {path}")
    except Exception as e:
        logger.error(f'delete_old_file.remove_file() :: Some unexpected error occurred :: {e}')


def get_file_or_folder_age(path):
    try:
        # getting ctime of the file/folder
        # time will be in seconds
        ctime = os.stat(path).st_ctime

        # returning the time
        return ctime
    except Exception as e:
        logger.error(f'delete_old_file.get_file_or_folder_age() :: Some unexpected error occurred :: {e}')


if __name__ == '__main__':
    main_function(path=argv[1], extension=argv[2], days=argv[3])
