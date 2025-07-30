# aleah - write a function that can return a list object containing all filepaths on the users drive. 
# ex - get_dir(target_drive : str) -> list:
# feel free to write your own sub functions within this file to aid in scraping the fpath data. 
# likely the only function from this file that will be used is the one mentioned above.



import os
class Directory_scrape():
    def get_directory_tree(start_path)-> str:
        all_files = []
        for root, _, files in os.walk(start_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                all_files.append(file_path)
        return all_files


    def sub_directory_path(start_path)-> str:
        for root, dirs, files in os.walk(start_path):
            root = root
            files = files
            dir_list = []
            dir_list.append(dirs)
            return dir_list


def main():
    directory_scan = '/' 
    file_list = Directory_scrape.get_directory_tree(directory_scan)
    path = Directory_scrape.sub_directory_path(directory_scan)
    
    print(file_list)

    for sub_paths in path:
        print(sub_paths)


    print(f"Total Files: {len(file_list)}")
    print(f"Total Sub-Directories: {len(sub_paths)}")

# aleah - make sure not to run your code here. Theres already a main.py file so use that for testing instead.
# also lmk if you need me to run any code. 

if __name__ == '__main__':
    main()