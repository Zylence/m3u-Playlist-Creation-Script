#For documentation refer to my Github: https://github.com/Zylence/m3u-Playlist-Creation-Script
import os
from optparse import OptionParser

def scanDirectories():
    """Scans 'startDirectory' and all subdirectories for all files listed in 'acceptedFormats' and
    writes them to a dictionary mapping files to a list of paths.
    """
    foundFiles = dict()
    for root, dirs, files in os.walk(startDirectory):
        if os.path.split(root)[1] not in excludeDirectories:
            for file in files:
                if os.path.splitext(file)[1] in acceptedFormats:
                    foundFiles.setdefault(file, []).append(root)
    return foundFiles


def createPathsHelper(filename, path):
    """Returns an absolute or relative path according to the'absolutePaths' variable.
    """

    if absolutePaths:
        return str(path + "/" + filename)
    else:
        return str(path.split(startDirectory)[1] + "/" + filename)


def createPaths(files):
    """Takes a dictionary of files mapping to paths. Returns a list of absolute or
    relative paths with duplicates either removed or not.
    """

    resPaths = []
    for filename, paths in files.items():    # paths is a list
        if removeDuplicates:
            # discard all but the first path
            resPaths.append(createPathsHelper(filename, paths[0]))
        else:
            # keep all paths
            for path in paths:
                resPaths.append(createPathsHelper(filename, path))
    return resPaths


def writePlaylist(paths):
    """Writes all the 'paths' into a playlist file named 'fileName' using 'mode'
    as method of writing.
    """

    f = open(fileName, mode, encoding=codec)
    for path in paths:
        f.write(path + "\n")
    f.close()


if __name__ == "__main__":
    # args parsing
    parser = OptionParser()
    parser.add_option("-n", metavar="fileName", default="playlist.m3u",
                      help="the name of your playlist, use '.m3u' extension")
    parser.add_option("-m", metavar="mode", default="w",
                      help="mode used for writing, choose 'a' to append, and 'w' to overwrite the playlist file")
    parser.add_option("-c", metavar="codec", default="utf-8",
                      help="codec used for opening (writing) a file")
    parser.add_option("-s", metavar="startDirectory", default=os.getcwd(),
                      help="the starting directory for the script to scan for music files, usually your music library")
    parser.add_option("-e", metavar="excludedDirectories", default="",
                      help="string containing subdirectories separated by whitespaces, e.g.: 'Celtic Classic' will "
                           "not be included in the playlist")
    parser.add_option("-d", metavar="removeDuplicates", default=False,
                      help="boolean determining whether or not to exclude duplicate files from the playlist")
    parser.add_option("-a", metavar="absolutePaths", default=True,
                      help="boolean determining whether to use absolute paths")
    parser.add_option("-f", metavar="acceptedFormats", default=".mp3 .flac .wav .aac",
                      help="string containing file formats separated by whitespaces, e.g.: '.mp3 .flac'")
    (options, args) = parser.parse_args()

    # if you prefer hard coding - edit those assignments
    fileName = options.n
    mode = options.m
    codec = options.c
    startDirectory = options.s
    excludeDirectories = options.e.split()
    removeDuplicates = options.d
    acceptedFormats = options.f.split()
    absolutePaths = options.a

    # main script
    foundFiles = scanDirectories()
    paths = createPaths(foundFiles)
    writePlaylist(paths)
