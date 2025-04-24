import os
import math
from tkinter import filedialog
from tkinter import Tk

def get_info(path):
    total_size_bytes = 0
    extensions_count = {}
    extensions_size = {}
    all_files = []

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                size_in_bytes = os.path.getsize(file_path)
                all_files.append((file_path, size_in_bytes))
                total_size_bytes += size_in_bytes
            except OSError as e:
                print(f"Error accessing file (initial scan): {file_path} - {e}")

    processed_size_bytes = 0
    number_of_files = len(all_files)

    for i, (file_path, size_in_bytes) in enumerate(all_files):
        try:
            file_extension = os.path.splitext(os.path.basename(file_path))[1]
            if file_extension in extensions_count:
                extensions_count[file_extension] += 1
                extensions_size[file_extension] += size_in_bytes
            else:
                extensions_count[file_extension] = 1
                extensions_size[file_extension] = size_in_bytes

            processed_size_bytes += size_in_bytes
            if total_size_bytes > 0:
                percentage = (processed_size_bytes / total_size_bytes) * 100
            else:
                percentage = 0

            print(f"Scanning... {percentage:.2f}% ({i + 1}/{number_of_files} files processed)", end='\r')

        except OSError as e:
            print(f"\nError accessing file (processing): {file_path} - {e}")

    print()
    return total_size_bytes, extensions_count, extensions_size


def format_bytes(size_bytes):
    # Converts bytes to a more readable format (KB, MB, GB)
    if size_bytes == 0:
        return "0 bytes"
    size_name = ("bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()

    if not folder_selected:
        print("No folder selected.")
    else:
        print(f"Preparing to scan files in '{folder_selected}' and calculate the progress. This might take a while...")
        total_bytes, extension_data, ext_size = get_info(folder_selected)
        formatted_total = format_bytes(total_bytes)

        if extension_data:
            print("\n--- Extension Breakdown ---")
            sorted_ext = sorted(extension_data.items(), key=lambda item: item[1])

            for key, value in sorted_ext:
                formatted_size = format_bytes(ext_size.get(key, 0))
                print(f"Extension: {key}, Count: {value}, Total Size: {formatted_size}")

            print(f"\n--- Summary ---")
            print(f"Total size of all files: {total_bytes} bytes ({formatted_total}) in '{folder_selected}'")

        else:
            print("\nNo files found in the selected folder.")

        print("Scanning complete.")
        root.destroy()

input("\nPress Enter to close the terminal...")