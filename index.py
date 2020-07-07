import getpass
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication
import mysql.connector
from mysql.connector import Error
from PyQt5.QtGui import QIntValidator
from xlrd import *
from xlsxwriter import *
from PyQt5 import QtCore

from main import Ui_MainWindow
# from PyQt5.uic import loadUiType

names_list = []
drugs_list = []
id_list = []
check_add_drugs = []
LastStateRole = QtCore.Qt.UserRole

# MainUI, _ = loadUiType('main.ui')


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.DB_Connect()
        self.Handel_Button()
        self.Ui_Changes()
        self.int_vaildator()
        self.d_validator()
        self.Add_fulid_to_combobox()
        self.get_names_from_db()
        self.patient_names_for_main()
        self.get_drug_from_db()
        self.add()
        self.patient_names_for_report()
        self.drug_names_for_report()
        self.set_today_date()
        self.get_patient_number_from_db()
        self.set_patient_number_for_report()
        self.show_daily_statics()

    #############################################
    def Ui_Changes(self):
        table1 = self.tableWidget.horizontalHeader()
        table1.setSectionResizeMode(0, QHeaderView.Stretch)
        table1.setSectionResizeMode(2, QHeaderView.Stretch)
        table1.setSectionResizeMode(4, QHeaderView.Stretch)
        table2 = self.tableWidget_2.horizontalHeader()
        table2.setSectionResizeMode(0, QHeaderView.Stretch)
        table2.setSectionResizeMode(2, QHeaderView.Stretch)
        table2.setSectionResizeMode(4, QHeaderView.Stretch)
        table3 = self.tableWidget_3.horizontalHeader()
        table3.setSectionResizeMode(0, QHeaderView.Stretch)
        table4 = self.tableWidget_4.horizontalHeader()
        table4.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        table4.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        table4.setSectionResizeMode(2, QHeaderView.Fixed)
        table4.setSectionResizeMode(3, QHeaderView.Fixed)
        table4.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        table4.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        table4.setSectionResizeMode(6, QHeaderView.Stretch)
        table4.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        table4.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        table5 = self.tableWidget_5.horizontalHeader()
        table5.setSectionResizeMode(0, QHeaderView.Stretch)
        table5.setSectionResizeMode(1, QHeaderView.Stretch)
        table6 = self.tableWidget_6.horizontalHeader()
        table6.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        table6.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget_7.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_6.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_4.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.lineEdit.setFocus()
        self.tabWidget_3.hide()
        self.pushButton_15.hide()
        self.lineEdit_6.setMaxLength(1)
        self.pushButton_17.hide()

    def DB_Connect(self):
        try:
            self.db = mysql.connector.connect(host='localhost',
                                              database='hospital',
                                              user='root',
                                              password='toor')
            self.cur = self.db.cursor(buffered=True)
            self.db.autocommit = False
            self.statusBar().showMessage('Database Connected Successfully')
        except Error as e:
            self.statusBar().showMessage('Failed To Connect To Database')

    def Handel_Button(self):
        ##########################################################
        ''' Add Drug'''
        self.pushButton_5.clicked.connect(self.add_drug)
        self.pushButton_29.clicked.connect(self.clear_drug_area)
        self.pushButton_28.clicked.connect(self.get_modify_drug)
        self.pushButton_27.clicked.connect(self.show_daily_statics_costum)
        self.pushButton_25.clicked.connect(self.delete_patient_visit)
        self.pushButton_26.clicked.connect(self.delete_patient_data)
        self.pushButton_24.clicked.connect(self.clear_patient_mang_data)
        self.pushButton_23.clicked.connect(self.get_patient_data_for_mangment)
        self.pushButton_22.clicked.connect(self.clear_database_data)
        self.lineEdit_15.editingFinished.connect(self.search_for_drug_to_update)
        self.pushButton_21.clicked.connect(self.update_drug)
        self.pushButton_18.clicked.connect(self.new_prescription_for_patient_has_old_one)
        self.pushButton_6.clicked.connect(self.save_patient_search)
        self.pushButton_7.clicked.connect(self.save_drug_search)
        self.pushButton_8.clicked.connect(self.save_genral_search)
        self.pushButton_17.clicked.connect(self.update_patient)
        self.pushButton_13.clicked.connect(self.save_all_drug_dose)
        self.pushButton_3.clicked.connect(self.add_Client)
        self.pushButton.clicked.connect(self.add_drug_to_table)
        self.lineEdit.editingFinished.connect(self.Check_Client_name)
        self.lineEdit.textChanged.connect(self.today_number)
        self.lineEdit_4.editingFinished.connect(self.check_drug_name)
        self.pushButton_4.clicked.connect(self.clear_data)
        self.pushButton_19.clicked.connect(self.clear_data)
        self.pushButton_20.clicked.connect(self.clear_data)
        self.pushButton_2.clicked.connect(self.handel_save_method)
        self.pushButton_9.clicked.connect(self.search_for_patient)
        self.pushButton_10.clicked.connect(self.search_for_drug)
        self.pushButton_11.clicked.connect(self.genral_search)
        self.pushButton_12.clicked.connect(self.genral_drug_dose)
        self.tabWidget.currentChanged.connect(self.tab_change_clear_data)
        self.tabWidget_2.currentChanged.connect(self.tab_change_clear_data_tab2)
        self.tabWidget_3.currentChanged.connect(self.tab_change_clear_data_tab3)
        self.comboBox_2.currentIndexChanged.connect(self.length_setter)
        self.lineEdit_12.returnPressed.connect(self.check_password)
        self.pushButton_14.clicked.connect(self.change_password)
        self.pushButton_15.clicked.connect(self.delete_item_from_table)
        self.pushButton_16.clicked.connect(self.go_to_today)
        self.tableWidget.itemSelectionChanged.connect(self.get_Selected_row)
        self.tableWidget_6.itemSelectionChanged.connect(self.get_Selected_prescription_no)
        self.tableWidget_4.cellChanged.connect(self.update_check_status)

        # self.tableWidget_4.itemClicked.connect(self.update_check_status)
        ##########################################################
        ''' Back to Home'''

    def int_vaildator(self):
        validator = QIntValidator(0, 10000, self)
        validator2 = QIntValidator(0, 9, self)
        self.lineEdit_6.setValidator(validator2)
        self.lineEdit_11.setValidator(validator)

    def d_validator(self):
        validator = QDoubleValidator(0.0, 99.99, 2)
        self.lineEdit_5.setValidator(validator)

    def get_names_from_db(self):
        names_list.clear()
        self.cur.execute('''SELECT name FROM patient''')
        data = self.cur.fetchall()
        for item in data:
            names_list.append(item[0])

    def patient_names_for_main(self):
        completer = QCompleter(names_list)
        self.lineEdit.setCompleter(completer)

    def get_drug_from_db(self):
        drugs_list.clear()

        self.cur.execute('''SELECT drug_name FROM drugs''')
        data = self.cur.fetchall()
        for item in data:
            drugs_list.append(item[0])

    def add(self):
        completer = QCompleter(drugs_list)
        self.lineEdit_4.setCompleter(completer)

    def patient_names_for_report(self):
        completer = QCompleter(names_list)
        self.lineEdit_8.setCompleter(completer)
        self.lineEdit_17.setCompleter(completer)

    def drug_names_for_report(self):
        completer = QCompleter(drugs_list)
        self.lineEdit_9.setCompleter(completer)
        self.lineEdit_15.setCompleter(completer)

    def get_patient_number_from_db(self):
        names_list.clear()

        self.cur.execute('''SELECT number FROM patient''')
        data = self.cur.fetchall()
        for item in data:
            id_list.append(str(item[0]))

    def set_patient_number_for_report(self):
        completer = QCompleter(id_list)
        self.lineEdit_11.setCompleter(completer)
        self.lineEdit_18.setCompleter(completer)

    def today_number(self):

        date = datetime.date.today()
        self.cur.execute('''SELECT  COUNT( distinct patient_id) FROM prescription_no WHERE date= %s ''', (date,))
        data = self.cur.fetchone()
        self.label_25.setText(str(data[0] + 1))

    def tab_change_clear_data(self, i):
        if i == 0:
            self.lineEdit.setFocus()
        elif i == 1:
            self.lineEdit_12.setFocus()
        elif i == 2:
            self.lineEdit_8.setFocus()

        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_10.clear()
        self.lineEdit_7.clear()
        self.lineEdit_12.clear()
        self.set_today_date()
        self.tabWidget_3.hide()
        self.pushButton_17.hide()
        self.statusBar().showMessage('')
        check_add_drugs.clear()
        self.label_32.clear()
        self.label_25.clear()
        self.label_8.clear()

        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)

    def clear_data(self):
        self.lineEdit.setFocus()
        self.lineEdit_12.setFocus()
        self.lineEdit.clear()
        self.label_38.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_10.clear()
        self.lineEdit_7.clear()
        self.lineEdit_12.clear()
        self.set_today_date()
        self.tabWidget_3.hide()
        self.pushButton_17.hide()
        self.statusBar().showMessage('')
        check_add_drugs.clear()
        self.label_32.clear()
        self.label_25.clear()
        self.lineEdit.setFocus()
        self.lineEdit_8.clear()
        self.lineEdit_11.clear()
        self.lineEdit_9.clear()
        self.label_8.clear()
        self.label_44.clear()

        while self.tableWidget_2.rowCount() > 0:
            self.tableWidget_2.removeRow(0)
        while self.tableWidget_3.rowCount() > 0:
            self.tableWidget_3.removeRow(0)
        while self.tableWidget_4.rowCount() > 0:
            self.tableWidget_4.removeRow(0)
        while self.tableWidget_5.rowCount() > 0:
            self.tableWidget_5.removeRow(0)

        self.set_today_date()
        self.statusBar().showMessage('')

        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)

    def clear_drug_area(self):
        self.label_44.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_10.clear()
        self.lineEdit_6.clear()
        self.label_23.clear()

    def tab_change_clear_data_tab2(self, i):
        if i == 0:
            self.lineEdit_8.setFocus()
        elif i == 1:
            self.lineEdit_9.setFocus()
        self.lineEdit_8.clear()
        self.lineEdit_11.clear()
        self.lineEdit_9.clear()
        while self.tableWidget_2.rowCount() > 0:
            self.tableWidget_2.removeRow(0)
        while self.tableWidget_3.rowCount() > 0:
            self.tableWidget_3.removeRow(0)
        while self.tableWidget_4.rowCount() > 0:
            self.tableWidget_4.removeRow(0)
        while self.tableWidget_5.rowCount() > 0:
            self.tableWidget_5.removeRow(0)
        self.set_today_date()
        self.statusBar().showMessage('')
        # if i == 2 :
        #     self.get_genral_search_auto()

    def tab_change_clear_data_tab3(self, i):
        if i == 0:
            self.lineEdit_7.setFocus()
        elif i == 1:
            self.lineEdit_15.setFocus()

    def check_password(self):
        user_password = self.lineEdit_12.text()
        self.cur.execute('''SELECT password FROM password ''')
        password = self.cur.fetchone()
        if password:
            if user_password == password[0]:
                self.tabWidget_3.show()
                self.lineEdit_7.setFocus()
                self.lineEdit_12.clear()

            else:
                message = QMessageBox.warning(self, "Log In ", "Password Is Not Valid !                  ",
                                              QMessageBox.Ok)
                self.lineEdit_12.setFocus()
                self.lineEdit_12.clear()

    def change_password(self):
        passwprd_1 = self.lineEdit_13.text()
        passwprd_2 = self.lineEdit_14.text()
        if passwprd_1 == passwprd_2:
            self.cur.execute('''UPDATE password SET password =%s WHERE id=%s ''', (passwprd_1, 1))
            self.db.commit()
            self.lineEdit_13.clear()
            self.lineEdit_14.clear()
            self.statusBar().showMessage("Password Updated Successfuly")
            self.tabWidget_3.setCurrentIndex(0)
        else:
            message = QMessageBox.warning(self, "Change Password ", "Passwords Is Not Equal !                  ",
                                          QMessageBox.Ok)
            self.lineEdit_13.clear()
            self.lineEdit_14.clear()
            self.lineEdit_13.setFocus()

    ##########################################################################################################
    #############################
    '''Add Drug '''

    ############################
    def add_drug(self):
        main_category = self.comboBox_2.currentIndex()
        drug_name = self.lineEdit_7.text()
        if drug_name.strip(" ") != "":
            if drug_name not in drugs_list:
                self.cur.execute('''INSERT INTO drugs (drug_name , main_category ) VALUES (%s,%s)''',
                                 (drug_name, main_category))
                self.db.commit()
                self.statusBar().showMessage("Drug Add Successfuly")
                self.lineEdit_7.clear()
                self.Add_fulid_to_combobox()
                self.get_drug_from_db()
                self.add()
                self.drug_names_for_report()
            else:
                message = QMessageBox.warning(self, "Add Drug ", "Drug Already Exist !                  ",
                                              QMessageBox.Ok)
                if message == QMessageBox.Ok:
                    self.lineEdit_7.setFocus()
        else:
            self.statusBar().showMessage("Enter Valid Data")

    def search_for_drug_to_update(self):
        drug_name = self.lineEdit_15.text()
        main_category = self.comboBox_4.currentIndex()
        if drug_name.strip(" ") != '':
            try:
                self.cur.execute('''SELECT id FROM drugs WHERE drug_name=%s AND main_category =%s''',
                                 (drug_name, main_category))
                drug_id = self.cur.fetchone()
                self.label_5.setText(str(drug_id[0]))
            except Exception as m:
                pass

    def update_drug(self):
        if self.label_5.text() != '':
            drug_id = self.label_5.text()
            main_category = self.comboBox_5.currentIndex()
            new_drug_name = self.lineEdit_16.text()
            if new_drug_name.strip(" ") != '':
                self.cur.execute('''UPDATE drugs SET drug_name=%s , main_category=%s WHERE id =%s ''',
                                 (new_drug_name, main_category, drug_id))
                self.db.commit()
                self.lineEdit_15.clear()
                self.label_5.clear()
                self.lineEdit_16.clear()
                self.statusBar().showMessage('Drug Updated Successfully')
                self.lineEdit_15.setFocus()
                self.Add_fulid_to_combobox()
                self.get_drug_from_db()
                self.add()
                self.drug_names_for_report()

            else:
                self.statusBar().showMessage('Drug Name Is Not Valid')

    def length_setter(self):

        if self.comboBox_2.currentIndex() == 2:
            self.lineEdit_7.setMaxLength(8)
        else:
            self.lineEdit_7.setMaxLength(20)

    ##########################################################################################################
    #############################
    '''Add Client '''

    ############################
    def add_Client(self):
        if self.label_8.text() == "":
            patient_Name = self.lineEdit.text()
            patient_id = self.lineEdit_2.text()
            phone = self.lineEdit_3.text()
            date = datetime.date.today()
            if patient_Name.strip(" ") == '':
                message = QMessageBox.warning(self, "Add patient ", "patient Name Is Required                  ",
                                              QMessageBox.Ok)
                if message == QMessageBox.Ok:
                    self.lineEdit.setFocus()
            elif patient_id.strip(" ") == '':
                message = QMessageBox.warning(self, "Add patient ", "patient ID Is Required                  ",
                                              QMessageBox.Ok)
                if message == QMessageBox.Ok:
                    self.lineEdit_2.setFocus()
            else:
                if patient_Name.strip(" ") != "" and patient_id.strip(" ") != "":
                    self.cur.execute('''INSERT INTO patient ( name , phone , number,add_date ) VALUES (%s,%s,%s,%s)''',
                                     (patient_Name, phone, patient_id, date))
                    self.db.commit()
                    message = QMessageBox.warning(self, "Add patient ", "patient Add Successfuly                 ",
                                                  QMessageBox.Ok)

                    self.lineEdit_6.setText('1')
                    self.pushButton_2.setEnabled(True)
                    self.cur.execute('''SELECT id FROM patient WHERE name = %s AND number =%s ''',
                                     (patient_Name, patient_id))
                    patient_number = self.cur.fetchone()
                    self.label_8.setText(str(patient_number[0]))
                    self.get_names_from_db()
                    self.patient_names_for_main()
                    self.lineEdit_4.setFocus()
                    self.pushButton_17.show()
                    self.show_daily_statics()


                else:
                    self.statusBar().showMessage('Data Is Not Valid')

        ##########################################################################################################
        #############################
        '''Check Client name from database '''

    ############################
    def Check_Client_name(self):
        self.cur.execute('''DELETE FROM prescription_detail WHERE prescription_no IS NUll''')
        self.db.commit()
        patient_Name = self.lineEdit.text()
        self.cur.execute('''SELECT * FROM patient where name =%s ''', (patient_Name,))
        patient = self.cur.fetchone()
        if patient:
            patient_id = patient[0]
            patient_Name = patient[1]
            patient_number = patient[2]
            phone = patient[3]
            self.lineEdit.setText(str(patient_Name))
            self.lineEdit_2.setText(str(patient_number))
            self.lineEdit_3.setText(str(phone))
            self.label_8.setText(str(patient_id))
            self.lineEdit_6.setText('1')
            self.pushButton_2.setEnabled(True)
            self.lineEdit_4.setFocus()
            self.pushButton_17.show()
            self.check_patient_old_prescription()

    def update_patient(self):
        patient_id = self.label_8.text()
        patient_Name = self.lineEdit.text()
        patient_number = self.lineEdit_2.text()
        phone = self.lineEdit_3.text()
        self.cur.execute('''UPDATE patient SET name=%s , number=%s , phone=%s WHERE id =%s ''',
                         (patient_Name, patient_number, phone, patient_id))
        self.db.commit()
        message = QMessageBox.warning(self, "Add patient ", "patient Updated Successfully                 ",
                                      QMessageBox.Ok)

    ##########################################################################################################
    #############################
    '''Add drug to table '''

    ############################
    def add_drug_to_table(self):
        drug = self.label_23.text()
        dose = self.lineEdit_5.text()
        volume = self.lineEdit_6.text()
        note = self.lineEdit_10.text()
        date = datetime.date.today()
        prescription_no = self.label_32.text()
        if drug.strip(" ") == '':
            message = QMessageBox.warning(self, "Add Drug ", "Drug Field Is Required                  ", QMessageBox.Ok)
            if message == QMessageBox.Ok:
                self.lineEdit_4.setFocus()
        elif dose.strip(" ") == '':
            message = QMessageBox.warning(self, "Add Drug ", "Dose Field Is Required                  ", QMessageBox.Ok)
            if message == QMessageBox.Ok:
                self.lineEdit_5.setFocus()
        elif volume.strip(" ") == '':
            message = QMessageBox.warning(self, "Add Drug ", "Volume Field Is Required                  ",
                                          QMessageBox.Ok)
            if message == QMessageBox.Ok:
                self.lineEdit_6.setFocus()
                self.lineEdit_5.setFocus()

        else:
            if self.label_44.text() != '':

                if drug in check_add_drugs:
                    message = QMessageBox.warning(self, "Add Drug ", "Drug is Already Exist                   ",
                                                  QMessageBox.Ok)
                    if message == QMessageBox.Ok:
                        self.lineEdit_4.setFocus()
                else:
                    fluid_name = self.comboBox.currentText()
                    record_id = self.label_44.text()
                    self.cur.execute('''SELECT id FROM drugs WHERE drug_name=%s ''', (fluid_name,))
                    fluid_id = self.cur.fetchone()
                    self.cur.execute('''UPDATE prescription_detail SET drug = %s , dose= %s , fluid= %s , volume= %s , note= %s 
                                        WHERE id =%s ''', (drug, dose, fluid_id[0], volume, note, record_id))

                    self.label_44.clear()
                    self.lineEdit_4.clear()
                    self.lineEdit_5.clear()
                    self.lineEdit_10.clear()
                    self.lineEdit_6.clear()
                    self.label_23.clear()
                    self.db.commit()
                    check_add_drugs.append(drug)
                    if prescription_no == '':
                        self.retrive_prescription_detail()
                    else:
                        self.retrive_old_prescription_detail()
                    self.statusBar().showMessage("Drug Is Updated ")
                    self.lineEdit_4.setFocus()
            else:
                if drug in check_add_drugs:
                    message = QMessageBox.warning(self, "Add Drug ", "Drug is Already Exist                   ",
                                                  QMessageBox.Ok)
                    if message == QMessageBox.Ok:
                        self.lineEdit_4.setFocus()
                else:
                    fluid_name = self.comboBox.currentText()
                    self.cur.execute('''SELECT id FROM drugs WHERE drug_name=%s ''', (fluid_name,))
                    fluid_id = self.cur.fetchone()
                    if self.label_32.text() != "":
                        self.cur.execute('''INSERT INTO prescription_detail (drug , dose , fluid , volume , note ,prescription_no ,date)
                                            VALUES (%s,%s,%s,%s,%s,%s,%s)
                                        ''', (drug, dose, fluid_id[0], volume, note, prescription_no, date))
                        self.update_dose(drug, dose, fluid_id[0], volume)
                    else:
                        self.cur.execute('''INSERT INTO prescription_detail (drug , dose , fluid , volume , note ,date)
                                            VALUES (%s,%s,%s,%s,%s,%s)
                                        ''', (drug, dose, fluid_id[0], volume, note, date))
                        self.update_dose(drug, dose, fluid_id[0], volume)
                    check_add_drugs.append(drug)
                    self.lineEdit_4.clear()
                    self.lineEdit_5.clear()
                    self.lineEdit_10.clear()
                    self.label_23.clear()
                    self.lineEdit_6.setText('1')
                    if self.label_32.text() != "":
                        self.retrive_old_prescription_detail()
                    else:
                        self.retrive_prescription_detail()
                    self.lineEdit_4.setFocus()

    def get_Selected_row(self):
        try:
            if self.tableWidget.rowCount() > 0:
                current_row = self.tableWidget.currentRow()
                item = self.tableWidget.item(current_row, 0).text()
                self.pushButton_15.show()

                return item
            else:
                message = QMessageBox.warning(self, "Drug ", "No Drug Selected                  ",
                                              QMessageBox.Ok)


        except Exception as m:
            print(m)

    def delete_item_from_table(self):
        try:
            prescription_no = self.label_32.text()
            item_name = self.get_Selected_row()
            if item_name:
                self.cur.execute('''SELECT id FROM drugs WHERE drug_name =%s ''', (item_name,))
                item_id = self.cur.fetchone()
                check_add_drugs.remove(str(item_id[0]))
                if prescription_no:
                    self.cur.execute('''DELETE FROM prescription_detail WHERE drug = %s AND prescription_no =%s  ''',
                                     (item_id[0], prescription_no))
                    self.retrive_old_prescription_detail()
                    self.get_drug_from_old_prescription()
                else:
                    self.cur.execute(
                        '''DELETE FROM prescription_detail WHERE drug = %s AND prescription_no IS NULL  ''',
                        (item_id[0],))
                    self.retrive_prescription_detail()
                self.db.commit()
                self.pushButton_15.hide()
                self.statusBar().showMessage("deleted")

            self.tableWidget.clearSelection()

        except Exception as m:
            print(m)

    def retrive_prescription_detail(self):
        self.cur.execute(
            '''SELECT drug,dose,fluid,volume,note FROM prescription_detail as p WHERE prescription_no IS NULL''')
        self.tableWidget.clearSelection()
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
            self.tableWidget.clearSelection()
        prescription_detail = self.cur.fetchall()
        for row_number, items in enumerate(prescription_detail):
            self.tableWidget.insertRow(row_number)
            for column_number, item in enumerate(items):
                if column_number == 0:
                    self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                    drug_name = self.cur.fetchone()
                    cell = QTableWidgetItem(str(drug_name[0]))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)
                elif column_number == 2:
                    self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                    drug_name = self.cur.fetchone()
                    cell = QTableWidgetItem(str(drug_name[0]))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)
                else:
                    cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)

    def retrive_old_prescription_detail(self):
        prescription_number = self.label_32.text()
        self.cur.execute('''SELECT drug,dose,fluid,volume,note FROM prescription_detail WHERE prescription_no = %s ''',
                         (prescription_number,))
        self.tableWidget.clearSelection()
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
            self.tableWidget.clearSelection()
        prescription_detail = self.cur.fetchall()
        for row_number, items in enumerate(prescription_detail):
            self.tableWidget.insertRow(row_number)
            for column_number, item in enumerate(items):
                if column_number == 0:
                    self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                    drug_name = self.cur.fetchone()
                    cell = QTableWidgetItem(str(drug_name[0]))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)
                elif column_number == 2:
                    self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                    drug_name = self.cur.fetchone()
                    cell = QTableWidgetItem(str(drug_name[0]))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)
                else:
                    cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)
        self.statusBar().showMessage(" ")

    def Add_drug_with_old_prescription(self):

        if self.tableWidget.rowCount() <= 0:
            self.statusBar().showMessage("There Is No Thing To Save")
        else:
            self.db.commit()
            self.tableWidget.clearSelection()
            while self.tableWidget.rowCount() > 0:
                self.tableWidget.removeRow(0)
                self.tableWidget.clearSelection()
            self.clear_data()
            self.statusBar().showMessage("Prescription Saved Successfully")
            self.lineEdit.setFocus()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            self.lineEdit_10.clear()
            self.label_23.clear()
            self.pushButton_17.hide()
            self.lineEdit_6.setText('1')
            self.show_daily_statics()
            check_add_drugs.clear()
            self.label_38.clear()

    def add_drug_with_new_prescription(self):
        patient_id = self.label_8.text()  # main_prescription
        date = datetime.date.today()  # main_prescription
        if self.tableWidget.rowCount() <= 0:
            self.statusBar().showMessage("There Is No Thing To Save")
        else:
            self.cur.execute('''INSERT INTO prescription_no (patient_id,date) VALUES (%s,%s)''', (patient_id, date))
            prescription_no = self.cur.lastrowid
            self.cur.execute('''UPDATE prescription_detail SET prescription_no =%s WHERE prescription_no IS NULL ''',
                             (prescription_no,))
            self.db.commit()
            self.tableWidget.clearSelection()
            while self.tableWidget.rowCount() > 0:
                self.tableWidget.removeRow(0)
                self.tableWidget.clearSelection()
            self.clear_data()
            self.statusBar().showMessage("Prescription Saved Successfully")
            self.lineEdit.setFocus()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            self.lineEdit_10.clear()
            self.label_23.clear()
            self.pushButton_17.hide()
            self.lineEdit_6.setText('1')
            self.show_daily_statics()
            check_add_drugs.clear()
            self.label_38.clear()

    def update_dose(self, drug, dose, fluid, volume):
        self.cur.execute('''UPDATE drugs set drug_outgoing = drug_outgoing +%s WHERE id = %s ''', (dose, drug))
        self.cur.execute('''UPDATE drugs set drug_outgoing = drug_outgoing +%s WHERE id = %s ''', (volume, fluid))
        self.db.commit()

    def check_patient_old_prescription(self):
        patient_id = self.label_8.text()
        self.cur.execute('''SELECT MAX(id) FROM prescription_no WHERE patient_id = %s ''', (patient_id,))
        prescription_number = self.cur.fetchone()
        if prescription_number[0] is not None:
            self.cur.execute('''SELECT date FROM prescription_no WHERE id = %s ''', (prescription_number[0],))
            date = self.cur.fetchone()
            self.label_38.setText(str(date[0]))
            result = prescription_number[0]
            self.label_32.setText(str(result))
            self.retrive_old_prescription_detail()
            self.get_drug_from_old_prescription()

    def handel_save_method(self):
        prescription_number = self.label_32.text()
        if prescription_number:
            self.Add_drug_with_old_prescription()
            self.get_names_from_db()
            self.patient_names_for_main()
            self.patient_names_for_report()
        else:
            self.add_drug_with_new_prescription()
            self.get_names_from_db()
            self.patient_names_for_main()
            self.patient_names_for_report()
        self.lineEdit.setFocus()

    def new_prescription_for_patient_has_old_one(self):
        message = QMessageBox.warning(self, "New prescription  ", "All Drug Will Be Copy                  ",
                                      QMessageBox.Yes, QMessageBox.No)
        if message == QMessageBox.Yes:
            self.tableWidget.clearSelection()
            while self.tableWidget.rowCount() > 0:
                self.tableWidget.removeRow(0)
                self.tableWidget.clearSelection()
            prescription_number = self.label_32.text()
            date = datetime.date.today()
            self.cur.execute(
                '''SELECT drug , dose , fluid , volume , note FROM prescription_detail WHERE prescription_no =%s ''',
                (prescription_number,))
            prescription_det = self.cur.fetchall()
            for drug in prescription_det:
                self.cur.execute('''INSERT INTO prescription_detail (drug , dose , fluid , volume , note ,date)
                                                      VALUES (%s,%s,%s,%s,%s,%s)
                                                  ''', (drug[0], drug[1], drug[2], drug[3], drug[4], date))
                # self.update_dose(drug[0], drug[1], drug[2], drug[3], drug[4])
                check_add_drugs.append(drug)
            self.retrive_prescription_detail()
            self.lineEdit_4.setFocus()
            self.label_32.clear()
            self.label_38.clear()

        if message == QMessageBox.No:
            self.lineEdit_4.setFocus()
            self.tableWidget.clearSelection()
            while self.tableWidget.rowCount() > 0:
                self.tableWidget.removeRow(0)
                self.tableWidget.clearSelection()
            self.label_32.clear()
            self.label_38.clear()
            check_add_drugs.clear()
        self.lineEdit_4.setFocus()

    def get_drug_from_old_prescription(self):
        check_add_drugs.clear()
        for currentRow in range(self.tableWidget.rowCount()):
            for currentColumn in range(self.tableWidget.columnCount()):
                try:
                    if currentColumn == 0:
                        drug_name = str(self.tableWidget.item(currentRow, currentColumn).text())
                        self.cur.execute('''SELECT id FROM drugs where drug_name =%s ''', (drug_name,))
                        drug_id = self.cur.fetchone()
                        check_add_drugs.append(str(drug_id[0]))


                except AttributeError:
                    pass

    ##########################################################################################################
    #############################
    #     '''Check drug name from database '''
    ############################
    def check_drug_name(self):
        drug = self.lineEdit_4.text()
        if drug.strip(" ") != "":
            self.cur.execute('''SELECT id FROM drugs where drug_name =%s ''', (drug,))
            drug_id = self.cur.fetchone()

            try:
                if drug_id[0]:
                    self.label_23.setText(str(drug_id[0]))
            except Exception as m:
                pass

    ##########################################################################################################
    #############################
    '''Add fulid to combobox  '''

    ############################
    def Add_fulid_to_combobox(self):
        self.cur.execute('''SELECT drug_name FROM drugs WHERE main_category=2 ''')
        drug_name = self.cur.fetchall()
        self.comboBox.clear()
        for drug in drug_name:
            self.comboBox.addItem(drug[0])

    ##########################################################################################################
    #############################
    ''' modify drug '''

    ############################
    def get_modify_drug(self):
        self.get_drug_from_old_prescription()
        drug_name = self.get_Selected_row()
        prescription_no = self.label_32.text()
        if drug_name and prescription_no:

            self.cur.execute('''SELECT id FROM drugs WHERE drug_name = %s ''', (drug_name,))
            drug_id = self.cur.fetchone()
            check_add_drugs.remove(str(drug_id[0]))
            self.cur.execute('''SELECT id , drug , dose , fluid,volume , note FROM prescription_detail 
                                WHERE drug = %s AND prescription_no = %s ''', (drug_id[0], prescription_no))
            data = self.cur.fetchone()
            self.label_44.setText(str(data[0]))
            self.lineEdit_4.setText(drug_name)
            self.lineEdit_5.setText(str(data[2]))
            self.lineEdit_6.setText(str(data[4]))
            self.lineEdit_10.setText(str(data[5]))
            self.label_23.setText(str(data[1]))
            self.cur.execute('''SELECT drug_name FROm drugs WHERE id = %s ''', (data[3],))
            fluid_name = self.cur.fetchone()
            all_item = {}
            for i in range(self.comboBox.count()):
                all_item[i] = self.comboBox.itemText(i)
            for key, value in all_item.items():
                if value == fluid_name[0]:
                    self.comboBox.setCurrentIndex(key)
        elif drug_name and prescription_no == '':
            self.cur.execute('''SELECT id FROM drugs WHERE drug_name = %s ''', (drug_name,))
            drug_id = self.cur.fetchone()
            check_add_drugs.remove(str(drug_id[0]))
            self.cur.execute('''SELECT id , drug , dose , fluid,volume , note FROM prescription_detail 
                                WHERE drug = %s AND prescription_no IS NULL ''', (drug_id[0],))
            data = self.cur.fetchone()
            self.label_44.setText(str(data[0]))
            self.lineEdit_4.setText(drug_name)
            self.lineEdit_5.setText(str(data[2]))
            self.lineEdit_6.setText(str(data[4]))
            self.lineEdit_10.setText(str(data[5]))
            self.label_23.setText(str(data[1]))
            self.cur.execute('''SELECT drug_name FROm drugs WHERE id = %s ''', (data[3],))
            fluid_name = self.cur.fetchone()
            all_item = {}
            for i in range(self.comboBox.count()):
                all_item[i] = self.comboBox.itemText(i)
            for key, value in all_item.items():
                if value == fluid_name[0]:
                    self.comboBox.setCurrentIndex(key)

    ##########################################################################################################
    #############################
    ''' Patient Mangement '''

    ############################
    def clear_patient_mang_data(self):
        self.lineEdit_17.clear()
        self.lineEdit_18.clear()
        self.label_41.clear()
        while self.tableWidget_6.rowCount() > 0:
            self.tableWidget_6.removeRow(0)
            self.tableWidget_6.clearSelection()
        while self.tableWidget_7.rowCount() > 0:
            self.tableWidget_7.removeRow(0)
            self.tableWidget_7.clearSelection()

    def get_patient_data_for_mangment(self):
        patient_name = self.lineEdit_17.text()
        patient_num = self.lineEdit_18.text()
        if patient_name.strip(" ") != "":
            self.cur.execute('''SELECT id , number FROM patient WHERE name = %s ''', (patient_name,))
            patient_id = self.cur.fetchone()
            if patient_id is not None:
                self.label_41.setText(str(patient_id[0]))
                self.lineEdit_18.setText(str(patient_id[1]))
                self.get_patient_prescription_no_for_mang()
            else:
                self.statusBar().showMessage("No Data Found For This Name ")

        elif patient_num.strip(" ") != "":
            self.cur.execute('''SELECT id , name FROM patient WHERE number = %s ''', (patient_num,))
            patient_id = self.cur.fetchone()
            if patient_id is not None:
                self.lineEdit_17.setText(str(patient_id[1]))
                self.label_41.setText(str(patient_id[0]))
                self.get_patient_prescription_no_for_mang()

            else:
                self.statusBar().showMessage("No Data Found For This Id")

    def get_patient_prescription_no_for_mang(self):
        patient_id = self.label_41.text()
        if self.label_41.text() != '':
            self.cur.execute('''SELECT id , date FROM prescription_no WHERE patient_id =%s ''', (patient_id,))
            prescription_no = self.cur.fetchall()
            self.tableWidget_6.clearSelection()
            while self.tableWidget_6.rowCount() > 0:
                self.tableWidget_6.removeRow(0)
                self.tableWidget_6.clearSelection()
            for row_number, items in enumerate(prescription_no):
                self.tableWidget_6.insertRow(row_number)
                for column_number, item in enumerate(items):
                    cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget_6.setItem(row_number, column_number, cell)

    def get_Selected_prescription_no(self):
        try:
            if self.tableWidget_6.rowCount() > 0:
                current_row = self.tableWidget_6.currentRow()
                item = self.tableWidget_6.item(current_row, 0).text()
                self.cur.execute(
                    '''SELECT drug , dose , fluid,volume,note FROM prescription_detail WHERE prescription_no =%s ''',
                    (item,))
                self.tableWidget_7.clearSelection()
                rescription_detail = self.cur.fetchall()
                self.tableWidget_7.clearSelection()
                while self.tableWidget_7.rowCount() > 0:
                    self.tableWidget_7.removeRow(0)
                    self.tableWidget_7.clearSelection()
                for row_number, items in enumerate(rescription_detail):
                    self.tableWidget_7.insertRow(row_number)
                    for column_number, item in enumerate(items):
                        if column_number == 0:
                            self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                            drug_name = self.cur.fetchone()
                            cell = QTableWidgetItem(str(drug_name[0]))
                            cell.setTextAlignment(Qt.AlignHCenter)
                            self.tableWidget_7.setItem(row_number, column_number, cell)
                        elif column_number == 2:
                            self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                            drug_name = self.cur.fetchone()
                            cell = QTableWidgetItem(str(drug_name[0]))
                            cell.setTextAlignment(Qt.AlignHCenter)
                            self.tableWidget_7.setItem(row_number, column_number, cell)
                        else:

                            cell = QTableWidgetItem(str(item))
                            cell.setTextAlignment(Qt.AlignHCenter)
                            self.tableWidget_7.setItem(row_number, column_number, cell)

        except Exception as m:
            print(m)

    def delete_patient_visit(self):
        if self.tableWidget_6.rowCount() > 0:
            current_row = self.tableWidget_6.currentRow()
            if current_row != -1:
                item = self.tableWidget_6.item(current_row, 0).text()
                message = QMessageBox.warning(self, "Delete Visit ",
                                              "ARE YOU SURE YOU WILL Delete Visit !                  ",
                                              QMessageBox.Yes, QMessageBox.No)
                if message == QMessageBox.Yes:
                    self.cur.execute('''DELETE FROM prescription_detail WHERE prescription_no = %s ''', (item,))
                    self.cur.execute('''DELETE FROM prescription_no WHERE id = %s ''', (item,))
                    self.db.commit()
                    self.get_patient_prescription_no_for_mang()
                    self.tableWidget_6.clearSelection()
                    message = QMessageBox.warning(self, "Deleted Successfully  ",
                                                  "Patient Visit Deleted Successfully   !                  ",
                                                  QMessageBox.Ok)

            else:
                self.statusBar().showMessage("No Thing Selected !")

    def delete_patient_data(self):
        try:
            patient_name = self.lineEdit_17.text()
            patient_num = self.lineEdit_18.text()
            if patient_name.strip(" ") != "" and patient_num.strip(" ") != '':
                message = QMessageBox.warning(self, "Delete ALL PATIENT DATA  ",
                                              "ARE YOU SURE YOU WILL Delete  ALL PATIENT DATA  !                  ",
                                              QMessageBox.Yes, QMessageBox.No)
                if message == QMessageBox.Yes:
                    self.cur.execute('''SELECT id FROM patient WHERE name =%s AND number =%s ''',
                                     (patient_name, patient_num))
                    patient_id = self.cur.fetchone()
                    self.cur.execute('''SELECT id FROM prescription_no WHERE patient_id = %s ''', (patient_id[0],))
                    item = self.cur.fetchall()
                    if item:
                        for one in item:
                            self.cur.execute('''DELETE FROM prescription_detail WHERE prescription_no = %s ''',
                                             (one[0],))
                            self.cur.execute('''DELETE FROM prescription_no WHERE id = %s ''', (one[0],))
                    self.cur.execute('''DELETE FROM patient WHERE id = %s ''', (patient_id[0],))
                    self.db.commit()
                    self.get_names_from_db()
                    self.patient_names_for_main()
                    self.patient_names_for_report()
                    self.get_patient_prescription_no_for_mang()
                    self.get_Selected_prescription_no()
                    self.clear_patient_mang_data()
                    message = QMessageBox.warning(self, "Deleted Successfully  ",
                                                  "All Patient Data Deleted Successfully   !                  ",
                                                  QMessageBox.Ok)


        except Exception as m:
            print(m)

    ##########################################################################################################
    #############################
    '''Search For Patient '''

    ############################
    def search_for_patient(self):
        patient_name = self.lineEdit_8.text()
        patient_num = self.lineEdit_11.text()
        date_from = self.dateEdit_2.date().toPyDate()
        date_to = self.dateEdit.date().toPyDate()
        patient_id = 0
        if patient_name.strip(" ") != "":
            self.cur.execute('''SELECT id , number FROM patient WHERE name = %s ''', (patient_name,))
            patient_id = self.cur.fetchone()
            self.lineEdit_11.setText(str(patient_id[1]))
        elif patient_num.strip(" ") != "":
            self.cur.execute('''SELECT id , name FROM patient WHERE number = %s ''', (patient_num,))
            patient_id = self.cur.fetchone()
            self.lineEdit_8.setText(str(patient_id[1]))

        else:
            self.statusBar().showMessage("No Data Found For This Name Or Id")
        if patient_id:
            self.cur.execute('''SELECT p.drug,p.dose,p.fluid,p.volume,p.note ,num.date FROM prescription_detail as p   
                                LEFT JOIN prescription_no as num  ON  p.prescription_no =  num.id 
                                WHERE num.patient_id = %s  AND p.date BETWEEN %s AND  %s
                                 ''', (patient_id[0], date_from, date_to))
            patient_data = self.cur.fetchall()
            while self.tableWidget_2.rowCount() > 0:
                self.tableWidget_2.removeRow(0)
                self.tableWidget_2.clearSelection()
            for row_number, items in enumerate(patient_data):
                self.tableWidget_2.insertRow(row_number)
                for column_number, item in enumerate(items):
                    if column_number == 0:
                        self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                        drug_name = self.cur.fetchone()
                        cell = QTableWidgetItem(str(drug_name[0]))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        self.tableWidget_2.setItem(row_number, column_number, cell)
                    elif column_number == 2:
                        self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                        drug_name = self.cur.fetchone()
                        cell = QTableWidgetItem(str(drug_name[0]))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        self.tableWidget_2.setItem(row_number, column_number, cell)
                    else:
                        cell = QTableWidgetItem(str(item))
                        cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget_2.setItem(row_number, column_number, cell)

        if self.tableWidget_2.rowCount() <= 0:
            row = self.tableWidget_2.rowCount()
            self.tableWidget_2.setRowCount(row + 1)
            col = 0
            cell = QTableWidgetItem(str(" No Data Found "))
            self.tableWidget_2.setItem(row, col, cell)

        ##########################################################################################################
        #############################
        '''Search For DRUG '''

    ############################
    def search_for_drug(self):
        drug_name = self.lineEdit_9.text()

        if drug_name.strip(" ") != "":
            self.cur.execute('''SELECT id , main_category FROM drugs WHERE drug_name = %s ''', (drug_name,))
            drug_id = self.cur.fetchone()
            date_from = self.dateEdit_4.date().toPyDate()
            date_to = self.dateEdit_3.date().toPyDate()
            drug_data = ""
            if drug_id:
                if drug_id[1] != 2:
                    self.cur.execute('''SELECT d.drug_name ,SUM(p.dose)  FROM drugs as d   
                                        LEFT JOIN prescription_detail as p ON p.drug = d.id
                                        WHERE d.id = %s AND date BETWEEN %s AND  %s
                                         ''', (drug_id[0], date_from, date_to))
                    drug_data = self.cur.fetchall()
                elif drug_id[1] == 2:
                    self.cur.execute('''SELECT d.drug_name ,SUM(p.volume)  FROM drugs as d
                                        LEFT JOIN prescription_detail as p ON p.fluid = d.id
                                        WHERE d.id = %s AND date BETWEEN %s AND  %s
                                         ''', (drug_id[0], date_from, date_to))
                    drug_data = self.cur.fetchall()
                if drug_data:
                    while self.tableWidget_3.rowCount() > 0:
                        self.tableWidget_3.removeRow(0)
                        self.tableWidget_3.clearSelection()
                    for row_number, items in enumerate(drug_data):
                        self.tableWidget_3.insertRow(row_number)
                        for column_number, item in enumerate(items):
                            if column_number == 1:
                                if item is not None:
                                    cell = QTableWidgetItem(str(item))
                                    cell.setTextAlignment(Qt.AlignHCenter)
                                    self.tableWidget_3.setItem(row_number, column_number, cell)

                            else:
                                cell = QTableWidgetItem(str(item))
                                cell.setTextAlignment(Qt.AlignHCenter)
                                self.tableWidget_3.setItem(row_number, column_number, cell)

        if self.tableWidget_3.rowCount() <= 0:
            row = self.tableWidget_2.rowCount()
            self.tableWidget_3.setRowCount(row + 1)
            col = 0
            cell = QTableWidgetItem(str(" No Data Found "))
            self.tableWidget_3.setItem(row, col, cell)

    # def get_genral_search_auto(self):
    #
    #     if self.tabWidget_2.currentIndex() == 2 :
    #         self.db.commit()
    #         self.tableWidget_4.clearSelection()
    #         self.genral_search()
    #         threading.Timer(120.0, self.get_genral_search_auto).start()
    #         self.statusBar().showMessage("Updated")
    # def message_update(self):
    #     self.tableWidget_4.clearSelection()
    #     threading.Timer(10.0, self.message_update).start()
    #     self.statusBar().showMessage("")

    # def savefile(self):
    #     filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)")
    #     wbk = xlwt.Workbook()
    #     sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
    #     style = xlwt.XFStyle()
    #     font = xlwt.Font()
    #     font.bold = True
    #     style.font = font
    #     self.add2(sheet)
    #     wbk.save(filename)
    #
    # def add2(self, sheet):
    #
    #     for currentColumn in range(self.tableWidget_2.columnCount()):
    #         for currentRow in range(self.tableWidget_2.rowCount()):
    #             try:
    #                 teext = str(self.tableWidget_2.item(currentRow, currentColumn).text())
    #                 sheet.write(currentRow, currentColumn, teext)
    #             except AttributeError:
    #                 print(("error"))

    def save_patient_search(self):
        try:
            pa_id = self.lineEdit_11.text()
            pa_name = self.lineEdit_8.text()
            d_from = self.dateEdit_2.date().toPyDate()
            d_to = self.dateEdit.date().toPyDate()
            def_path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', def_path, ".xlsx(*.xlsx)")
            if filename:
                wb = Workbook(filename)
                sheet1 = wb.add_worksheet()
                cell_format = wb.add_format({'bold': True})
                cell_format.set_font_size(20)
                sheet1.set_column(0, 0, 30, cell_format)
                sheet1.set_column(2, 2, 30, cell_format)
                sheet1.set_column(4, 4, 30, cell_format)
                sheet1.set_column(1, 1, 15, cell_format)
                sheet1.set_column(3, 3, 15, cell_format)
                sheet1.set_column(5, 5, 15, cell_format)
                main_cell = wb.add_format({'bold': True, 'bg_color': 'gray', 'font_size': 20})
                sheet1.set_row(0, None, cell_format)
                sheet1.set_row(1, None, cell_format)
                sheet1.set_row(2, None, cell_format)
                sheet1.set_row(3, None, main_cell)
                cell_format.set_align('center')
                main_cell.set_align('center')
                cell_format.set_font_size(14)
                sheet1.merge_range(0, 0, 0, 5, 'Patient Search', cell_format)
                sheet1.write(1, 0, ' Patient Name')
                sheet1.write(1, 1, pa_name)
                sheet1.write(1, 2, ' Patient ID ')
                sheet1.write(1, 3, pa_id)
                sheet1.write(2, 0, ' From ')
                sheet1.write(2, 1, str(d_from))
                sheet1.write(2, 2, ' To ')
                sheet1.write(2, 3, str(d_to))
                sheet1.write(3, 0, 'Drug')
                sheet1.write(3, 1, 'Dose')
                sheet1.write(3, 2, 'Fluid')
                sheet1.write(3, 3, 'Volume')
                sheet1.write(3, 4, 'Note')

                for currentColumn in range(self.tableWidget_2.columnCount()):
                    for currentRow in range(self.tableWidget_2.rowCount()):
                        try:
                            teext = str(self.tableWidget_2.item(currentRow, currentColumn).text())
                            sheet1.write(currentRow + 4, currentColumn, str(teext))
                        except AttributeError:
                            pass
                wb.close()
                self.statusBar().showMessage('Report Created Successfully')
        except Exception as m:
            pass

    def save_drug_search(self):
        try:
            d_from = self.dateEdit_4.date().toPyDate()
            d_to = self.dateEdit_3.date().toPyDate()
            def_path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', def_path, ".xlsx(*.xlsx)")
            if filename:
                wb = Workbook(filename)
                sheet1 = wb.add_worksheet()
                cell_format = wb.add_format({'bold': True})
                main_cell = wb.add_format({'bold': True, 'bg_color': 'gray', 'font_size': 20})
                sheet1.set_column(0, 1, 30, cell_format)
                cell_format.set_align('center')
                main_cell.set_align('center')
                cell_format.set_font_size(14)
                sheet1.set_row(0, None, cell_format)
                sheet1.set_row(1, None, cell_format)
                sheet1.set_row(2, None, cell_format)
                sheet1.set_row(3, None, main_cell)
                sheet1.merge_range(0, 0, 0, 3, 'Drug Search', cell_format)
                sheet1.write(1, 0, ' From ')
                sheet1.write(1, 1, str(d_from))
                sheet1.write(2, 0, ' To ')
                sheet1.write(2, 1, str(d_to))
                sheet1.write(3, 0, 'Drug')
                sheet1.write(3, 1, 'Total Dose')

                for currentColumn in range(self.tableWidget_3.columnCount()):
                    for currentRow in range(self.tableWidget_3.rowCount()):
                        try:
                            teext = str(self.tableWidget_3.item(currentRow, currentColumn).text())
                            sheet1.write(currentRow + 4, currentColumn, str(teext))
                        except AttributeError:
                            pass
                wb.close()
                self.statusBar().showMessage('Report Created Successfully')
        except Exception as m:
            pass

    def save_genral_search(self):
        try:
            d_from = self.dateEdit_6.date().toPyDate()
            d_to = self.dateEdit_5.date().toPyDate()
            def_path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', def_path, ".xlsx(*.xlsx)")
            if filename:
                wb = Workbook(filename)
                sheet1 = wb.add_worksheet()
                cell_format = wb.add_format({'bold': True})
                cell_format.set_font_size(14)
                cell_format.set_bold()
                cell_format.set_align('center')
                main_cell = wb.add_format({'bold': True, 'bg_color': 'gray', 'font_size': 20})
                main_cell.set_align('center')

                sheet1.set_column(0, 1, 30, cell_format)
                sheet1.set_column(2, 4, 15, cell_format)
                sheet1.set_column(5, 5, 30, cell_format)
                sheet1.set_column(6, 6, 15, cell_format)
                sheet1.set_row(0, None, cell_format)
                sheet1.set_row(1, None, cell_format)
                sheet1.set_row(2, None, main_cell)
                sheet1.merge_range(0, 0, 0, 7, 'Genral Search', cell_format)
                sheet1.write(1, 0, ' From ')
                sheet1.write(1, 1, str(d_from))
                sheet1.write(1, 3, ' To ')
                sheet1.write(1, 4, str(d_to))
                sheet1.write(2, 0, 'Patient Name')
                sheet1.write(2, 1, 'Patient ID')
                sheet1.write(2, 2, 'Drug')
                sheet1.write(2, 3, 'Dose')
                sheet1.write(2, 4, 'Fluid')
                sheet1.write(2, 5, 'Volume')
                sheet1.write(2, 6, 'Note')
                sheet1.write(2, 7, 'Date')

                for currentColumn in range(self.tableWidget_4.columnCount()):
                    for currentRow in range(self.tableWidget_4.rowCount()):
                        try:
                            teext = str(self.tableWidget_4.item(currentRow, currentColumn).text())
                            sheet1.write(currentRow + 3, currentColumn, str(teext))
                        except AttributeError:
                            pass
                wb.close()
                self.statusBar().showMessage('Report Created Successfully')
        except Exception as m:
            pass

    def save_all_drug_dose(self):
        try:
            d_from = self.dateEdit_8.date().toPyDate()
            d_to = self.dateEdit_7.date().toPyDate()
            def_path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', def_path, ".xlsx(*.xlsx)")
            if filename:
                wb = Workbook(filename)
                sheet1 = wb.add_worksheet()
                cell_format = wb.add_format({'bold': True})
                cell_format.set_font_size(14)
                cell_format.set_bold()
                cell_format.set_align('center')
                main_cell = wb.add_format({'bold': True, 'bg_color': 'gray', 'font_size': 20})
                main_cell.set_align('center')

                sheet1.set_column(0, 0, 30, cell_format)
                sheet1.set_column(1, 1, 15, cell_format)
                sheet1.set_row(0, None, cell_format)
                sheet1.set_row(1, None, cell_format)
                sheet1.set_row(2, None, cell_format)
                sheet1.set_row(3, None, main_cell)
                sheet1.merge_range(0, 0, 0, 2, 'All Drug Dose Search', cell_format)
                sheet1.write(1, 0, ' From ')
                sheet1.write(1, 1, str(d_from))
                sheet1.write(2, 0, ' To ')
                sheet1.write(2, 1, str(d_to))
                sheet1.write(3, 0, 'Drug Name')
                sheet1.write(3, 1, 'Total Dose')
                for currentColumn in range(self.tableWidget_5.columnCount()):
                    for currentRow in range(self.tableWidget_5.rowCount()):
                        try:
                            teext = str(self.tableWidget_5.item(currentRow, currentColumn).text())
                            sheet1.write(currentRow + 4, currentColumn, str(teext))
                        except AttributeError:
                            pass
                wb.close()
                self.statusBar().showMessage('Report Created Successfully')
        except Exception as m:
            pass

    ##########################################################################################################
    #############################
    '''Genral Search '''

    ############################
    def genral_search(self):
        date_from = self.dateEdit_6.date().toPyDate()
        date_to = self.dateEdit_5.date().toPyDate()
        # self.cur.execute('''SELECT pname.name FROM prescription_detail as pre
        #                     LEFT JOIN prescription_no as pid ON  pid.id = pre.prescription_no
        #                     LEFT JOIN patient as pname ON pid.patient_id = pname.id
        #                     ORDER BY pre.id DESC LIMIT 1''')
        # last_prescription = self.cur.fetchone()

        self.cur.execute('''SELECT  pname.name ,pname.number, d.drug_name , p.dose ,p.fluid , p.volume , p.note , p.date,p.is_checked , p.prescription_no FROM prescription_detail as p 
                            JOIN drugs as d ON p.drug = d.id
                            LEFT JOIN prescription_no as pid ON  pid.id = p.prescription_no 
                            LEFT JOIN patient as pname ON pid.patient_id = pname.id 
                            WHERE p.date BETWEEN %s AND  %s
                            ORDER BY p.date desc, p.id desc 
                            ''', (date_from, date_to))
        full_search = self.cur.fetchall()
        self.tableWidget_4.clearSelection()
        while self.tableWidget_4.rowCount() > 0:
            self.tableWidget_4.removeRow(0)
            self.tableWidget_4.clearSelection()
        for row_number, items in enumerate(full_search):
            self.tableWidget_4.insertRow(row_number)
            for column_number, item in enumerate(items):
                if column_number == 4:
                    self.cur.execute('''SELECT drug_name From drugs WHERE id = %s''', (item,))
                    drug_name = self.cur.fetchone()
                    cell = QTableWidgetItem(str(drug_name[0]))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget_4.setItem(row_number, column_number, cell)
                elif column_number == 8:
                    if item == 0:
                        chkBoxItem = QTableWidgetItem()
                        chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        chkBoxItem.setCheckState(Qt.Unchecked)
                        self.tableWidget_4.setItem(row_number, column_number, chkBoxItem)

                    else:
                        chkBoxItem = QTableWidgetItem()
                        chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        chkBoxItem.setCheckState(Qt.Checked)
                        self.tableWidget_4.setItem(row_number, column_number, chkBoxItem)
                        self.check_color_green(row_number)


                else:
                    cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget_4.setItem(row_number, column_number, cell)


    def check_color_green(self, item):
        self.tableWidget_4.item(item, 0).setBackground(QColor("green"))
        self.tableWidget_4.item(item, 1).setBackground(QColor("green"))
        self.tableWidget_4.item(item, 2).setBackground(QColor("green"))
        self.tableWidget_4.item(item, 3).setBackground(QColor("green"))
        self.tableWidget_4.item(item, 4).setBackground(QColor("green"))
        self.tableWidget_4.item(item, 5).setBackground(QColor("green"))
        self.tableWidget_4.item(item, 6).setBackground(QColor("green"))
        self.tableWidget_4.item(item, 7).setBackground(QColor("green"))
        self.tableWidget_4.item(item, 8).setBackground(QColor("green"))

    def update_check_status(self, row, column):
        item = self.tableWidget_4.item(row, column)
        lastState = item.data(LastStateRole)
        currentState = item.checkState()
        if currentState != lastState:
            if currentState == Qt.Checked:
                code = self.tableWidget_4.item(row, 1).text()
                name = self.tableWidget_4.item(row, 0).text()
                self.cur.execute('''SELECT id FROM patient WHERE number=%s AND name = %s ''', (code, name))
                pa_id = self.cur.fetchone()
                self.cur.execute('''select id from prescription_no  WHERE patient_id=%s  ORDER BY id DESC LIMIT 1  ''',
                                 (pa_id[0],))
                pre_id = self.cur.fetchone()
                self.cur.execute('''UPDATE prescription_detail SET is_checked =%s WHERE prescription_no=%s ''',
                                 (1, pre_id[0]))
                self.db.commit()

    ##########################################################################################################
    #############################
    # '''Genral Search '''
    ############################
    def genral_drug_dose(self):
        main_category = -1
        user_choise = self.comboBox_3.currentIndex()
        if user_choise == 0:
            main_category = 0
        elif user_choise == 1:
            main_category = 1
        else:
            main_category = 2
        date_from = self.dateEdit_8.date().toPyDate()
        date_to = self.dateEdit_7.date().toPyDate()
        self.cur.execute(''' SELECT d.drug_name , SUM(p.dose) FROM prescription_detail as p 
                            LEFT JOIN drugs AS d ON p.drug = d.id 
                            WHERE d.main_category =%s AND p.date BETWEEN %s AND  %s 
                            GROUP BY d.id
                            ORDER BY p.date, d.drug_name 

                            ''', (main_category, date_from, date_to))
        all_drugs = self.cur.fetchall()
        self.cur.execute(''' SELECT d.drug_name , SUM(p.volume) FROM prescription_detail as p 
                            LEFT JOIN drugs AS d ON p.fluid = d.id 
                            WHERE d.main_category =%s AND p.date BETWEEN %s AND  %s 
                            GROUP BY d.id
                            ORDER BY p.date, d.drug_name 
                            ''', (main_category, date_from, date_to))
        all_fluid = self.cur.fetchall()

        while self.tableWidget_5.rowCount() > 0:
            self.tableWidget_5.removeRow(0)
            self.tableWidget_5.clearSelection()
        for row_number, items in enumerate(all_fluid):
            self.tableWidget_5.insertRow(row_number)
            for column_number, item in enumerate(items):
                cell = QTableWidgetItem(str(item))
                cell.setTextAlignment(Qt.AlignHCenter)
                self.tableWidget_5.setItem(row_number, column_number, cell)
        for row_number, items in enumerate(all_drugs):
            self.tableWidget_5.insertRow(row_number)
            for column_number, item in enumerate(items):
                if column_number == 1:
                    data = str(item)
                    if data.split(".")[-1] == "0":
                        print("here")
                        cell = QTableWidgetItem(str(data.split(".")[0]))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        self.tableWidget_5.setItem(row_number, column_number, cell)
                    else:
                        new = round(item, 2)
                        cell = QTableWidgetItem(str(new))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        self.tableWidget_5.setItem(row_number, column_number, cell)
                else:
                    cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget_5.setItem(row_number, column_number, cell)

    def show_daily_statics(self):
        date = datetime.date.today()
        self.cur.execute('''SELECT distinct COUNT(p.id) FROM patient as p WHERE add_date=%s ''', (date,))
        total_new = self.cur.fetchone()
        self.lcdNumber_3.display(int(total_new[0]))

    def show_daily_statics_costum(self):
        date_from = self.dateEdit_9.date().toPyDate()
        date_to = self.dateEdit_10.date().toPyDate()
        self.cur.execute('''SELECT COUNT(distinct p.id) FROM patient as p WHERE add_date BETWEEN %s AND %s ''',
                         (date_from, date_to))
        total_old = self.cur.fetchone()
        self.lcdNumber_4.display(int(total_old[0]))

    def go_to_today(self):

        self.tabWidget.setCurrentIndex(4)

    ##########################################################################################################
    #############################
    '''Set_TOday_date '''

    ############################
    def set_today_date(self):
        date = datetime.date.today()
        self.dateEdit_2.setDate(date)
        self.dateEdit.setDate(date)
        self.dateEdit_3.setDate(date)
        self.dateEdit_4.setDate(date)
        self.dateEdit_5.setDate(date)
        self.dateEdit_6.setDate(date)
        self.dateEdit_7.setDate(date)
        self.dateEdit_8.setDate(date)
        self.dateEdit_9.setDate(date)
        self.dateEdit_10.setDate(date)

    def clear_database_data(self):
        message = QMessageBox.warning(self, "Clear DATABASE ",
                                      "ARE YOU SURE YOU WILL CLEAR ALL DATA WILL BE LOSS !                  ",
                                      QMessageBox.Yes, QMessageBox.No)
        if message == QMessageBox.Yes:
            message = QMessageBox.warning(self, "Clear DATABASE ",
                                          "Last Step Press No To Clear DataBase !                  ",
                                          QMessageBox.Yes, QMessageBox.No)
            if message == QMessageBox.No:
                self.cur.execute('''DELETE FROM prescription_detail WHERE id != 0''')
                self.cur.execute('''DELETE FROM prescription_no WHERE id != 0''')
                self.cur.execute('''DELETE FROM drugs WHERE id != 0''')
                self.cur.execute('''DELETE FROM patient WHERE id != 0''')
                self.db.commit()
                names_list.clear()
                drugs_list.clear()
                id_list.clear()
                check_add_drugs.clear()
                self.clear_data()
                self.close()
                message = QMessageBox.warning(self, "Clear DATABASE ",
                                              "Database Is Clear !                  ",
                                              QMessageBox.Ok)

    def closeEvent(self, event):

        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message',
                                     quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()
            event.accept()

        else:
            event.ignore()


#######################################################
'''App Exicution'''


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.setWindowTitle('Oncology Pharmacy')
    window.setWindowIcon(QIcon('icon.ico'))
    window.setFixedSize(1100, 700)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
