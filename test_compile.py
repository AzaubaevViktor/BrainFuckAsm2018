import os
from pprint import pprint

from compiler import CompiledFile


class Errors(dict):
    def __setitem__(self, key, value):
        gi = super().__getitem__
        si = super().__setitem__

        v = self.get(key)

        if v is None:
            si(key, [value])
        else:
            v.append(value)


errors = Errors()

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
            if "code" in c.params:
                print("Check code... ", end="")

                if c.code != c.params["code"]:
                    err = f"\nError[Code]: need:\n`{c.params['code']}`\n, but in fact:\n`{c.code}`"
                    print(err)
                    errors[file_path] = err
                else:
                    print('OK')


print("============ RESULTS =============")
print(f"Errors: {len(errors)}")
pprint(errors)

