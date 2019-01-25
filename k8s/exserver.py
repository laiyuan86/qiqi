#对服务器的操作

import paramiko


class connect_server(object):

    #基于用户名和密码的sshclient方式登录
    def con_server_ssh_by_user_passwd(self, IP, PORT, USER, PASSWORD):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=IP, port=PORT, username=USER, password=PASSWORD)

        #去登录的服务器上操作
        while True:
            input_command = input('>>>:')
            if input_command == 'quit' or input_command == 'exit':
                break
            stdin, stdout, stderr = ssh.exec_command(input_command)
            result = stdout.read() #read方法读取输出结果
            if len(result) == 0: #判断如果输出结果长度等于0表示为错误输出
                print(stderr.read())
            else:
                print(str(result, 'utf-8'))
        ssh.close()

    #远程执行命令
    def ex_command(self, IP, PORT, USER, PASSWORD, COMMAND):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=IP, port=PORT, username=USER, password=PASSWORD)
        stdin, stdout, stderr = ssh.exec_command(COMMAND)
        result = stdout.read()
        if len(result) == 0:
            print(stderr.read())
        else:
            result = str(result, 'utf-8')
            print(result)
            return result


if __name__ == '__main__':
    IP = '172.24.132.182'
    PORT = 22
    USER = 'root'
    PASSWORD = 'sgdbyjc@2018'
    exconser = connect_server()
    exconser.con_server_ssh_by_user_passwd(IP, PORT, USER, PASSWORD)

