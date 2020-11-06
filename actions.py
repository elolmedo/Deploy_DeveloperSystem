#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 13:12:41 2020
@author: badrom
@function:  File to show agrupate functions executation
            of this app, Example: Communications, commad in Server, Command in local,etc. 
"""

import paramiko
import funct_deploy_rom1 as f
from os import sys
import os
import subprocess

'''Log files'''
log_control        = "/home/badrom/Backup_Rom1Server/logs/control_deploy_Rom1.log"
log_error         = "/home/badrom/Backup_Rom1Server/logs/error_deploy_Rom1.log"

"""
    CONSTANTS

"""
#Date of files to dowload
dateBackup = "_28_10_2020"
#Path to Server backup directory docker.tar/
bkp_server_docker   = "/backup/docker/"
#Path to Server backup directory Virtual HD
bkp_server_mounts   = "/backup/docker/Mounts/"
#Path Directory of Develop Machine 
dir_devel_Rom1      = "/home/badrom/Backup_Rom1Server/"  
#Path to Directory of devel virtual HD
dir_devel_mounts    = "/home/badrom/Discos_Virtuales/"


"""
    function: Function to download snapshot.tar from Rom1Server
"""
def download_docks(dock_list):
    
    msg = "Iniciamos descargas de los contenedores"
    f.write_log(log_control, msg)
    
    for dock in dock_list:        
        downloadDock(dock)
       
"""
    function: Function to download Virtual HD from Rom1Server
"""
def download_mounts(files_mount_list):
    
    msg = "Iniciamos descargas de los Discos Virtuales"
    f.write_log(log_control, msg)
    
    for mount in files_mount_list:        
        downloadMount(mount)
            
    
    msg = "Fin de la descarga de Discos Virtuales."
    f.write_log(log_control, msg)

def downloadDock(dock):
    
    user = "root"
    host = "91.121.90.206"        
    sshclient = paramiko.SSHClient()
    sshclient.load_system_host_keys()        
    sshclient.connect(hostname=host, username=user)
    
    path_server = bkp_server_docker+"backup_"+dock+""+dateBackup+".tar"
    path_home   = dir_devel_Rom1+"backup_"+dock+""+dateBackup+".tar"
                    
    sftp = sshclient.open_sftp()
    msg = "Descarga de "+path_server
    f.write_log(log_control, msg)
    try:
            sftp.get(path_server, path_home)            
            
    except FileNotFoundError:
        msg = "[ERR] File Not found Error: "+path_server                
        f.write_log(log_error, msg)        
        msg = "[ERR] File Not found Error: "+path_home
        f.write_log(log_error, msg)
    except:                    
        print("Error inesperado:", sys.exc_info()[0])
        f.write_log(log_error, msg)
    else:
        msg = "La descarga acabo correctamente"
        f.write_log(log_control, msg)            
    finally:
        sftp.close()

def downloadMount(mount):
    user = "root"
    host = "91.121.90.206"
    
    sshclient = paramiko.SSHClient()
    sshclient.load_system_host_keys()
    
    sshclient.connect(hostname=host, username=user)
    
    msg = "Inicio de la comprobación de directorios en local: "+dir_devel_mounts+"VHD_"+mount+"/"
    f.write_log(log_control, msg)
                          
    if (os.path.exists(dir_devel_mounts+"VHD_"+mount+"/") == True):
        msg = "[OK] El directorio existe en servidor de Desarrollo."
        f.write_log(log_control,msg)
    else:
        try:
            msg = "[WR!] El directorio de Descarga, lo creamos"
            f.write_log(log_control,msg)
            os.mkdir(dir_devel_mounts+"VHD_"+mount+"")
            
        except FileNotFoundError:
            msg = "[ERR] File Not found Error: "+dir_devel_mounts+"VHD_"+mount+""
            f.write_log(log_error, msg)
        except:
            msg = "Error inesperado:", sys.exc_info()[0]
            f.write_log(log_error, msg)
        else:
            msg = "Directorio creado con éxito"
            f.write_log(log_control, msg)
        finally:
            msg = "Operación creación directorio, terminada!"
            f.write_log(log_control, msg)
     
    path_server = bkp_server_mounts+"VHD_"+mount+"/VHD_"+mount+""+dateBackup+".tar"
    path_home   = dir_devel_mounts+"VHD_"+mount+"/VHD_"+mount+""+dateBackup+".tar"
         
    sftp = sshclient.open_sftp()
    msg = "Descarga de "+path_server
    f.write_log(log_control, msg)
    
    try:
        sftp.get(path_server, path_home)            
        
    except FileNotFoundError:
        msg = "[ERR] File Not found Error: "+path_server                
        f.write_log(log_error, msg)        
        msg = "[ERR] File Not found Error: "+path_home
        f.write_log(log_error, msg)
    except:                    
        print("Error inesperado:", sys.exc_info()[0])
        f.write_log(log_error, msg)
    else:
        msg = "La descarga acabo correctamente"
        f.write_log(log_control, msg)            
    finally:
            sftp.close()

def stop_dock(dock):
    value = subprocess.call('docker stop '+dock, shell=True)        
    if value > 0:
        msg = "El container "+dock+" NO existe, continuámos con el siguiente. "
        f.write_log(log_control, msg)
        
    else : 
        msg = "El Contenedor dock ha sido parado. Prodecemos a su eliminación"
        f.write_log(log_control, msg)
        """
            DELETE OLD CONTAINER
        """
        newvalue = subprocess.call('docker rm '+dock, shell=True)
        if newvalue > 0:
            msg = "[ERR] El container "+dock+" NO ha podido ser parado. "
            f.write_log(log_error,msg)
        else:
            msg = "El container "+dock+" ha sido eliminado"
            f.write_log(log_control, msg)

def stop_containers(dock_list):
    
    msg = "Parada de contenedores en el equipo Local"
    f.print_title(msg)
        
    for dock in dock_list:        
        msg = "Iniciando parada del contenedor: "+dock
        print(msg)                
        """
            STOP OLD CONTAINERS
        """
        stop_dock(dock)

"""
    function: Deleted concreted image
"""
def delete_image(dock):
    cmd = 'docker inspect --format {{.Id}} '+'backup_'+dock.lower()
    idcontainer = subprocess.check_output(cmd,shell=True)
    idimage = idcontainer.decode("utf-8").split(":")
    msg = "INIT Procces to eliminate image backup_"+dock+" con Id: "+idimage[1]
    f.write_log(log_control, msg)
    
    cmd = "docker image rm "+idimage[1]
    rvalue = subprocess.call(cmd, shell=True)    
    if rvalue > 0:
        msg = "[ERR] Error al Eliminar la imagen backup_"+dock.lower()
        f.write_log(log_error, msg)
    else:
        msg = "[CTR] La imagen se eliminó correctamente."
        f.write_log(log_control, msg)

def delete_all_images(dock_list):
    for image in dock_list:
        delete_image(image)
