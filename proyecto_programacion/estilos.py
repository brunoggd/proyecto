estilo = """
QMainWindow {background: transparent;
            font-family: 'Trebuchet MS';}
                           
QLabel {color: black;
        font-size: 25px;
        font-family: 'Trebuchet MS';}
                           
QPushButton {background-color: transparent;
            color: rgba(0, 0, 0,200);
            font-size: 20px;
            font-family: 'Trebuchet MS';
            border: 2px solid #F5EA2F;
            border-radius: 15px;
            padding: 10px 10px;}
                           
QPushButton::hover {background-color: #EDE877;
                    color: rgba(0, 0, 0,255);
                    font-family: 'Trebuchet MS';}
                           
QTextEdit {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 25px;
            font-family: 'Trebuchet MS';
            border: 2px solid #F5EA2F;
            border-radius: 15px;
            padding: 10px 10px;}
                           
QCalendarWidget {
                background-color: #f0f0f0;
                font-family: "Comic Sans MS";
                border: 1px solid #ccc;
            }
                           
QCalendarWidget QAbstractItemView:enabled {
    font-size: 14px;
    color: #333;
    background-color: white;
    selection-background-color: #a0c4ff;
    selection-color: black;        
}
                           
#qt_calendar_navigationbar {
    background-color: #707070;
    border-bottom: 1px solid #ccc;
}
                           
#qt_calendar_prevmonth, #qt_calendar_nextmonth {
    icon-size: 20px;
    background-color: transparent;
}
                           
#qt_calendar_monthbutton, #qt_calendar_yearbutton {
    font-weight: bold;
    background-color: transparent;
}
                           
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
            font-size: 20px;
            border-radius: 20px;
            padding: 10px 10px;
            font-family: 'Trebuchet MS';}
                           
QComboBox::drop-down {subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 25px;
                    border-left: 1px solid #F5EA2F;}
                           
QComboBox QAbstractItemView {
    background-color: #F5EA2F;
    color: black;
    border: 2px solid #F3FF00;
    selection-background-color: #FAFFB8;
    selection-color: black;
    font-size: 14px;
}

QListWidget {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 25px;
            font-family: 'Trebuchet MS';
            border: 2px solid #F5EA2F;
            border-radius: 15px;
            padding: 10px 10px;}
            
QLineEdit {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 20px;
            border-radius: 20px;
            padding: 10px 10px;
            font-family: 'Aptos';}
            
QMessageBox {background-color: #F7FA46;
            color: black;}
            
QSlider::groove:horizontal {border: 1px solid yellow;
                            height: 8px;
                            background: #FFFF00;}

QSlider::handle:horizontal {background: white;
                            border: 1px solid #E8E8E8;
                            width: 15px;
                            margin: -5px;
                            border-radius: 3px;}"""

estilo_tema_oscuro = """
QMainWindow {background: transparent;
            font-family: 'Trebuchet MS';}
                           
QLabel {color: white;
        font-size: 25px;
        font-family: 'Trebuchet MS';}
                           
QPushButton {background-color: rgba(0,0,0,200);
            color: rgba(242, 255, 0,200);
            font-size: 20px;
            font-family: 'Trebuchet MS';
            border: 2px solid #F5EA2F;
            border-radius: 15px;
            padding: 10px 10px;}
                           
QPushButton::hover {background-color: black;
                    color: rgba(242, 255, 0,255);
                    font-family: 'Trebuchet MS';}
                           
QTextEdit {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 25px;
            font-family: 'Trebuchet MS';
            border: 2px solid #F5EA2F;
            border-radius: 15px;
            padding: 10px 10px;}
                           
QCalendarWidget {
                background-color: #f0f0f0;
                font-family: "Comic Sans MS";
                border: 1px solid #ccc;
            }
                           
QCalendarWidget QAbstractItemView:enabled {
    font-size: 14px;
    color: #333;
    background-color: white;
    selection-background-color: #a0c4ff;
    selection-color: black;        
}
                           
#qt_calendar_navigationbar {
    background-color: #707070;
    border-bottom: 1px solid #ccc;
}
                           
#qt_calendar_prevmonth, #qt_calendar_nextmonth {
    icon-size: 20px;
    background-color: transparent;
}
                           
#qt_calendar_monthbutton, #qt_calendar_yearbutton {
    font-weight: bold;
    background-color: transparent;
}
                           
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
            font-size: 20px;
            border-radius: 20px;
            padding: 10px 10px;
            font-family: 'Trebuchet MS';}
                           
QComboBox::drop-down {subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 25px;
                    border-left: 1px solid #F5EA2F;}
                           
QComboBox QAbstractItemView {
    background-color: rgba(0,0,0,100);
    color: rgba(242, 255, 0,150);
    border: 2px solid #F3FF00;
    selection-background-color: rgba(0,0,0,100);
    selection-color: rgba(242, 255, 0,255);
    font-size: 14px;
}

QListWidget {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 25px;
            font-family: 'Trebuchet MS';
            border: 2px solid #F5EA2F;
            border-radius: 15px;
            padding: 10px 10px;}
            
QLineEdit {background-color: rgba(0,0,0,100);
            color: white;
            font-size: 20px;
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
                            border-radius: 3px;}"""