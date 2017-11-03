import os
import kivy

kivy.require('1.10.0')

from kivy.app import App
from functools import partial
from kivy.uix.label import Label
from kivy.base import runTouchApp
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.filechooser import FileChooserListView

def calculate(instance, file_chooser, ip_btn):
    if not file_chooser:
        return

    with open('proof', 'w') as f:
        for filepath in file_chooser.selection:
            f.write(filepath + '\n')
        f.write(ip_btn.text)

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        def redraw(self, args):
            self.bg_rect.size = self.size
            self.bg_rect.pos = self.pos

        with self.canvas:
            self.bg_rect = Rectangle(source="steel.jpg", pos=self.pos,
                                     size=self.size)
            self.bind(pos=redraw, size=redraw)

        root = BoxLayout(orientation='vertical', padding=[15],
                         spacing=15)
        
        # Add loading file with data
        gl = GridLayout(cols=2, size_hint=(1, 0.95),
                        size_hint_min=(100, 100), spacing=10)
        
        # Results section
        resl = BoxLayout(size_hint=(0.6, 0.98), size_hint_min=(100, 100),
                         orientation='vertical', spacing=15)
        
        # Graph
        graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                      x_ticks_major=25, y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=-0, xmax=100,
                      ymin=-1, ymax=1)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, x) for x in range(0, 101)]
        graph.add_plot(plot)
        
        resl.add_widget(graph)
        
        # Options section
        bl = BoxLayout(size_hint=(0.4, 0.98), size_hint_min=(100, 100),
                       orientation='vertical', spacing=15)
        
        bl.add_widget(Label(text='Wybierz plik danych',
                            size_hint=(1, 0.05),
                            size_hint_min=(200, 20)))
        files = FileChooserListView(size_hint=(1, 0.95),
                                    path=os.environ['HOMEDRIVE'] \
                                    + os.environ['HOMEPATH'])
        bl.add_widget(files)
        
        bl.add_widget(Label(text='Wybierz metodę interpolacji',
                            size_hint=(1, 0.05),
                            size_hint_min=(200, 30)))

        # Choosing interpolation method
        dd = DropDown()
        for interpolation in ['liniowa', 'wielomianowa']:
            btn = Button(text=interpolation, size_hint_y=None,
                         height=30)
            btn.bind(on_release=lambda btn: dd.select(btn.text))
            dd.add_widget(btn)

        dd_interpol_btn = Button(text='liniowa', size_hint=(1, 0.05),
                                 size_hint_min=(80, 30))
        dd_interpol_btn.bind(on_release=dd.open)
        dd.bind(on_select=lambda instance, x: setattr(dd_interpol_btn,
                                                      'text', x))

        bl.add_widget(dd_interpol_btn)
        
        # Add widgets to root layout
        root.add_widget(Label(text='Entalpy Calculator',
                              size_hint=(1, 0.05),
                              size_hint_min_y=20))
        gl.add_widget(Label(text='Wyniki', size_hint=(0.6, 0.02),
                            size_hint_min_y=20))
        gl.add_widget(Label(text='Opcje', size_hint=(0.4, 0.02),
                            size_hint_min_y=20))
        gl.add_widget(resl)
        gl.add_widget(bl)
        root.add_widget(gl)
        
        calculate_btn = Button(text='Oblicz', size_hint=(1, 0.05),
                               size_hint_min_y=30)
        calc_callback = partial(calculate, file_chooser=files,
                                ip_btn=dd_interpol_btn)
        calculate_btn.bind(on_release=calc_callback)
        root.add_widget(calculate_btn)
        
        self.add_widget(root)

class EntalpyApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    EntalpyApp().run()
