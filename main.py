from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.list.list import TwoLineRightIconListItem,TwoLineAvatarIconListItem
from kivymd.uix.button.button import MDFillRoundFlatButton,MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
#from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from datetime import datetime
from data import Base
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

Window.size = (350,650)
database = Base('data.db')

class ItemWidget(TwoLineAvatarIconListItem):
    delete_dialog = None
    info_dialog = None
    edit_dialog = None

                ## DELETE DIALOG

    def cancel(self,obj):
        self.delete_dialog.dismiss()        

    def delete(self,obj):
        self.parent.remove_widget(self)
        database.delete(self.text)
        self.delete_dialog.dismiss()

    def remove_dial(self):
        if not self.delete_dialog:
            self.delete_dialog = MDDialog(
                title="Remove reminder?",
                text='Are you sure?',
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        on_release=self.cancel
                    ),
                    MDFlatButton(
                        text="Delete",
                        on_release=self.delete
                    ),
                ],
            )
        self.delete_dialog.open()

           ## INFO DIALOG

    def info_dial(self):       
        if not self.info_dialog:
            self.info_dialog = MDDialog(
                title = 'Details',
                type="custom",
                auto_dismiss = False,
                content_cls=DetailsContent(),
                buttons = [MDFlatButton(
                        text="Close",
                        on_release=self.close
                    )],
            )
        self.info_dialog.content_cls.ids.detailsname.text = database.search(self.text)[0][1]
        self.info_dialog.open()

    def close(self,obj):
        self.info_dialog.dismiss()

                    ### EDIT DIALOG

    def edit_dial(self):
        value = database.search(self.text)
        if not self.edit_dialog:
            self.edit_dialog = MDDialog(
                title=f'Edit: {value[0][0]}',
                type='custom',
                auto_dismiss=False,
                content_cls=EditContent(),
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        on_release=self.exit
                    ),
                    MDFlatButton(
                        text="Save",
                        on_release=self.save
                    ),
                ],
            )
        self.edit_dialog.open()
        self.edit_dialog.content_cls.ids.edittext.text = value[0][1]
        self.edit_dialog.content_cls.ids.editdate.text = value[0][2]
        self.edit_dialog.content_cls.ids.edittime.text = value[0][3]

    def exit(self,obj):
        self.edit_dialog.dismiss()

    def save(self,obj):
        change_second_text = self.edit_dialog.content_cls.ids.edittext.text
        change_date = self.edit_dialog.content_cls.ids.editdate.text
        change_time = self.edit_dialog.content_cls.ids.edittime.text
        database.update(change_second_text,change_date,change_time,self.text)
        self.secondary_text = f'{change_date}  {change_time}'
        self.edit_dialog.dismiss()

class EditContent(MDFloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def show_date(self):
        self.date_dialog = MDDatePicker(width=self.width)
        self.date_dialog.bind(on_save=self.change_date)
        self.date_dialog.open()

    def change_date(self, instance, value, date_range):
        date = value.strftime('%d %b %Y')
        self.ids.editdate.text = date

    def show_time(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.change_time)
        time_dialog.open()

    def change_time(self, instance, time):
        self.ids.edittime.text = str(time.strftime('%H:%M'))
        

class DetailsContent(MDFloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)   

class Content(MDFloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.date.text = datetime.now().strftime('%d %b %Y')
        self.ids.time.text = datetime.now().strftime('%H:%M')


    def show_date_picker(self):
        self.date_dialog = MDDatePicker(width=self.width)
        self.date_dialog.bind(on_save=self.on_save)
        self.date_dialog.open()

    def on_save(self, instance, value, date_range):
        date = value.strftime('%d %b %Y')
        self.ids.date.text = date

    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def get_time(self, instance, time):
        self.ids.time.text = str(time.strftime('%H:%M'))


class MainApp(MDApp):
    dialog = None
    def build(self):
        return Builder.load_file('not.kv')
    
    def on_start(self):
        for note in database.view_all():
            app.root.ids.list.add_widget(ItemWidget(text = note[0],secondary_text=f'{note[2]}  {note[3]}'))

    
    def say(self,item):
        self.parent.remove_widget(item)

    def add_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Add a note!",
                type="custom",
                auto_dismiss = False,
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        on_release=self.cancel
                    ),
                    MDFlatButton(
                        text="Add",
                        on_release=self.add
                    ),
                ],
            )
        self.dialog.open() 

    def cancel(self,obj):
        self.dialog.dismiss() 
        self.dialog.content_cls.ids.title1.text = ''
        self.dialog.content_cls.ids.details1.text = ''

    def add(self,obj):
        first = self.dialog.content_cls.ids.title1.text
        second = self.dialog.content_cls.ids.date.text
        third = self.dialog.content_cls.ids.time.text
        second_text = self.dialog.content_cls.ids.details1.text
        check = database.exist(first.lower())
        if check[0][0] == 1:
            self.dialog.content_cls.ids.title1.error = True
            self.dialog.content_cls.ids.title1.helper_text= 'Already exists'
        else:
            app.root.ids.list.add_widget(ItemWidget(text=first,secondary_text= f'{third}  {second}'))
            database.add_entry(first.lower(),second_text.lower(),second,third)
            self.dialog.dismiss()
            self.dialog.content_cls.ids.title1.text = ''
            self.dialog.content_cls.ids.details1.text = ''
            self.dialog.content_cls.ids.title1.error = False

    
if __name__ == '__main__':
    app = MainApp()
    app.run()

