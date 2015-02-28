import configparser

cp = configparser.ConfigParser()

f = '''
[DEFAULT]
name = Simon
age = 18
good = yes
bad = false

[shiyang]
name = Shiyang
age = 17
good = false
bad = no

[simontang]
name = Simon Tang
'''

cp.read_string(f)

print(cp.sections())
print(cp.getboolean("shiyang", "good"))
print(cp.getint("simontang", "age"))
print(cp["simontang"].popitem)
