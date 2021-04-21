#! /bin/bash

let path;
if [[ $1 == "" ]] 
then
    echo "Path for resourses was not sended. Using default path: res"
    path="res"
else
    path=$1
fi
pyinstaller --onefile -F --add-data "$path/:$path" src/main.py

