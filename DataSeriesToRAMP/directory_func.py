import os

def make_results_dir(directory_name):
    if os.path.exists(directory_name) and os.path.isdir(directory_name):
        print("Directory Exists, no new folder created")
    else:
        # error if not permitted
        try:
            print(f"Making directory:{directory_name}")
            os.mkdir(directory_name)
        except OSError as e:
            print(f"directory exists: {e}")


if (__name__ == "__main__"):
    path = os.getcwd()
    name = "unnamed_dir"
    print(f"current: {path}")

    make_results_dir(name)