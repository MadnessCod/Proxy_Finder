import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


def save_settings(database_name, user_name, password, host, port):
    settings_content = f"""
    DATABASE = {{
        'database_name': '{database_name}',
        'user_name': '{user_name}',
        'password': '{password}',
        'host': '{host}',
        'port': {port}
    }}
    """

    with open('local_settings.py', 'w') as f:
        f.write(settings_content)


class DatabaseSettingsForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.add_widget(Label(text='Database Name'))
        self.database_name = TextInput(multiline=False)
        self.add_widget(self.database_name)

        self.add_widget(Label(text='Username'))
        self.user_name = TextInput(multiline=False)
        self.add_widget(self.user_name)

        self.add_widget(Label(text='Password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        self.add_widget(Label(text='Port'))
        self.port = TextInput(text='5432', multiline=False)
        self.add_widget(self.port)

        self.submit = Button(text='Save Settings')
        self.submit.bind(on_press=self.save_settings)
        self.add_widget(self.submit)

    def save_settings(self, instance):
        database_name = self.database_name.text
        user_name = self.user_name.text
        password = self.password.text
        host = self.port.text
        port = self.port.text

        save_settings(database_name, user_name, password, host, port)


class DatabaseSettingsApp(App):
    def build(self):
        return DatabaseSettingsForm()


# if __name__ == '__main__':
#     DatabaseSettingsApp().run()
