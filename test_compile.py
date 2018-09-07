import os

from compiler import Compiler

if __name__ == "__main__":
    for root, subdirs, files in os.walk('./tests'):
        for file_name in files:
            if ".bfasm1" != file_name[-7:]:
                continue
            print(f"============ {file_name} =============")
            file_name = os.path.join(root, file_name)
            f = open(file_name, "rt")
            lines = f.readlines()
            c = Compiler(lines)
            print(c.lines)
            print(c.root_block.beauty_str())
            print(c.code)
