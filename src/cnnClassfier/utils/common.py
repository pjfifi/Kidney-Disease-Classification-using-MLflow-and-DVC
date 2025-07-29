import os
from box.exceptions import BoxValueError
import yaml
from cnnClassfier import logger
import json
import joblib
from ensure import ensure_annotations
from typing import Any
from box import ConfigBox
from pathlib import Path
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its content as a ConfigBox object.
    
    Args:
        path_to_yaml (Path): Path to the YAML file.
        
    Returns:
        ConfigBox: Content of the YAML file as a ConfigBox object.
    """
    try:
        with open(path_to_yaml, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file {path_to_yaml} read successfully.")
            return ConfigBox(content)
    except FileNotFoundError as e:
        logger.error(f"File not found: {path_to_yaml}")
        raise e
    except yaml.YAMLError as e:
        logger.error(f"Error reading YAML file: {e}")
        raise e
    
    @ensure_annotations
    def create_directories(paths_to_diectories: list[Path], verbose=True):
        """
        Creates directories if they do not exist.
        
        Args:
            paths (list[Path]): List of directory paths to create.
            ignore (bool): If True, logs the creation of directories.
        """
        for path in paths_to_diectories:
            try:
                path.mkdir(path, exist_ok=True)
                if verbose:
                    logger.info(f"Directory created: {path}")
            except Exception as e:
                logger.error(f"Error creating directory {path}: {e}")
                raise e
            
@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Saves a dictionary to a JSON file.
    
    Args:
        path (Path): Path to the JSON file.
        data (dict): Data to save in json file.
    """
    try:
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
            logger.info(f"Data saved to JSON file: {path}")
    except Exception as e:
        logger.error(f"Error saving JSON file {path}: {e}")
        raise e
    
@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Loads a JSON file and returns its content as a ConfigBox object.
    
    Args:
        path (Path): Path to the JSON file.
        
    Returns:
        ConfigBox: Content of the JSON file as a ConfigBox object.
    """
    try:
        with open(path, 'r') as json_file:
            content = json.load(json_file)
            logger.info(f"JSON file {path} loaded successfully.")
            return ConfigBox(content)
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        raise e
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON file: {e}")
        raise e
    
@ensure_annotations
def load_binary(path: Path) -> Any:
    """
    Loads a binary file using joblib.
    
    Args:
        path (Path): Path to the binary file.
        
    Returns:
        Any: Content of the binary file.
    """
    try:
        content = joblib.load(path)
        logger.info(f"Binary file {path} loaded successfully.")
        return content
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        raise e
    except Exception as e:
        logger.error(f"Error loading binary file: {e}")
        raise e

@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"

def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())