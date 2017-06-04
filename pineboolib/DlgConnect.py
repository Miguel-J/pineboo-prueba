# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from builtins import str
import os
from PyQt4 import QtGui, QtCore, uic

from pineboolib.utils import filedir

# Using Python's SQLite Module: self-contained, serverless, zero-configuration and transactional. It is very fast and lightweight, and the entire database is stored in a single disk file.
import sqlite3

# añado conexión con qt4:
from PyQt4 import QtCore, QtGui, QtSql
from PyQt4.QtSql import QSqlQueryModel,QSqlQuery
from PyQt4.QtGui import QTableView, QApplication
import sys


# añado debugging modulo:
import pdb


class DlgConnect(QtGui.QWidget):
    ruta = ""
    username = ""
    password = ""
    hostname = ""
    portnumber = ""
    database = ""
    ui = None
    # uic.loadUi(filedir('forms/dlg_connect.ui'))


    def load(self):
        # DEFINIMOS LO QUE HACEN LOS BOTONES
        self.ui = uic.loadUi(filedir('forms/dlg_connect.ui'), self)
        self.ui.pbnStart.clicked.connect(self.conectar)
        self.ui.pbnSearchFolder.clicked.connect(self.findPathProject)
        self.ui.pbnSearchFolder_2.clicked.connect(self.findProject)
        self.ui.pbnCargarDatos.clicked.connect(self.ChargeProject)
        self.ui.pbnMostrarProyectos.clicked.connect(self.ShowTable)
        self.ui.pbnBorrarProyecto.clicked.connect(self.DeleteProject)
        self.ui.pbnGuardarProyecto.clicked.connect(self.SaveProject)


        # Creates or opens a file called mydb with a SQLite3 DB
        db = sqlite3.connect('./projects/pinebooconectores.sqlite')

        # Get a cursor object para crear la tabla "proyectos"
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proyectos(id INTEGER PRIMARY KEY, name TEXT, dbname TEXT, dbtype TEXT, dbhost TEXT, dbport TEXT, username TEXT, password TEXT)
''')
        db.commit()

        # Get a cursor object  para AÑADIR CAMPOS
        cursor = db.cursor()
        name1 = 'A'
        dbname1 = 'B'
        dbtype1 = 'C'
        dbhost1 = 'D'
        dbport1 = 'E'
        username1 = 'F'
        password1 = 'G'

        with db:
            cursor.execute('''
        INSERT INTO proyectos(name, dbname, dbtype, dbhost, dbport, username, password) VALUES (?,?,?,?,?,?,?)''', (name1, dbname1, dbtype1, dbhost1, dbport1, username1, password1))
        db.commit()
        print ("PROYECTO GRABADO")

        # When we are done working with the DB we need to close the connection:
        db.close()


        dlg = QtGui.QDialog()

        DlgConnect.leFolder = self.ui.leFolderSQLITE
        DlgConnect.leFolder_2 = self.ui.leProyElegID
        DlgConnect.leID = self.ui.leID
        DlgConnect.leName = self.ui.leName
        DlgConnect.leDBName = self.ui.leDBName
        DlgConnect.leDBType = self.ui.leDBType
        DlgConnect.leHost = self.ui.leHost
        DlgConnect.lePort = self.ui.lePort
        DlgConnect.leUserName = self.ui.leUserName
        DlgConnect.lePassword = self.ui.lePassword

        # muestra tabla
        DlgConnect.TABLEVIEW = self.ui.tableView
        # DlgConnect.view1.show()


        # myapp = MyForm()
        # myapp.show()

    
    @QtCore.pyqtSlot()
    def conectar(self):
        DlgConnect.ruta = filedir(str(DlgConnect.leFolder.text()), str(DlgConnect.leName.text()))
        DlgConnect.username = DlgConnect.leUserName.text()
        DlgConnect.password = DlgConnect.lePassword.text()
        DlgConnect.hostname = DlgConnect.leHostName.text()
        DlgConnect.portnumber = DlgConnect.lePort.text()
        DlgConnect.database = DlgConnect.leDBName.text()

        if not DlgConnect.leName.text():
            DlgConnect.ruta = ""
        elif not DlgConnect.ruta.endswith(".xml"):
            DlgConnect.ruta += ".xml"
        if not os.path.isfile(DlgConnect.ruta) and DlgConnect.leName.text():
            QtGui.QMessageBox.information(self, "AVISO", "El proyecto \n" + DlgConnect.ruta +" no existe")
            DlgConnect.ruta = None
        else:
            self.close()
    
    @QtCore.pyqtSlot()       
    def findPathProject(self):
        filename = QtGui.QFileDialog.getExistingDirectory(self, "Seleccione Directorio")
        if filename:
            DlgConnect.leFolder.setText(str(filename))

    @QtCore.pyqtSlot()       
    def findProject(self):
        filenameP = QtGui.QFileDialog.getExistingDirectory(self, "Seleccione DirectorioP")
        if filenameP:
            DlgConnect.leFolder_2.setText(str(filenameP))
    
    @QtCore.pyqtSlot()
    def ChargeProject(self):
        # elegir un campo e imprimirlo de la tabla "proyectos"

        db = sqlite3.connect('./projects/pinebooconectores.sqlite')
        cursor = db.cursor()
        cursor.execute('''SELECT id, name, dbname, dbtype, dbhost, dbport, username, password FROM proyectos''')
        conectores1 = cursor.fetchone()

        # escribir el campo 0 de la fila 1:
        DlgConnect.leID.setText(str(conectores1[0]))
        DlgConnect.leName.setText(str(conectores1[1]))
        DlgConnect.leDBName.setText(str(conectores1[2]))
        DlgConnect.leDBType.setText(str(conectores1[3]))
        DlgConnect.leHost.setText(str(conectores1[4]))
        DlgConnect.lePort.setText(str(conectores1[5]))
        DlgConnect.leUserName.setText(str(conectores1[6]))
        DlgConnect.lePassword.setText(str(conectores1[7]))


        db.commit()
        print ("DATOS CARGADOS")
        db.close()

    @QtCore.pyqtSlot()
    def ShowTable(self):
        
        # DEBUGGING:
        # pdb.set_trace()
        # print ("escribe `n´(next) para continuar / `q´(quit) para salir / `c´ para seguir sin debugg")

        # db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        # db.setDatabaseName('./projects/pinebooconectores.sqlite')   

        
        db = sqlite3.connect('./projects/pinebooconectores.sqlite')
        cursor = db.cursor()
        
        # mostrar la tabla proyectos de la base de datos SQLITE pinebooconectores.sqlite con los campos en el widget viewTable de dlgconnect.ui
        # initializeModel(model)
        # DlgConnect.ui.tableView.setModel(self.model)
        
        # view1.clicked.connect(findrow)

        class MyForm(QtGui.QDialog):
            def ShowTable(self) :
                # QtGui.QWidget.ShowTable(self)
                self.ui = uic.loadUi(filedir('forms/dlg_connect.ui'), tableView)
                # self.ui = Ui_Dialog()
                # self.ui.tableView(self)
                self.model = QtSql.QSqlTableModel(self)
                self.model.setTable("proyectos")
                self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
                self.model.select()
                # model = QtSql.QSqlTableModel()
                # model.setTable('proyectos')
                # model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
                # model.select()
                self.model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
                self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Name")
                self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Database")
                self.model.setHeaderData(3, QtCore.Qt.Horizontal, "DB Type")
                self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Hostname")
                self.ui.tableView.setModel (self.model)
        # app = QtGui.QApplication(sys.argv)
        # self.ui.tableView.show()
        if __name__ == '__main__': # only executes the below code if it python has run it as the main
            app = QtGui.QApplication(sys.argv) # before this was getting called twice
            myapp = MyForm()
            myapp.show()
            sys.exit(app.exec_())
        # def createView(title, model):
        #   view = QtGui.QTableView()
        #   view.setModel(model)
        #   view.setWindowTitle(title)
        #   return view
        # view1 = createView("Table Model (View 1)", model)
        
        # DlgConnect.TABLEVIEW.show()
        # projectModel = QSqlQueryModel()

        # projectModel.setQuery("select * from proyectos",db)
        # projectView = QTableView()
        # projectView.setModel(projectModel)
        # projectView.show()

        print ("TABLA MOSTRADA")

        # db.close()

        DlgConnect.TABLEVIEW.show()

    @QtCore.pyqtSlot()
    def DeleteProject(self):

        db = sqlite3.connect('./projects/pinebooconectores.sqlite')
        cursor = db.cursor()
        cursor.execute('''SELECT id, name, dbname, dbtype, dbhost, dbport, username, password FROM proyectos''')
        conectores1 = cursor.fetchone()
        # Get a cursor object  para AÑADIR CAMPOS
        cursor = db.cursor()
        name1 = ''
        dbname1 = ''
        dbtype1 = ''
        dbhost1 = ''
        dbport1 = ''
        username1 = ''
        password1 = ''
        
        with db:
            cursor.execute('''
        INSERT INTO proyectos(name, dbname, dbtype, dbhost, dbport, username, password) VALUES (?,?,?,?,?,?,?)''', (name2, dbname2, dbtype2, dbhost2, dbport2, username2, password2))
        db.commit()
        print ("PROYECTO BORRADO")

        db.close()

    @QtCore.pyqtSlot()
    def SaveProject(self):

        db = sqlite3.connect('./projects/pinebooconectores.sqlite')
        cursor = db.cursor()
        cursor.execute('''SELECT id, name, dbname, dbtype, dbhost, dbport, username, password FROM proyectos''')
        conectores1 = cursor.fetchone()
        # Get a cursor object  para AÑADIR CAMPOS
        cursor = db.cursor()
        id2 = str(self.ui.leID.text())
        name2 = str(self.ui.leName.text())
        dbname2 = str(self.ui.leDBName.text())
        dbtype2 = str(self.ui.leDBType.text())
        dbhost2 = str(self.ui.leHost.text())
        dbport2 = str(self.ui.lePort.text())
        username2 = str(self.ui.leUserName.text())
        password2 = str(self.ui.lePassword.text())


        with db:
            cursor.execute('''
        INSERT INTO proyectos(id, name, dbname, dbtype, dbhost, dbport, username, password) VALUES (?,?,?,?,?,?,?,?)''', (id2, name2, dbname2, dbtype2, dbhost2, dbport2, username2, password2))
        db.commit()
        print ("PROYECTO GUARDADO")


        db.close()