import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QImage

ids = ["return", "zero", "abc", "python", "class"]

class Form(QWidget):
    def __init__(self):
        super(Form, self).__init__()
        self.path = ''
        self.form = QFormLayout()
        self.setLayout(self.form)
        self.form.setVerticalSpacing(10)
        # Qt.AlignRight / Qt.AlignLeft
        self.form.setLabelAlignment(Qt.AlignCenter)

        self.lnName = QLineEdit()
        self.lnPNum2 = QLineEdit()
        self.lnId = QLineEdit()
        self.btnFindId = QPushButton("중복검사")
        self.lblChkId = QLabel("ID 중복검사를 진행해주세요")
        self.btnOk = QPushButton("확인")
        self.findFile = QPushButton("찾기")
        self.spAge = QSpinBox()
        self.spAge.setValue(19)
        self.lnPNum = QLineEdit()

        self.vbId = QHBoxLayout()
        self.vbId.addWidget(self.lnId)
        self.vbId.addWidget(self.btnFindId)
        self.vbId.addWidget(self.findFile)


        self.form.addRow("이름: ", self.lnName)
        self.form.addRow("ID: ", self.vbId)
        self.form.addWidget(self.lblChkId)
        self.form.addRow(QLabel(self.path))
        self.form.addRow("나이: ", self.spAge)
        self.form.addRow("연락처: ", self.lnPNum)
        self.form.addRow("보호자연락처: ", self.lnPNum2)
        self.form.addRow(self.btnOk)

        self.btnFindId.clicked.connect(self.chk_id)
        self.btnOk.clicked.connect(self.chk_ok)
        self.findFile.clicked.connect(self.get_filename)

    def get_filename(self):
        fname = QFileDialog.getOpenFileNames(self)
        self.path = fname[0][0]

    def chk_id(self):
        if len(self.lnId.text()) < 2:
            self.lblChkId.setText("2글자 이상 입력하세요")
        else:
            if ids.count(self.lnId.text()) == 1:
                self.lblChkId.setText("중복되는 ID가 존재합니다")
            else:
                self.lblChkId.setText("멋진 ID네요!")

    def chk_ok(self):
        str = ""
        if self.lnName.text() == "":
            str += "이름 "
        if self.lblChkId.text() != "멋진 ID네요!":
            str += "ID "
        if len(self.lnPNum.text()) < 13:
            str += "연락처 "
        if str != "":
            self.btnOk.setText(str + "을(를) 확인하세요")
        else:
            self.btnOk.setText("처리되었습니다")

app = QApplication([])
form = Form()
form.show()
sys.exit(app.exec_())