from kivy.clock import Clock
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp
from phue import Bridge

class LampControlApp(App):
    def build(self):
        self.bridge = Bridge('95.49.57.121')  # Zastąp tym adresem IP swoim adresem mostka

        # Zmiana koloru tła całego okna
        Window.clearcolor = (0.2, 0, 0, 1)  # Ciemnoczerwone tło

        layout = RelativeLayout()
        background = BackgroundWidget()  # Nowy widget do obsługi tła
        layout.add_widget(background)

        # Dodanie etykiety "loveSender" nad przyciskiem
        label_love_sender = Label(
            text="loveSender",
            color=(1, 1, 1, 1),
            font_size=dp(30),
            pos_hint={'center_x': 0.5, 'center_y': 0.9},  # Umiejscowienie na środku
            size_hint_y=None
        )
        layout.add_widget(label_love_sender)

        

        przycisk = RoundedButton(
            text="ZAWIADOM KAMIL",
            background_color=(0.8, 0, 0, 1),  # Jasnoczerwony kolor przycisku
            size_hint=(0.5, 0.1),  # Rozmiar przycisku
            pos_hint={'center_x': 0.5, 'center_y': 0.6}  # Umiejscowienie na środku
        )
        przycisk.bind(on_press=self.obsluz_klikniecie)
        layout.add_widget(przycisk)

        self.licznik_klikniec = 0
        self.label_licznik = Label(
            text=f"Liczba kliknięć: {self.licznik_klikniec}",
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.75},  # Umiejscowienie na środku
            size_hint_y=None
        )


        
        layout.add_widget(self.label_licznik)

        self.wczytaj_licznik()

        return layout

    def obsluz_klikniecie(self, instance):
        # Jeśli zmiana koloru trwa, nie wykonuj kolejnej akcji
        if not hasattr(self, 'last_click_time'):
            self.last_click_time = 0

        current_time = Clock.get_time()
        elapsed_time = current_time - self.last_click_time

        if elapsed_time > 2:
            self.last_click_time = current_time

            self.licznik_klikniec += 1
            self.label_licznik.text = f"Liczba kliknięć: {self.licznik_klikniec}"
            self.zapisz_licznik()

            self.bridge.set_light(1, 'on', True)
            self.bridge.set_light(1, 'hue', 0)
            self.bridge.set_light(1, 'sat', 254)

            self.timer_start()

    def timer_start(self):
        Clock.schedule_once(self.zakoncz_akcje, 2)

    def zakoncz_akcje(self, dt):
        self.bridge.set_light(1, 'on', False)

    def zapisz_licznik(self):
        with open("licznik.txt", "w") as file:
            file.write(str(self.licznik_klikniec))

    def wczytaj_licznik(self):
        try:
            with open("licznik.txt", "r") as file:
                self.licznik_klikniec = int(file.read())
                self.label_licznik.text = f"Liczba kliknięć: {self.licznik_klikniec}"
        except FileNotFoundError:
            pass

class BackgroundWidget(Label):
    def __init__(self, **kwargs):
        super(BackgroundWidget, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.2, 0, 0, 1)  # Ciemnoczerwone tło
            Rectangle(pos=self.pos, size=self.size)

    def on_size(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.2, 0, 0, 1)  # Ciemnoczerwone tło
            Rectangle(pos=self.pos, size=self.size)

class RoundedButton(Button):
    pass

if __name__ == "__main__":
    LampControlApp().run()
