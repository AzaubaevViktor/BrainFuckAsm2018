import os
import sys
from pprint import pprint

from compiler import CompiledFile, CompileError


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

            try:
                c.compile()
            except CompileError as e:
                if "error" in c.params:
                    print("Ошибка перехвачена!")
                    exc_level, line_n, pos = c.params["error"].split(' ')
                    err = None
                    if e.line.n != int(line_n):
                        err = f"Error[Error]: need: line number `{int(line_n)}`, but in fact:`{e.line.n}`"
                        print(err)
                        errors[file_path] = err
                    if e.pos != int(pos):
                        err = f"Error[Error]: need: pos `{pos}`, but in fact:`{e.pos}`"
                        print(err)
                        errors[file_path] = err
                    if e.level != exc_level:
                        err = f"Error[Error]: need: level `{exc_level}`, but in fact:`{e.level}`"
                        print(err)
                        errors[file_path] = err
                else:
                    err = f"Error[Error]: need: No error, but in fact:`{e}`"
                    print(err)
                    errors[file_path] = err

                print(e, file=sys.stderr if err else sys.stdout)

                continue

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

