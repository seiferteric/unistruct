**Unistruct**

When having to deal with large deeply nested data structures (often json) it can be a little tedious and error prone with python. If the structure of the data may be malformed, or values are optional you often have to have a lot of boiler plate code ensuring the data is present to avoid errors. With data like this:
```
in_json = """
{
    "name": "Eric Seifert",
    "github": "https://github.com/seiferteric",
    "two-words": "Hello World",
    "nested": {
        "subnest": {
            "subkey": "subval"
        }
    },
    "nested2": {
        "subvals": [2, 3, 4]
    }
}
"""
```
You might have to do something like this:

```
needed_val = None
if out_dict.get("nested") and out_dict.get("nested").get("subnest"):
    needed_val = out_dict.get("nested").get("subnest").get("subkey")

```
Or perhaps a bit cleaner:
```
needed_val = out_dict.get("nested", {}).get("subnest", {}).get("subkey")
```
But if there is an array, you might need to check the length first like:
```
needed_val = out_dict.get("nested2", {}).get("subvals", {})
if len(needed_val) > 2:
    needed_val = needed_val[2]
else:
    needed_val = None
```

Even worse, sometimes (in writing ansible resource modules for instance) you might have a structure that contains "None" values if they are not present instead of just not being there, so providing a default value in .get() does not work. Then you might have to do something like this:
```
needed_val = (out_dict.get("nested") or {}).get("subnest", {}).get("subkey")
```

This library provides some convenient ways to access data from the structure and operate on it if it exists. I don't suggest this is a great way to do things, but more of an expirement. Also I recently found [jsonpath-ng](https://pypi.org/project/jsonpath-ng/) which looks great and frankely is probably better to use than this.. Anyway, here are some examples.

**Examples:**

```
sj = Unistruct(in_json)

# Abuse iterator to only run if value exists.
# Note you can chain together dictionary and array
# types, if value does not exist, you will get "None"
for s in sj['nested2']['subvals'][3]:
    print(s)

# Myval will be of type Unistruct
myval = sj['nested2']['subvals'][3]
#To get actual value, call .val()
myrealval = myval.val()

# You can check if value exists with if statement,
# You won't get exception if it does not.
if sj['nested2']['subvals']:
    # do something
    pass

# Support lambda to operate on value if it exists,
# and support else statement.
sj['nested2']['subvals'][2].run_if(lambda val: 
    print(f"My value: {val}"),
run_else=lambda :
    print("No Value")
)


# If you need more than one line that lambda supports,
# You can do it like this
myval = sj['nested2']['subvals'][2]
if myval:
    print("YES")
else:
    print("NO")

```

**Install:**
```
python3 -m pip install git+https://github.com/seiferteric/unistruct.git
```
