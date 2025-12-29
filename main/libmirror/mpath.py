__API_VERSION = 1

from os import path
from sys import argv

# ------------------------ Get Path --------------------------


# # ------------------------ Process Path --------------------------


# def get_filename_from_abspath(abs_path: str) -> str:
#     return os.path.basename(abs_path)


# def resolve_relative_path(path: str) -> str:
#     # 简化路径：它会去掉路径中的多余部分，如重复的斜杠（//），或者路径中的 . 和 ..（当前目录和父目录）。
#     # 标准化路径分隔符：它会根据操作系统的规范将路径中的分隔符转换为合适的格式，例如 Windows 上的反斜杠（\）和 Unix 系统上的正斜杠（/）
#     return os.path.normpath(path)


def get_parent_path(file_path_all: str) -> str:
    # C:\Users\Documents\file.txt --> C:\Users\Documents
    # C:\Users\Documents\ -->  C:\Users
    # Users\Documents\file.txt --> Users\Documents
    # Split the path into drive and path components
    drive, path_without_drive = path.splitdrive(file_path_all)
    # Get the directory path
    directory_path = path.dirname(path_without_drive)
    # Return the full path including the drive
    return path.join(drive, directory_path)


def get_entry_folder() -> str:
    return get_parent_path(path.abspath(argv[0]))


def join_file_path(*args: str) -> str:
    # 一定会得到结尾不为'/'的结果
    if "" == args[0]:
        return path.join(args[1:])
    joined_path = path.join(*args)
    return joined_path.replace("/", "\\")


def join_file_path_remote(*args: str) -> str:
    joined_path = join_file_path(*args)
    return joined_path.replace("\\", "/")


# TODO: 这些方法慢慢都debug后实现
# def is_file_exist(path_all_file: str) -> bool:
#     return path.exists(path_all_file)


# def create_folder_of_file_if_not_exist(file_path_all: str):
#     parent_folder = path.dirname(file_path_all)
#     if not parent_folder:
#         makedirs(parent_folder)


# def get_basename(file_path: str) -> str:
#     basename, _ = os.path.splitext(os.path.basename(file_path))
#     return basename


# def get_extension(file_path: str) -> str:
#     _, extension = os.path.splitext(file_path)
#     return extension


# def rollback_path(path, levels):
#     """
#     Roll back a specified path by a given number of levels.

#     :param path: The original file or directory path.
#     :param levels: Number of levels to roll back (default is 2).
#     :return: The rolled-back path.
#     """
#     if levels < 0:
#         raise ValueError("Levels must be a non-negative integer.")
#     for _ in range(levels):
#         path = os.path.dirname(path)
#     return path

# -------------------- Basename --------------------
# .auto
#   config
#   Github_ChinaUX
#   Gerrit_ChinaUX
#   Gerrit_ChinaUX_T6Y
BASENAME_AUTO = ".auto"
BASENAME_CONFIG = "config"
BASENAME_SOURCE_REPO = "Github_ChinaUX"
BASENAME_SUBMIT_REPO = "Gerrit_ChinaUX"
BASENAME_SUBMIT_REPO_T6Y = "Gerrit_ChinaUX_T6Y"
# #   log
# #   data
# BASENAME_LOG = "log"
# BASENAME_DATA = "data"

# --------------------- Remote Folder(Path) ---------------
from mconfig import get_host_remote

HOST_REMOTE = get_host_remote()
FOLDER_REMOTE_AUTO = join_file_path_remote(HOST_REMOTE, BASENAME_AUTO)
PATH_REMOTE_AUTO_LOG = FOLDER_REMOTE_AUTO + "log/"
PATH_REMOTE_AUTO_DATA = FOLDER_REMOTE_AUTO + "data/"
FOLDER_REMOTE_AUTO_CONFIG = join_file_path_remote(FOLDER_REMOTE_AUTO, BASENAME_CONFIG)
FOLDER_REMOTE_AUTO_SOURCE_REPO = join_file_path_remote(
    FOLDER_REMOTE_AUTO, BASENAME_SOURCE_REPO
)
FOLDER_REMOTE_AUTO_SUBMIT_REPO = join_file_path_remote(
    FOLDER_REMOTE_AUTO, BASENAME_SUBMIT_REPO
)
FOLDER_REMOTE_AUTO_SUBMIT_REPO_T6Y = join_file_path_remote(
    FOLDER_REMOTE_AUTO, BASENAME_SUBMIT_REPO_T6Y
)
