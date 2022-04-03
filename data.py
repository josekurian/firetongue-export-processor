import xml.etree.ElementTree as ET
from typing import Iterator, List
import constants as const


def find_albums(name: str, albums: Iterator):
    """
    matched_album examines the album names and determines whether they match the search criteria

    Args:
        name (str): the search criteria - does the name match
        albums (Iterator): Iterator over the Albums structure of the data file

    Returns:
        List: List of lists, with the inner list made up of the matching album name and its unique Id
    """
    matches = []
    found = 0

    for album in albums:
        albumname = album.find(const.TITLE).text
        if ((albumname != None) and (albumname.find(name) > 0)):
            matches.append([albumname, album.get(const.ID)])
            found += 1

    print(" matches made = " + str(found))
    return matches


def get_album(id: str, albums: Iterator):
    album = [{const.TITLE, ""}]

    return album
