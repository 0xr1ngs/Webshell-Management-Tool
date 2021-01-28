from PyQt5.QtCore import *
from PyQt5.Qsci import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from testConnShell import *
import keyword


class highlight(QsciLexerPython):
    def __init__(self, parent):
        QsciLexerPython.__init__(self, parent)
        font = QFont()
        font.setFamily('Courier')
        font.setPointSize(12)
        font.setFixedPitch(True)
        self.setFont(font)
        self.setColor(QColor(0, 0, 0))
        self.setPaper(QColor(255, 255, 255))
        self.setColor(QColor("#FF8000"), QsciLexerPython.ClassName)
        self.setColor(QColor("#B0171F"), QsciLexerPython.Keyword)
        self.setColor(QColor("#01DF01"), QsciLexerPython.Comment)
        self.setColor(QColor("#FF00FF"), QsciLexerPython.Number)
        self.setColor(QColor("#0000FF"), QsciLexerPython.DoubleQuotedString)
        self.setColor(QColor("#0000FF"), QsciLexerPython.SingleQuotedString)
        self.setColor(QColor("#288B22"), QsciLexerPython.TripleSingleQuotedString)
        self.setColor(QColor("#288B22"), QsciLexerPython.TripleDoubleQuotedString)
        self.setColor(QColor("#0000FF"), QsciLexerPython.FunctionMethodName)
        self.setColor(QColor("#191970"), QsciLexerPython.Operator)
        self.setColor(QColor("#000000"), QsciLexerPython.Identifier)
        self.setColor(QColor("#00FF00"), QsciLexerPython.CommentBlock)
        self.setColor(QColor("#0000FF"), QsciLexerPython.UnclosedString)
        self.setColor(QColor("#FFFF00"), QsciLexerPython.HighlightedIdentifier)
        self.setColor(QColor("#FF8000"), QsciLexerPython.Decorator)
        self.setFont(QFont('Courier', 12, weight=QFont.Bold), 5)
        self.setFont(QFont('Courier', 12, italic=True), QsciLexerPython.Comment)


class setEditor(QsciScintilla):
    def __init__(self, url, password, mainWindow, filenameArg, fileConetent, tabWidget):
        QsciScintilla.__init__(self)
        self.url = url
        self.password = password
        self.mainWindow = mainWindow
        self.filenameArg = filenameArg
        self.fileConetent = fileConetent
        self.tabWidget = tabWidget
        
    def set(self):
        font = QFont()
        font.setFamily('Courier')
        font.setPointSize(12)
        font.setFixedPitch(True)

        self.setFont(font)
        self.setUtf8(True)
        self.setMarginsFont(font)
        self.setMarginWidth(0, len(str(len(self.text().split('\n')))) * 20)
        self.setMarginLineNumbers(0, True)
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColor(QColor(0, 0, 0))

        self.setBraceMatching(QsciScintilla.StrictBraceMatch)

        self.setIndentationsUseTabs(True)
        self.setIndentationWidth(4)
        self.setTabIndents(True)
        self.setAutoIndent(True)
        self.setBackspaceUnindents(True)
        self.setTabWidth(4)

        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor('#FFFFCD'))
        self.setIndentationGuides(True)

        self.setFolding(QsciScintilla.PlainFoldStyle)
        self.setMarginWidth(2, 12)

        self.markerDefine(QsciScintilla.Minus, QsciScintilla.SC_MARKNUM_FOLDEROPEN)
        self.markerDefine(QsciScintilla.Plus, QsciScintilla.SC_MARKNUM_FOLDER)
        self.markerDefine(QsciScintilla.Minus, QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.markerDefine(QsciScintilla.Plus, QsciScintilla.SC_MARKNUM_FOLDEREND)

        self.setMarkerBackgroundColor(QColor("#FFFFFF"), QsciScintilla.SC_MARKNUM_FOLDEREND)
        self.setMarkerForegroundColor(QColor("#272727"), QsciScintilla.SC_MARKNUM_FOLDEREND)
        self.setMarkerBackgroundColor(QColor("#FFFFFF"), QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.setMarkerForegroundColor(QColor("#272727"), QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionCaseSensitivity(True)
        self.setAutoCompletionReplaceWord(False)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionUseSingle(QsciScintilla.AcusExplicit)
        # 设置高亮
        self.lexer = highlight(self)
        self.setLexer(self.lexer)
        self.mod = False
        self.__api = QsciAPIs(self.lexer)
        autocompletions = keyword.kwlist + ["abs", "all", "any", "basestring", "bool",
                                            "callable", "chr", "classmethod", "cmp", "compile",
                                            "complex", "delattr", "dict", "dir", "divmod",
                                            "enumerate", "eval", "execfile", "exit", "file",
                                            "filter", "float", "frozenset", "getattr", "globals",
                                            "hasattr", "hex", "id", "int", "isinstance",
                                            "issubclass", "iter", "len", "list", "locals", "map",
                                            "max", "min", "object", "oct", "open", "ord", "pow",
                                            "property", "range", "reduce", "repr", "reversed",
                                            "round", "set", "setattr", "slice", "sorted",
                                            "staticmethod", "str", "sum", "super", "tuple", "type",
                                            "vars", "zip", 'print']
        for ac in autocompletions:
            self.__api.add(ac)
        self.__api.prepare()
        self.autoCompleteFromAll()
        # 设置文本
        self.setText(self.fileConetent)

        new_tab = QWidget()
        gridLayout = QGridLayout(new_tab)
        gridLayout.addWidget(self, 0, 0)
        self.tabWidget.addTab(new_tab, self.filenameArg)

        # 绑定保存快捷键
        shortcut = QShortcut(Qt.ControlModifier | Qt.Key_S, self)
        shortcut.activated.connect(self.save)

        self.textChanged.connect(self.onTextChanged)

    def onTextChanged(self):
        if self.text() != self.fileConetent:
            self.mod = True
        else:
            self.mod = False
        self.setMarginWidth(0, len(str(len(self.text().split('\n')))) * 20)

    def askforsave(self):
        if self.mod:
            r = QMessageBox.question(self.mainWindow, '询问', '是否要保存?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if r == QMessageBox.Cancel:
                return False
            elif r == QMessageBox.Yes:
                try:
                    self.save()
                except Exception as e:
                    QMessageBox.about(self.mainWindow, "保存失败", str(Exception(e)))
                return True
            elif r == QMessageBox.No:
                return True

    def save(self):
        print(1)
        self.mod = False
        r = uploadFile(self.url, self.password, self.text(), self.filenameArg)
        if r != '1':
            raise Exception('可能没有权限')
