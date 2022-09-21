import re 
emails = ''' 
    https://www.google.com
    http://coreyms.com
    https://youtube.com
    https://www.nasa.com
'''
# pattern = re.compile(r'[a-zA-Z0-9.-]+@[a-zA-Z-]+\.(com|edu)')
pattern = re.compile(r'https?(www\.)?\w+\.\w+')
matches = pattern.finditer(emails)
for m in matches:
    print(m)