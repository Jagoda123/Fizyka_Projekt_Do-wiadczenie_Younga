import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
print("Bieżący folder roboczy:", os.getcwd())
from ipywidgets import interact, IntSlider  

class EkranZeSzczelinami:
    def __init__(self, sciezka_obrazka):
        self.sciezka_obrazka = sciezka_obrazka
        self.ekran = self.wczytaj_ekran()

    def wczytaj_ekran(self):
        """obraz z paint -> macierz 2D, 1 = szczelina  0 = brak szczeliny"""
        try:
            obrazek = Image.open(self.sciezka_obrazka).convert("L")  
            ekran = np.array(obrazek) / 255  
            ekran = (ekran > 0.5).astype(int)  
            return ekran
        except FileNotFoundError:
            print(f"Błąd: Nie można znaleźć pliku '{self.sciezka_obrazka}'.")
            print(f"Bieżący folder roboczy: {os.getcwd()}")
            raise

    def pokaz_ekran(self):
        """Wyświetla ekran ze szczelinami"""
        plt.imshow(self.ekran, cmap='gray')
        plt.title("Ekran ze szczelinami")
        plt.colorbar()
        plt.show()
    
    def czy_sa_szczeliny(self):
        """czy na ekranie są szczeliny?"""
        return np.any(self.ekran == 1)

    def czy_ekran_jest_czarny(self):
        """czy ekran jest całkowicie czarny?"""
        return np.all(self.ekran == 0)


class Symulacja3D:
    def __init__(self, ekran_ze_szczelinami, A=1, k=2*np.pi):
        self.ekran_ze_szczelinami = ekran_ze_szczelinami
        self.A = A  
        self.k = k  

    def fala_kulista(self, x, y, z, x0, y0, z0):
        """Oblicza wartość fali kulistej w punkcie (x, y, z) pochodzącej od szczeliny w (x0, y0, z0)"""
        r = np.sqrt((x - x0)**2 + (y - y0)**2 + (z - z0)**2)
        return self.A / (r + 1e-10) * np.cos(self.k * r)  

    def oblicz_interferencje(self, ekran_obserwacyjny_z):
        """wzór interferencyjny na ekranie obserwacyjnym"""
        ekran = self.ekran_ze_szczelinami.ekran
        x, y = np.meshgrid(np.arange(ekran.shape[1]), np.arange(ekran.shape[0]))
        wzor = np.zeros_like(ekran, dtype=float)

        for i in range(ekran.shape[0]):
            for j in range(ekran.shape[1]):
                if ekran[i, j] == 1:  
                    wzor += self.fala_kulista(x, y, ekran_obserwacyjny_z, j, i, 0) 

        return wzor

    def pokaz_wzor_interferencyjny(self, wzor):
        plt.imshow(wzor, cmap='inferno')
        plt.title("Wzór interferencyjny 3D")
        plt.colorbar()
        plt.show()


def main():
    
    
    sciezka_obrazka = "S:\\sem3\\fizyka\\ekran7.png" 
    ekran_ze_szczelinami = EkranZeSzczelinami(sciezka_obrazka)
    ekran_ze_szczelinami.pokaz_ekran()

    if ekran_ze_szczelinami.czy_ekran_jest_czarny():
        print("Ekran jest całkowicie czarny (brak szczelin). Wyświetlam czarny ekran obserwacyjny.")
        plt.imshow(np.zeros_like(ekran_ze_szczelinami.ekran), cmap='gray', vmin=0, vmax=1)
        plt.title("Ekran obserwacyjny (brak światła)")
        plt.colorbar()
        plt.show()
        return

    symulacja = Symulacja3D(ekran_ze_szczelinami)

   
    def aktualizuj_wzor(odleglosc):
        wzor = symulacja.oblicz_interferencje(odleglosc)
        symulacja.pokaz_wzor_interferencyjny(wzor)

    interact(aktualizuj_wzor, odleglosc=IntSlider(min=10, max=500, step=10, value=100, description="Odległość (Z):"))


if __name__ == "__main__":
    main()