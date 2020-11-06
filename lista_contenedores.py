#!/usr/bin/env python3
# -*- coding: utf-8 -*-

dock_list =  {
    "apache-proxy",
    "pspvApp",
    "pspvDB",
    "mysql8",
    "romWeb",
    "seoRomWeb",
    "iaRomWeb",
    "blogRomWeb",
    "notasRomWeb"
        
    }

docker_list = {
    "apacheproxy":"apache-proxy",
    "pspvapp":"pspvApp",
    "pspvDB":"pspvDB",
    "mysql8":"mysql8",
    "romsolutions":"romWeb",
    "seorom":"seoRomWeb",
    "iarom":"iaRomWeb",
    "blogrom":"blogRomWeb",
    "notas":"notasRomWeb"
    }


#List with file names and names of directory for mounts
files_mount_list = {
    "apache-proxy":"apacheproxy",
    "pspvApp":"pspvapp",
    "pspvDB":"pspvDB",
    "mysql8":"mysql8",
    "romsolutions":"romsolutions",
    "seoRom":"seorom",
    "iaRom":"iarom",
    "blogRom":"blogrom",
    "notas":"notas"
    }

mount_data_names_web = {
    "etc_",
    "log_",
    "www_"
    
    }

mount_data_names_db = {
    "etc_",
    "log_",
    "data_"
    }

docker_menu_start = {
    "[1] Download backups",
    "[2] Recovery backups",
    "[3] Edit list of images (docker_list)",
    "[4] Edit image_backup (change Name)",
    "[5] Create new container",
    "[6] Delete a container"
    "[A] Mode automate // Download, recovery and all images "
    "[9] Exit of script"
    
    }

