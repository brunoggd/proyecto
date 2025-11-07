estilo = """
QMainWindow {font-family: 'Trebuchet MS';}
                           
QLabel {color: white;
        font-size: 18px;
        font-family: 'Trebuchet MS';
        background: transparent;}
                           
QPushButton {background-color: rgba(59, 115, 255, 50);
            color: rgba(255,255,255,200);
            font-size: 20px;
            font-family: 'Trebuchet MS';
            border: 2px solid #0C5AFA;
            border-radius: 15px;
            padding: 10px 10px;}
                           
QPushButton::hover {background-color: #4784FC;
                    color: rgba(255,255,255,255);
                    font-family: 'Trebuchet MS';}
                           
QTextEdit {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 18px;
            font-family: 'Trebuchet MS';
            border: 2px solid #0C5AFA;
            border-radius: 15px;
            padding: 10px 10px;}
                           
QCalendarWidget {
                background-color: #f0f0f0;
                font-family: 'Trebuchet MS';
                border: 1px solid #4784FC;
            }
                           
QCalendarWidget QAbstractItemView:enabled {
    font-size: 14px;
    color: black;
    background-color: white;
    selection-background-color: #a0c4ff;
    selection-color: black;
    border: 2px solid #0C5AFA;
    border-radius: 16px;
    padding: 5px;        
}

#qt_calendar_navigationbar{color: white;
                            background-color: #3B73FF;
                            border: 2px solid #0C5AFA;
                            border-radius: 15px;
                            padding: 10px;}

QCalendarWidget QComboBox#qt_calendar_monthbox, QCalendarWidget QComboBox#qt_calendar_yearbox {background-color: #1B61F5;
                                                                                                color: white;}

QCalendarWidget QToolButton {color: rgba(255,255,255,200);
                            font-family: 'Trebuchet MS';
                            font-size: 20px; }

QCalendarWidget QToolButton:hover {color: rgba(255,255,255,255);
                                    background-color: #3471ED;}

#qt_calendar_prevmonth:hover,#qt_calendar_nextmonth:hover {background-color: #3471ED;}

QCalendarWidget QMenu {background-color: #3F7BF2;
                        border: 2px solid #2C6FF5;
                        border-radius: 15px;
                        padding: 10px;
                        color: white;
                        font-size: 16px;}

QMenu {
    background: lightgray;
}
                           
QMenu::item:selected {
    background: lightblue;
    border-radius: 2px;
}
                           
QSplitter::handle {background-color: #F3FF00;}
                           
QComboBox {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 18px;
            border-radius: 20px;
            padding: 10px 10px;
            font-family: 'Trebuchet MS';}
                           
QComboBox::drop-down {subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 25px;
                    border-left: 1px solid #199CFC;}
                           
QComboBox QAbstractItemView {
    background-color: #477DF5;
    color: black;
    border: 2px solid #199CFC;
    selection-background-color: #2C6DF5;
    selection-color: white;
    font-size: 14px;
}

QListWidget {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 25px;
            font-family: 'Trebuchet MS';
            border: 2px solid #0C5AFA;
            border-radius: 15px;
            padding: 10px 10px;}
            
QLineEdit {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 16px;
            border-radius: 20px;
            padding: 10px 10px;
            font-family: 'Aptos';}
            
QMessageBox {background-color: #3B73FF;
            color: black;}
            
QSlider::groove:horizontal {border: 1px solid yellow;
                            height: 8px;
                            background: #199CFC;}

QSlider::handle:horizontal {background: white;
                            border: 1px solid #E8E8E8;
                            width: 15px;
                            margin: -5px;
                            border-radius: 3px;}
                            
QRadioButton {color: white;
            font-family: 'Trebuchet MS';
            font-size: 25px;
            spacing: 30px;}

QRadioButton::indicator {width: 16px;
                        height: 16px;
                        border-radius: 8px;
                        border: 2px solid #E8E8E8;
                        background-color: white;}

QRadioButton::indicator:checked {background-color: #4CAF50;
                                border: 2px solid #2E7D32;}

QRadioButton::indicator:hover {border: 2px solid black;}

QGroupBox {background-color: transparent;
            border: 2px solid #0C5AFA;
            border-radius: 8px;
            color: white;}
            
QGroupBox::title {subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                color: white;}
                
QGroupBox QLabel {
    color: white;
}"""


estilo_etiqueta_fecha = """background-color: rgba(0,0,0,100);
                            color: white;
                            border-radius: 20px;
                            padding: 5px;"""

titulo_mis_tareas = "font-size: 25px;"

estilo_contenedor = """background-color: rgba(0,0,0,50);
                        border-radius: 20px;"""

estilo_tema_oscuro = """
QMainWindow {background: transparent;
            font-family: 'Trebuchet MS';}
                           
QLabel {color: white;
        font-size: 18px;
        font-family: 'Trebuchet MS';
        background: transparent;}
                           
QPushButton {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 20px;
            font-family: 'Trebuchet MS';
            border: 2px solid #3BAAFF;
            border-radius: 15px;
            padding: 10px 10px;}
                           
QPushButton::hover {background-color: black;
                    color: #3BAAFF;
                    font-family: 'Trebuchet MS';}
                           
QTextEdit {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 18px;
            font-family: 'Trebuchet MS';
            border: 2px solid #3BAAFF;
            border-radius: 15px;
            padding: 10px 10px;}
                           
QCalendarWidget {
                background-color: #f0f0f0;
                font-family: 'Trebuchet MS';
                border: 1px solid #ccc;
            }
                           
QCalendarWidget QAbstractItemView:enabled {
    font-size: 14px;
    color: #333;
    background-color: white;
    selection-background-color: #a0c4ff;
    selection-color: black;
    border: 2px solid #3BAAFF;
    border-radius: 16px;
    padding: 5px;        
}

#qt_calendar_navigationbar{color: white;
                            background-color: black;
                            border: 2px solid #3BAAFF;
                            border-radius: 15px;
                            padding: 10px;}

QCalendarWidget QComboBox#qt_calendar_monthbox, QCalendarWidget QComboBox#qt_calendar_yearbox {background-color: blue;
                                                                                                color: white;}

QCalendarWidget QToolButton {color: rgba(255,255,255,175);
                            font-family: 'Trebuchet MS';
                            font-size: 20px; }

QCalendarWidget QToolButton:hover {color: rgba(255,255,255,255);
                                    background-color: transparent;}

#qt_calendar_prevmonth:hover,#qt_calendar_nextmonth:hover {background-color: transparent;}

QCalendarWidget QMenu {background-color: rgba(0,0,0,100);
                        border: 2px solid black;
                        border-radius: 15px;
                        padding: 10px;
                        color: white;
                        font-size: 16px;}
                           
QMenu {
    background: lightgray;
}
                           
QMenu::item:selected {
    background: lightblue;
    border-radius: 2px;
}
                           
QSplitter::handle {background-color: #F3FF00;}
                           
QComboBox {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 18px;
            border-radius: 20px;
            padding: 10px 10px;
            font-family: 'Trebuchet MS';}
                           
QComboBox::drop-down {subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 25px;
                    border-left: 1px solid white;}
                           
QComboBox QAbstractItemView {
    background-color: rgba(0,0,0,100);
    color: rgba(255, 255, 255, 150);
    border: 2px solid #3BAAFF;
    selection-background-color: rgba(0,0,0,100);
    selection-color: rgba(255, 255, 255, 255);
    font-size: 14px;
}

QListWidget {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 25px;
            font-family: 'Trebuchet MS';
            border: 2px solid #3BAAFF;
            border-radius: 15px;
            padding: 10px 10px;}
            
QLineEdit {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 16px;
            border-radius: 20px;
            padding: 10px 10px;
            font-family: 'Aptos';}
            
QMessageBox {background-color: rgba(0,0,0,100);
            color: white;}
            
QSlider::groove:horizontal {border: 1px solid white;
                            height: 8px;
                            background: black;}
                                    
QSlider::handle:horizontal {background: white;
                            border: 1px solid black;
                            width: 15px;
                            margin: -5px;
                            border-radius: 3px;}
                            
QRadioButton {color: white;
            font-family: 'Trebuchet MS';
            font-size: 25px;
            spacing: 30px;}

QRadioButton::indicator {width: 16px;
                        height: 16px;
                        border-radius: 8px;
                        border: 2px solid black;
                        background-color: white;}

QRadioButton::indicator:checked {background-color: #4CAF50;
                                border: 2px solid #2E7D32;}

QRadioButton::indicator:hover {border: 2px solid white;}

QGroupBox {background-color: transparent;
            border: 2px solid #3BAAFF;
            border-radius: 8px;}
            
QGroupBox::title {subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;}"""

estilo_etiqueta_año = """color: white;
                        background-color: rgba(0,0,0,100);
                        border-radius: 20px;
                        padding: 5px 5px;"""