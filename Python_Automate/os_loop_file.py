import os
for folderName, subFolders, filenames in os.walk('/Users/weizheng/ebooks'):
    print('The current folder is ' + folderName)
    for subfolder in subFolders:
        print('SUBFOLDER OF ' + folderName + ': ' + subfolder)
    for filename in filenames:
        print('FILE INSIDE' + folderName + ': ' + filename)
print('done!') 