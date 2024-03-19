from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import json
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

class MyGUI(QMainWindow):
    def __init__(self):
        self.dataset = []
        self.data = {}
        self.data['tokens'] = []
        self.data['spo_list'] = []
        self.data['spo_details'] = []
        self.data['pos_tags'] = []
        self.spo_list = []
        self.spo_details = []
        self.record = []
        super(MyGUI, self).__init__()
        uic.loadUi('AppLabelData.ui', self)
        ### load components ###
        #input
        self.button = self.findChild(QPushButton, 'pushButton')
        self.button.clicked.connect(self.process_clicked)
        
        self.text_input = self.findChild(QLineEdit, 'text_input')
        self.link_data = self.findChild(QLineEdit, 'link_data')
        
        self.del_button = self.findChild(QPushButton, 'del_button')
        self.del_button.clicked.connect(self.del_click)
        
        self.load_data_button = self.findChild(QPushButton, 'load_data_file')
        self.load_data_button.clicked.connect(self.load_data)
        
        #index & token for 1
        self.get_index1_button = self.findChild(QPushButton, 'get_index1')
        self.get_index1_button.clicked.connect(self.getIndex1)
        
        self.index1_input = self.findChild(QLineEdit, 'index1_input')
        self.token1 = self.findChild(QTextEdit, 'token1')
        self.type1 = self.findChild(QComboBox, 'type1')

        #index & token for 2
        self.get_index2_button = self.findChild(QPushButton, 'get_index2')
        self.get_index2_button.clicked.connect(self.getIndex2)

        self.index2_input = self.findChild(QLineEdit, 'index2_input')
        self.token2 = self.findChild(QTextEdit, 'token2')
        self.type2 = self.findChild(QComboBox, 'type2')
        
        #View tokens and pos tags
        self.table = self.findChild(QTableWidget, 'table')
        self.table.verticalHeader().setVisible(False)
        self.table.itemClicked.connect(self.ent_att_relaion_clicked)

        #finish button
        self.type_relation = self.findChild(QComboBox, 'type_relation')
        
        self.finish_button = self.findChild(QPushButton, 'finish_button')
        self.finish_button.clicked.connect(self.finish_click)
        
        self.output = self.findChild(QTextEdit, 'output')
        
        self.save_button = self.findChild(QPushButton, 'save_button')
        self.save_button.clicked.connect(self.save_click)
        
        self.delete_all_button = self.findChild(QPushButton, 'delete_all_button')
        self.delete_all_button.clicked.connect(self.delete_all_click)

        ###adjust the combo box for chose type of entity and relation
        self.type2.currentIndexChanged.connect(self.combo2_changed)
        self.combo2_changed(self.type2.currentIndex())
        
        self.show()
    def load_data(self):
        link_file = self.link_data.text()
        try:
            with open(link_file, 'r') as file:
                # Process the file
                self.dataset = json.load(file)
                QMessageBox.information(self, "Load", "Data has been loaded from " + link_file)
        except FileNotFoundError:
            result = QMessageBox.question(self, "File Not Found", "The file does not exist. Would you like to create a new file?", QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                try:
                    with open(link_file, 'w') as file:
                        self.dataset = []
                        file.write(json.dumps(self.dataset,indent=2))
                        # Initialize the file
                        QMessageBox.information(self, "New File", "File has been create at " + link_file)
                except Exception as e:
                    QMessageBox.critical(self, "Error", "Could not create file: " + str(e))
            else:
                pass
        except Exception as e:
            QMessageBox.critical(self, "Error", "Could not load file: " + str(e))
            
    def process_clicked(self):
        self.data['tokens'] = []
        self.data['pos_tags'] = []
        text = self.text_input.text()
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        self.table.setRowCount(len(tokens))
        for i, (token, pos) in enumerate(pos_tags):
            self.table.setItem(i, 0, QTableWidgetItem(str(i)))
            self.table.setItem(i, 1, QTableWidgetItem(token))
            self.table.setItem(i, 2, QTableWidgetItem(pos))
            self.data['tokens'].append(token)
            self.data['pos_tags'].append(pos)
        self.index1_input.setText("")
        self.index2_input.setText("")
        self.token1.setText("")
        self.token2.setText("")
    def del_click(self):
        self.text_input.setText("")
    def ent_att_relaion_clicked(self, item):
        row = item.row()
        self.record = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
    def getIndex1(self):
        if self.index1_input.text() == "":
            QMessageBox.critical(self, "Error", "Please input index for entity 1")
            return
        try:
            range_index = self.index1_input.text().split('-')
            range_index = [int(range_index[0]), int(range_index[1])]
        except:
            QMessageBox.critical(self, "Error", "Please input correct format for index 1")
            return
        token1_string = ""
        if self.data['tokens'] == []:
            QMessageBox.critical(self, "Error", "Please input text first")
            return
        if range_index[1] > len(self.data['tokens']) or range_index[0] < 0:
            QMessageBox.critical(self, "Error", "Index out of range")
            return
        for i in range(range_index[0], range_index[1]):
            token1_string += self.data['tokens'][i] + " "
        self.token1.setText(token1_string)
    def getIndex2(self):
        if self.index2_input.text() == "":
            QMessageBox.critical(self, "Error", "Please input index for entity 2")
            return
        try:
            range_index = self.index2_input.text().split('-')
            range_index = [int(range_index[0]), int(range_index[1])]
        except:
            QMessageBox.critical(self, "Error", "Please input correct format for index 2")
            return
        token2_string = ""
        if self.data['tokens'] == []:
            QMessageBox.critical(self, "Error", "Please input text first")
            return
        if range_index[1] > len(self.data['tokens']) or range_index[0] < 0:
            QMessageBox.critical(self, "Error", "Index out of range")
            return
        for i in range(range_index[0], range_index[1]):
            token2_string += self.data['tokens'][i] + " "
        self.token2.setText(token2_string)
    def finish_click(self):
        type1 = self.type1.currentText()
        type2 = self.type2.currentText()
        relation = self.type_relation.currentText()
        token1 = self.token1.toPlainText()
        token2 = self.token2.toPlainText()
        if token1 == "" or token2 == "":
            QMessageBox.critical(self, "Error", "Please input token for both entities")
            return
        range_index1 = self.index1_input.text().split('-')
        range_index1 = [int(range_index1[0]), int(range_index1[1])]
        range_index2 = self.index2_input.text().split('-')
        range_index2 = [int(range_index2[0]), int(range_index2[1])]
        spo_list =[ token1, relation, token2]
        spo_details = [range_index1[0], range_index1[1], type1, relation, range_index2[0], range_index2[1], type2]
        if spo_list in self.data['spo_list']:
            QMessageBox.critical(self, "Error", "This spo list already exists")
            return
        if spo_details in self.data['spo_details']:
            QMessageBox.critical(self, "Error", "This spo details already exists")
            return
        self.data['spo_list'].append(spo_list)
        self.data['spo_details'].append(spo_details)
        self.output.setText(self.data.__str__())
    def combo2_changed(self,index):
        if self.type2.itemText(index) == "ENTITY":  # Replace "Your Option" with the option that should enable a certain option in the second combo box
            for i in range(self.type_relation.count()):
                if self.type_relation.itemText(i) == "relation with":  # Replace "Other Option" with the option that should be enabled
                    self.type_relation.model().item(i).setEnabled(True)
                    self.type_relation.setCurrentIndex(i)
                else:
                    self.type_relation.model().item(i).setEnabled(False)
        else:
            for i in range(self.type_relation.count()):
                if self.type_relation.itemText(i) == "relation with":  # Replace "Other Option" with the option that should be enabled
                    self.type_relation.model().item(i).setEnabled(False)
                else:
                    self.type_relation.model().item(i).setEnabled(True)
                    self.type_relation.setCurrentIndex(i)
    def save_click(self):
        self.dataset.append(self.data)
        try:
            with open(self.link_data.text(), 'w') as file:
                file.write(json.dumps(self.dataset, indent=2))
            QMessageBox.information(self, "Save", "Data has been saved ")
        except Exception as e:
            QMessageBox.critical(self, "Error", "Could not save file: " + str(e))
            return 
        self.data = {}
        self.data['tokens'] = []
        self.data['spo_list'] = []
        self.data['spo_details'] = []
        self.data['pos_tags'] = []
        self.output.setText("")
        self.table.setRowCount(0)
        self.text_input.setText("")
        self.token1.setText("")
        self.token2.setText("")
        self.index1_input.setText("")
        self.index2_input.setText("")
        self.type1.setCurrentIndex(0)
        self.type2.setCurrentIndex(0)
        self.type_relation.setCurrentIndex(0)
    def delete_all_click(self):
        self.output.setText("")
        self.table.setRowCount(0)
        self.text_input.setText("")
        self.token1.setText("")
        self.token2.setText("")
        self.index1_input.setText("")
        self.index2_input.setText("")
        self.type1.setCurrentIndex(0)
        self.type2.setCurrentIndex(0)
        self.type_relation.setCurrentIndex(0)
def main():
    app = QApplication([])
    window = MyGUI()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()