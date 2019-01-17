# keepass_to_1password

A simple script to convert KeePass-exported XML database to [1Password-compatible CSV](https://support.1password.com/create-csv-files/#login).

For each "Entry" in XML, it converts only the bare minimum:

* XML element "Title" is saved as "title" CSV field
* "URL" as "website"
* "UserName" as "username"
* "Password" as "password"
* "Notes" as "notes"

Only non-expired entries are considered.

## How to use

Create a virtualenv:

    python3 -m venv venv
    source ./venv/bin/activate

Install `poetry` as described in [its documenation](https://poetry.eustace.io/docs/).

Then run:

    poetry install

Now you can use `cli` script:

    cli --help
    cli convert --help
    cli info --help

## Examples

Convert entries from `export.xml` and group `my_group` to `import.csv`:

    cli -i export.xml convert -o import.csv -g my_group

Show all the groups in `export.xml`:

    cli -i export.xml info

## License

The MIT License (MIT)

Copyright (c) 2019 slavos1

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

