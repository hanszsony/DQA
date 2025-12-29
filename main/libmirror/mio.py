__API_VERSION = 1

from mstr import ENCODE

from os import path, makedirs
from shutil import rmtree, copy, copytree
from json import load, dumps

from mlogger import LOGGER

# ----------------------------- File Read/Write -----------------------------


def write_data_to_file(file_all_path: str, data: str):
    """
    Write data to a file, overwriting existing content.

    :param file_all_path: Full path of the file to write.
    :param data: Data to write to the file.
    """
    LOGGER.debug(f"[write_data_to_file] Start writing data to {file_all_path}")
    try:
        file_parent_path = os.path.dirname(file_all_path)
        if file_parent_path and not os.path.exists(file_parent_path):
            os.makedirs(file_parent_path)
            LOGGER.info(f"Path created: {file_parent_path}")
        with open(file_all_path, "w", encoding=ENCODE) as file:
            file.write(str(data))
        LOGGER.debug(
            f"[write_data_to_file] Data written successfully to {file_all_path}"
        )
    except Exception as e:
        LOGGER.error(f"[write_data_to_file] Error: {e}")


def append_data_to_file(file_all_path: str, data: str):
    """
    Append data to a file without overwriting existing content.

    :param file_all_path: Full path of the file to append data to.
    :param data: Data to append to the file.
    """
    LOGGER.debug(f"[append_data_to_file] Start appending data to {file_all_path}")
    try:
        file_parent_path = os.path.dirname(file_all_path)
        if not os.path.exists(file_parent_path):
            os.makedirs(file_parent_path)
            LOGGER.info(f"Path created: {file_parent_path}")
        with open(file_all_path, "a", encoding=ENCODE) as file:
            file.write(str(data))
        LOGGER.debug(
            f"[append_data_to_file] Data appended successfully to {file_all_path}"
        )
    except Exception as e:
        LOGGER.error(f"[append_data_to_file] Error: {e}")


def read_data_from_file(file_all_path: str) -> str:
    """
    Read data from a file.

    :param logger: Logger for logging messages.
    :param file_all_path: Full path of the file to read from.
    :return: Data read from the file.
    """
    LOGGER.debug(f"[read_data_from_file] Start reading data from {file_all_path}")
    try:
        with open(file_all_path, "r", encoding=ENCODE) as file:
            data = file.read()
        LOGGER.debug(
            f"[read_data_from_file] Data read successfully from {file_all_path}"
        )
        return data
    except Exception as e:
        LOGGER.error(f"[read_data_from_file] Error: {e}")


# ----------------------------- JSON Read/Write -----------------------------


def get_json_from_file(file_all_path: str) -> dict:
    try:
        with open(file_all_path, "r", encoding=ENCODE) as file:
            json_data = load(file)
        return json_data
    except Exception as e:
        LOGGER.warning(f"error: {e}")


def write_json_to_file(file_all_path: str, json_data, indent: int = 4):
    try:
        json_data = dumps(json_data, indent=indent, ensure_ascii=False)
        create_folder_of_file_if_not_exist(file_all_path)
        write_data_to_file(file_all_path, json_data)
    except Exception as e:
        LOGGER.error(f"error: {e}")


# ----------------------------- File Search -----------------------------


def find_files(file_path: str = "", file_name: str = ".apk", filter: str = "") -> list:
    """
    Search for files by keyword, file format, or specific file name.

    :param file_path: Path to search within.
    :param file_name: File name or extension to search for.
    :param filter: Keyword to filter files.
    :return: List of found file paths.
    """
    LOGGER.debug(f"[find_files] Start searching files in {file_path}")
    try:
        if filter:
            LOGGER.debug(f"[find_files] Searching files containing '{filter}'")
            found_files = []
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    if filter in file:
                        found_path = os.path.join(root, file)
                        found_files.append(found_path)
                        LOGGER.debug(f"[find_files] Found: {found_path}")
            return found_files

        elif file_name.startswith("."):
            LOGGER.debug(f"[find_files] Searching files with extension '{file_name}'")
            found_files = []
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    if file.endswith(file_name):
                        found_path = os.path.join(root, file)
                        found_files.append(found_path)
                        LOGGER.debug(f"[find_files] Found: {found_path}")
            return found_files

        else:
            LOGGER.debug(f"[find_files] Searching for file '{file_name}'")
            found_files = []
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    if file == file_name:
                        found_path = os.path.join(root, file)
                        found_files.append(found_path)
                        LOGGER.debug(f"[find_files] Found: {found_path}")
            return found_files
    except Exception as e:
        LOGGER.error(f"[find_files] Error: {e}")
        return []


def find_files_nc(
    file_path: str = "", file_name: str = ".apk", filter: str = ""
) -> list:
    """
    Search for files in a given directory based on a keyword, file format, or specific file name.

    :param file_path: Directory path where the search is performed. Defaults to the current directory.
    :param file_name: File extension or specific file name to search for. Defaults to '.apk'.
    :param filter: A keyword to filter files by name.
    :return: A list of file paths that match the search criteria.
    """
    LOGGER.debug(
        f"[find_files_nc] Starting search with parameters: file_path='{file_path}', file_name='{file_name}', filter='{filter}'"
    )
    try:
        # Ensure the file path exists
        if not os.path.exists(file_path):
            LOGGER.warning(f"Provided path does not exist: {file_path}")
            return []

        # Search for files by keyword
        if filter:
            LOGGER.debug(
                f"Searching for files containing keyword '{filter}' in '{file_path}'"
            )
            found_files = []
            for file in os.listdir(
                file_path
            ):  # Only list files in the current directory
                if filter in file:
                    found_path = os.path.join(file_path, file)
                    found_files.append(found_path)
                    LOGGER.debug(f"Found file: {found_path}")
            LOGGER.debug(
                f"Total files found with keyword '{filter}': {len(found_files)}"
            )
            return found_files

        # Search for files by format
        elif file_name.startswith("."):
            LOGGER.debug(
                f"Searching for files with format '{file_name}' in '{file_path}'"
            )
            found_files = []
            for file in os.listdir(
                file_path
            ):  # Only list files in the current directory
                if file.endswith(file_name):
                    found_path = os.path.join(file_path, file)
                    found_files.append(found_path)
                    LOGGER.debug(f"Found file: {found_path}")
            LOGGER.debug(
                f"Total files found with format '{file_name}': {len(found_files)}"
            )
            return found_files

        # Search for a specific file
        else:
            LOGGER.debug(f"Searching for file named '{file_name}' in '{file_path}'")
            found_path_list = []
            for file in os.listdir(
                file_path
            ):  # Only list files in the current directory
                if file == file_name:
                    found_path = os.path.join(file_path, file)
                    LOGGER.debug(f"Found file: {found_path}")
                    found_path_list.append(found_path)
            LOGGER.debug(
                f"Total files found with name '{file_name}': {len(found_path_list)}"
            )
            return found_path_list

    except Exception as e:
        LOGGER.error(f"[find_files_nc] An error occurred during file search: {e}")
        return []
    finally:
        LOGGER.debug(f"[find_files_nc] Search completed for path '{file_path}'")


def find_files_nc_without_extension(
    folder_path: str, *without_file_extension_list
) -> list:
    """
    Find files in a folder that do not belong to specified file extensions.

    :param folder_path: Path to the folder.
    :param without_file_extension_list: List of file extensions to exclude.
    :return: List of files that do not have the specified extensions.
    """
    LOGGER.debug(f"Starting search in folder: {folder_path}")
    LOGGER.debug(f"Excluding files with extensions: {without_file_extension_list}")

    # Validate the folder path
    if not os.path.isdir(folder_path):
        LOGGER.error(f"The folder path '{folder_path}' is not a valid directory.")
        raise ValueError(f"The folder path '{folder_path}' is not a valid directory.")

    # Convert the extensions to lowercase and validate input
    excluded_extensions = tuple(
        ext.lower() for ext in without_file_extension_list if isinstance(ext, str)
    )
    LOGGER.debug(f"Converted excluded extensions to lowercase: {excluded_extensions}")

    try:
        # Filter files in the folder
        files = [
            f
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))  # Include only files
            and not f.lower().endswith(
                excluded_extensions
            )  # Exclude specified extensions
        ]
        LOGGER.info(f"Found {len(files)} files not matching the excluded extensions.")
        for file in files:
            LOGGER.debug(f"File included: {file}")

        return files
    except Exception as e:
        LOGGER.error(f"An error occurred while searching files: {e}")


# ----------------------------- Delete Files -----------------------------


def delete_files(file_path: str = "", file_name_or_format: str = ""):
    """
    Delete all files, files of a specific format, or a specific file in a directory.

    :param file_path: Path to the directory.
    :param file_name_or_format: Specific file name or format to delete.
    """
    LOGGER.debug(f"[delete_files] Start deleting in {file_path}")
    try:
        if file_name_or_format == "":
            LOGGER.debug(f"[delete_files] Deleting all files in {file_path}")
            rmtree(file_path)
        elif file_name_or_format.startswith("."):
            LOGGER.debug(
                f"[delete_files] Deleting files with extension '{file_name_or_format}'"
            )
            for file in find_files(LOGGER, file_path, file_name=file_name_or_format):
                os.remove(file)
        else:
            LOGGER.debug(
                f"[delete_files] Deleting specific file '{file_name_or_format}'"
            )
            os.remove(join_file_path(file_path, file_name_or_format))
        LOGGER.info(f"[delete_files] Deletion successful")
    except Exception as e:
        LOGGER.error(f"[delete_files] Error: {e}")



def remove_empty_folders(directory: str):
    """
    Recursively delete all empty folders in the specified directory.

    :param directory: The path of the directory to clean.
    """
    # Traverse all files and subdirectories in the directory
    for foldername, subfolders, filenames in os.walk(directory, topdown=False):
        # Traverse all subdirectories
        for subfolder in subfolders:
            folder_path = os.path.join(foldername, subfolder)
            # If the folder is empty, delete it
            if not os.listdir(folder_path):  # Folder is empty
                os.rmdir(folder_path)
                LOGGER.debug(f"Deleted empty folder: {folder_path}")


# ----------------------------- Copy Files -----------------------------


def copy_files(
    from_folder_path: str = "/",
    from_file_name_or_format: str = "",
    to_folder_path: str = "/",
    to_file_name: str = "",
):
    """Copy all files/copy all files of a specific format in a file tree/copy a single file."""
    try:
        # If no file is specified, copy all files
        if "" == from_file_name_or_format:
            LOGGER.debug(
                f"copy all file in folder {from_folder_path} to folder {to_folder_path}"
            )
            if not path.exists(to_folder_path):
                LOGGER.info(
                    f"target folder {to_folder_path} does not exist, creating... "
                )
                makedirs(to_folder_path)
                LOGGER.info(f"succeed in makedirs!")
            copytree(from_folder_path, to_folder_path)
        # If a file format is passed, copy files of that format
        elif from_file_name_or_format.startswith("."):
            LOGGER.debug(
                f"copy file of format {from_file_name_or_format} in folder {from_folder_path} to folder {to_folder_path}"
            )
            found_files = find_files(from_folder_path, from_file_name_or_format)
            if not found_files:
                LOGGER.warning(f"file in format {from_file_name_or_format} not found")
                return
            if not path.exists(to_folder_path):
                LOGGER.info(
                    f"target folder {to_folder_path} does not exist, creating... "
                )
                makedirs(to_folder_path)
                LOGGER.info(f"succeed in makedirs!")
            for file in found_files:
                copy(file, to_folder_path)
        # Copy a specific file
        else:
            if "" == to_file_name:
                to_file_name = from_file_name_or_format
            LOGGER.debug(
                f"copy file of name {from_file_name_or_format} in folder {from_folder_path} to folder {to_folder_path}, and renamed as {to_file_name}"
            )
            if not path.exists(to_folder_path):
                LOGGER.info(
                    f"target folder {to_folder_path} does not exist, creating... "
                )
                makedirs(to_folder_path)
                LOGGER.info(f"succeed in makedirs!")
            copy(
                join_file_path(from_folder_path, from_file_name_or_format),
                join_file_path(to_folder_path, to_file_name),
            )
        LOGGER.info(f"succeed in copy files!")
    except Exception as e:
        LOGGER.error(f"error: {e}")


def copy_folder(from_folder_path: str, to_folder_path: str):
    import shutil

    """
    Copy all files and subfolders from one folder to another, preserving the folder structure.

    :param from_folder_path: Source folder path.
    :param to_folder_path: Destination folder path.
    """
    try:
        # Check if the source folder exists
        if not os.path.exists(from_folder_path):
            raise FileNotFoundError(
                f"Source folder '{from_folder_path}' does not exist!"
            )

        # Ensure the destination folder exists
        if not os.path.exists(to_folder_path):
            os.makedirs(to_folder_path)
            LOGGER.info(f"Created target folder: {to_folder_path}")

        # Traverse the source folder and its subfolders
        for root, dirs, files in os.walk(from_folder_path):
            # Copy subfolder structure
            for dir_name in dirs:
                src_dir = os.path.join(root, dir_name)
                dest_dir = os.path.join(
                    to_folder_path, os.path.relpath(src_dir, from_folder_path)
                )
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                    LOGGER.debug(f"Created subdirectory: {dest_dir}")

            # Copy files
            for file_name in files:
                src_file = os.path.join(root, file_name)
                dest_file = os.path.join(
                    to_folder_path, os.path.relpath(src_file, from_folder_path)
                )
                shutil.copy2(src_file, dest_file)
                LOGGER.debug(f"Copied file: {src_file} to {dest_file}")

        LOGGER.info(
            f"Successfully copied all files and subfolders from '{from_folder_path}' to '{to_folder_path}'."
        )

    except Exception as e:
        LOGGER.error(f"Error while copying files: {e}")


# ----------------------------- Make Files -----------------------------


def create_folder_if_not_exist(folder_path: str) -> bool:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        LOGGER.info(f"Directory '{folder_path}' has been created.")
    else:
        # LOGGER.debug(f"'{path}' already exists.")
        return


# ----------------------------- Tools Method -----------------------------


def get_filename_from_pathall(file_path_all: str) -> str:
    return path.basename(file_path_all)


def resolve_relative_path(path: str) -> str:
    """
    Resolve a given path with `..` components to its absolute path.

    Args:
        path (str): The input path containing `..` components.

    Returns:
        str: The resolved absolute path.
    """
    resolved_path = os.path.normpath(path)
    return resolved_path


def get_filepath_from_pathall(file_path_all: str) -> str:
    # Split the path into drive and path components
    drive, path_without_drive = path.splitdrive(file_path_all)
    # Get the directory path
    directory_path = path.dirname(path_without_drive)
    # Return the full path including the drive
    return path.join(drive, directory_path)


def join_file_path(*args: str) -> str:
    if "" == args[0]:
        return path.join(args[1:])
    joined_path = path.join(*args)
    return joined_path.replace("/", "\\")


def join_file_path_remote(*args: str) -> str:
    joined_path = join_file_path(*args)
    return joined_path.replace("\\", "/")


def is_file_exist(path_all_file: str) -> bool:
    return path.exists(path_all_file)


def create_folder_of_file_if_not_exist(file_path_all: str):
    parent_folder = path.dirname(file_path_all)
    if not parent_folder:
        makedirs(parent_folder)


def get_basename(file_path: str) -> str:
    basename, _ = os.path.splitext(os.path.basename(file_path))
    return basename


def get_extension(file_path: str) -> str:
    _, extension = os.path.splitext(file_path)
    return extension


def rollback_path(path, levels):
    """
    Roll back a specified path by a given number of levels.

    :param path: The original file or directory path.
    :param levels: Number of levels to roll back (default is 2).
    :return: The rolled-back path.
    """
    if levels < 0:
        raise ValueError("Levels must be a non-negative integer.")
    for _ in range(levels):
        path = os.path.dirname(path)
    return path


# ----------------------------- File Size -----------------------------

import os


def get_file_size_mb(file_path: str) -> float:
    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / (1024 * 1024)
    return file_size_mb
