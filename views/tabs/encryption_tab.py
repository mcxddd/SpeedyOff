from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QSpacerItem, QSizePolicy, QComboBox, QLineEdit, QHBoxLayout, QPushButton, QMessageBox, QCheckBox
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot


class EncryptionTab(QWidget):
    file_upload_requested = pyqtSignal(str)
    encrypt_decrypt_requested = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._initUI()
        self.file_name = None

    def _initUI(self):
        self.mainVLayout = QVBoxLayout()

        self.welcomeLabel = QLabel('请导入文件。')
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.importButton = QPushButton("选择文件")
        self.importButton.clicked.connect(self.open_file_dialog)

        self.importRowLayout = QHBoxLayout()
        self.importRowLayout.addWidget(self.welcomeLabel)
        self.importRowLayout.addWidget(self.importButton)
        self.mainVLayout.addLayout(self.importRowLayout)

        self.uploadfileInfo = QLabel('还没选呢')
        self.uploadfileInfo.setAlignment(Qt.AlignRight)
        self.mainVLayout.addWidget(self.uploadfileInfo)

        self.indicesRowLayout = QHBoxLayout()
        self.column_indices_input = QLineEdit()
        self.column_indices_input.setPlaceholderText(
            '输入需要操作的列 (例如, 0,2,4)')
        self.include_all_columns = QCheckBox(
            '包括所有的列')
        self.indicesRowLayout.addWidget(self.column_indices_input)
        self.indicesRowLayout.addWidget(self.include_all_columns)
        self.mainVLayout.addLayout(self.indicesRowLayout)

        self.algorithm_selector = QComboBox()
        self.algorithm_selector.addItems(["SHA256", "MD5", "SM4", 'BASE64'])
        self.algorithm_selector.currentIndexChanged.connect(
            self.toggle_sm4_mode_selector)

        spacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Encrypt", "Decrypt"])
        self.mode_selector.setFixedWidth(250)
        self.mode_selector.setVisible(False)

        self.algorithmRowLayout = QHBoxLayout()
        self.algorithmRowLayout.addWidget(self.algorithm_selector)
        self.algorithmRowLayout.addItem(spacer)
        self.algorithmRowLayout.addWidget(self.mode_selector)
        self.mainVLayout.addLayout(self.algorithmRowLayout)

        self.key_input = QLineEdit(self)
        self.key_input.setPlaceholderText("输入密钥")
        self.key_input.setVisible(False)  # Initially invisible
        # Assuming you're using a QVBoxLayout
        self.mainVLayout.addWidget(self.key_input)
        self.algorithm_selector.currentTextChanged.connect(
            self.toggle_sm4_mode_selector)

        self.mainVLayout.addStretch(1)
        self.encrypt_button = QPushButton('加密/解密 文件')
        self.encrypt_button.clicked.connect(self.request_encryption_decryption)

        self.encryptionRowLayout = QHBoxLayout()
        self.encryptionRowLayout.addStretch(1)
        self.encryptionRowLayout.addWidget(self.encrypt_button)

        self.mainVLayout.addLayout(self.encryptionRowLayout)
        self.setLayout(self.mainVLayout)

    def open_file_dialog(self):
        print('Opening file dialog')
        options = QFileDialog.Options()
        file_filter = "CSV Files (*.csv);;Excel Files (*.xlsx *.xls)"
        self.file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", file_filter, options=options)
        if self.file_path:
            # Get the file name from the file path
            self.file_upload_requested.emit(self.file_path)

    def request_encryption_decryption(self):
        column_indices_text = self.column_indices_input.text().strip()
        include_all = self.include_all_columns.isChecked()
        selected_algorithm = self.algorithm_selector.currentText()
        selected_mode = self.mode_selector.currentText()

        if not column_indices_text and not include_all:
            QMessageBox.warning(
                self, '缺失数值', '请输入需要操作的列或在右侧操作所有列处打勾。')
            return

        column_indices = []
        if column_indices_text:
            try:
                column_indices = list(map(int, column_indices_text.split(',')))
                column_indices = [x - 1 for x in column_indices]

            except ValueError:
                QMessageBox.warning(
                    self, " 输入不正确", "请输入有效的列数 (e.g., 0,1,4).")
                return

        data = {
            'column_indices': column_indices,
            'include_all': include_all,
            'selected_algorithm': selected_algorithm,
            'selected_mode': selected_mode,
            'key_input': self.key_input.text()
        }
        self.encrypt_decrypt_requested.emit(data)

    @pyqtSlot(str)
    def update_file_info(self, file_name):
        self.uploadfileInfo.setText(f'已选择的文件: {file_name}')

    def toggle_sm4_mode_selector(self):
        if self.algorithm_selector.currentText() == "SM4":
            self.mode_selector.setVisible(True)
            self.key_input.setVisible(True)

        else:
            self.mode_selector.setVisible(False)
            self.key_input.setVisible(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_combobox_lengths()

    def adjust_combobox_lengths(self):
        parent_width = self.algorithmRowLayout.geometry().width()
        algorithm_selector_width = parent_width * 0.75
        sm4_mode_selector_width = parent_width * 0.25
        self.algorithm_selector.setFixedWidth(algorithm_selector_width)
        self.mode_selector.setFixedWidth(sm4_mode_selector_width)
