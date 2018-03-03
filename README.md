# keyaTalk

## Usage

```shell
usage: keyaTalk.py [-h] [--json] [--html] [--time] -d DATABASE -f MEDIA

keyaki meassages

optional arguments:
  --json       save to data.json
  --html       save to index.html
  --time       print media datetime
  -d DATABASE  main.db
  -f MEDIA     a media folder
```

## Example

Step 1
```shell
keyaTalk.py -d main.db -f media --time
```

Step 2

rename all media files based on media_name_list.txt

Step 3
```shell
keyaTalk.py -d main.db -f media [--html]
or
keyaTalk.py -d main.db -f media --json
```