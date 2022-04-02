# FireTongue DB export parser
#
#  to run this tool the commandline is py main.py <filename>[.txt|.oxl|.xml]
#
# useful resources
# https://flask.palletsprojects.com/en/2.1.x/
# https://docs.python.org/3/library/xml.etree.elementtree.html

from typing import Iterator, List
from flask import Flask, request, render_template
import xml.etree.ElementTree as ET
import sys
import constants


argStr = ""
argLower = ""
root = None

arg_len = len(sys.argv)
print("No. args " + str(arg_len))
print("args " + str(sys.argv))

for i, arg in enumerate(sys.argv):
    print("arg " + str(i) + " is " + sys.argv[i])

for i, arg in enumerate(sys.argv):
    argLower = arg.lower()
    print("arg=" + argLower)
    if (argLower.endswith(".txt")):
        fileHandle = open(arg, "r")
        argStr += fileHandle.read() + "</p>"
        print("Read " + argLower)
    elif (argLower.endswith(".xml") or argLower.endswith(".oxl")):
        print("Read XML " + argLower)
        tree = ET.parse(argLower)
        root = tree.getroot()
    else:
        argStr += ">" + arg + "< !=  a readable file - will switch to default"
        argLower = ""

    print(argStr)
    if (len(argLower) == 0):
        argLower = "firetongue.oxl"


app = Flask(__name__)

if (root == None):
    tree = ET.parse(argLower)

root = tree.getroot()


def extractSearchCriteria(args, baseUrl: str):
    """
    Locates the search parameter and returns it

    Args:
        args (_type_): MultiDict structure defined by Flask
        baseUrl (str): _description_
    ToDo: handle white space etc in the search string
    Returns:
        str: Search name to use
    """
    searchStr = args.get("search")

    print("Search request using >" + str(searchStr) + "<")
    return searchStr


def extractIdCriteria(args, baseUrl: str):
    """
    Locates the id parameter and returns it

    Args:
        args (_type_): MultiDict structure defined by Flask
        baseUrl (str): _description_

    Returns:
        str: Search name to use
    """
    id_str = args.get("id")

    print("Search request using >" + str(id_str) + "<")
    return id_str


def listout(my_list: list):
    pretty_list = ""
    for my_item in my_list:
        if (isinstance(my_item, str)):
            pretty_list += str(my_item) + "</br>"
        elif ((isinstance(my_item, (tuple, list)))):
            pretty_list += str(my_item[0]) + " : " + str(my_item[1]) + "</br>"
        else:
            print("unknown type")
    return pretty_list


def matchedAlbum(name: str, albums: Iterator):
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
        albumname = album.find(constants.TITLE).text
        if ((albumname != None) and (albumname.find(name) > 0)):
            matches.append([albumname, album.get(constants.ID)])
            found += 1

    print(" matches made = " + str(found))
    return matches


@ app.route('/help')
def params():
    return "TODO: Add Help info here"


@ app.route('/test/')
def test():
    return render_template('test.html', my_string="This a test, do not panic",
                           my_list=["Album 1", "Album 2", "Album 3", "Album 4"])


@ app.route('/test2')
def test2():
    result = ""
    for child in root:
        result += child.tag + "</p>"

    result += "------</p>"
    for child in root.iter(constants.ALBUM):
        print(child.find(constants.TITLE).text)
        # result += child.get('Title') + "</p>"
    return result


@ app.route('/album')
def listAlbums():
    root = tree.getroot()
    id = None
    search = extractSearchCriteria(request.args, request.base_url)
    if ((search == None) or (len(search) < 1)):
        id = extractIdCriteria(request.args, request.base_url)
    else:
        albums = listout(matchedAlbum(search, root.iter(constants.ALBUM)))
    return albums


if __name__ == '__main__':
    app.run(debug=True, port=constants.PORT, host=constants.HOST)
