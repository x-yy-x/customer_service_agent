#为整个工程提供绝对路径
import os

def get_project_root():
    
    current_file =os.path.abspath(__file__)
    current_dir =  os.path.dirname(current_file)
    
    project_root = os.path.dirname(current_dir)
    return project_root


def get_abs_path(relative_path):
    project_root = get_project_root()
    abs_path = os.path.join(project_root, relative_path)
    return abs_path


if __name__ == "__main__":
    # Example usage
    relative_path = "data/sample.txt"
    absolute_path = get_abs_path(relative_path)
    print(f"Absolute path: {absolute_path}") 