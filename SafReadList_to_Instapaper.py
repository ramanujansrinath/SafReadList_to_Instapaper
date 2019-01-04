import plistlib

INPUT_FILE  = 'Bookmarks.plist'
exportFile = 'instapaperImport.csv'

# I think, because of SIP, I can't access the plist file anymore.
# Copy it to the current folder. It is in "/Users/USERNAME/Library/Safari/"
with open(INPUT_FILE, 'rb') as plist_file:
    plist = plistlib.load(plist_file)

# Look for the child node which contains the Reading List data.
# There should only be one Reading List item
children = plist['Children']
for child in children:
    if child.get('Title', None) == 'com.apple.ReadingList':
        reading_list = child

# Extract the bookmarks
bookmarks = reading_list['Children']

# For each bookmark in the bookmark list, grab the URL and the URI which contains the saved title
urls = (bookmark['URLString'] for bookmark in bookmarks)
titles = (bookmark['URIDictionary'] for bookmark in bookmarks)

# Instapaper imports a csv in "URL,Title,Selection,Folder" format
# have the selection be empty and the status be unread
text = []
for url,title in zip(urls,titles):
    text.append(url.strip() + ',' + title['title'].strip() + ',,Unread')

# write to a csv file to import to Instapaper
with open(exportFile, 'w') as f:
    f.write("%s\n" % 'URL,Title,Selection,Folder')
    for item in text:
        f.write("%s\n" % item)