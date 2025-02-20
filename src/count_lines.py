import os
import json
from typing import Tuple, Optional

class ConfigNotConfiguredError(Exception):
    def __init__(self, message="config.json not configured"):
        self.message = message
        super().__init__(self.message)

def count_lines_of_code(directory: str, extensions: Tuple[str, ...]) -> int:
    total_lines = 0

    for root, dirs, files in os.walk(directory):
        # Exclude 'test' directories
        dirs[:] = [d for d in dirs if d.lower() != 'test']
        
        for file in files:
            # Count only .ts and .tsx files
            if file.endswith(extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = sum(1 for line in f if line.strip())
                        total_lines += lines
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")
    
    return total_lines

def count_files(directory: str, extensions: Tuple[str, ...]) -> int:
    ts_file_count = 0

    for root, dirs, files in os.walk(directory):
        # Exclude 'test' directories
        dirs[:] = [d for d in dirs if d.lower() != 'test']
        
        for file in files:
            # Count only .ts and .tsx files
            if file.endswith(extensions):
                ts_file_count += 1

    return ts_file_count

def parse_json() -> Tuple[Optional[str], Optional[Tuple[str, ...]]]:
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)

        directory = config['Directory']
        extensions = config["FileTypes"]

        if directory == "" or len(extensions) == 0:
            raise ConfigNotConfiguredError()

        return (directory, tuple(extensions))
    except FileNotFoundError:
        print("\nError: config.json not found\n")
        return None, None
    except json.JSONDecodeError:
        print("\nError: config.json has invalid json\n")
        return None, None
    except Exception as e:
        print(f"\nException Caught: {e}\n")
        return None, None


if __name__ == "__main__":
    directory, extensions = parse_json()

    if directory is not None or extensions is not None:
        lines = count_lines_of_code(directory, extensions)
        files = count_files(directory,extensions)
        print(f"\nLines of Code: {lines:,}")
        print(f"Number of Files: {files:,}\n")