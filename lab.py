#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
from shutil import copyfile
import subprocess
import pyperclip
import argparse
import csv

# source=os.path.abspath(__file__)+'gr'
# source=source.replace('/labgr','')+'/LAB'
source='/home/lab/bin/LAB'
run_dir=os.path.abspath(os.curdir)

def mkdir (dirr):
    if not os.path.exists(dirr):
        os.makedirs(dirr)

def createParser ():
    parser = argparse.ArgumentParser(
            description = '''Полезная программа для генерации "скелета" лабораторной работы, '''
            '''быстрого создания схем, графиков и таблиц.''',
            epilog = '''Сарафанов Ф.Г.  (c) 2018'''
            )   

    # Создание лабораторной работы
    parser.add_argument ('-n', '--name', default='labwork')
    parser.add_argument ('-t','--title', default='Some title')
    parser.add_argument ('-с','--number','--count', default='000')
    parser.add_argument ('-g','--group', default='420')
    parser.add_argument ('-a','--authors', default='Понур К.А., Сарафанов Ф.Г., Сидоров Д.А.')

    subparsers = parser.add_subparsers (dest='command')
 
    img_parser = subparsers.add_parser ('ris')
    img_parser.add_argument ('subname', nargs='?')
    img_parser.add_argument ('-n', '--name')
    img_parser.add_argument ('-c','--caption')
    img_parser.add_argument ('-l','--label')
    img_parser.add_argument ('-w','--width')

    img_parser = subparsers.add_parser ('chem')
    img_parser.add_argument ('subname', nargs='?')
    img_parser.add_argument ('-n', '--name')
    img_parser.add_argument ('-c','--caption')
    img_parser.add_argument ('-l','--label')
    img_parser.add_argument ('-w','--width')

    img_parser = subparsers.add_parser ('plot')
    img_parser.add_argument ('subname', nargs='?')
    img_parser.add_argument ('-n', '--name')
    img_parser.add_argument ('-c','--caption')
    img_parser.add_argument ('-l','--label')
    img_parser.add_argument ('-w','--width')    
    img_parser.add_argument ('-s','--style')    

    table_parser = subparsers.add_parser ('table')
    table_parser.add_argument ('subname', nargs='?')
    table_parser.add_argument ('-n', '--name')
 
    return parser

def savecopy(From, To):
    if (os.path.exists(To)) and (os.path.isfile(To)):
        key='askhgl;a'
        while not key in ['y','n','']:
            key=input("Файл уже существует! Заменить? [y/n]: ")
        if (key=='y') or (key==''):
            copyfile(From, To)
            return True
        else:
            return False        
    else:
        copyfile(From, To)
        return True


def check(To):
    if (os.path.exists(To)) and (os.path.isfile(To)):
        key='askhgl;a'
        while not key in ['y','n','']:
            key=input("Файл уже существует! Заменить? [y/n]: ")
        if (key=='y') or (key==''):
            return True
        else:
            return False        
    else:
        return True

def readTable(name):
    with open(run_dir+'/data/'+name+'.tsv','r', encoding="utf-8") as tsvin:
        tsv = csv.DictReader(tsvin, dialect='excel-tab')
        return ','.join(tsv.fieldnames)

def genList(name):
    with open(run_dir+'/data/'+name+'.tsv','r', encoding="utf-8") as tsvin:
        tsv = csv.DictReader(tsvin, dialect='excel-tab')
        # csvout = csv.writer(csvout)
        text='\t\tcolumns/F/.style={\n\t\t\tcolumn name={F},\n\t\t\t% precision=2\n\t\t},\n'
        out=''
        for i in tsv.fieldnames:
            out+=text.replace('F',i)
        return out

def createTable (namespace):
    if namespace.subname:
        tablename=namespace.subname
    else:
        if namespace.name:
            tablename=namespace.name
        else:
            tablename=input("Имя таблицы (на английском, без расширения): ")
    tabledirf=run_dir+'/table/'+tablename+'.tex'
    if (os.path.exists(run_dir+'/data/'+tablename+'.tsv')) and (os.path.isfile(run_dir+'/data/'+tablename+'.tsv')):
        if check(tabledirf):
            NAME=os.path.split(os.getcwd())[1]
            with open(source+'/table/table.tex', "r") as f:
                index=f.read()
                index=index.replace(r'NAME',NAME)
                index=index.replace(r'HEADER',readTable(tablename))
                index=index.replace(r'MODIFY',genList(tablename))
                index=index.replace(r'DATA',tablename)
                # f.write(index)       
            with open(tabledirf, "w+") as f:
               f.write(index)    

            subprocess.check_output(['bash','-c', "subl3 "+run_dir+'/table/'+tablename+'.tex:6:9'])         
            pyperclip.copy('\input{table/'+tablename+'.tex}')
    else:
        print('Ошибка: нет исходных данных для таблицы')
        key='sdfadf'
        while not key in ['y','n','']:
            key=input("Скопировать файл шаблона? [y/n]: ")
        if (key=='y') or (key==''):
            if savecopy(source+'/table/table.tex', tabledirf):
                pyperclip.copy('\input{table/'+tablename+'.tex}')                
                subprocess.check_output(['bash','-c', "subl3 "+run_dir+'/table/'+tablename+'.tex:6:9'])                     
        else:
            pass         


def createRis (namespace):
    if namespace.subname:
        imgname=namespace.subname
    else:
        if namespace.name:
            imgname=namespace.name
        else:
            imgname=input("Имя изображения (на английском): ")

    savecopy(source+'/ris/img.tex', run_dir+'/ris/'+imgname+'.tex')

    imgname=input("Имя изображения (на английском): ")
    subprocess.check_output(['bash','-c', "subl3 "+run_dir+'/ris/'+imgname+'.tex:28:9'])

    with open(source+"/ris/ris_.tex", "r") as lines:
        imgg=lines.read() # или сразу
        imgg=imgg.replace(r'{addr}','ris/'+imgname)

        if namespace.label:
            imgg=imgg.replace(r'{label}',namespace.label)
        else:
            imgg=imgg.replace(r'{label}',imgname)

        if namespace.caption:
            imgg=imgg.replace(r'\caption{}','\caption{'+namespace.caption+'}')

        if namespace.width:
            imgg=imgg.replace(r'[]','[width='+namespace.width+']')            
        pyperclip.copy(imgg)

def createChem (namespace):
    if namespace.subname:
        imgname=namespace.subname
    else:
        if namespace.name:
            imgname=namespace.name
        else:
            imgname=input("Имя схемы (на английском): ")

    savecopy(source+'/chem/chem.tex', run_dir+'/chem/'+imgname+'.tex')
    subprocess.check_output(['bash','-c', "subl3 "+run_dir+'/chem/'+imgname+'.tex:6:9'])

    with open(source+"/chem/chem_.tex", "r") as lines:
        imgg=lines.read() # или сразу
        imgg=imgg.replace(r'{addr}','chem/'+imgname)
        imgg=imgg.replace(r'{fig:','{chem:')

        if namespace.label:
            imgg=imgg.replace(r'{label}',namespace.label)
        else:
            imgg=imgg.replace(r'{label}',imgname)

        if namespace.caption:
            imgg=imgg.replace(r'\caption{}','\caption{'+namespace.caption+'}')

        if namespace.width:
            imgg=imgg.replace(r'[]','[width='+namespace.width+']')            
        pyperclip.copy(imgg)

def createPlot (namespace):
    if namespace.subname:
        imgname=namespace.subname
    else:
        if namespace.name:
            imgname=namespace.name
        else:
            imgname=input("Имя графика (на английском): ")

    if namespace.style=='min':
        savecopy(source+'/plot/plot-min.tex', run_dir+'/plot/'+imgname+'.tex')
    elif namespace.style=='full':
        savecopy(source+'/plot/plot-full.tex', run_dir+'/plot/'+imgname+'.tex')
    else:
        savecopy(source+'/plot/plot-min.tex', run_dir+'/plot/'+imgname+'.tex')

    subprocess.check_output(['bash','-c', "subl3 "+run_dir+'/plot/'+imgname+'.tex:6:9'])

    with open(source+"/plot/plot_.tex", "r") as lines:
        imgg=lines.read() # или сразу
        imgg=imgg.replace(r'{addr}','plot/'+imgname)
        imgg=imgg.replace(r'{fig:','{plot:')

        if namespace.label:
            imgg=imgg.replace(r'{label}',namespace.label)
        else:
            imgg=imgg.replace(r'{label}',imgname)

        if namespace.caption:
            imgg=imgg.replace(r'\caption{}','\caption{'+namespace.caption+'}')

        if namespace.width:
            imgg=imgg.replace(r'[]','[width='+namespace.width+']')            
        pyperclip.copy(imgg)

def createLab (namespace):
    # print(namespace)
    if namespace.title=='Some title':
        namespace.title=input("Название лабораторной работы (полное на русском): ")
        if namespace.title=='':
            namespace.title=='Some title'

    if namespace.name=='labwork':
        namespace.name=input("Имя репозитория (одно английское слово): ")
        if namespace.name=='':
            namespace.name=='labwork'

    if namespace.number=='000':
        namespace.number=input("Номер лабораторной работы: ")
        if namespace.number=='':
            namespace.number=='000'
                                                               
    directory=run_dir+'/'+namespace.name;
    mkdir(directory)

    mkdir(directory+'/data')
    mkdir(directory+'/tables')

    mkdir(directory+'/ris')
    mkdir(directory+'/chem')
    mkdir(directory+'/plot')
    
    mkdir(directory+'/text')
    idx=directory+"/"+namespace.name+'.tex';

    with open(source+"/index.tex", "r") as lines:
        index=lines.read() # или сразу

    with open(idx, "w+") as f:
        index=index.replace(r'{number}',namespace.number)
        index=index.replace(r'{title}',namespace.title)
        index=index.replace(r'{group}',namespace.group)
        index=index.replace(r'{authors}',namespace.authors)
        f.write(index)       

    copyfile(source+'/text/diss.tex', directory+'/text/diss.tex')
    copyfile(source+'/text/titlepage.tex', directory+'/text/titlepage.tex')
    
    subprocess.check_output(['bash','-c', "subl3 "+idx+r":26:10"])    
 
 
if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
 
    # print (namespace)
 
    if namespace.command in ['ris','chem','plot','table']:
        Dir=run_dir+'/'+namespace.command
        if os.path.exists(Dir):
            if namespace.command=='ris':
                createRis(namespace) 
            elif namespace.command=='chem':
                createChem(namespace)      
            elif namespace.command=='plot':
                createPlot(namespace)    
            elif namespace.command=='table':
                createTable(namespace)  
        else:
            print('Программа запущена вне папки лабораторной!')         
    else:
        createLab(namespace)