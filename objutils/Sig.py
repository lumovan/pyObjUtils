#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.1.0"

__copyright__ = """
    pyObjUtils - Object file library for Python.

   (C) 2010-2013 by Christoph Schueler <github.com/Christoph2,
                                        cpu12.gems@googlemail.com>

   All Rights Reserved

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import objutils.HexFile as HexFile

DATA=1
EOF=2

FORMATS=(
    (DATA,":AAAALLBBDDCC"),
    (EOF,":00")
)

class Reader(HexFile.Reader):
    def __init__(self, inFile, dataSep = None):
        super(Reader, self).__init__(FORMATS, inFile, dataSep)

    def checkByte(self,checksum,b):
        checksum^=b
        checksum<<=1
        if checksum & 0x100==0x100:
            checksum|=0x01
        checksum &= 0xff
        return checksum

    def checkLine(self,line,formatType):
        if formatType==DATA:
            if line.length!=len(line.chunk):
                raise HexFile.InvalidRecordLengthError("Byte count doesn't match length of actual data.")
            addrChecksum=0
            for b in [(line.address & 0xff00)>>8,line.address & 0xff,line.length]:
                addrChecksum=self.checkByte(addrChecksum,b)
            if line.addrChecksum!=addrChecksum:
                raise HexFile.InvalidRecordChecksumError()
            checksum=0
            for b in line.chunk:
                checksum=self.checkByte(checksum,b)
            if line.checksum!=checksum:
                raise HexFile.InvalidRecordChecksumError()

    def isDataLine(self,line,formatType):
        return formatType==DATA

