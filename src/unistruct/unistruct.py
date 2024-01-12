import json

class ValueNotFound(Exception):
    "Value Not Found"
    pass
class Unistruct(object):
    def __init__(self, struct_in=None):
        if isinstance(struct_in, str):
            self.in_struct = json.loads(struct_in)
        else:
            self.in_struct = struct_in
        self._index = 0

    def get_if(self, key, *args):
        out_struct = None
        if isinstance(self.in_struct, dict):
            out_struct = self.in_struct.get(key)
        elif isinstance(self.in_struct, list):
            if isinstance(key, int) and key < len(self.in_struct):
                out_struct = self.in_struct[key]
            else:
                out_struct = None
        else:
            pass
        if args:
            keys = list(args)
            return Unistruct(out_struct).get_if(keys.pop(0), *keys)
        return Unistruct(out_struct)
    def val(self, default=None, exception=False):
        if self.in_struct == None:
            if exception:
                raise ValueNotFound
            if default != None:
                return default
        return self.in_struct
    def __bool__(self):
        return self.in_struct != None
    def __enter__(self, default=None, exception=False):
        if self.in_struct:
            return self.val(default, exception)
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def __iter__(self):
        return self
    def __next__(self):
        if self._index or self.in_struct == None:
            self._index = 0
            raise StopIteration
        self._index = 1
        return self.val()
    def __getitem__(self, item):
        return self.get_if(item)
    def run_if(self, func, run_else=None):
        if self:
            func(self.val())
        elif run_else:
            run_else()
        return self
    def run_else(self, func):
        if not self:
            func()
        return self
