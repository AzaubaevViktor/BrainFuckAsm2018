import os

from compiler import CompiledFile

if __name__ == "__main__":
    for root, subdirs, files in os.walk('./tests'):
        for file_path in files:
            if ".bfasm1" != file_path[-7:]:
                continue
            print(f"============ {file_path} =============")
            file_path = os.path.join(root, file_path)
            c = CompiledFile(file_path)
            print(c.lines)
            print(c.root_block.beauty_str())
            print(c.code)
