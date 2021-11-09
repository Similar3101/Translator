from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QPlainTextEdit, QWidget
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QMessageBox
from PyQt5.QtWidgets import QPushButton, QCheckBox, QMenuBar, QMenu, QAction
from PyQt5.QtGui import QIcon, QFont, QCursor, QPalette, QPixmap
from PyQt5.QtCore import QSize, QMetaObject, QRect, Qt
from googletrans import Translator, constants
import sys
import sqlite3
import random


con = sqlite3.connect('History_Of_Translate.db')


class MainTranslator(QMainWindow):
    def __init__(self):
        super().__init__()
        # всё это расстановка всех кнопок и панелей (до 114 строки)
        self.setObjectName("Translator")
        self.resize(1090, 635)
        self.setMinimumSize(QSize(1090, 635))
        self.setMaximumSize(QSize(1090, 635))
        self.setStyleSheet("")
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.BtnTranslate = QPushButton(self.centralwidget)
        self.BtnTranslate.setGeometry(QRect(480, 330, 121, 51))
        font = QFont()
        font.setPointSize(10)
        self.BtnTranslate.setFont(font)
        self.BtnTranslate.setStyleSheet("")
        self.BtnTranslate.setObjectName("BtnTranslate")
        self.text_from_lang = QPlainTextEdit(self.centralwidget)
        self.text_from_lang.setGeometry(QRect(10, 50, 420, 550))
        font = QFont()
        font.setPointSize(11)
        self.text_from_lang.setFont(font)
        self.text_from_lang.setStyleSheet("")
        self.text_from_lang.setPlainText("")
        self.text_from_lang.setObjectName("text_from_lang")
        self.text_to_lang = QPlainTextEdit(self.centralwidget)
        self.text_to_lang.setGeometry(QRect(660, 50, 420, 550))
        font = QFont()
        font.setPointSize(11)
        self.text_to_lang.setFont(font)
        self.text_to_lang.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.text_to_lang.setAutoFillBackground(True)
        self.text_to_lang.setStyleSheet("")
        self.text_to_lang.setPlainText("")
        self.text_to_lang.setObjectName("text_to_lang")
        self.choice_from_lang = QPushButton(self.centralwidget)
        self.choice_from_lang.setGeometry(QRect(70, 10, 200, 30))
        palette = QPalette()
        self.choice_from_lang.setPalette(palette)
        font = QFont()
        font.setPointSize(9)
        self.choice_from_lang.setFont(font)
        self.choice_from_lang.setStyleSheet("")
        self.choice_from_lang.setObjectName("choice_from_lang")
        self.choice_to_lang = QPushButton(self.centralwidget)
        self.choice_to_lang.setGeometry(QRect(870, 10, 201, 31))
        font = QFont()
        font.setPointSize(9)
        self.choice_to_lang.setFont(font)
        self.choice_to_lang.setStyleSheet("")
        self.choice_to_lang.setObjectName("choice_to_lang")
        self.btnSaving = QCheckBox(self.centralwidget)
        self.btnSaving.setGeometry(QRect(500, 420, 91, 41))
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.btnSaving.setFont(font)
        self.btnSaving.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnSaving.setTabletTracking(False)
        self.btnSaving.setStyleSheet("")
        self.btnSaving.setChecked(True)
        self.btnSaving.setTristate(False)
        self.btnSaving.setObjectName("btnSaving")
        self.choice_from_lang.raise_()
        self.BtnTranslate.raise_()
        self.text_from_lang.raise_()
        self.text_to_lang.raise_()
        self.choice_to_lang.raise_()
        self.btnSaving.raise_()
        self.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 1090, 26))
        self.menuBar.setObjectName("menuBar")
        self.menu = QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.setMenuBar(self.menuBar)
        self.BtnHistory = QAction(self)
        self.BtnHistory.setCheckable(False)
        self.BtnHistory.setObjectName("BtnHistory")
        self.BtnQuiz = QAction(self)
        self.BtnQuiz.setObjectName("BtnQuiz")
        self.menu.addAction(self.BtnHistory)
        self.menu.addAction(self.BtnQuiz)
        self.menuBar.addAction(self.menu.menuAction())
        self.setWindowTitle("Translator")
        self.BtnTranslate.setText("Translate")
        self.choice_from_lang.setText("Change language")
        self.choice_to_lang.setText("Change language")
        self.btnSaving.setText("Saving")
        self.menu.setTitle("|||")
        self.BtnHistory.setText("History")
        self.BtnQuiz.setText("Quiz")
        QMetaObject.connectSlotsByName(self)
        self.setWindowIcon(QIcon('Icon.png'))
        # дальше идёт подключения кнопок
        self.BtnTranslate.clicked.connect(self.translate)  # кнопка по середине поключена к функции для перевода
        self.choice_from_lang.clicked.connect(self.change_from_or_to_lang)  # для обоих кнопок одна функция для -
        self.choice_to_lang.clicked.connect(self.change_from_or_to_lang)  # - смены языка
        self.choice_from_lang.setText('english')  # по умолчанию стоит английский язык
        self.choice_to_lang.setText('english')  # по умолчанию стоит английский язык
        # кнопки меню
        self.BtnHistory.triggered.connect(self.to_history)
        self.BtnQuiz.triggered.connect(self.to_quiz)
        # здесь некоторые аргументы
        self.language = {b: a for a, b in constants.LANGUAGES.items()}  # все рабочие языки на переводчике
        self.num = 0  # используется только для индексации в истории переводов
        self.cun = con.cursor()  # для отправления информации в SQL таблицу

    def translate(self):
        try:
            from_lang, to_lang = self.choice_from_lang.text(), self.choice_to_lang.text()
            cut_from_lang, cut_to_lang = self.language[from_lang], self.language[to_lang]
            print(cut_from_lang, cut_to_lang)
            text_from_lang = self.text_from_lang.toPlainText()
            t = Translator()
            t = t.translate(text_from_lang, src=cut_from_lang, dest=cut_to_lang)
            self.text_to_lang.setPlainText(t.text)
            print(self.btnSaving.checkState())
            if self.btnSaving.checkState():
                self.num += 1
                self.cun.execute(f'''
INSERT INTO History (id, from_Lang, text_from_Lang, to_Lang, text_to_Lang)
VALUES {int(self.num), str(cut_from_lang), str(text_from_lang), str(cut_to_lang), str(t.text)};''')
            con.commit()
        except Exception as e:
            print(e)

    def change_from_or_to_lang(self):
        try:
            ctl = self.choice_to_lang.text()
            display_lang = self.language.keys()
            language, ok_pressed = QInputDialog.getItem(self,
                                                        'выбор языка',
                                                        'какой язык?',
                                                        display_lang,
                                                        list(display_lang).index(ctl),
                                                        False)
            if ok_pressed:
                self.sender().setText(language)
        except Exception as e:
            print(e)

    def to_quiz(self):
        try:
            win = Quiz(self)
            self.hide()
            win.show()
        except Exception as e:
            print(e)

    def to_history(self):
        try:
            win = History(self)
            self.hide()
            win.show()
        except Exception as e:
            print(e)


class History(QMainWindow):
    def __init__(self, parent=None):
        try:
            self.cun = con.cursor()

            super(History, self).__init__(parent)
            self.parent = parent

            # uic.loadUi('History.ui', self)

            self.format_text()

            self.actionBack_2.triggered.connect(self.back)

            self.Page.valueChanged.connect(self.format_text)
            self.Page.setValue(1)

        except Exception as e:
            print(e)

    def format_text(self):
        try:
            ind = self.Page.value()
            loh = self.cun.execute('''
SELECT COUNT(*) FROM History''').fetchone()[0]
            self.Page.setMinimum(1)
            self.Page.setMaximum(loh // 13 if loh > 13 else 1)
            res = self.cun.execute('''
SELECT from_Lang, text_from_Lang, to_Lang, text_to_Lang FROM History
WHERE id BETWEEN ? AND ?;''', (13 * (ind - 1), 13 * ind)
                              ).fetchmany(13 if 13 < loh else loh)
            self.HistoryOfTranslate.setRowCount(13)
            self.HistoryOfTranslate.setColumnCount(4)
            i = -1
            for elem in res:
                i += 1
                for j, val in enumerate(elem):
                    self.HistoryOfTranslate.setItem(i, j, QTableWidgetItem(str(val)))
        except Exception as e:
            print(e)

    def back(self):
        self.hide()
        self.parent.show()


class Quiz(QMainWindow):
    def __init__(self, parent=None):
        try:
            super(Quiz, self).__init__(parent)
            self.parent = parent
            self.integer = 0
            # uic.loadUi('Quiz.ui', self)

            self.Start_Quiz.hide()
            self.End_Quiz.hide()
            self.ok.hide()
            self.jpg.hide()

            self.Choicebtn.clicked.connect(self.change)
            self.ok.clicked.connect(self.return_to_quiz)
            self.End_Quiz.clicked.connect(self.end_of_quiz)
            self.Start_Quiz.clicked.connect(self.start_of_quiz)

            self.ActionBack.triggered.connect(self.back)

            self.cun = con.cursor()
            self.name = list()
            self.correct_res = ''
            self.correct_output = ''
        except Exception as e:
            print(e)

    def change(self):
        b = []
        a = self.cun.execute('''
SELECT DISTINCT to_Lang, from_Lang FROM History;''').fetchall()
        if a:
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
                self.ToTranslate.setText(self.name[0])
                self.FromTranslate.setText(self.name[1])
        else:
            error = QMessageBox()
            error.setText('для начала нужно что-нибудь перевести')
            error.setWindowTitle('Error')
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()

    def start_of_quiz(self):
        try:
            a = self.cun.execute('''
SELECT DISTINCT text_to_Lang, text_from_Lang FROM History
WHERE to_Lang = ? AND from_Lang = ?;''', tuple(self.name)).fetchall()
            b, c = random.choice(a)
            self.correct_output = ''.join(b.split('\n'))
            self.correct_res = ''.join(c.split('\n'))
            self.TranslatableText.setText(self.correct_output)
            self.Result.setText('')
            self.End_Quiz.show()
            self.Start_Quiz.hide()
        except Exception as e:
            print(e)

    def end_of_quiz(self):
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
            self.label_2.hide()
            self.label_3.hide()
            self.ToTranslate.hide()
            self.FromTranslate.hide()
            self.TranslatableText.hide()
            self.ok.show()
        except Exception as e:
            print(e)

    def return_to_quiz(self):
        self.jpg.hide()
        self.ok.hide()
        self.Choicebtn.show()
        self.Start_Quiz.show()
        self.Result.show()
        self.label_2.show()
        self.label_3.show()
        self.ToTranslate.show()
        self.FromTranslate.show()
        self.TranslatableText.show()
        self.TranslatableText.setText('Here will be 1 proposal')
        self.Result.setText('Here will be your translate')

    def back(self):
        self.hide()
        self.parent.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('Icon.png'))
    ex = MainTranslator()
    ex.show()
    sys.exit(app.exec())
