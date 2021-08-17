# wdtool.py
***This tool has been deprecated. Please use [`wdreconcile`](https://github.com/hay/wdreconcile) instead.***

> Command line utility to match strings to Wikidata items, written in Python 3

## Examples
To match strings, first get a CSV file with QID's that you want to match (e.g., from the [Wikidata Query Service](https://query.wikidata.org/)) and get the metadata for all items

    wdtool.py import -i query.csv

If your CSV file has multiple columns and a header, you need to give it the key of the column where your qids are located as well

    wdtool.py import -i query.csv -k item

This will download all item data and write it to a JSON file, by default in a directory called `data` in the same folder as where you execute `wdtool.py`.

To match your CSV file of strings try

    wdtool.py reconcile -i strings.csv -o strings-matched.csv

If you have a CSV file with a header and multiple columns you can use the `-k` argument again

    wdtool.py reconcile -i items.csv -k item -o strings-matched.csv

`strings-matched.csv` will contain the effort wdtool has made.

## Troubleshooting
* Before opening an issue, try running your command with the `-v` (verbose) switch, because this will give you more debug information.

## All options
You'll get this output when running `wdtool.py -h`.

```bash
usage: wdtool.py [-h] [--has-header] -i INPUT [-k KEY] [-o OUTPUT]
                 [-dp DATA_PATH] [-v]
                 [{import,reconcile}]

Tool to match strings to Wikidata items

positional arguments:
  {import,reconcile}

optional arguments:
  -h, --help            show this help message and exit
  --has-header          CSV file has a header
  -i INPUT, --input INPUT
                        Input CSV file
  -k KEY, --key KEY     If a CSV file has multiple columns, give the key of
                        the column
  -o OUTPUT, --output OUTPUT
                        Output CSV file
  -dp DATA_PATH, --data-path DATA_PATH
                        Path where the JSON Wikidata files will be saved,
                        defaults to /Users/hkrane01/htdocs/wdtool/data
  -v, --verbose         Display debug information
```

## License
Licensed under the [MIT license](https://opensource.org/licenses/MIT).

## Credits
Written by [Hay Kranen](https://www.haykranen.nl).