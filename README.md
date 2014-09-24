## elphel-kml-generator<br />Elphel KML generator.

>Elphel KML generator.

### Description
This tool generate a KML file based on input JP4 folder.

### Table of contents

- [Dependencies](#dependencies)
    - [Details](#details)
    - [Installation](#installation)
- [Usage](#usage)
- [Example usage scenario](#example-usage-scenario)
- [Copyright](#copyright)
- [License](#license)

### Dependencies

#### Details

1. [python-pip](https://pypi.python.org/pypi/pip)
2. [exifread](https://pypi.python.org/pypi/ExifRead)

#### Installation

    sudo apt-get install python-pip
    sudo pip install exifread

### Usage
    Usage: ./kml_generator.py [OPTIONS]

    -h --help           Prints this
    -i --input          Input JP4 folder
    -o --output         Output KML file
    -b --baseurl        KML base URL

### Example usage scenario
    ./kml_generator.py -i data/footage/run1/out -o /data/footage/run1/map_points.kml -b "http://127.0.0.1/footage/run1/0/"

### Copyright

Copyright (c) 2014 FOXEL SA - [http://foxel.ch](http://foxel.ch)<br />
This program is part of the FOXEL project <[http://foxel.ch](http://foxel.ch)>.

Please read the [COPYRIGHT.md](COPYRIGHT.md) file for more information.


### License

This program is licensed under the terms of the
[GNU Affero General Public License v3](http://www.gnu.org/licenses/agpl.html)
(GNU AGPL), with two additional terms. The content is licensed under the terms
of the
[Creative Commons Attribution-ShareAlike 4.0 International](http://creativecommons.org/licenses/by-sa/4.0/)
(CC BY-SA) license.

Please read <[http://foxel.ch/license](http://foxel.ch/license)> for more
information.
