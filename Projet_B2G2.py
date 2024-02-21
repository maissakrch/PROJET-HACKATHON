#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 22:50:08 2023

@author: maissa
"""
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import os
from PIL import Image, ImageTk
import sqlite3

conn = sqlite3.connect('addressBOOK.db')
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS contacts(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   surname TEXT,
                   phone TEXT,                   
                   email TEXT
                   )
               ''')
conn.commit()
conn.close

Profile={1:""}

def add_customer():
    name=entryName.get()
    surname=entrySurname.get()
    phone=entryPhone.get()
    email=entryEmail.get()
    photo=entryPhoto.get()
    
    conn = sqlite3.connect('addressBOOK.db')
    cur = conn.cursor()
    
    cur.execute("INSERT INTO contacts ('name','surname','phone','email') values(?,?,?,?)",(name,surname,phone,email))
    conn.commit()
    conn.close()
    
    print("yes")
    
    conn = sqlite3.connect('addressBOOK.db')
    cur = conn.cursor()
    select=cur.execute("SELECT*FROM contacts order by ID desc")
    select = list(select)
    tree.insert('',END,values=select[0])
    conn.close()
    
    conn = sqlite3.connect('addressBOOK.db')
    cur = conn.cursor()
    select = cur.execute("SELECT*FROM contacts order by ID desc")
    select = list(select)
    id = select[0][0]
    filename = entryPhoto.get()
    im=Image.open(filename)
    rgb_im=im.convert('RGB')
    rgb_im.save(('profile_'+str(id)+'.'+'jpg'))
    conn.close()
    entryName.delete(0,tk.END)
    entrySurname.delete(0,tk.END)
    entryPhone.delete(0,tk.END)
    entryEmail.delete(0,tk.END)
    entryPhoto.delete(0,tk.END)
    

def delete_customer():
    idSelect=tree.item(tree.selection())['values'][0]
    conn = sqlite3.connect('addressBOOK.db')
    cur = conn.cursor()
    delete = cur.execute("delete from contacts where id={}".format(idSelect))
    conn.commit()
    tree.delete(tree.selection())

def edit_customer():
    idSelect = tree.item(tree.selection())['values'][0]
    name = entryName.get()
    surname = entrySurname.get()
    phone = entryPhone.get()
    email = entryEmail.get()

    if not name or not surname or not phone or not email:
        messagebox.showwarning("Warning", "Veuillez remplir toutes les informations du contact.")
        return

    conn = sqlite3.connect('addressBOOK.db')
    cur = conn.cursor()

    cur.execute("UPDATE contacts SET name=?, surname=?, email=?, phone=? WHERE id=?", (name, surname, email, phone, idSelect))

    conn.commit()
    conn.close()

    # Mettre à jour l'affichage dans l'arbre (TreeView)
    # Effacer l'élément sélectionné actuel de l'arbre
    tree.delete(tree.selection())
    # Insérer le contact mis à jour dans l'arbre
    conn = sqlite3.connect('addressBOOK.db')
    cur = conn.cursor()
    select = cur.execute("SELECT * FROM contacts WHERE id=?", (idSelect,))
    updated_contact = cur.fetchone()
    conn.close()
    tree.insert('', END, values=updated_contact)

    

def sort_by_name():
    for x in tree.get_children():
        tree.delete(x)
    conn = sqlite3.connect('addressBOOK.db')
    cur = conn.cursor()
    select = cur.execute("select*from contacts order by name asc")
    conn.commit()
    for row in select:
        tree.insert('',END,values=row)
    conn.close()
    
def SearchByName(event):
    for x in tree.get_children():
        tree.delete(x)
    name = entrySearchByName.get()
    conn = sqlite3.connect('addressBOOK.db')
    cur = conn.cursor()
    select = cur.execute('SELECT*FROM contacts WHERE name = (?)',(name,))
    conn.commit()
    for row in select:
        tree.insert('',END,values=row) 
    conn.close()
    

def SearchByPhone(event):
    for x in tree.get_children():
        tree.delete(x)
    phone = entrySearchByPhone.get()
    conn = sqlite3.connect('addressBOOK.db')
    cur = conn.cursor()
    select = cur.execute('SELECT*FROM contacts WHERE phone = (?)',(phone,))
    conn.commit()
    for row in select:
        tree.insert('',END,values=row)
    conn.close()    
    

def browsePhoto():
    entryPhoto.delete(0,END)
    filename=filedialog.askopenfilename(initialdir="/",title="select file")
    entryPhoto.insert(END,filename)

def treeActionSalect(event):
    label_image.destroy()
    
    idSelect = tree.item(tree.selection())['values'][0]
    nameSelect= tree.item(tree.selection())['values'][1]
    surnameSelect=tree.item(tree.selection())['values'][2]
    phoneSelect=tree.item(tree.selection())['values'][3]
    emailSelect=tree.item(tree.selection())['values'][4]
    
    try :
        imgProfile ="profile_"+str(idSelect)+"."+"jpg"
        load = Image.open(imgProfile)
        load.thumbnail((175, 175))
        photo = ImageTk.PhotoImage(load)
        Profile[1]=photo
        lblImage = Label(root,bg='white',image=photo)
        lblImage.place(x=670, y=195)
    except Exception as e:
        load = Image.open("profile.png")
        load.thumbnail((175, 175))
        photo = ImageTk.PhotoImage(load)
        Profile[1]=photo
        lblImage = Label(root,bg='blue',image=photo)
        lblImage.place(x=670, y=195)
        
    monCanvas=Canvas(root, width=255, height=140, bg=rgb_hack((92,199,178)))
    monCanvas.place(x=565,y=50)
        
    lid=Label(root,text="ID: "+str(idSelect),bg=rgb_hack((92,199,178)),fg ="black")
    lid.place(x=580,y=50)
    lname=Label(root,text="Name: "+str(nameSelect),bg=rgb_hack((92,199,178)),fg ="black")
    lname.place(x=580,y=80)
    lsurname=Label(root,text='Surname: '+str(surnameSelect),bg=rgb_hack((92,199,178)),fg ="black")
    lsurname.place(x=580,y=110)
    lphone=Label(root,text='Phone: '+str(phoneSelect),bg=rgb_hack((92,199,178)),fg ="black")
    lphone.place(x=580,y=140)
    lemail=Label(root,text='Email: '+str(emailSelect),bg=rgb_hack((92,199,178)),fg ="black")
    lemail.place(x=580,y=170)
    
    
    
def rgb_hack(rgb):
    return "#%02x%02x%02x" % rgb


root = Tk()
root.title("Address Book")
root.geometry("875x390")
root.configure(bg=rgb_hack((42,42,42))) 

lblTitle = Label(root, text = "Carnet d'adresses", font=("Arial",23), bg=rgb_hack((92,199,178)),fg="white")
lblTitle.place(x=0,y=0,width=250)

contour1=Label(root,bg=rgb_hack((92,199,178)))
contour1.place(x=250,y=0,width=625,height=5)
contour2=Label(root,bg=rgb_hack((92,199,178)))
contour2.place(x=0,y=385,width=875,height=5)

#RECHERCHE______________________________
lbSearchByName = Label(root,text="Recherche prénom",bg=rgb_hack((92,199,178)),fg="white")
lbSearchByName.place(x=280,y=20,width=120)
entrySearchByName=Entry(root)
entrySearchByName.bind("<Return>",SearchByName)
entrySearchByName.configure(bg=rgb_hack((170,225,215)))
entrySearchByName.place(x=400,y=20,width=160)

lbSearchByPhone = Label(root,text="Recherche tel",bg=rgb_hack((92,199,178)) ,fg="white")
lbSearchByPhone.place(x=565,y=20,width=120)
entrySearchByPhone=Entry(root)
entrySearchByPhone.bind("<Return>",SearchByPhone)
entrySearchByPhone.configure(bg=rgb_hack((170,225,215)))
entrySearchByPhone.place(x=685,y=20,width=160)

#PRENOM___________________________
lbName = Label(root, text ="Prénom: ", bg=rgb_hack((42,42,42)), fg ="white")
lbName.place(x=25,y=50,width=125)
entryName=Entry(root)
entryName.place(x=160,y=50,width=400)

#NOM___________________________
lbSurname = Label(root, text ="Nom: ", bg=rgb_hack((42,42,42)), fg ="white")
lbSurname.place(x=25,y=80,width=125)
entrySurname=Entry(root)
entrySurname.place(x=160,y=80,width=400)

#TELEPHONE___________________________
lblPhone = Label(root, text ="N° téléphone", bg=rgb_hack((42,42,42)), fg ="white")
lblPhone.place(x=25,y=110,width=125)
entryPhone=Entry(root)
entryPhone.place(x=160,y=110,width=400)

#PHOTO___________________________
lblPhoto = Label(root, text ="Photo ", bg=rgb_hack((42,42,42)), fg ="white")
lblPhoto.place(x=25,y=140,width=125)
bPhoto = Button(root , text="Browse",bg="white",fg="black",command=browsePhoto)
bPhoto.place(x=490,y=140,height=25)
entryPhoto=Entry(root)
entryPhoto.place(x=160,y=140,width=320)

#EMAIL___________________________
lblEmail = Label(root, text ="Email ", bg=rgb_hack((42,42,42)), fg ="white")
lblEmail.place(x=25,y=170,width=125)
entryEmail=Entry(root)
entryEmail.place(x=160,y=170,width=400)

bAdd= Button(root, text="Ajouter contact", command=add_customer,  bg="white", fg="black")
bAdd.place(x=25,y=195,width=255)

bDelete= Button(root, text="Supprimer contact", command=delete_customer, bg="white", fg="black")
bDelete.place(x=25,y=230,width=255)

bEdit= Button(root, text="Modifier contact", command=edit_customer, bg="white", fg="black")
bEdit.place(x=25,y=265,width=255)

bSort= Button(root, text="Trier par nom", command=sort_by_name, bg="white", fg="black")
bSort.place(x=25,y=300,width=255)

bExit= Button(root, text="Sortir", command=root.destroy ,bg="white", fg="black")
bExit.place(x=25,y=335,width=255)

try:
    load = Image.open("profile.png")
    load.thumbnail((175, 175))
    photo = ImageTk.PhotoImage(load)
    label_image = Label(root, image=photo)
    label_image.place(x=670, y=195)
except Exception as e:
    print(f"Erreur lors du chargement de l'image : {e}")
    
tree = ttk.Treeview(root, columns = (1,2,3,4),height=5,show = "headings")
tree.place(x="285",y=195,width=380,height=179)
tree.bind("<<TreeviewSelect>>",treeActionSalect)

tree.heading(1,text="ID")
tree.heading(2,text="Prénom")
tree.heading(3,text="Nom")
tree.heading(4,text="Phone")

tree.column(1,width=50)
tree.column(2,width=100)
tree.column(3,width=100)
tree.column(4,width=120)

conn = sqlite3.connect('addressBOOK.db')
cur = conn.cursor()
select = cur.execute("select*from contacts")
for row in select : 
    tree.insert('',END,value=row)
conn.close()



root.mainloop()
