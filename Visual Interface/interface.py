from pathlib import Path

from PyQt6.QtCore import QPoint, Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QFontDatabase, QPainter, QPolygon
from PyQt6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
                             QDoubleSpinBox, QLabel, QLineEdit, QMainWindow, QMessageBox,
                             QPushButton, QScrollArea, QSizePolicy, QSpinBox,
                             QStackedWidget, QStyle, QStyleOptionSpinBox,
                             QTextEdit, QVBoxLayout, QWidget)

from managers import BlackjackManager, GoFishManager
from players import GoFishHumanPlayer


def setApplicationFont(app):
    fontPaths = [Path("C:/Windows/Fonts/segoeui.ttf"),
                 Path("C:/Windows/Fonts/arial.ttf")]
    for fontPath in fontPaths:
        if fontPath.exists():
            fontId = QFontDatabase.addApplicationFont(str(fontPath))
            if fontId >= 0:
                fontFamilies = QFontDatabase.applicationFontFamilies(fontId)
                if len(fontFamilies) > 0:
                    app.setFont(QFont(fontFamilies[0], 10))
                    return


def clearLayout(layout):
    while layout.count() > 0:
        item = layout.takeAt(0)
        if item.widget() is not None:
            widget = item.widget()
            widget.setParent(None)
            widget.deleteLater()
        elif item.layout() is not None:
            clearLayout(item.layout())


class PlayerCountSpinBox(QSpinBox):

    def paintEvent(self, event):
        super().paintEvent(event)
        option = self.styleOption()
        upRect = self.style().subControlRect(
            QStyle.ComplexControl.CC_SpinBox, option,
            QStyle.SubControl.SC_SpinBoxUp, self)
        downRect = self.style().subControlRect(
            QStyle.ComplexControl.CC_SpinBox, option,
            QStyle.SubControl.SC_SpinBoxDown, self)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#f5f2e8"))

        upCenter = upRect.center()
        upArrow = QPolygon([
            QPoint(upCenter.x(), upCenter.y() - 4),
            QPoint(upCenter.x() - 5, upCenter.y() + 3),
            QPoint(upCenter.x() + 5, upCenter.y() + 3)
        ])
        painter.drawPolygon(upArrow)

        downCenter = downRect.center()
        downArrow = QPolygon([
            QPoint(downCenter.x() - 5, downCenter.y() - 3),
            QPoint(downCenter.x() + 5, downCenter.y() - 3),
            QPoint(downCenter.x(), downCenter.y() + 4)
        ])
        painter.drawPolygon(downArrow)


    def styleOption(self):
        option = QStyleOptionSpinBox()
        self.initStyleOption(option)
        return option


class CardWidget(QFrame):

    def __init__(self, card=None, hidden=False, compact=False):
        super().__init__()
        self.setObjectName("playingCard")

        if compact:
            self.setFixedSize(62, 88)
        else:
            self.setFixedSize(90, 126)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cardLabel = QLabel()
        cardLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cardLabel.setWordWrap(True)

        if hidden:
            self.setProperty("hiddenCard", True)
            cardLabel.setText("CARD\nBACK")
        else:
            cardLabel.setText(f"{card.rank}\n\nof\n\n{card.suit}")
            if card.suit in ["Hearts", "Diamonds"]:
                cardLabel.setStyleSheet("color: #b42318; font-weight: 700;")
            else:
                cardLabel.setStyleSheet("color: #17212b; font-weight: 700;")

        layout.addWidget(cardLabel)


class CardGameWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Card Games")
        self.resize(1120, 760)
        self.setMinimumSize(900, 650)

        self.blackjackManager = BlackjackManager()
        self.goFishManager = GoFishManager()
        self.blackjackName = "Player"
        self.blackjackPlayers = 2
        self.blackjackAwaitingBet = False
        self.goFishName = "Player"
        self.goFishPlayers = 2

        self.computerTimer = QTimer(self)
        self.computerTimer.setSingleShot(True)
        self.computerTimer.timeout.connect(self.runComputerTurn)

        self.blackjackBetTimer = QTimer(self)
        self.blackjackBetTimer.setSingleShot(True)
        self.blackjackBetTimer.timeout.connect(self.prepareBlackjackBet)

        self.pages = QStackedWidget()
        self.setCentralWidget(self.pages)

        self.menuPage = self.buildMenuPage()
        self.blackjackSetupPage = self.buildBlackjackSetupPage()
        self.goFishSetupPage = self.buildGoFishSetupPage()
        self.blackjackPage = self.buildBlackjackPage()
        self.goFishPage = self.buildGoFishPage()

        for page in [self.menuPage, self.blackjackSetupPage, self.goFishSetupPage,
                     self.blackjackPage, self.goFishPage]:
            self.pages.addWidget(page)

        self.applyStyles()
        self.showMenu()


    def applyStyles(self):
        self.setStyleSheet("""
            QWidget {
                color: #f5f2e8;
                font-size: 15px;
            }
            QMainWindow, QStackedWidget, QWidget#gamePage {
                background-color: #102a22;
            }
            QWidget#menuPage, QWidget#setupPage {
                background-color: #14253d;
            }
            QLabel {
                background-color: transparent;
            }
            QLabel#titleLabel {
                font-size: 42px;
                font-weight: 800;
                color: #f8d477;
            }
            QLabel#screenTitle {
                font-size: 27px;
                font-weight: 750;
                color: #f8d477;
            }
            QLabel#statusLabel {
                background-color: #183d31;
                border: 1px solid #3b715f;
                border-radius: 9px;
                padding: 10px;
                font-size: 17px;
                font-weight: 650;
            }
            QFrame#panel {
                background-color: #17372d;
                border: 1px solid #3c6d5d;
                border-radius: 10px;
            }
            QFrame#playingCard {
                background-color: #f8f5ea;
                border: 2px solid #d3cbb8;
                border-radius: 8px;
            }
            QFrame#playingCard[hiddenCard="true"] {
                background-color: #254f78;
                border: 3px double #a7c8e8;
                color: white;
            }
            QPushButton {
                background-color: #315f50;
                border: 1px solid #5b8c7b;
                border-radius: 7px;
                padding: 9px 18px;
                font-weight: 650;
            }
            QPushButton:hover {
                background-color: #3f7865;
            }
            QPushButton:disabled {
                background-color: #3c4b46;
                color: #8d9994;
                border-color: #4f5c57;
            }
            QPushButton#accentButton {
                background-color: #c88a25;
                color: #17212b;
                border-color: #e4b45f;
            }
            QPushButton#accentButton:hover {
                background-color: #dda33f;
            }
            QPushButton#accentButton:disabled {
                background-color: #3c4b46;
                color: #8d9994;
                border-color: #4f5c57;
            }
            QPushButton#dangerButton {
                background-color: #8f3b3b;
                border-color: #bd6565;
            }
            QLineEdit, QSpinBox, QComboBox, QTextEdit {
                background-color: #f7f4ea;
                color: #17212b;
                border: 1px solid #b8b09f;
                border-radius: 6px;
                padding: 7px;
                selection-background-color: #315f50;
            }
            QSpinBox {
                padding-right: 38px;
                min-height: 24px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                subcontrol-origin: border;
                width: 34px;
                background-color: #315f50;
                border-left: 1px solid #5b8c7b;
            }
            QSpinBox::up-button {
                subcontrol-position: top right;
                border-top-right-radius: 5px;
                border-bottom: 1px solid #5b8c7b;
            }
            QSpinBox::down-button {
                subcontrol-position: bottom right;
                border-bottom-right-radius: 5px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #3f7865;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
        """)


    def makeButton(self, text, callback, accent=False, danger=False):
        button = QPushButton(text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(callback)
        if accent:
            button.setObjectName("accentButton")
        elif danger:
            button.setObjectName("dangerButton")
        return button


    def buildMenuPage(self):
        page = QWidget()
        page.setObjectName("menuPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("CARD GAMES")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = QLabel("Choose a game and take a seat at the table")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        blackjackButton = self.makeButton("Play Blackjack", self.showBlackjackSetup, accent=True)
        goFishButton = self.makeButton("Play Go Fish", self.showGoFishSetup, accent=True)
        exitButton = self.makeButton("Exit Application", self.exitApplication, danger=True)
        for button in [blackjackButton, goFishButton, exitButton]:
            button.setFixedWidth(280)
            button.setMinimumHeight(48)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(35)
        layout.addWidget(blackjackButton, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(goFishButton, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(15)
        layout.addWidget(exitButton, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        return page


    def buildBlackjackSetupPage(self):
        page = QWidget()
        page.setObjectName("setupPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(160, 80, 160, 80)

        title = QLabel("BLACKJACK SETUP")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description = QLabel("Try to finish closest to 21 without going over. You begin with $10.00 in chips and may wager up to $2.00 after staying. The dealer wins tied high scores.")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form = QFrame()
        form.setObjectName("panel")
        formLayout = QVBoxLayout(form)
        formLayout.setContentsMargins(35, 30, 35, 30)
        formLayout.addWidget(QLabel("Player name"))
        self.blackjackNameInput = QLineEdit("Player")
        self.blackjackNameInput.setMaxLength(24)
        formLayout.addWidget(self.blackjackNameInput)
        formLayout.addSpacing(15)
        formLayout.addWidget(QLabel("Total players (including you and the dealer)"))
        self.blackjackPlayerInput = PlayerCountSpinBox()
        self.blackjackPlayerInput.setRange(2, 4)
        self.blackjackPlayerInput.setValue(2)
        self.blackjackPlayerInput.setAccelerated(True)
        formLayout.addWidget(self.blackjackPlayerInput)

        buttons = QHBoxLayout()
        buttons.addWidget(self.makeButton("Back", self.showMenu))
        buttons.addWidget(self.makeButton("Start Blackjack", self.startBlackjack, accent=True))

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(25)
        layout.addWidget(form)
        layout.addSpacing(20)
        layout.addLayout(buttons)
        layout.addStretch()
        return page


    def buildGoFishSetupPage(self):
        page = QWidget()
        page.setObjectName("setupPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(160, 70, 160, 70)

        title = QLabel("GO FISH SETUP")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description = QLabel("Collect same-rank pairs. The game ends when a hand or the draw pile is empty.")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form = QFrame()
        form.setObjectName("panel")
        formLayout = QVBoxLayout(form)
        formLayout.setContentsMargins(35, 30, 35, 30)
        formLayout.addWidget(QLabel("Player name"))
        self.goFishNameInput = QLineEdit("Player")
        self.goFishNameInput.setMaxLength(24)
        formLayout.addWidget(self.goFishNameInput)
        formLayout.addSpacing(15)
        formLayout.addWidget(QLabel("Total players"))
        self.goFishPlayerInput = PlayerCountSpinBox()
        self.goFishPlayerInput.setRange(2, 4)
        self.goFishPlayerInput.setValue(2)
        self.goFishPlayerInput.setAccelerated(True)
        formLayout.addWidget(self.goFishPlayerInput)

        buttons = QHBoxLayout()
        buttons.addWidget(self.makeButton("Back", self.showMenu))
        buttons.addWidget(self.makeButton("Start Go Fish", self.startGoFish, accent=True))

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(25)
        layout.addWidget(form)
        layout.addSpacing(20)
        layout.addLayout(buttons)
        layout.addStretch()
        return page


    def makeGameHeader(self, titleText, resetCallback):
        header = QHBoxLayout()
        title = QLabel(titleText)
        title.setObjectName("screenTitle")
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.makeButton("Reset Game", resetCallback))
        header.addWidget(self.makeButton("Main Menu", self.showMenu))
        header.addWidget(self.makeButton("Exit", self.exitApplication, danger=True))
        return header


    def makeScrollRow(self, minimumHeight):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(minimumHeight)
        container = QWidget()
        row = QHBoxLayout(container)
        row.setContentsMargins(8, 8, 8, 8)
        row.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        scroll.setWidget(container)
        return scroll, row


    def buildBlackjackPage(self):
        page = QWidget()
        page.setObjectName("gamePage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 18, 24, 18)
        layout.addLayout(self.makeGameHeader("BLACKJACK", self.restartBlackjack))

        self.blackjackStatus = QLabel("Your turn.")
        self.blackjackStatus.setObjectName("statusLabel")
        self.blackjackStatus.setWordWrap(True)
        layout.addWidget(self.blackjackStatus)

        layout.addWidget(QLabel("Other players"))
        opponentScroll, self.blackjackOpponentsLayout = self.makeScrollRow(180)
        layout.addWidget(opponentScroll)

        self.blackjackPlayerLabel = QLabel("Your hand")
        self.blackjackPlayerLabel.setObjectName("screenTitle")
        layout.addWidget(self.blackjackPlayerLabel)
        handScroll, self.blackjackHandLayout = self.makeScrollRow(155)
        layout.addWidget(handScroll)

        actionRow = QHBoxLayout()
        self.blackjackHitButton = self.makeButton("Hit", self.hitBlackjack, accent=True)
        self.blackjackStayButton = self.makeButton("Stay", self.prepareBlackjackBet)
        self.blackjackHitButton.setMinimumWidth(140)
        self.blackjackStayButton.setMinimumWidth(140)
        self.blackjackBetInput = QDoubleSpinBox()
        self.blackjackBetInput.setRange(0.0, 2.0)
        self.blackjackBetInput.setDecimals(2)
        self.blackjackBetInput.setSingleStep(0.25)
        self.blackjackBetInput.setPrefix("$")
        self.blackjackBetInput.setSuffix(" USD")
        self.blackjackBetButton = self.makeButton("Place Bet and Finish", self.finishBlackjack, accent=True)
        actionRow.addStretch()
        actionRow.addWidget(self.blackjackHitButton)
        actionRow.addWidget(self.blackjackStayButton)
        actionRow.addSpacing(20)
        actionRow.addWidget(QLabel("Wager"))
        actionRow.addWidget(self.blackjackBetInput)
        actionRow.addWidget(self.blackjackBetButton)
        actionRow.addStretch()
        layout.addLayout(actionRow)
        return page


    def buildGoFishPage(self):
        page = QWidget()
        page.setObjectName("gamePage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.addLayout(self.makeGameHeader("GO FISH", self.restartGoFish))

        self.goFishStatus = QLabel("Your turn.")
        self.goFishStatus.setObjectName("statusLabel")
        self.goFishStatus.setWordWrap(True)
        layout.addWidget(self.goFishStatus)

        opponentScroll, self.goFishOpponentsLayout = self.makeScrollRow(150)
        layout.addWidget(opponentScroll)

        self.goFishLog = QTextEdit()
        self.goFishLog.setReadOnly(True)
        self.goFishLog.setMaximumHeight(145)
        layout.addWidget(self.goFishLog)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Ask"))
        self.goFishTargetChoice = QComboBox()
        controls.addWidget(self.goFishTargetChoice)
        controls.addWidget(QLabel("for"))
        self.goFishRankChoice = QComboBox()
        controls.addWidget(self.goFishRankChoice)
        self.goFishAskButton = self.makeButton("Ask for Card", self.askGoFish, accent=True)
        controls.addWidget(self.goFishAskButton)
        layout.addLayout(controls)

        self.goFishPlayerLabel = QLabel("Your hand")
        self.goFishPlayerLabel.setObjectName("screenTitle")
        layout.addWidget(self.goFishPlayerLabel)
        handScroll, self.goFishHandLayout = self.makeScrollRow(145)
        layout.addWidget(handScroll)
        return page


    def showMenu(self):
        self.computerTimer.stop()
        self.blackjackBetTimer.stop()
        self.pages.setCurrentWidget(self.menuPage)


    def showBlackjackSetup(self):
        self.computerTimer.stop()
        self.blackjackBetTimer.stop()
        self.pages.setCurrentWidget(self.blackjackSetupPage)


    def showGoFishSetup(self):
        self.computerTimer.stop()
        self.pages.setCurrentWidget(self.goFishSetupPage)


    def exitApplication(self):
        response = QMessageBox.question(
            self, "Exit Card Table", "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        if response == QMessageBox.StandardButton.Yes:
            QApplication.instance().quit()


    def startBlackjack(self):
        enteredName = self.blackjackNameInput.text().strip()
        if enteredName == "":
            enteredName = "Player"
        self.blackjackName = enteredName
        self.blackjackPlayers = self.blackjackPlayerInput.value()
        self.blackjackManager.startSession()
        self.restartBlackjack()


    def restartBlackjack(self):
        self.blackjackBetTimer.stop()
        self.blackjackManager.reset(self.blackjackName, self.blackjackPlayers)
        self.blackjackAwaitingBet = False
        self.blackjackBetInput.setMaximum(min(2.0, self.blackjackManager.chips.amount))
        self.blackjackBetInput.setValue(0.0)
        self.pages.setCurrentWidget(self.blackjackPage)
        self.blackjackStatus.setText("Your turn: choose Hit to draw or Stay to choose your wager.")
        self.renderBlackjack()


    def renderBlackjack(self):
        manager = self.blackjackManager
        clearLayout(self.blackjackOpponentsLayout)

        for player in manager.players[1:]:
            panel = QFrame()
            panel.setObjectName("panel")
            panelLayout = QVBoxLayout(panel)
            panelLayout.addWidget(QLabel(str(player)), alignment=Qt.AlignmentFlag.AlignCenter)

            cards = QHBoxLayout()
            cards.setAlignment(Qt.AlignmentFlag.AlignCenter)
            for idx in range(len(player.hand)):
                hidden = not manager.finished and idx == 0
                cards.addWidget(CardWidget(player.hand[idx], hidden=hidden, compact=True))
            panelLayout.addLayout(cards)

            if manager.finished:
                scoreText = str(player.giveScore())
            else:
                scoreText = "?"
            panelLayout.addWidget(QLabel(f"Score: {scoreText}"), alignment=Qt.AlignmentFlag.AlignCenter)
            self.blackjackOpponentsLayout.addWidget(panel)

        clearLayout(self.blackjackHandLayout)
        for card in manager.humanPlayer.hand:
            self.blackjackHandLayout.addWidget(CardWidget(card))

        humanScore = manager.humanPlayer.giveScore()
        self.blackjackPlayerLabel.setText(
            f"{manager.humanPlayer.name}'s hand — Score: {humanScore} — Cards: {len(manager.humanPlayer.hand)} — Chips: {manager.formatCurrency(manager.chips)}")
        active = not manager.finished
        choosingCards = active and not self.blackjackAwaitingBet
        self.blackjackHitButton.setEnabled(choosingCards and not manager.humanTurnIsOver())
        self.blackjackStayButton.setEnabled(choosingCards)
        self.blackjackBetInput.setEnabled(active and self.blackjackAwaitingBet)
        self.blackjackBetButton.setEnabled(active and self.blackjackAwaitingBet)


    def hitBlackjack(self):
        drawnCard = self.blackjackManager.hitHuman()
        if drawnCard is None:
            return

        score = self.blackjackManager.humanPlayer.giveScore()
        self.blackjackStatus.setText(f"You drew the {drawnCard}. Your score is now {score}.")
        self.renderBlackjack()

        if self.blackjackManager.humanTurnIsOver():
            self.blackjackBetTimer.start(500)


    def prepareBlackjackBet(self):
        self.blackjackBetTimer.stop()
        if self.blackjackManager.finished or self.blackjackAwaitingBet:
            return

        self.blackjackAwaitingBet = True
        maxBet = min(2.0, self.blackjackManager.chips.amount)
        self.blackjackBetInput.setMaximum(maxBet)
        self.blackjackBetInput.setValue(maxBet)
        self.blackjackStatus.setText(
            f"Your hand is complete. Choose a wager from $0.00 to ${maxBet:.2f}, then finish the game.")
        self.renderBlackjack()


    def finishBlackjack(self):
        if self.blackjackManager.finished:
            return
        if not self.blackjackAwaitingBet:
            self.prepareBlackjackBet()
            return

        betAmount = self.blackjackBetInput.value()
        result = self.blackjackManager.completeGame(betAmount)
        self.blackjackAwaitingBet = False
        self.renderBlackjack()
        self.blackjackStatus.setText(f"Game complete — {result}")


    def startGoFish(self):
        enteredName = self.goFishNameInput.text().strip()
        if enteredName == "":
            enteredName = "Player"
        self.goFishName = enteredName
        self.goFishPlayers = self.goFishPlayerInput.value()
        self.restartGoFish()


    def restartGoFish(self):
        self.computerTimer.stop()
        self.goFishManager.reset(self.goFishName, self.goFishPlayers)
        self.pages.setCurrentWidget(self.goFishPage)
        self.goFishLog.clear()
        self.goFishLog.append("The cards are dealt.")
        self.appendGoFishMessages(self.goFishManager.openingMessages)
        self.renderGoFish()


    def appendGoFishMessages(self, messages):
        for message in messages:
            self.goFishLog.append(message)
        scrollBar = self.goFishLog.verticalScrollBar()
        scrollBar.setValue(scrollBar.maximum())


    def renderGoFish(self):
        manager = self.goFishManager
        human = manager.humanPlayer
        clearLayout(self.goFishOpponentsLayout)

        for player in manager.players[1:]:
            panel = QFrame()
            panel.setObjectName("panel")
            panelLayout = QVBoxLayout(panel)
            panelLayout.addWidget(QLabel(str(player)), alignment=Qt.AlignmentFlag.AlignCenter)
            preview = QHBoxLayout()
            preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cardsToShow = min(len(player.hand), 5)
            for _ in range(cardsToShow):
                preview.addWidget(CardWidget(hidden=True, compact=True))
            panelLayout.addLayout(preview)
            cardWord = "card" if len(player.hand) == 1 else "cards"
            pairWord = "pair" if player.giveScore() == 1 else "pairs"
            panelLayout.addWidget(
                QLabel(f"{len(player.hand)} {cardWord} · {player.giveScore()} {pairWord}"),
                alignment=Qt.AlignmentFlag.AlignCenter)
            self.goFishOpponentsLayout.addWidget(panel)

        clearLayout(self.goFishHandLayout)
        for card in human.hand:
            self.goFishHandLayout.addWidget(CardWidget(card))

        pairRanks = []
        for pair in human.pairs:
            pairRanks.append(pair[0].rank)
        if len(pairRanks) == 0:
            pairText = "None yet"
        else:
            pairText = ", ".join(pairRanks)
        self.goFishPlayerLabel.setText(
            f"{human.name}'s hand — Pairs: {pairText} — Draw pile: {len(manager.deck.drawPile)}")

        self.goFishTargetChoice.clear()
        for idx in range(len(manager.players)):
            player = manager.players[idx]
            if player != human and len(player.hand) > 0:
                self.goFishTargetChoice.addItem(
                    f"{player.name} ({len(player.hand)} cards)", idx)

        self.goFishRankChoice.clear()
        for rank in human.giveRanks():
            self.goFishRankChoice.addItem(rank)

        humanTurn = (not manager.finished and
                     isinstance(manager.giveCurrentPlayer(), GoFishHumanPlayer))
        self.goFishTargetChoice.setEnabled(humanTurn)
        self.goFishRankChoice.setEnabled(humanTurn)
        self.goFishAskButton.setEnabled(
            humanTurn and self.goFishTargetChoice.count() > 0 and self.goFishRankChoice.count() > 0)

        if manager.finished:
            message, _ = manager.determineWinner()
            self.goFishStatus.setText(message)
        elif humanTurn:
            self.goFishStatus.setText("Your turn: choose an opponent and one of the ranks in your hand.")
        else:
            currentPlayer = manager.giveCurrentPlayer()
            self.goFishStatus.setText(f"{currentPlayer} is thinking...")


    def askGoFish(self):
        if self.goFishManager.finished:
            return

        targetIdx = self.goFishTargetChoice.currentData()
        requestedRank = self.goFishRankChoice.currentText()
        if targetIdx is None or requestedRank == "":
            return

        human = self.goFishManager.humanPlayer
        askedPlayer = self.goFishManager.players[targetIdx]
        event = self.goFishManager.performRequest(human, askedPlayer, requestedRank)
        self.appendGoFishMessages(event["messages"])
        if event["drawnCard"] is not None:
            self.goFishLog.append(f"You drew the {event['drawnCard']}.")

        self.renderGoFish()
        if event["gameOver"]:
            self.finishGoFish()
        elif not isinstance(self.goFishManager.giveCurrentPlayer(), GoFishHumanPlayer):
            self.scheduleComputerTurn()


    def scheduleComputerTurn(self):
        if not self.goFishManager.finished:
            self.computerTimer.start(800)


    def runComputerTurn(self):
        if self.pages.currentWidget() is not self.goFishPage:
            return
        if self.goFishManager.finished:
            return
        if isinstance(self.goFishManager.giveCurrentPlayer(), GoFishHumanPlayer):
            return

        event = self.goFishManager.computerAction()
        self.appendGoFishMessages(event["messages"])
        self.renderGoFish()

        if event["gameOver"]:
            self.finishGoFish()
        elif not isinstance(self.goFishManager.giveCurrentPlayer(), GoFishHumanPlayer):
            self.scheduleComputerTurn()


    def finishGoFish(self):
        self.computerTimer.stop()
        message, scores = self.goFishManager.determineWinner()
        self.goFishLog.append("")
        self.goFishLog.append("Final pairs:")
        for player, score in scores:
            pairWord = "pair" if score == 1 else "pairs"
            self.goFishLog.append(f"{player}: {score} {pairWord}")
        self.goFishLog.append(message)
        self.goFishStatus.setText(message)
        self.renderGoFish()


    def closeEvent(self, event):
        response = QMessageBox.question(
            self, "Exit Card Table", "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        if response == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
