#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 17:36:43 2020

@author: badrom
@function: Recovery Backup of image and volums of container creates in Rom1Server
@Need: Docker.io installed

"""

"""
    LIBRARYS
    os .> execute commnads, control directorys 
    
"""
import funct_deploy_rom1 as f
import actions as a
from lista_contenedores import dock_list 
from lista_contenedores import files_mount_list
from lista_contenedores import mount_data_names_web
from lista_contenedores import mount_data_names_db
from lista_contenedores import docker_list

"""
    CONSTANTS

"""
#Date of files to dowload
dateBackup = "_13_10_2020"

#Path to Server backup directory docker.tar/
bkp_server_docker   = "/backup/docker/"

#Path to Server backup directory Virtual HD
bkp_server_mounts   = "/backup/docker/Mounts/"

#Path Directory of Develop Machine 
dir_devel_Rom1      = "/home/badrom/Backup_Rom1Server/"  

#Path to Directory of devel virtual HD
dir_devel_mounts    = "/home/badrom/Discos_Virtuales/"

#Control File
log_control        = "/home/badrom/Backup_Rom1Server/logs/control_deploy_Rom1.log"

#Error File
log_error         = "/home/badrom/Backup_Rom1Server/logs/error_deploy_Rom1.log"

"""
    END CONSTANTS
"""
#
#Start Script
f.control_file(log_error)
f.control_file(log_control)

print()

title = "Iniciamos Deployment Rom1Server"
f.print_title(title)
f.write_log(log_control,title)

# # # 1
#Pass One - Download files backup
a.download_docks(dock_list)
a.download_mounts(files_mount_list)

# # #
# Pass Two - Stop and Removed old Containers
title = "Iniciando la parada e eliminación de los contenedores"
f.print_title(title)
f.write_log(log_control,title)
##############################################################################
a.stop_containers(dock_list)

# # # #
# # Pass Three - Deleted all old backup images
title = "Iniciando la eliminación de images backup"
f.print_title(title)
f.write_log(log_control,title)
##############################################################################
f.delete_old_images(dir_devel_Rom1,dateBackup,dock_list)


# # #
# Pass Three - removed old mounts, remove directorys, recovery mounts, recovery directory
# Recovery mounts Docker
title = "Iniciando el borrado de los discos dockers y creación de nuevo"
f.print_title(title)
msg = "[CTR] Iniciando el borrado de los discos dockers y creación de nuevo"
f.write_log(log_control,msg)
# #Recovery Mounts
title = "Eliminamos y Creamos los Discos Virtuales"
f.print_title(title)
msg = "Eliminamos y Creamos los Discos Virtuales"
f.write_log(log_control,msg)
f.recovery_mounts(files_mount_list,mount_data_names_web,mount_data_names_db,dir_devel_mounts)
###############################################################################
# Recovery directories
title = "Eliminamos  y Recuperamos los archivos "
f.print_title(title)
msg = "Eliminamos  y Recuperamos los archivos "
f.write_log(log_control,msg)
f.recovery_dirs(files_mount_list,mount_data_names_web,mount_data_names_db,dir_devel_mounts,dateBackup)
##############################################################################
######
#OJO!!!!
# Funciona bien, pero no esta borrando el directorio sobrante al terminar!!

# # #
# Pass Four - Up Containers with image recovered
title = "Iniciando Levantado de Contenedores"
f.print_title(title)
msg = "[CTR] Iniciando Levantado de Contenedores"
f.write_log(log_control,msg)


for dock in docker_list:
    cmd = f.startCommand(dock,mount_data_names_web,mount_data_names_db)
    cmd = f.finishCommand(dock,cmd,docker_list)
    print
    print("Levantando el contenedor :" +  dock)
    print("Con el comando: "+ cmd)
    f.up_container(cmd,dock)    
    
    
    
















    






