from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem
from PyQt5.QtWidgets import QMainWindow, QInputDialog
from googletrans import Translator as trans, constants
import sys
import sqlite3
import random
from PyQt5.QtGui import QPixmap


class Translator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Translator.ui', self)
        self.Button.clicked.connect(self.translate)

        self.choice_from_lang.clicked.connect(self.change_from_lang)
        self.choice_to_lang.clicked.connect(self.change_to_lang)
        self.choice_from_lang.setText('english')
        self.choice_to_lang.setText('english')

        self.History.triggered.connect(self.ToHistory)
        self.Quiz.triggered.connect(self.ToQuiz)

        self.language = {b: a for a, b in constants.LANGUAGES.items()}

        self.con = sqlite3.connect('History_Of_Translate.db')
        self.num = 0

    def translate(self):
        try:
            a1, a2 = self.choice_from_lang.text(), self.choice_to_lang.text()
            b = self.text_from_lang.toPlainText()
            t = trans()
            t = t.translate(b, src=a1, dest=a2)
            self.text_to_lang.setPlainText(t.text)
            if self.btnSaving.checkState():
                self.cun = self.con.cursor()
                self.num += 1
                self.cun.execute(f'''
INSERT INTO History (id, from_Lang, text_from_Lang, to_Lang, text_to_Lang)
VALUES {int(self.num), str(a1), str(b), str(a2), str(t.text)};''')
            self.con.commit()
        except Exception as e:
            print(e)

    def change_from_lang(self):
        try:
            a = self.choice_from_lang.text()
            b = self.language.keys()
            name, ok_pressed = QInputDialog.getItem(self,
                                                    'выбор языка',
                                                    'какой язык?',
                                                    b,
                                                    list(b).index(a),
                                                    False)
            if ok_pressed:
                self.choice_from_lang.setText(name)
        except Exception as e:
            print(e)

    def change_to_lang(self):
        try:
            a = self.choice_to_lang.text()
            b = self.language.keys()
            name, ok_pressed = QInputDialog.getItem(self,
                                                    'выбор языка',
                                                    'какой язык?',
                                                    b,
                                                    list(b).index(a),
                                                    False)
            if ok_pressed:
                self.choice_to_lang.setText(name)
        except Exception as e:
            print(e)

    def ToQuiz(self):
        win = Quiz(self)
        self.hide()
        win.show()


    def ToHistory(self):
        try:
            win = History(self)
            self.hide()
            win.show()
        except Exception as e:
            print(e)


class History(QMainWindow):
    def __init__(self, parent=None):
        try:
            super(History, self).__init__(parent)
            self.parent = parent

            uic.loadUi('History.ui', self)

            self.con = sqlite3.connect('History_Of_Translate.db')
            self.format_text()

            self.actionBack_2.triggered.connect(self.Back)

            self.Page.valueChanged.connect(self.format_text)
            self.Page.setValue(1)
        except Exception as e:
            print(e)

    def ToTranslater(self):
        self.parent.show()
        self.hide()

    def format_text(self):
        try:
            cur = self.con.cursor()
            ind = self.Page.value()
            loh = cur.execute('''
SELECT COUNT(*) FROM History''').fetchone()[0]
            # print(loh, type(loh))
            self.Page.setMinimum(1)
            self.Page.setMaximum(loh // 13 if loh > 13 else 1)
            res = cur.execute('''
SELECT from_Lang, text_from_Lang, to_Lang, text_to_Lang FROM History
WHERE id BETWEEN ? AND ?;''', (13 * (ind - 1), 13 * ind)
                              ).fetchmany(13 if 13 < loh else loh)
            self.HistoryOfTranslate.setRowCount(13)
            self.HistoryOfTranslate.setColumnCount(4)
            # print(res)
            i = -1
            for elem in res:
                i += 1
                for j, val in enumerate(elem):
                    self.HistoryOfTranslate.setItem(i, j, QTableWidgetItem(str(val)))
        except Exception as e:
            print(e)

    def Back(self):
        self.hide()
        self.parent.show()


class Quiz(QMainWindow):
    def __init__(self, parent=None):
        try:
            super(Quiz, self).__init__(parent)
            self.parent = parent
            self.integer = 0
            uic.loadUi('Quiz.ui', self)

            self.Start_Quiz.hide()
            self.End_Quiz.hide()
            self.ok.hide()
            self.jpg.hide()

            self.Choicebtn.clicked.connect(self.Change)
            self.ok.clicked.connect(self.OK)
            self.End_Quiz.clicked.connect(self.end)
            self.Start_Quiz.clicked.connect(self.start)

            self.ActionBack.triggered.connect(self.Back)

            self.con = sqlite3.connect('History_Of_Translate.db')
        except Exception as e:
            print(e)

    def Change(self):
        cur = self.con.cursor()
        b = []
        a = cur.execute('''
SELECT DISTINCT to_Lang, from_Lang FROM History;''').fetchall()
        for res in a:
            print(res)
            b.append(' - '.join(res))
        self.name, ok_pressed = QInputDialog.getItem(self,
                                                     'выбор',
                                                     'С какого на какой язык?',
                                                     b,
                                                     False)
        if ok_pressed:
            self.Start_Quiz.show()
            self.name = self.name.split(' - ')
            self.ToTranslate.setText(self.name[0])
            self.FromTranslate.setText(self.name[1])

    def start(self):
        try:
            cur = self.con.cursor()
            a = cur.execute('''
SELECT DISTINCT text_to_Lang, text_from_Lang FROM History
WHERE to_Lang = ? AND from_Lang = ?;''', tuple(self.name)).fetchall()
            self.correct_res = random.choice(a)[1]
            self.TranslatableText.setText(random.choice(a)[0])
            self.Result.setText('')
            self.End_Quiz.show()
            self.Start_Quiz.hide()
        except Exception as e:
            print(e)

    def end(self):
        try:
            if self.correct_res == self.Result.text():
                jpg = QPixmap('1.jpg')
            else:
                jpg = QPixmap('2.jpg')
            self.jpg.setPixmap(jpg)
            self.jpg.show()
            self.Choicebtn.hide()
            self.End_Quiz.hide()
            self.Start_Quiz.hide()
            self.Result.hide()
            self.Instruction.hide()
            self.label_2.hide()
            self.label_3.hide()
            self.ToTranslate.hide()
            self.FromTranslate.hide()
            self.TranslatableText.hide()
            self.ok.show()
        except Exception as e:
            print(e)

    def OK(self):
        self.jpg.hide()
        self.ok.hide()
        self.Choicebtn.show()
        self.End_Quiz.show()
        self.Start_Quiz.show()
        self.Result.show()
        self.Instruction.show()
        self.label_2.show()
        self.label_3.show()
        self.ToTranslate.show()
        self.FromTranslate.show()
        self.TranslatableText.show()
        self.TranslatableText.setText('Here will be 1 proposal')
        self.Result.setText('Here will be your translate')

    def Back(self):
        self.hide()
        self.parent.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Translator()
    ex.show()
    sys.exit(app.exec())
