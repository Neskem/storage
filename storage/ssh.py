from time import sleep
import paramiko

class SSHException(Exception):
    pass

class SSHConnectionException(SSHException):
    pass

class SSHCommandException(SSHException):
    pass

class SSHSession:
    def __init__(self, host, username, password, timeout=60):
        self.host = host
        self.username = username
        self.password = password
        self.timeout = timeout
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __enter__(self):
        try:
            self.ssh.connect(hostname=self.host, username=self.username, password=self.password, timeout=self.timeout, look_for_keys=False)
        except paramiko.BadHostKeyException:
            raise SSHConnectionException('SSH Server host key could not be verified')
        except paramiko.AuthenticationException:
            raise SSHConnectionException('SSH Authentication failed')
        except paramiko.SSHException as e:
            raise SSHConnectionException(f'Paramiko SSH Connection Problem: {e}')
        except Exception as e:
            raise SSHConnectionException(f'SSH Connection Exception: {e}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            sleep(2)
            self.ssh.close()
        except Exception:
            pass

    def execute_command(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            output = stdout.readlines()
            error = stderr.readlines()
            return output, error
        except Exception as e:
            raise SSHCommandException(f'Unable to run given command "{command}": {e}')

# 使用示例：
# with SSHSession(host, username, password) as ssh:
#     output, error = ssh.execute_command('ls -l')
#     print('Output:', output)
#     print('Error:', error)
