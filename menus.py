#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 13:12:41 2020
@author: badrom
@function:  File to show agrupate functions to show menus and executation
            of this app. 
"""

'''Library internal and external'''
import subprocess
import lista_contenedores as l
import funct_deploy_rom1 as f
import actions as a

'''Log files'''
#Control File
log_control        = "/home/badrom/Backup_Rom1Server/logs/control_deploy_Rom1.log"
#Error File
log_error         = "/home/badrom/Backup_Rom1Server/logs/error_deploy_Rom1.log"


def print_title(msg):
    print(msg)
    print()
    print()
    
def printTitle(msg):
    cmd = "figlet -f digital " + msg
    title = subprocess.call(cmd,shell=True)
    print(title)

def selectOption():
    msg = "Select a option:  "    
    option = int(input(msg))
    return option

def selectOptionString():
    msg = "Select a option with the name:  "    
    option = input(msg)
    return option

def showMenuPrincipal():
    #Menu Principal
    for menu in l.docker_menu_start:    
        print(menu);
    option = selectOption()
    
    if option == 1:
        showMenuDownload()
    elif option == 2:
        showMenuRecovery()
    elif option == 3:
        showMenuEditList()        
    elif option == 4:
        print(option)
    elif option == 5:
        print(option)            
    elif option == 6:
        print(option)                
    elif option == 9:
        print(option)
    elif option == "a" or option == "A":
        print(option)
    elif option == "":
        error = "Opción vacía en el Menú principal"    
        print(error)    
    else:
        error = "Opción seleccionado no existente en el Menú principal"    
        print(error)       

def showMenuDownload():
    title = "Menu Secundario Descarga"
    printTitle(title)    
    ##Select between all, images or Mounts
    msg = "Select to action."
    print(msg)
    list_options = {"[1] All",
                    "[2] Images",
                    "[3] Mounts", 
                    "[4] Return To Principal Menu"}
    for option in list_options:
        print(option)        
    option = selectOption()
        
    if option == 1:
        msg = "Download  Images"
        print(msg)
        a.download_docks(l.dock_list)
        msg = "Download Mounts"
        print(msg)
        a.download_mounts(l.files_mount_list)
                    
    #Menú Download Images    
    elif option == 2:
        showMenuDownloadImages()        
        
    #Menú Download Mounts        
    elif option == 3:
        showMenuDownloadMounts()
        
    elif option == 4:
        showMenuPrincipal()
        
    elif option == "":
        msg == "[ERR] Option null in Menu Action Secundatio Descarga."
        f.write_log(log_error, msg)
    else:
        msg == "[ERR] Option no identified in Menu Action Secundatio Descarga."
        f.write_log(log_error, msg)
      
def showMenuDownloadImages():
    msg = "Descarga Images.tar"
    printTitle(msg)
    
    for menu in l.dock_list:
        print("NameFile: "+menu)
    msg = "[A] Download All Images. Select with 'A' or 'a'"
    print(msg)
    msg = "[R] Return to Download Menu."
    print(msg)
    print()
    
    msg = "Please put the name exactaly with the list."    
    print(msg)        
    select = selectOptionString()    
    for option in l.dock_list:
        if option == select:
            a.downloadDock(option)
        elif select == "a" or select == "A":
            a.download_docks(l.dock_list)
        elif select == "r" or select == "R":
            showMenuDownload()
            
def showMenuDownloadMounts():
    msg = "Descarga Mount.tar"
    printTitle(msg)
    
    for menu in l.files_mount_list:
        print("NameFile: "+menu)
    msg = "[A] Download All Images. Select with 'A' or 'a'"
    print(msg)
    msg = "[R] Return to Download Menu."
    print(msg)
    print()
    
    msg = "Please put the name exactaly with the list."    
    print(msg)        
    select = selectOptionString()    
    for option in l.files_mount_list:
        if option == select:
            a.downloadMount(option)
        elif select == "a" or select == "A":
            a.download_mounts(l.files_mount_list)
        elif select == "r" or select == "R":
            showMenuDownload()
        
def showMenuEditList():
    msg = "Menu de listas"
    printTitle(msg)
    
def showMenuRecovery():
    msg = "Menu Recovery"
    printTitle(msg)
    
    ##TODO continuar con el menu recover y las distintas partes
    ##PASS 1
    showMenuStopContainer()
    ##PASS 2
    showMenuRemoveImages()
    ##PASS 3

def showMenuStopContainer():
    msg = "Pass 1. Stop containers"
    print_title(msg)     
    for dock in l.dock_list:
        print("Name Dock: "+dock)
    msg = "[A] Stop All Containers"
    print(msg)    
    option = selectOptionString()
    for dock in l.dock_list:
        if option == dock:
            a.stop_dock(dock)
        elif option == "A" or option == "a":
            a.stop_containers(l.dock_list);
    
def showMenuRemoveImages():
    msg = "Pass 2. Remove old backup images"
    print_title(msg)
    
    for dock in l.dock_list:
        print("Name Image: backup_"+dock.lower())
        print(msg)
    msg = "[A] Remove All Images"
    print(msg)    
    option = selectOptionString()
    for image in l.dock_list:
        if option == image.lower():
            a.delete_image(image)
        elif option == "A" or option == "a":
            a.delete_all_images(l.dock_list)     
    
    
    
    
    