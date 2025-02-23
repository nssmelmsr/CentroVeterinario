import paramiko #para server SSH2

def crear_clienteSSH():
    ssh_client = paramiko.SSHClient()

    #credenciales de server remoto
    host = "hostname"     #cambiar
    username = "username" #cambiar
    password = "password" #cambiar
    port = 22             #puede cambiar

    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host,port=port,username=username,password=password)

    ## crear objeto cliente SFTP
    ftp = ssh_client.open_sftp()
    return ssh_client, ftp