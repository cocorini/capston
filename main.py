import sys
import capston
import riding_kickboard as riding
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QToolTip, QLabel, QFileDialog, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class UserApp(QWidget):

    def __init__(self):
        super(UserApp, self).__init__()
        self.initUI()
        self.show()
    
    def initUI(self):
        BtnReg = QPushButton('REGISTER', self)
        BtnReg.setToolTip('유저 등록')
        BtnReg.move(280, 100)
        BtnReg.resize(BtnReg.sizeHint())
        BtnReg.clicked.connect(self.BtnReg_clicked)

        BtnRide = QPushButton('RIDE', self)
        BtnRide.setToolTip('킥보드 탑승')
        BtnRide.move(450, 100)
        BtnRide.resize(BtnRide.sizeHint())
        BtnRide.clicked.connect(self.BtnRide_clicked)

        self.setWindowTitle('User Page')
        self.move(300,300)
        self.resize(300,200)

    def BtnReg_clicked(self):
        bytecode, abi = riding.compile_solidity()
        capstonstoragee = riding.contract_inform(bytecode, abi, CA)
        self.second = UserRegApp()


class UserCompleteApp(QWidget):

    def __init__(self):
        super(UserCompleteApp, self).__init__()
        self.initUI()
        self.show()
    
    def initUI(self):
        label1 = QLabel('유저 등록 완료', self)
        label1.setAlignment(Qt.AlignCenter)
        font1 = label1.font()
        font1.setPointSize(20)
        label1.setFont(font1)
        
        Btn = QPushButton('Back', self)
        Btn.resize(Btn.sizeHint())
        Btn.clicked.connect(self.Btn_clicked)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(Btn)

        self.setLayout(layout)
        self.setWindowTitle('register Page')
        self.move(300,300)
        self.resize(300,200)

    def Btn_clicked(self):
        self.close()

class MypageApp(QWidget):

    def __init__(self):
        super(MypageApp, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        label1 = QLabel('유저 정보', self)
        label1.setAlignment(Qt.AlignCenter)
        font1 = label1.font()
        font1.setPointSize(30)
        font1.setBold(True)
        label1.setFont(font1)

        user_inform = riding.result(TextAddr, capstonstoragee)
        label2 = QLabel(user_inform, self)
        label2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        font2 = label2.font()
        font2.setPointSize(10)
        label2.setFont(font2)

        Btn = QPushButton('Back', self)
        Btn.resize(Btn.sizeHint())
        Btn.clicked.connect(self.Btn_clicked)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(Btn)

        self.setLayout(layout)
        self.setWindowTitle('User State Page')
        self.move(300,300)
        self.resize(400,350)

    def Btn_clicked(self):
        self.close()

class UserRegApp(QWidget):

    def __init__(self):
        super(UserRegApp, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.AddLineEdit()

        BtnReg = QPushButton('REGISTER', self)
        BtnReg.setToolTip('유저 등록')
        BtnReg.move(30, 150)
        BtnReg.resize(BtnReg.sizeHint())
        BtnReg.clicked.connect(self.BtnReg_clicked)

        BtnRide = QPushButton('RIDE', self)
        BtnRide.setToolTip('킥보드 탑승')
        BtnRide.move(130, 150)
        BtnRide.resize(BtnRide.sizeHint())
        BtnRide.clicked.connect(self.BtnRide_clicked)

        BtnMypage = QPushButton('MyPage', self)
        BtnMypage.setToolTip('내 정보')
        BtnMypage.move(230,150)
        BtnMypage.resize(BtnMypage.sizeHint())
        BtnMypage.clicked.connect(self.BtnMypage_clicked)

        BtnBack = QPushButton('Back', self)
        BtnBack.move(130, 190)
        BtnBack.resize(BtnBack.sizeHint())
        BtnBack.clicked.connect(self.BtnBack_clicked)

        self.setWindowTitle('User Register Page')
        self.move(300,300)
        self.resize(350,250)

    def AddLineEdit(self):
        QLabel('User Address:', self).move(30,50)
        QLabel('Private Key:', self).move(30,80)
        
        # address 받기
        self.UserAddress = QLineEdit(self)
        self.UserAddress.move(150,45)
        self.UserAddress.setPlaceholderText('input your adress')
        
        # privatekey 받기
        self.PrivateKey = QLineEdit(self)
        self.PrivateKey.move(150, 75)
        self.PrivateKey.setPlaceholderText('input your privatekey')
        self.PrivateKey.setEchoMode(QLineEdit.Password)
    
    def BtnBack_clicked(self):
        self.close()

    def BtnReg_clicked(self):
        global TextAddr, TextPk
        TextAddr=self.UserAddress.text()
        TextPk=self.PrivateKey.text()

        isBlack, isUser = riding.check_init(TextAddr, capstonstoragee)

        if (isUser and isBlack):
            self.second = BlackErrorApp()
        elif isUser and isBlack==False:
            self.second = RegErrorApp()
        else:
            riding.register(capstonstoragee, TextAddr, TextPk)
            self.second = UserCompleteApp()
            riding.result(TextAddr, capstonstoragee)

    def BtnRide_clicked(self):
        global TextAddr, TextPk
        TextAddr=self.UserAddress.text()
        TextPk=self.PrivateKey.text()

        isBlack=False
        isUser=False
        
        isBlack, isUser = riding.check_init(TextAddr, capstonstoragee)
        
        if isBlack and isUser:
            self.second = BlackErrorApp()
        elif isUser and isBlack==False:
            self.second = RideApp()
        elif isUser==False:
            self.second = UserErrorApp()

    def BtnMypage_clicked(self):
        global TextAddr, TextPk
        TextAddr=self.UserAddress.text()
        TextPk=self.PrivateKey.text()

        isBlack=False
        isUser=False
        
        isBlack, isUser = riding.check_init(TextAddr, capstonstoragee)

        if isUser:
            self.second = MypageApp()
        else:
            self.second = UserErrorApp()

class DpyCompleteApp(QWidget):

    def __init__(self):
        super(DpyCompleteApp, self).__init__()
        self.initUI()
        self.show()
    
    def initUI(self):
        label1 = QLabel('컨트랙트 배포 완료', self)
        label1.setAlignment(Qt.AlignCenter)
        font1 = label1.font()
        font1.setPointSize(20)
        label1.setFont(font1)
        
        Btn = QPushButton('Back', self)
        Btn.resize(Btn.sizeHint())
        Btn.clicked.connect(self.Btn_clicked)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(Btn)

        self.setLayout(layout)
        self.setWindowTitle('Deploy Page')
        self.move(300,300)
        self.resize(300,200)

    def Btn_clicked(self):
        self.close()

#######################################################################
#######################################################################
#########################   RIDE APPLICATION   ########################
#######################################################################


class RideApp(QWidget):

    def __init__(self):
        super(RideApp, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.qclist = []
        self.position = 0

        self.Lgrid = QGridLayout()
        self.setLayout(self.Lgrid)
 
        self.label1 = QLabel('',self)
        self.label2 = QLabel('', self)
        self.label3 = QLabel('', self)
 
        BtnOpen = QPushButton('Open Image',self)
        self.Lgrid.addWidget(self.label1, 1, 1)
        self.Lgrid.addWidget(BtnOpen, 2, 1)
        BtnOpen.clicked.connect(self.BtnOpen_clicked)
 
        BtnSave = QPushButton('Save Image', self)
        self.Lgrid.addWidget(self.label2, 3, 1)
        self.Lgrid.addWidget(BtnSave, 4, 1)
        BtnSave.clicked.connect(self.BtnSave_clicked)

    # 사진이랑 aduino값 받기
        BtnReturn = QPushButton('Return', self)
        self.Lgrid.addWidget(self.label3, 5, 1)
        self.Lgrid.addWidget(BtnReturn, 6, 1)
        BtnReturn.clicked.connect(self.BtnReturn_clicked)

        self.setWindowTitle("Return Page")
        self.resize(300, 300)
    
    def BtnReturn_clicked(self):
        ## 반납할 때 쓸 함수 불러와야함...
        # 사진 업로드 하기
        riding.parking(TextAddr, capstonstoragee, TextPk)
        riding.result(TextAddr, capstonstoragee)
        self.close()

    def BtnOpen_clicked(self):
        self.File = QFileDialog.getOpenFileName(self, 'Open Image', './')
        self.label1.setText(self.File[0])
	# self.File 경로를 저장해서 파일 입출력 read, write를 통해 해당 경로의 파일을 지정된 경로로 넣어야 할 것 같음
    # 여기서 모듈화시킨 cnn실행 코드를 이용해서 cnn 실행.? 여기서 실행 시켜야할까 아니면
    # parking 함수에서 아두이노 실행시키는 것처럼 실행할까..? 이걸 고민해보자.
    # riding.parking(...)
                    
        
    # 사실상 save 버튼은 필요가 없다?
    def BtnSave_clicked(self):
        self.File = QFileDialog.getSaveFileName(self, 'Save Image', './')
	
#######################################################################
#######################################################################
########################   ERROR APPLICATION   ########################
#######################################################################

class RegErrorApp(QWidget):
    def __init__(self):
        super(RegErrorApp, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        label1 = QLabel('Error: 이미 등록된 사용자입니다', self)
        label1.setAlignment(Qt.AlignCenter)
        font1 = label1.font()
        font1.setPointSize(20)
        label1.setFont(font1)
        
        Btn = QPushButton('Back', self)
        Btn.resize(Btn.sizeHint())
        Btn.clicked.connect(self.Btn_clicked)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(Btn)

        self.setLayout(layout)
        self.setWindowTitle('Error Page')
        self.move(300,300)
        self.resize(300,200)

    def Btn_clicked(self):
        self.close()


class BlackErrorApp(QWidget):
    def __init__(self):
        super(BlackErrorApp, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        riding.result(TextAddr, capstonstoragee)
        label1 = QLabel('Error: 블랙리스트에 등록된 사용자입니다', self)
        label1.setAlignment(Qt.AlignCenter)
        font1 = label1.font()
        font1.setPointSize(20)
        label1.setFont(font1)
        
        Btn = QPushButton('Back', self)
        Btn.resize(Btn.sizeHint())
        Btn.clicked.connect(self.Btn_clicked)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(Btn)

        self.setLayout(layout)
        self.setWindowTitle('Error Page')
        self.move(300,300)
        self.resize(400,200)

    def Btn_clicked(self):
        self.close()

class ErrorApp(QWidget):

    def __init__(self):
        super(ErrorApp, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        label1 = QLabel('Error!', self)
        label1.setAlignment(Qt.AlignCenter)
        font1 = label1.font()
        font1.setPointSize(20)
        label1.setFont(font1)

        Btn = QPushButton('Back', self)
        Btn.resize(Btn.sizeHint())
        Btn.clicked.connect(self.Btn_clicked)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(Btn)

        self.setLayout(layout)
        self.setWindowTitle('Error Page')
        self.move(300,300)
        self.resize(300,200)

    def Btn_clicked(self):
        self.close()

class UserErrorApp(QWidget):

    def __init__(self):
        super(UserErrorApp, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        label1 = QLabel('Error: 등록되지 않은 사용자입니다', self)
        label1.setAlignment(Qt.AlignCenter)
        font1 = label1.font()
        font1.setPointSize(20)
        label1.setFont(font1)

        Btn = QPushButton('Back', self)
        Btn.resize(Btn.sizeHint())
        Btn.clicked.connect(self.Btn_clicked)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(Btn)

        self.setLayout(layout)
        self.setWindowTitle('Error Page')
        self.move(300,300)
        self.resize(300,200)

    def Btn_clicked(self):
        self.close()

#######################################################################
#######################################################################
#######################    MAIN APPLICATION   #########################
#######################################################################

class MainApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.qclist = []
        self.position = 0

        self.Lgrid = QGridLayout()
        self.setLayout(self.Lgrid)
 
        self.label1 = QLabel('',self)
        self.label2 = QLabel('', self)
        self.label3 = QLabel('', self)

        Btn = QPushButton('MAKE CONTRACT', self)
        Btn.setToolTip('컨트랙트 Deploy')
        self.Lgrid.addWidget(self.label1, 1, 1)
        self.Lgrid.addWidget(Btn, 2, 1)
        Btn.clicked.connect(self.Btn_clicked)

        BtnReg = QPushButton('REGISTER', self)
        BtnReg.setToolTip('유저 등록')
        self.Lgrid.addWidget(self.label2, 3, 1)
        self.Lgrid.addWidget(BtnReg, 4, 1)
        self.Lgrid.addWidget(self.label3, 5, 1)
        BtnReg.clicked.connect(self.BtnReg_clicked)


        self.setWindowTitle('KICKBOARD')
        self.setGeometry(300, 300, 300, 200)
        self.resize(300, 400)
        self.show() 

    def Btn_clicked(self):
        global bytecode, abi
        bytecode, abi = capston.compile_solidity()
        global CA
        CA = capston.make_CA(bytecode, abi)
        if CA != '':
            self.second = DpyCompleteApp()
        else :
            self.second = ErrorApp()

    def BtnReg_clicked(self):
        global capstonstoragee
        if 'CA' in globals():
            capstonstoragee = riding.contract_inform(bytecode, abi, CA)
            self.second = UserRegApp()
        else:
            self.second = ErrorApp()


#######################################################################
#######################################################################
#######################################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    sys.exit(app.exec_())