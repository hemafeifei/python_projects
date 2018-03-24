#! python3
# Adds bullet point to each line
import pyperclip

#在外面copy一段文字
# text = pyperclip.paste()

#打开一个本地文件并读取它
fobj = open('/Users/weizheng/Data/NYC_TAXI/readme.txt')
text = fobj.read()

# TODO: Separate lines and stars.
lines = text.split('\n')
for i in range(len(lines)):
    lines[i] = '*' + lines[i]
#连接修改过的行
text = '\n'.join(lines)

#将处理后的内容复制到剪贴板
pyperclip.copy(text)

