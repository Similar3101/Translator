from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QPlainTextEdit, \
    QWidget, QAbstractSpinBox, QLabel, QTableWidget, QSpinBox, QMainWindow, \
    QInputDialog, QMessageBox, QPushButton, QCheckBox, QMenuBar, QMenu, \
    QAction, QSizePolicy, QLineEdit
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
        # self.centralwidget.setObjectName("centralwidget")
        self.BtnTranslate = QPushButton(self.centralwidget)
        self.BtnTranslate.setGeometry(QRect(480, 330, 121, 51))
        font = QFont()
        font.setPointSize(10)
        self.BtnTranslate.setFont(font)
        self.BtnTranslate.setStyleSheet("")
        # self.BtnTranslate.setObjectName("BtnTranslate")
        self.text_from_lang = QPlainTextEdit(self.centralwidget)
        self.text_from_lang.setGeometry(QRect(10, 50, 420, 550))
        font = QFont()
        font.setPointSize(11)
        self.text_from_lang.setFont(font)
        self.text_from_lang.setStyleSheet("")
        self.text_from_lang.setPlainText("")
        # self.text_from_lang.setObjectName("text_from_lang")
        self.text_to_lang = QPlainTextEdit(self.centralwidget)
        self.text_to_lang.setGeometry(QRect(660, 50, 420, 550))
        font = QFont()
        font.setPointSize(11)
        self.text_to_lang.setFont(font)
        self.text_to_lang.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.text_to_lang.setAutoFillBackground(True)
        self.text_to_lang.setStyleSheet("")
        self.text_to_lang.setPlainText("")
        # self.text_to_lang.setObjectName("text_to_lang")
        self.choice_from_lang = QPushButton(self.centralwidget)
        self.choice_from_lang.setGeometry(QRect(70, 10, 200, 30))
        palette = QPalette()
        self.choice_from_lang.setPalette(palette)
        font = QFont()
        font.setPointSize(9)
        self.choice_from_lang.setFont(font)
        self.choice_from_lang.setStyleSheet("")
        # self.choice_from_lang.setObjectName("choice_from_lang")
        self.choice_to_lang = QPushButton(self.centralwidget)
        self.choice_to_lang.setGeometry(QRect(870, 10, 201, 31))
        font = QFont()
        font.setPointSize(9)
        self.choice_to_lang.setFont(font)
        self.choice_to_lang.setStyleSheet("")
        # self.choice_to_lang.setObjectName("choice_to_lang")
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
        # self.btnSaving.setObjectName("btnSaving")
        self.choice_from_lang.raise_()
        self.BtnTranslate.raise_()
        self.text_from_lang.raise_()
        self.text_to_lang.raise_()
        self.choice_to_lang.raise_()
        self.btnSaving.raise_()
        self.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 1090, 26))
        # self.menuBar.setObjectName("menuBar")
        self.menu = QMenu(self.menuBar)
        # self.menu.setObjectName("menu")
        self.setMenuBar(self.menuBar)
        self.BtnHistory = QAction(self)
        self.BtnHistory.setCheckable(False)
        # self.BtnHistory.setObjectName("BtnHistory")
        self.BtnQuiz = QAction(self)
        # self.BtnQuiz.setObjectName("BtnQuiz")
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
            super(History, self).__init__(parent)
            self.resize(800, 600)
            self.setIconSize(QSize(30, 30))
            self.centralwidget = QWidget(self)
            # self.centralwidget.setObjectName("centralwidget")
            self.HistoryOfTranslate = QTableWidget(self.centralwidget)
            self.HistoryOfTranslate.setGeometry(QRect(110, 10, 680, 530))
            # self.HistoryOfTranslate.setObjectName("HistoryOfTranslate")
            self.HistoryOfTranslate.setColumnCount(0)
            self.HistoryOfTranslate.setRowCount(0)
            self.label = QLabel(self.centralwidget)
            self.label.setGeometry(QRect(20, 50, 55, 21))
            font = QFont()
            font.setPointSize(10)
            self.label.setFont(font)
            # self.label.setObjectName("label")
            self.Page = QSpinBox(self.centralwidget)
            self.Page.setGeometry(QRect(20, 80, 71, 41))
            font = QFont()
            font.setPointSize(10)
            self.Page.setFont(font)
            self.Page.setAlignment(Qt.AlignCenter)
            self.Page.setButtonSymbols(QAbstractSpinBox.PlusMinus)
            self.Page.setCorrectionMode(QAbstractSpinBox.CorrectToPreviousValue)
            self.Page.setMinimum(1)
            # self.Page.setObjectName("Page")
            self.setCentralWidget(self.centralwidget)
            self.menubar = QMenuBar(self)
            self.menubar.setGeometry(QRect(0, 0, 800, 26))
            # self.menubar.setObjectName("menubar")
            self.menu = QMenu(self.menubar)
            # self.menu.setObjectName("menu")
            self.setMenuBar(self.menubar)
            self.actionBack = QAction(self)
            # self.actionBack.setObjectName("actionBack")
            self.actionBack_2 = QAction(self)
            # self.actionBack_2.setObjectName("actionBack_2")
            self.menu.addAction(self.actionBack_2)
            self.menubar.addAction(self.menu.menuAction())
            self.label.setText("Page:")
            self.menu.setTitle("|||")
            self.actionBack.setText("Back")
            self.actionBack_2.setText("Back")
            self.setWindowTitle("History")

            QMetaObject.connectSlotsByName(self)
            self.cun = con.cursor()

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
            self.HistoryOfTranslate.setColumnWidth(10, 680 // 4)
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
            self.resize(800, 400)
            sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
            self.setSizePolicy(sizePolicy)
            font = QFont()
            font.setPointSize(9)
            self.setFont(font)
            self.centralwidget = QWidget(self)
            self.centralwidget.setObjectName("centralwidget")
            self.Start_Quiz = QPushButton(self.centralwidget)
            self.Start_Quiz.setGeometry(QRect(330, 90, 150, 50))
            font = QFont()
            font.setPointSize(10)
            font.setBold(False)
            font.setItalic(False)
            font.setUnderline(False)
            font.setWeight(50)
            font.setStrikeOut(False)
            font.setKerning(True)
            self.Start_Quiz.setFont(font)
            self.Start_Quiz.setObjectName("Start_Quiz")
            self.TranslatableText = QLabel(self.centralwidget)
            self.TranslatableText.setGeometry(QRect(200, 170, 400, 40))
            font = QFont()
            font.setFamily("Times New Roman")
            font.setPointSize(14)
            self.TranslatableText.setFont(font)
            self.TranslatableText.setFocusPolicy(Qt.NoFocus)
            self.TranslatableText.setScaledContents(False)
            self.TranslatableText.setAlignment(Qt.AlignCenter)
            self.TranslatableText.setOpenExternalLinks(False)
            self.TranslatableText.setObjectName("TranslatableText")
            self.Choicebtn = QPushButton(self.centralwidget)
            self.Choicebtn.setGeometry(QRect(285, 20, 240, 50))
            font = QFont()
            font.setPointSize(10)
            self.Choicebtn.setFont(font)
            self.Choicebtn.setObjectName("Choicebtn")
            self.label_2 = QLabel(self.centralwidget)
            self.label_2.setGeometry(QRect(50, 170, 135, 40))
            font = QFont()
            font.setPointSize(10)
            self.label_2.setFont(font)
            self.label_2.setObjectName("label_2")
            self.label_3 = QLabel(self.centralwidget)
            self.label_3.setGeometry(QRect(50, 260, 130, 40))
            font = QFont()
            font.setPointSize(10)
            self.label_3.setFont(font)
            self.label_3.setObjectName("label_3")
            self.ToTranslate = QLabel(self.centralwidget)
            self.ToTranslate.setGeometry(QRect(60, 220, 101, 21))
            font = QFont()
            font.setPointSize(10)
            self.ToTranslate.setFont(font)
            self.ToTranslate.setText("")
            self.ToTranslate.setObjectName("ToTranslate")
            self.FromTranslate = QLabel(self.centralwidget)
            self.FromTranslate.setGeometry(QRect(60, 310, 101, 21))
            font = QFont()
            font.setPointSize(10)
            self.FromTranslate.setFont(font)
            self.FromTranslate.setText("")
            self.FromTranslate.setObjectName("FromTranslate")
            self.End_Quiz = QPushButton(self.centralwidget)
            self.End_Quiz.setGeometry(QRect(330, 90, 150, 50))
            font = QFont()
            font.setPointSize(10)
            font.setBold(False)
            font.setItalic(False)
            font.setUnderline(False)
            font.setWeight(50)
            font.setStrikeOut(False)
            font.setKerning(True)
            self.End_Quiz.setFont(font)
            self.End_Quiz.setObjectName("End_Quiz")
            self.ok = QPushButton(self.centralwidget)
            self.ok.setGeometry(QRect(310, 10, 150, 50))
            font = QFont()
            font.setPointSize(12)
            font.setBold(False)
            font.setItalic(False)
            font.setUnderline(False)
            font.setWeight(50)
            font.setStrikeOut(False)
            font.setKerning(True)
            self.ok.setFont(font)
            self.ok.setObjectName("ok")
            self.jpg = QLabel(self.centralwidget)
            self.jpg.setGeometry(QRect(0, 0, 800, 370))
            self.jpg.setText("")
            self.jpg.setScaledContents(True)
            self.jpg.setAlignment(Qt.AlignCenter)
            self.jpg.setWordWrap(False)
            self.jpg.setIndent(1)
            self.jpg.setOpenExternalLinks(False)
            self.jpg.setObjectName("jpg")
            self.Result = QLineEdit(self.centralwidget)
            self.Result.setGeometry(QRect(200, 250, 400, 60))
            font = QFont()
            font.setPointSize(14)
            self.Result.setFont(font)
            self.Result.setAlignment(Qt.AlignCenter)
            self.Result.setObjectName("Result")
            self.jpg.raise_()
            self.Start_Quiz.raise_()
            self.TranslatableText.raise_()
            self.Choicebtn.raise_()
            self.label_2.raise_()
            self.label_3.raise_()
            self.ToTranslate.raise_()
            self.FromTranslate.raise_()
            self.End_Quiz.raise_()
            self.Result.raise_()
            self.ok.raise_()
            self.setCentralWidget(self.centralwidget)
            self.menubar = QMenuBar(self)
            self.menubar.setGeometry(QRect(0, 0, 800, 26))
            self.menubar.setObjectName("menubar")
            self.menu = QMenu(self.menubar)
            self.menu.setObjectName("menu")
            self.setMenuBar(self.menubar)
            self.ActionBack = QAction(self)
            self.ActionBack.setObjectName("ActionBack")
            self.actionHistory = QAction(self)
            self.actionHistory.setObjectName("actionHistory")
            self.menu.addAction(self.ActionBack)
            self.menubar.addAction(self.menu.menuAction())
            self.parent = parent
            self.integer = 0
            self.setWindowTitle("Quiz")
            self.Start_Quiz.setText("Let\'s Start")
            self.TranslatableText.setText("Here will be 1 proposal")
            self.Choicebtn.setText("Choice to and from Translate")
            self.label_2.setText("Translatable text:")
            self.label_3.setText("Translated text:")
            self.End_Quiz.setText("I\'ve Done")
            self.ok.setText("OK")
            self.Result.setText("Here will be your translate")
            self.menu.setTitle("|||")
            self.ActionBack.setText("Back")
            self.actionHistory.setText("History")
            QMetaObject.connectSlotsByName(self)

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
        else:
            error = QMessageBox()
            error.setText('для начала нужно что-нибудь перевести')
            error.setWindowTitle('Error')
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()

    def start_of_quiz(self):
        try:
            text_for_quiz = self.cun.execute('''
SELECT DISTINCT text_to_Lang, text_from_Lang FROM History
WHERE to_Lang = ? AND from_Lang = ?;''', tuple(self.name)).fetchall()
            b, c = random.choice(text_for_quiz)
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
