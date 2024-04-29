import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        if self._mese == 0:
            self._view.create_alert("Seleziona mese")
        else:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("L'umidità media nel mese selzionato è:"))

            result = self._model.handle_umidita_media(self._mese)
            self._view.lst_result.controls.append(ft.Text(f"Genova {result[0]}"))
            self._view.lst_result.controls.append(ft.Text(f"Milano {result[1]}"))
            self._view.lst_result.controls.append(ft.Text(f"Torino {result[2]}"))

            self._view.update_page()


    def handle_sequenza(self, e):
        result_tuple = self._model.handle_sequenza(self._mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {result_tuple[0]} ed è:"))
        for situation_str in result_tuple[1]:
            self._view.lst_result.controls.append(ft.Text(situation_str))
        self._view.update_page()


    def read_mese(self, e):
        self._mese = e.control.value

