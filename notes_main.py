#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QGroupBox, QHBoxLayout, QWidget, QPushButton, QLabel, QRadioButton, QVBoxLayout, QListWidget, QTextEdit, QLineEdit, QInputDialog, QFormLayout
import json

app = QApplication([])

notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(900, 600)

list_notes = QListWidget()
list_notes_label = QLabel('Cписок заметок')

button_note_create = QPushButton('Создать заметку')
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')
field_text = QTextEdit()

button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать заметки по тегу')

list_tags = QListWidget()
list_tags_label = QLabel('Список тегов')

layout_notes = QHBoxLayout()
col1 = QVBoxLayout()
col1.addWidget(field_text)

col2 = QVBoxLayout()
col2.addWidget(list_notes_label)
col2.addWidget(list_notes)
row1 = QHBoxLayout()
row1.addWidget(button_note_create)
row1.addWidget(button_note_del)

row2 = QHBoxLayout()
row2.addWidget(button_note_save)

col2.addLayout(row1)
col2.addLayout(row2)

col2.addWidget(list_tags_label)
col2.addWidget(list_tags)
col2.addWidget(field_tag)

row3 = QHBoxLayout()
row3.addWidget(button_tag_add)
row3.addWidget(button_tag_del)

row4 = QHBoxLayout()
row4.addWidget(button_tag_search)

col2.addLayout(row3)
col2.addLayout(row4)

layout_notes.addLayout(col1, stretch = 2)
layout_notes.addLayout(col2, stretch = 1)

notes_win.setLayout(layout_notes)

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Добавить заметку', 'Название заметки:')
    if ok and note_name != '':
        note = list()
        note = [note_name, '', []]
        notes.append(note)
        list_notes.addItem(note[0])
        list_tags.addItems(note[2])
        print(notes)
        with open(str(len(notes)-1) + ".txt", "w") as file:
            file.write(note[0] + '\n')

def show_note():
    key = list_notes.selectedItems()[0].text( )
    print(key)
    for note in notes:
        if note[0] == key:
            field_text.setText(note[1])
            list_tags.clear()
            list_tags.addItems(note[2])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        index = 0
        for note in notes:
            if note[0] == key:
                note[1] = field_text.toPlainText()
                with open(str(index) + ".txt", "w") as file:
                    file.write(note[0] + '\n')
                    file.write(note[1] + '\n')
                    for tag in note[2]:
                        file.write( tag + '  ')
                    file.write('\n')
            index += 1
        print(notes)
    else:
        print('Заметка для сохранения не выбрана!')    

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_tag.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для удаления не собрана!')
def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open('notes_data.json', "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для добавления не собрана!')

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open('notes_data.json', "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Тег для удаления не выбран!')

def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == 'Искать заметку по тегу' and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note]=notes[note]
        button_tag_search.setText('Сбросить поиск')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems[notes]
        print(button_tag_search.text())
    elif button_tag_search.text() == 'Сбросить поиск':
        list_notes.clear()
        list_tags.clear()
        field_tag.clear()
        list_notes.addItems[notes]
        button_tag_search.setText('Искать заметку по тегу')
    else:
        pass

button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)
notes_win.show()

note = []
name = 0
notes = []


while True:
    filename = str(name) + ".txt"
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.replace('\n', '')
                note.append(line)
        tags = note[2].split(' ')
        note[2] = tags

        notes.append(note)
        note = []
        name += 1
    except IOError:
        break
print(notes)
for note in notes:
    list_notes.addItem(note[0])
    
app.exec()