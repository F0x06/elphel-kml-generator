#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  elphel-kml-generator - Elphel KML generator

  Copyright (c) 2014 FOXEL SA - http://foxel.ch
  Please read <http://foxel.ch/license> for more information.


  Author(s):

       Kevin Velickovic <k.velickovic@foxel.ch>


  This file is part of the FOXEL project <http://foxel.ch>.

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Affero General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Affero General Public License for more details.

  You should have received a copy of the GNU Affero General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.


  Additional Terms:

       You are required to preserve legal notices and author attributions in
       that material or in the Appropriate Legal Notices displayed by works
       containing it.

       You are required to attribute the work as explained in the "Usage and
       Attribution" section of <http://foxel.ch/license>.
"""

import getopt
import glob
import os
import string
import sys

import exifread

# Global variables

# KML file header
KML_Header = \
"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.2">
<Document>
"""

# KML file entry
KML_Entry = \
"""<PhotoOverlay>
    <Camera>
        <longitude>%f</longitude>
        <latitude>%f</latitude>
        <altitude>%s</altitude>
        <heading>%d</heading>
        <tilt>%d</tilt>
        <roll>%d</roll>
    </Camera>
    <Icon>
        <href>%s/%s</href>
    </Icon>
</PhotoOverlay>
"""

# KML file footer
KML_Footer = \
"""</Document>
</kml>"""

# Function to convert a fractioned EXIF array into degrees
def array2degrees(dms):

    # Rounding factor
    _round=1000000

    # Splitting input values
    d = string.split(str(dms.values[0]), '/')
    m = string.split(str(dms.values[1]), '/')
    s = string.split(str(dms.values[2]), '/')

    # Variables padding
    if len(d) == 1:
        d.append(1)
    if len(m) == 1:
        m.append(1)
    if len(s) == 1:
        s.append(1)

    # Compute degrees
    rslt = float(d[0]) / float(d[1]) + (float(m[0]) / float(m[1])) / 60.0 + (float(s[0]) / float(s[1])) / 3600.0

    # Return result
    return round(_round*rslt)/_round

# Function to convert a fractioned EXIF altidute into meters
def parseAlt(alt):

    # Rounding factor
    _round=1000000

    # Splitting input values
    a = string.split(str(alt), '/')

    # Variables padding
    if len(a) == 1:
        a.append(1)

    # Compute altitude
    rslt = float(a[0]) / float(a[1])

    # Return result
    return round(_round*rslt)/_round

# Function to generate KML file
def generateKML(Input, Output, BaseURL):

    # Open KML file for writing
    KML_File = open(Output, "wb")

    # Write header
    KML_File.write(KML_Header)

    # Walk over files
    for f in sorted(glob.glob("%s/*_1.jp4" % Input)):

        # Open image and extract EXIF data
        Image = open(f, "rb")
        EXIFData = exifread.process_file(Image)
        Image.close()

        # Compute GPS data
        Longitude = (-1 if (EXIFData['GPS GPSLongitudeRef'] == "W") else 1) * array2degrees(EXIFData['GPS GPSLongitude'])
        Latitude  = (-1 if (EXIFData['GPS GPSLatitudeRef'] == "S") else 1) * array2degrees(EXIFData['GPS GPSLatitude'])
        Altitude  = (-1 if (EXIFData['GPS GPSAltitudeRef'] == "S") else 1) * parseAlt(EXIFData['GPS GPSAltitude'])

        Heading = 0
        Tilt    = 90
        Roll    = 0

        if 'GPS GPSImgDirection' in EXIFData:

            # Compute GPS data
            Heading = parseAlt(EXIFData['GPS GPSImgDirection'])
            Tilt    = (-1 if (EXIFData['GPS GPSDestLatitudeRef'] == "S") else 1) * array2degrees(EXIFData['GPS GPSDestLatitude']) + 90.0

            if (Tilt < 0):
                Tilt = 0
            elif (Tilt > 180):
                Tilt = 180

            Roll = (-1 if (EXIFData['GPS GPSDestLongitudeRef'] == "W") else 1) * array2degrees(EXIFData['GPS GPSDestLongitude'])

        # Write KML entry
        KML_File.write(KML_Entry % (Longitude, Latitude, "{0:.1f}".format(Altitude), Heading, Tilt, Roll, BaseURL, os.path.split(f)[1]))

    # Write KML footer
    KML_File.write(KML_Footer)

    # Close KML file
    KML_File.close()

# Usage display function
def _usage():
    print """
    Usage: %s [OPTIONS]

    -h --help           Prints this
    -i --input          Input JP4 folder
    -o --output         Output KML file
    -b --baseurl        KML base URL
    """ % sys.argv[0]

# Program entry point function
def main(argv):

    # Arguments variables initialisation
    __Input__    = ""
    __Output__   = ""
    __Base_URL__ = ""

    # Arguments parser
    try:
        opt, args = getopt.getopt(argv, "hi:o:b:", ["help", "input=", "output=", "baseurl="])
        args = args
    except getopt.GetoptError, err:
        print str(err)
        _usage()
        sys.exit(2)
    for o, a in opt:
        if o in ("-h", "--help"):
            _usage()
            sys.exit()
        elif o in ("-i", "--input"):
            __Input__  = a.rstrip('/')
        elif o in ("-o", "--output"):
            __Output__  = a.rstrip('/')
        elif o in ("-b", "--baseurl"):
            __Base_URL__  = a.rstrip('/')
        else:
            assert False, "unhandled option"

    # Arguments check
    if len(argv) < 2:
        _usage()
        return

    # Generate KML
    generateKML(__Input__, __Output__, __Base_URL__)

# Program entry point
if __name__ == "__main__":
    main(sys.argv[1:])
