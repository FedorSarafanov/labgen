import os,subprocess

dest=os.path.realpath(__file__).replace('install.py','')
print(dest)
source=os.path.join(dest,'LAB')

def win_install_alias():
    with open(os.path.join(dest,'template.cmd'), "r") as lines:
        text=lines.read()
        text=text.replace(r'{0}','python '+os.path.join('',dest,'lab.py'))
        with open(os.path.join(dest,'aliases.cmd'), "w+") as f:
               f.write(text)
    with open(os.path.join(dest,'regadd_template.cmd'), "r") as lines:
        text=lines.read()
        text=text.replace(r'{0}','"'+os.path.join(dest,'aliases.cmd')+'"')
        with open(os.path.join(dest,'regadd.cmd'), "w+") as f:
               f.write(text)
    # subprocess.check_output(os.path.join(dest,'regadd.cmd'))     
    # добавит в cmd, но неудобно

    if git_aliases!='':
        with open(git_aliases, 'a') as file:
            file.write('\nalias lab='+"'"+'python "'+'/'.join(dest.split('\\'))+'/lab.py"'+"'")


def get_reg_entries(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]

    software_list = []

    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]
            software['location'] = winreg.QueryValueEx(asubkey, "InstallLocation")[0]
            software_list.append(software)
        except EnvironmentError:
            continue

    return software_list

if os.name=='nt':
    import winreg,re
    software_list = get_reg_entries(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) +\
                get_reg_entries(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) +\
                get_reg_entries(winreg.HKEY_CURRENT_USER, 0)

    git_aliases=editor_path=''
    for software in software_list:
        if 'Sublime Text' in software['name']:
            editor_path = r''+software['location']+'sublime_text.exe'
        if 'Git version' in  software['name']:
            git_aliases = os.path.join(software['location'],'etc','profile.d','aliases.sh')
    win_install_alias()
elif os.name=='posix':
    from os.path import expanduser
    home = expanduser("~")
    apps=os.listdir("/usr/bin")
    for app in apps:
        if 'subl' in app:
            editor_path = app
    with open(os.path.join(home,'.bashrc'), 'a') as file:
        file.write('\nalias lab='+"'"+'python "'+os.path.realpath(__file__).replace('install.py','')+'/lab.py"'+"'")    
# print(editor_path)
# 


