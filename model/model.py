import copy

from database import meteo_dao
class Model:
    def __init__(self):
        self._sequenza_ottima = []
        self._costo_minimo = -1

        pass

    def handle_umidita_media(self, mese):
        meteoDAO = meteo_dao.MeteoDao()
        situations_list = meteoDAO.get_all_situazioni()
        sl_by_month = []
        for situation in situations_list:
            if situation.data.strftime("%m") == mese :
                sl_by_month.append(situation)


        u_genova = []
        u_milano = []
        u_torino = []
        for situation in sl_by_month:
            if situation.localita == "Genova":
                u_genova.append(situation.umidita)
            if situation.localita == "Milano":
                u_milano.append(situation.umidita)
            if situation.localita == "Torino":
                u_torino.append(situation.umidita)

        um_G = round((sum(u_genova) / len(u_genova)), 4)
        um_M = round((sum(u_milano) / len(u_milano)), 4)
        um_T = round((sum(u_torino) / len(u_torino)), 4)

        return um_G, um_M, um_T

    def opzione_verificata(self, parziale, opzione):
        if len(parziale) == 0:
            return True
        else:
            if opzione.localita == parziale[-1].localita:
                if sum(1 for p in parziale if p.localita == opzione.localita) > 5:
                    return False
                else:
                    return True

            else:
                if sum(1 for p in parziale if p.localita == opzione.localita) > 5:
                    return False

                elif len(parziale) < 3:
                    return False
                elif parziale[-1].localita == parziale[-2].localita == parziale[-3].localita:
                    return True
                else:
                    return False

    def calcola_costo(self, parziale, counter_go):
        num_spostamenti = counter_go
        tappe = parziale

        total_cost = num_spostamenti * 200
        for tappa in tappe:
            total_cost += tappa.umidita

        return total_cost

    def parziale_stringa(self, parziale, counter_go):
        output = []
        for p in parziale:
            output.append(p.localita)
        output.append(self.calcola_costo(parziale, counter_go))
        return output



    def recursive_sequenza(self, list, parziale, counter_go):
        if len(parziale) == 15:
            print(self.parziale_stringa(parziale, counter_go))
            costo = self.calcola_costo(parziale, counter_go)
            if costo < self._costo_minimo or self._costo_minimo == -1:
                self._costo_minimo = costo
                self._sequenza_ottima = copy.deepcopy(parziale)
        else:
            options = []
            for situation in sorted(list, key=lambda situation: situation.data):
                if int(situation.data.strftime("%d")) == len(parziale)+1:
                    options.append(situation)

            for opzione in options:
                if self.opzione_verificata(parziale, opzione):
                    if len(parziale) != 0 and opzione.localita != parziale[-1].localita:
                        counter_go += 1
                        parziale.append(opzione)
                        self.recursive_sequenza(list, parziale, counter_go)
                        parziale.pop()
                        counter_go -= 1
                    else:
                        parziale.append(opzione)
                        self.recursive_sequenza(list, parziale, counter_go)
                        parziale.pop()





    def handle_sequenza(self, mese):
        meteoDAO = meteo_dao.MeteoDao()
        situations_list = meteoDAO.get_all_situazioni()
        sl_by_month = []
        for situation in situations_list:
            if situation.data.strftime("%m") == mese and int(situation.data.strftime("%d")) <= 15:
                sl_by_month.append(situation)

        self.recursive_sequenza(sl_by_month, [], 0)

        tappe_str = []
        for tappa in self._sequenza_ottima:
            tappe_str.append(tappa.__str__())

        return self._costo_minimo, tappe_str




