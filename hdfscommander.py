import json
import requests
import os
from sys import argv

prog, server, port, user = argv

# server = 'localhost'
# port = '50070'
connstr = 'http://' + server + ':' + port + '/webhdfs/v1'
# user = 'trn'
current_path = '/user/' + user + '/'
local_path = os.getcwd()


def tryconn():
    op = 'LISTSTATUS'
    try:
        res = requests.get(connstr + current_path + '?\\user.name=' + user + '&op=' + op)
        if res:
            print('\n  -> CONNECTED.')
            menu()
        else:
            print('\n  <- AN HTTP ERROR OCCURED! - ', str(res.status_code))
            quit()
    except:
        print('\n  <- SEEMS CONNECTION WAS UNSUCCESSFUL OR YOU WAS DISCONNECTED.'
              '\n     Check connection data and try again.\n')
        quit()


def mkdir(param1, param2):
    op = 'MKDIRS'
    name = param1  # ДД: Проверить на нормальное название
    permnum = param2  # ДД: Проверить на нормальное число
    res = requests.put(connstr + current_path + name + '?\\user.name=' + user + '&op=' + op + '&permission=' + permnum)
    if res:
        parsed_res = json.loads(res.text)
        print('\n  -> MKDIR SUCCESS ' + str(parsed_res['boolean']) + ' -> ')
    else:
        print('\n -> GOT AN ERROR RESPONSE -> ')
    menu()


def put(param):
    op = 'CREATE'
    name = param  # ДД: Проверить на нормальное название
    res = requests.put(connstr + current_path + name + '?\\user.name=' + user + '&op=' + op, allow_redirects=False)
    if res.status_code == 307:
        print('\n  -> REDIRECTED (' + str(res.status_code) + ') -> ')
        redirect_url = res.headers['Location']
        reader = open(param)
        respost = requests.put(redirect_url, reader)
        if respost:
            print('  -> CREATE SUCCESS (' + str(respost.status_code) + ') ->')
            path_of_new_file = respost.headers['Location']
            path_of_new_file = path_of_new_file[path_of_new_file.find('0/') + 2:]
            print('  -> NEW FILE CREATED:', path_of_new_file)
        else:
            print('\n  -> GOT AN ERROR RESPONSE (on create) -> ')
            print(respost.status_code)
    else:
        print('\n  -> GOT AN ERROR RESPONSE (on redirect) -> ')
        print(res.status_code)
    menu()


def get(param):
    op = 'OPEN'
    name = param  # ДД: Проверить на нормальное название
    res = requests.get(connstr + current_path + name + '?\\user.name=' + user + '&op=' + op, allow_redirects=False)
    if res.status_code == 307:
        print('\n  -> REDIRECTED (' + str(res.status_code) + ') -> ')
        redirect_url = res.headers['Location']
        respost = requests.get(redirect_url)
        if respost:
            print('  -> GET SUCCESS (' + str(respost.status_code) + ') ->')
            writer = open(name, "w")
            writer.write(respost.text)
            writer.close()
        else:
            print('\n  -> GOT AN ERROR RESPONSE (on get) -> ')
    else:
        print('\n  -> GOT AN ERROR RESPONSE (on redirect) -> ')
    menu()


def append(param1, param2):
    op = 'APPEND'
    name = param2  # ДД: Проверить на нормальное название
    res = requests.post(connstr + current_path + name + '?\\user.name=' + user + '&op=' + op, allow_redirects=False)
    if res.status_code == 307:
        print('\n  -> REDIRECTED (' + str(res.status_code) + ') ->')
        redirect_url = res.headers['Location']
        reader = open(param1)
        respost = requests.post(redirect_url, reader)
        if respost:
            print('  -> APPEND SUCCESS (' + str(respost.status_code) + ') ->')
        else:
            print('\n  -> GOT AN ERROR RESPONSE (on append) ->')
    else:
        print('\n  -> GOT AN ERROR RESPONSE (on redirect) -> ')
    menu()


def delete(param1):
    op = 'DELETE'
    name = param1  # ДД: Проверить на нормальное название
    # rec_bool = param2                # ДД: Проверить на нормальное число
    res = requests.delete(connstr + current_path + name + '?\\user.name=' + user + '&op=' + op + '&recursive=true')
    if res:
        parsed_res = json.loads(res.text)
        print('\n  -> DELETE SUCCESS ->', parsed_res['boolean'])
    else:
        print('\n  -> GOT AN ERROR RESPONSE -> ')
    menu()


def ls():
    op = 'LISTSTATUS'
    path = 'user/trn/'
    res = requests.get(connstr + current_path + '?\\user.name=' + user + '&op=' + op)
    if res:
        print('\n  -> LISTSTATUS SUCCESS ->')
        parsed_res = json.loads(res.text)
        # print(json.dumps(parsed_res, indent=2, sort_keys=True))
        print('  -> ' + current_path + ' -> ')
        activecase = parsed_res['FileStatuses']['FileStatus']
        cols = 72
        print('      ' + 'FILEID'.ljust(10), 'NAME'.ljust(10), 'OWNER'.ljust(10), 'GROUP'.ljust(10),
              'PERMISSONS'.ljust(10), 'TYPE'.ljust(10))
        for item in activecase:
            print('   -  ' + str(item['fileId']).ljust(10), item['pathSuffix'].ljust(10),
                  item['owner'].ljust(10), item['group'].ljust(10), item['permission'].ljust(10),
                  item['type'].ljust(10))

    else:
        print('\n  -> GOT AN ERROR RESPONSE -> ')
    menu()


def cd(param):
    global current_path
    print('\n  -> CURRENT DIRECTORY IS: ' + current_path)
    changed_path = param
    if changed_path == '..':
        # changed_path = changed_path.rfind('/', 1)
        ch = current_path[:-1]
        current_path = ch[:ch.rfind('/') + 1]
        print('  -> CHANGED LOCATION TO:', current_path)
    elif changed_path == '.':
        pass
    elif changed_path[0] == '*':
        if changed_path[-1] == '/':
            current_path = changed_path[1:]
            print('  -> CHANGED LOCATION TO:', current_path)
        else:
            current_path = changed_path[1:] + '/'
            print('  -> CHANGED LOCATION TO:', current_path)
    else:
        if changed_path[-1] == '/':
            current_path = current_path + changed_path
            print('  -> CHANGED LOCATION TO:', current_path)
        else:
            current_path = current_path + changed_path + '/'
            print('  -> CHANGED LOCATION TO:', current_path)
    menu()


def lls():
    # LOCAL PROCEDURE!
    local_path = os.getcwd()
    print('\n  -> CURRENT LOCAL DIR:', local_path)
    print('  -> ' + local_path + ' -> ')
    # os.system('ls -la')
    print('      ' + 'NAME'.ljust(25), 'TYPE'.ljust(10))
    files = list(filter(os.path.isfile, os.listdir()))
    dirs = list(filter(os.path.isdir, os.listdir()))
    for item in dirs:
        print('   -  ' + item.ljust(25), 'DIRECTORY'.ljust(10))
    for item in files:
        print('   -  ' + item.ljust(25), 'FILE'.ljust(10))
    menu()


def lcd(param):
    global local_path
    print('\n  -> CURRENT DIRECTORY IS: ' + local_path)
    if param == '..':
        os.chdir('..')
        changed_path = os.getcwd()
        local_path = changed_path
        print('  -> CHANGED TO: ' + local_path)
    elif param == '.':
        pass
    elif param[0] == '*':
        os.chdir(param[1:])
        local_path = os.getcwd()
        print('  -> CHANGED TO: ' + local_path)
    else:
        os.chdir(param)
        local_path = os.getcwd()
        print('  -> CHANGED TO: ' + local_path)
    menu()


def help():
    print('\n  TRN / WEBHDFS COMMANDER / HTTP REST API \n'
          '  If you are in program, connection is successful.\n'
          '  to successfully connect use > python3 ./{hdfsagent.py} {ip} 50070 {username}\n\n'
          '  '
          '  Available commands:\n'
          '   - mkdir {dirname} {permissions in OCT} - Creating a HDFS directory in current path.\n'
          '      Example: $ > mkdir newdirectory 755\n'
          '   - put {localfile}                      - Upload file to HDFS current path.\n'
          '      Example: $ > put testfile.txt\n'
          '   - get {remotefile}                     - Download file to local path of your machine.\n'
          '      Example: $ > get testfile.hdp\n'
          '   - append {localfile} {remotefile}      - Append (concat) local file with remote file.\n'
          '      Example: $ > append test01 test02\n'
          '   - delete {remotefile}                  - Recursively delete file or directory on HDFS.\n'
          '      Example: $ > delete junkfolder\n'
          '   - ls                                   - List status of current path on HDFS.\n'
          '      Example: $ > ls\n'
          '   - cd [., .., {directory}, *{path}]     - Change directory of HDFS path recognition.\n'
          '      Example: $ > cd .                     .       - Is remain you into your current path.\n'
          '      Example: $ > cd ..                    ..      - Is moving you on level high.\n'
          '      Example: $ > cd intfolder             {dir}   - Is moving you to directory.\n'
          '      Example: $ > cd */user/wow            *{path} - Is moving you to absolute path.\n'
          '   - lls                                  - List status of local path.\n'
          '      Example: $ > lls\n'
          '   - lcd [., .., {directory}, *{path}]    - Change directory of local machine.\n'
          '      Example check out on "cd" command. All is the same.\n\n'
          '  WARN! Your LOCL and HDFS path is global variable. For perfect working\n'
          '        after changing directories (HDFS or LOCAL) type LS or LLS commands\n'
          '        for checking out paths to correct values.\n')
    menu()


def menu():
    print(('\n  <- HDFS PATH: ' + current_path))
    print(('  <- LOCL PATH: ' + local_path))

    chs = input(' $ > ')
    execute = list(chs.split(sep=' '))
    if execute[0] == 'mkdir':
        mkdir(execute[1], execute[2])
    elif execute[0] == 'put':
        put(execute[1])
    elif execute[0] == 'get':
        get(execute[1])
    elif execute[0] == 'append':
        append(execute[1], execute[2])
    elif execute[0] == 'delete':
        delete(execute[1])
    elif execute[0] == 'ls':
        ls()
    elif execute[0] == 'cd':
        cd(execute[1])
    elif execute[0] == 'lls':
        lls()
    elif execute[0] == 'lcd':
        lcd(execute[1])
    elif execute[0] == 'help' or execute[0] == '?':
        help()
    elif execute[0] == 'q':
        print('\n  -> DISCONNECT.')
        quit()
    elif execute[0] == '':
        menu()
    else:
        print('\n  -> UNSUPPORTED COMMAND, TRY > help or ? ')
        menu()


tryconn()
