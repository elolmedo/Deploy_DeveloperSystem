#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created on Tue Oct  6 17:36:43 2020

@author: badrom
@Need: Library of functions for deploy docker in rom1

"""
from os import sys
import os
import subprocess
from datetime import datetime
import paramiko


#Control File
log_control        = "/home/badrom/Backup_Rom1Server/logs/control_deploy_Rom1.log"

#Error File
log_error         = "/home/badrom/Backup_Rom1Server/logs/error_deploy_Rom1.log"


def create_file (file):
    try:
        with open(file,'w') as fileopen:
            return fileopen.read()
    except:
        print("Error inesperado:", sys.exc_info()[0])
        
    else:
        msg = "El fichero "+ file +" se creo con éxito"
        print(msg)
    finally:
        msg = "Contínuamos la deployment de los Docker Rom1"
        print(msg)

def control_file (file):
        
    try:             
        with open(file, 'r') as fileopen:
            return fileopen.read()    
        
    except FileNotFoundError:
        msg = "El fichero no existe, procedemos a su creación..."
        print(msg)
        create_file(file)
                
    except:
        print("Error inesperado:", sys.exc_info()[0])
        
    else:
        #No exception, run this code
        msg = "El fichero "+file+" se abrío éxito"
        print(msg)
            
    finally:
        #Always run this code
        msg = "Fin de control del fichero "
        print(msg)
        
def now():
    now = datetime.now()
    nowformat = now.strftime('%d/%m/%Y - %H:%M:%S')
    return nowformat
        
def write_log (file,msg):    
    print(msg)
    file = open(file,"a")
    nowformat = now()
    file.write(msg+" [DATE "+nowformat+" ]\n")
    file.close()
    
def print_title(msg):
    print(msg)
    print()

    
def printTitle(msg):
    cmd = "figlet -f digital " + msg
    title = subprocess.call(cmd,shell=True)
    print(title)

def showMenuPrincipal():
    #Menu Principal
    for menu in docker_menu_start:    
        print(menu);
    
    msg = "Select a option:  "    
    option = int(input(msg))
    return option


    


"""
    function: Function to download snapshot.tar from Rom1Server
"""
def download_docks(bkp_server_docker,dir_devel_Rom1,dateBackup,dock_list):
    
    msg = "Iniciamos descargas de los contenedores"
    write_log(log_control, msg)
    
    for dock in dock_list:        
        user = "root"
        host = "91.121.90.206"
        
        sshclient = paramiko.SSHClient()
        sshclient.load_system_host_keys()
        
        sshclient.connect(hostname=host, username=user)
        
        path_server = bkp_server_docker+"backup_"+dock+""+dateBackup+".tar"
        path_home   = dir_devel_Rom1+"backup_"+dock+""+dateBackup+".tar"
                        
        sftp = sshclient.open_sftp()
        msg = "Descarga de "+path_server
        write_log(log_control, msg)
        
        try:
            sftp.get(path_server, path_home)            
        except:
            msg = "[ERR]] Fallo al descargar: "+path_server
            write_log(log_error, msg)
        else:
            msg = "La descarga acabo correctamente"
            write_log(log_control, msg)            
        finally:
            sftp.close()
            
    
    msg = "Fin de la descarga de contenedores."
    write_log(log_control, msg)
    
"""
    function: Function to download Virtual HD from Rom1Server
"""
def download_mounts(bkp_server_mounts,                   
                   dir_devel_mounts,
                   dateBackup,files_mount_list):
    
    msg = "Iniciamos descargas de los Discos Virtuales"
    write_log(log_control, msg)
    
    for mount in files_mount_list:        
        user = "root"
        host = "91.121.90.206"
        
        sshclient = paramiko.SSHClient()
        sshclient.load_system_host_keys()
        
        sshclient.connect(hostname=host, username=user)
        
        msg = "Inicio de la comprobación de directorios en local: "+dir_devel_mounts+"VHD_"+mount+"/"
        write_log(log_control, msg)
                              
        if (os.path.exists(dir_devel_mounts+"VHD_"+mount+"/") == True):
            msg = "[OK] El directorio existe en servidor de Desarrollo."
            write_log(log_control,msg)
        else:
            try:
                msg = "[WR!] El directorio de Descarga, lo creamos"
                write_log(log_control,msg)
                os.mkdir(dir_devel_mounts+"VHD_"+mount+"")
                
            except FileNotFoundError:
                msg = "[ERR] File Not found Error: "+dir_devel_mounts+"VHD_"+mount+""
                write_log(log_error, msg)
            except:
                msg = "Error inesperado:", sys.exc_info()[0]
                write_log(log_error, msg)
            else:
                msg = "Directorio creado con éxito"
                write_log(log_control, msg)
            finally:
                msg = "Operación creación directorio, terminada!"
                write_log(log_control, msg)

            
            
        path_server = bkp_server_mounts+"VHD_"+mount+"/VHD_"+mount+""+dateBackup+".tar"
        path_home   = dir_devel_mounts+"VHD_"+mount+"/VHD_"+mount+""+dateBackup+".tar"
             
        sftp = sshclient.open_sftp()
        msg = "Descarga de "+path_server
        write_log(log_control, msg)
        
        try:
            sftp.get(path_server, path_home)            
            
        except FileNotFoundError:
                msg = "[ERR] File Not found Error: "+path_server                
                write_log(log_error, msg)        
                msg = "[ERR] File Not found Error: "+path_home
                write_log(log_error, msg)
        except:                    
            print("Error inesperado ostia:", sys.exc_info()[0])
            write_log(log_error, msg)
        else:
            msg = "La descarga acabo correctamente"
            write_log(log_control, msg)            
        finally:
            sftp.close()
            
    
    msg = "Fin de la descarga de Discos Virtuales."
    write_log(log_control, msg)
                
"""
    function:   Function to  stop all container if the container is stop process
                to eliminate container
"""
def stop_containers(dock_list):
    for dock in dock_list:
        
        msg = "Tratamiento del contenedor "+dock
        print(msg)                
        """
            STOP OLD CONTAINERS
        """
        value = subprocess.call('docker stop '+dock, shell=True)
        
        if value > 0:
            msg = "El container "+dock+" NO existe, continuámos con el siguiente. "
            write_log(log_control, msg)
            
        else : 
            msg = "El Contenedor dock ha sido parado. Prodecemos a su eliminación"
            write_log(log_control, msg)
            """
                DELETE OLD CONTAINER
            """
            newvalue = subprocess.call('docker rm '+dock, shell=True)
            if newvalue > 0:
                msg = "[ERR] El container "+dock+" NO ha podido ser parado. "
                write_log(log_error,msg)
            else :
                msg = "El container "+dock+" ha sido eliminado"
                write_log(log_control, msg)

"""
    Function: Function for recovery a image docker with file.tar
"""
def create_image(dir_devel_Rom1,dock,dateBackup):
     cmd = "docker load -i "+dir_devel_Rom1+"backup_"+dock+""+dateBackup+".tar"
     file = dir_devel_Rom1+"backup_"+dock+""+dateBackup+".tar"
     msg = "[CTR] Iniciando proceso de recuperación de Imagen docker"
     write_log(log_control,msg)
     
     rvalue = subprocess.call(cmd,shell=True)
     if rvalue > 0:
         msg = "[ERR] Al intentar recuperar la imagen: "+file
         write_log(log_error, msg)
     else:
         msg = "[CTR] La imagen fue recuperada con éxito"
         write_log(log_control, msg)                               

"""
    function: Deleted concreted image
"""
def delete_image(dir_devel_Rom1,dock,dateBackup):
    cmd = 'docker inspect --format {{.Id}} '+'backup_'+dock.lower()
    idcontainer = subprocess.check_output(cmd,shell=True)
    idimage = idcontainer.decode("utf-8").split(":")
    msg = "INIT Procces to eliminate image backup_"+dock+" con Id: "+idimage[1]
    write_log(log_control, msg)
    
    cmd = "docker image rm "+idimage[1]
    rvalue = subprocess.call(cmd, shell=True)
    
    if rvalue > 0:
        msg = "[ERR] Error al Eliminar la imagen backup_"+dock.lower()
        write_log(log_error, msg)
    else:
        msg = "[CTR] La imagen se eliminó correctamente."
        write_log(log_control, msg)
        create_image(dir_devel_Rom1,dock,dateBackup)
               
"""
    function:  Function to find all backup_images, if this exists process to delete
               and create the new backup_image, if no exist process to create new
               backup image
"""    
def delete_old_images(dir_devel_Rom1,dateBackup,dock_list):
    for dock in dock_list:
        #Search image
        cmd = 'docker image ls | grep backup_'+dock.lower()+' | cut -d" " -f1'
        value = subprocess.check_output(cmd,shell=True)
        if not value:
            msg = "Imagen no encontrada procedemos a su creación."
            write_log(log_error, msg)
            create_image(dir_devel_Rom1, dock, dateBackup)
            
        else:
            msg = "Imagen encontrada procedemos a su eliminación."
            write_log(log_control, msg)
            delete_image(dir_devel_Rom1,dock,dateBackup)
            
"""
    Function: Create a new local persist
"""
def create_local_persist(dir_devel_mounts,mount,pre,nameM):
    cmd = "docker volume create -d local-persist -o mountpoint="+dir_devel_mounts+"VHD_"+mount+"/"+pre.replace('_','')+" --name="+nameM 
    rvalue = subprocess.call(cmd,shell=True)
    if rvalue > 0:
        msg = "[ERR] Error en la creación del Disco virtual."
        write_log(log_error, msg)
    else:
        msg = "[CTR] Disco Virtual: "+nameM+" creado con éxito!"
        write_log(log_control, msg)

""" 
    Function: List a docker with Name
"""
def list_dock_in_os(nameM):
     cmd = "docker volume ls -f name="+nameM+" | wc -l"
     rvalue = subprocess.check_output(cmd, shell=True)
     value = int(rvalue.decode('utf-8'))
     return value
                 
"""
    Function: remove a volume with name
"""
def remove_local_volume(nameM):
    cmd = "docker volume rm -f "+nameM
    rvalue = subprocess.call(cmd,shell=True)
    if rvalue > 0:
        msg = "[ERR] Error en la eliminación del Disco virtual."
        write_log(log_error, msg)
        exit(1)
    else:
        msg = "[CTR] Disco Virtual: "+nameM+" eliminado con éxito!"
        write_log(log_control, msg)
"""
    
    Function: removed old mounts and recovery mounts
"""        
def recovery_mounts(files_mount_list,mount_data_names_web,mount_data_names_db,dir_devel_mounts):
    msg = "[CTR] Iniciando recuperación de mounts dockers"
    write_log(log_control, msg)
    
    for mount in files_mount_list:
        if ((mount == "pspvDB") or (mount == "mysql8")):            
            for pre in mount_data_names_db:
                
                nameM = pre+files_mount_list[mount]                
                msg = "[CTR] Iniciando la recuperación del disco: "+nameM
                write_log(log_control, msg)
                msg = " [CTR] Comprobamos su existencia."
                write_log(log_control, msg)                
                
                value = list_dock_in_os(nameM)
                
                if value > 1:
                    msg = "[CTR] La disco virtual existe, procedemos a su eliminación."
                    write_log(log_control, msg)                
                    remove_local_volume(nameM)
                    
                elif value == 1:
                    msg = "[CTR] El volumen docker "+nameM+" no existe."
                    write_log(log_control,msg)
                    msg = "[CTR] Procedemos a la creación del volumen docker "+nameM
                    write_log(log_control,msg)
                    create_local_persist(dir_devel_mounts,mount,pre,nameM)
                
        else:
             for pre in mount_data_names_web:
                nameM = pre+files_mount_list[mount]                
                
                msg = "[CTR] Iniciando la recuperación del disco: "+nameM
                write_log(log_control, msg)
                msg = " [CTR] Comprobamos su existencia."
                write_log(log_control, msg)                
                
                value = list_dock_in_os(nameM)
               
                if value > 1:
                    msg = "[CTR] La disco virtual existe, procedemos a su eliminación."
                    write_log(log_control, msg)                   
                    remove_local_volume(nameM)

                        
                elif value == 1:
                    msg = "[CTR] El volumen docker "+nameM+" no existe."
                    write_log(log_control,msg)
                    msg = "[CTR] Procedemos a la creación del volumen docker "+nameM
                    write_log(log_control,msg)                   
                    create_local_persist(dir_devel_mounts,mount,pre,nameM)


"""
    Function: removed old dirs and recovery dirs
"""
def recovery_dirs(files_mount_list,mount_data_names_web,mount_data_names_db,dir_devel_mounts,dateBackup):
    msg = "[CTR] Iniciando Recuperación de directorios"
    write_log(log_control, msg)

            
    for mount in files_mount_list:
        if ((mount == "pspvDB") or (mount == "mysql8")):
            for pre in mount_data_names_db:
                 msg = "[CTR] Nos aseguramos de eliminar los archivos antiguos."
                 write_log(log_control, msg)
                 
                 msg = "[CTR] Eliminando los archivos de "+dir_devel_mounts+"VHD_"+mount+"/"+pre.replace('_','')
                 write_log(log_control, msg)
                 
                 cmd = "rm -rf "+dir_devel_mounts+"VHD_"+mount+"/"+pre.replace('_','')+"/*"
                 os.system(cmd)
                 msg = "[CTR] Archivos eliminados"                 
                 write_log(log_control, msg)
                 
                 msg = "[CTR] Iniciamos Descompresión del backup de Disco"
                 write_log(log_control, msg)
                 #Eliminamos el primer caracter de
                 dir_extrac = dir_devel_mounts[1:]
                 cmd = "tar -xvf "+dir_devel_mounts+"VHD_"+mount+"/VHD_"+mount+dateBackup+".tar "+dir_extrac+"VHD_"+mount+"/"+pre.replace('_','')                 
                 os.system(cmd)
                 
                 #Cambiar permisos directorio o usuario que ejecuta la acción de descompresión
                 #@TODO
                 
                 
                 msg = "[CTR] Copia de Archivos en el directorio correcto"
                 write_log(log_control, msg)                 
                 cmd = "cp -rf "+dir_extrac+"VHD_"+mount+"/"+pre.replace('_','')+"/* "+dir_devel_mounts+"VHD_"+mount+"/"+pre.replace('_','')+"/"
                 os.system(cmd)
  
        else:
            for pre in mount_data_names_web:
                msg = "[CTR] Nos aseguramos de eliminar los archivos antiguos."
                write_log(log_control, msg)
                
                msg = "[CTR] Eliminando los archivos de "+dir_devel_mounts+"VHD_"+mount+"/"+pre.replace('_','')
                write_log(log_control, msg)
                
                cmd = "rm -rf "+dir_devel_mounts+"VHD_"+mount+"/"+pre.replace('_','')+"/*"
                os.system(cmd)
                msg = "[CTR] Archivos eliminados"                 
                write_log(log_control, msg)
                
                msg = "[CTR] Iniciamos Descompresión del backup de Disco"
                write_log(log_control, msg)
                #Eliminamos el primer caracter de
                dir_extrac = dir_devel_mounts[1:]
                cmd = "tar -xvf "+dir_devel_mounts+"VHD_"+mount+"/VHD_"+mount+dateBackup+".tar "+dir_extrac+"VHD_"+mount+"/"+pre.replace('_','')                 
                os.system(cmd)
                
                #Cambiar permisos directorio o usuario que ejecuta la acción de descompresión
                #@TODO
                
                
                msg = "[CTR] Copia de Archivos en el directorio correcto"
                write_log(log_control, msg)                 
                cmd = "cp -rf "+dir_extrac+"VHD_"+mount+"/"+pre.replace('_','')+"/* "+dir_devel_mounts+"VHD_"+mount+"/"+pre.replace('_','')+"/"
                os.system(cmd)
                
        
        
        msg = "[CTR] Fin de las copias de los directorios."
        write_log(log_control, msg)
        msg = "[CTR] Procedemos a la eliminación del direcotorio sobrante"
        write_log(log_control, msg)
        
        cmd = "rm -rf /home/badrom/Workspace/pythonSpace/Deploy_RomSolutions/home/"
        os.system(cmd)
                
"""
    Fucntion: Create First part of command to UP Container
"""


"""
    Function: Start Command to up de containers
"""        
def startCommand(dock,mount_data_names_web,mount_data_names_db):
    #docker list
    #-> lower to name of image: backup_pspvdb
    #-> name of Containers
    
    #files_mount_list
    #-> names of Mounts
    
    msg = "Iniciamos todos los contenedores con sus Discos Virtuales"
    write_log(log_control, msg)

    ##Create a comand docker run until Mounts
    
    cmd = "docker run -d " 
    msg = "Creando el comando necesario..."
    write_log(log_control, msg)
    
    if (dock == "mysql8"):
        cmd += "-e MYSQL_ROOT_PASSWORD=al19rab3$ "
        for pre in mount_data_names_db:
            namedock = str(dock)
            nameVolume = pre+namedock
            if pre == "data_":
                cmd += "-v "+nameVolume+":/var/lib/mysql "
                        
            elif pre == "log_":   
                cmd += "-v "+nameVolume+":/var/"+pre.replace('_','')+" "
            else:
                cmd += "-v "+nameVolume+":/"+pre.replace('_','')+" "
               
    elif (dock == "pspvDB"):
        cmd += "-e POSTGRES_PASSWORD=al19rab3$ "
        for pre in mount_data_names_db:
            namedock = str(dock)
            nameVolume = pre+namedock
            if pre == "data_":
                cmd += "-v "+nameVolume+":/var/lib/postgresql/"+pre.replace('_','')+" "                       
            elif pre == "log_":   
                cmd += "-v "+nameVolume+":/var/"+pre.replace('_','')+" "
            else:
                cmd += "-v "+nameVolume+":/"+pre.replace('_','')+" "
    elif (dock == "apacheproxy"):
        for pre in mount_data_names_web:
            namedock = str(dock)
            nameVolume = pre+namedock            
            if ((pre == "log_") or (  pre == "www_")):
                cmd += "-v "+nameVolume+":/var/"+pre.replace('_','')+" "
            else:
                cmd += "-v "+nameVolume+":/"+pre.replace('_','')+" "
        cmd += '-p 80:80 -p 443:443 '

    else:
        for pre in mount_data_names_web:
            namedock = str(dock)
            nameVolume = pre+namedock            
            if ((pre == "log_") or (  pre == "www_")):
                cmd += "-v "+nameVolume+":/var/"+pre.replace('_','')+" "
            else:
                cmd += "-v "+nameVolume+":/"+pre.replace('_','')+" "
    return cmd
            
"""
    Function: Finish command with Name of container and add de correct image
    to recovery
"""
def finishCommand(dock,cmd,docker_list):    
    cmd += "--name " + docker_list[dock] + " "    
    cmd += " backup_"+docker_list[dock].lower()
    return cmd        
        
"""
    Function: Lanzamos el comando para levantart el contenedor pasado 
"""    
def up_container(cmd,dock):    
    value = subprocess.call(cmd, shell=True)
    if value > 0:
        msg = "[ERR] Error al levantar el container: "+dock
        write_log(log_error, msg)
        write_log(log_control, msg)
    else:
        msg = "[CTR] OK! Container levantado de forma correcta. Dock: "+dock
        write_log(log_control, msg)
        
        
        
        
    

            
    
        
        
        
        
        
                
        
        
            
        
        
        
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        
        
        
        
    
        
        