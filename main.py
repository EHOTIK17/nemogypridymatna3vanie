from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QTextEdit, QLineEdit, QHBoxLayout, QVBoxLayout, QInputDialog
import json

notes = {
    'Добро пожаловать!': {
        'текст': 'Это самое лучшше приложение для заметок в мире!',
        'теги': ['добро', 'инструкция']
    }
}

with open('notes_data.json', 'r') as file:
    notes = json.load(file)

def show_note():
    name = list_note.selectedItems()[0].text()
    print(name)
    text_note.setText(notes[name]['текст'])
    list_teg.clear()
    list_teg.addItems(notes[name]['теги'])

def add_note():
    notes_name, ok = QInputDialog.getText(main_win, 'Добавить заметку', 'Название заметки')
    if notes_name != '' and ok:
        notes[notes_name] = {
            'текст': '',
            'теги': []
        }
        list_teg.clear()
        list_note.addItem(notes_name)

def del_note():
    if list_note.selectedItems():
        name = list_note.selectedItems()[0].text()
        del notes[name]
        list_note.clear()
        text_note.clear()
        list_teg.clear()
        list_note.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)
        print(notes)
    else:
        print('Заметка для удаление не выбрана!')

def add_tag():
    if list_note.selectedItems():
        key = list_note.selectedItems()[0].text()
        tag = search_teg.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_teg.addItem(tag)
            search_teg.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)

def del_tag():
    if list_teg.selectedItems():
        name_note = list_note.selectedItems()[0].text()
        name_tag = list_teg.selectedItems()[0].text()
        notes[name_note]['теги'].remove(name_tag)
        list_teg.clear()
        list_teg.addItems(notes[name_note]['теги'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Искать заметки по тегу" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        button_tag_search.setText("Сбросить поиск")
        list_note.clear()
        list_tag.clear()
        list_note.addItems(notes_filtered)
    elif button_tag_search.text() == "Сбросить поиск":
        field_tag.clear()
        list_note.clear()
        list_tag.clear()
        list_note.addItems(notes)
        button_tag_search.setTex

def savee_note():
    if list_note.selectedItems():
        key = list_note.selectedItems()[0].text()
        notes[key]['текст'] = text_note.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)


app = QApplication([])
main_win = QWidget()

create_note = QPushButton('Создать заметку')
delete_note = QPushButton('Удалить заметку')
save_note = QPushButton('Сохранить заметку')
append_note = QPushButton('Добавить к заметке')
unpin_note = QPushButton('Открепить от задачи')
search_note = QPushButton('Искать заметки по тегу')

create_note.clicked.connect(add_note)
delete_note.clicked.connect(del_note)
save_note.clicked.connect(savee_note)
append_note.clicked.connect(add_tag)
unpin_note.clicked.connect(del_tag)

list_note = QListWidget()
list_teg = QListWidget()
text_note = QTextEdit()
search_teg = QLineEdit()

List_note = QLabel("Список заметок")
List_teg = QLabel('Список тегов')

layout_buttonH = QHBoxLayout()
layout_buttonH.addWidget(create_note)
layout_buttonH.addWidget(delete_note)

layout_buttonH2 = QHBoxLayout()
layout_buttonH2.addWidget(append_note)
layout_buttonH2.addWidget(unpin_note)

layout_buttonV = QVBoxLayout()
layout_buttonV.addWidget(List_note)
layout_buttonV.addWidget(list_note)
layout_buttonV.addLayout(layout_buttonH)
layout_buttonV.addWidget(save_note)
layout_buttonV.addWidget(List_teg)
layout_buttonV.addWidget(list_teg)
layout_buttonV.addWidget(search_teg)
layout_buttonV.addLayout(layout_buttonH2)
layout_buttonV.addWidget(search_note)

layout_main = QHBoxLayout()
layout_main.addWidget(text_note)
layout_main.addLayout(layout_buttonV)

list_note.itemClicked.connect(show_note)

list_note.addItems(notes)

#пасхалка

main_win.setLayout(layout_main)
main_win.show()
app.exec_()
