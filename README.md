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

See the related [file](LICENSE).
