# aleah - write a function that can return a list object containing all filepaths on the users drive. 
# ex - get_dir(target_drive : str) -> list:
# feel free to write your own sub functions within this file to aid in scraping the fpath data. 
# likely the only function from this file that will be used is the one mentioned above.



import os
from pathlib import Path

class Directory_scrape:
    def __init__(self):
        self.dir_list = []
        self.all_files = []

    def get_directory_tree(self, start_path: Path) -> list[Path]:
        self.all_files = []
        for root, _, files in os.walk(start_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                self.all_files.append(file_path)
        return self.all_files


    def sub_directory_path(self, start_path: Path) -> list[Path]:
        self.dir_list = []
        for item in Path(start_path).iterdir():
            if item.is_dir():
                self.dir_list.append(item)
        return self.dir_list


    def loop_subdir(self, start_path: Path) -> dict[Path, list[Path]]:
        subdir_dict = {}
        for directory in self.dir_list:
            files = []
            for root, _, filenames in os.walk(directory):
                for name in filenames:
                    files.append(Path(root) / name)
            subdir_dict[directory] = files
        return subdir_dict

def main():
    scraper = Directory_scrape()
    root_scan = '/'
    file_list = scraper.get_directory_tree(root_scan)
    path = scraper.sub_directory_path(root_scan)
    loop_subdir = scraper.loop_subdir(root_scan)

    print(f"""////Every file in hard drive:{file_list}////""")

    print(f"Total Files: {len(file_list)}")
    print(f"Total Sub-Directories:{len(path)}")


    print(f"////Every Sub-Directory////")
    for sub_paths in path:
        print(f"--({sub_paths}")

    for subdir, files in loop_subdir.items():
        print(f"{subdir} ({len(files)} files)")


if __name__ == '__main__':
    main()