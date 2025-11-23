import tkinter as tk
from tkinter import messagebox
from Adatmento_FÁ import AdatokSQL_FÁ
from datetime import datetime

class ParkingGUI_FÁ:
    def __init__(self, root):
        self.root = root
        self.root.title("Parkolóhely Nyilvántartó – app")
        self.root.geometry("900x500")
        AdatokSQL_FÁ.init_db()
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side="left", padx=20, pady=20)
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side="right", padx=20, pady=20, fill="y")
        self.selected_spot = None
        loaded = AdatokSQL_FÁ.load_all()
        self.spots = loaded if loaded else {}
        self.create_parking_buttons_FÁ()
        self.create_control_panel_FÁ()


    def create_parking_buttons_FÁ(self):
        row = 0
        col = 0

        for i in range(1, 11):
            spot_id = f"A{i}"

            if spot_id not in self.spots:
                self.spots[spot_id] = {"foglalt": "szabad", "rendszám": "","kezdes": ""}
                AdatokSQL_FÁ.save_spot(spot_id, "szabad", "","")

            foglalt_flag = self.spots[spot_id]["foglalt"] == "foglalt"

            button = tk.Button(
                self.left_frame,
                text=spot_id,
                width=10,
                height=3,
                bg="red" if foglalt_flag else "green",
                command=lambda s=spot_id: self.select_spot_FÁ(s)
            )
            button.grid(row=row, column=col, padx=10, pady=10)
            self.spots[spot_id]["button"] = button

            col += 1
            if col == 2:
                col = 0
                row += 1

    def select_spot_FÁ(self, spot_id):
        self.selected_spot = spot_id
        data = self.spots[spot_id]

        self.label_selected.config(text=f"Kiválasztott hely: {spot_id}")

        self.entry_plate.delete(0, tk.END)
        if data["foglalt"] == "foglalt":
            self.entry_plate.insert(0, data["rendszám"])

    # ----------------------------------------------------------
    def create_control_panel_FÁ(self):
        tk.Label(self.right_frame, text="Parkolóhely adatai", font=("Arial", 16)).pack(pady=10)

        self.label_selected = tk.Label(self.right_frame, text="Kiválasztott hely: -", font=("Arial", 12))
        self.label_selected.pack(pady=5)

        tk.Label(self.right_frame, text="Rendszám:").pack()
        self.entry_plate = tk.Entry(self.right_frame, width=20)
        self.entry_plate.pack(pady=5)

        self.btn_occupy = tk.Button(
            self.right_frame,
            text="PARKOLÁS",
            width=20,
            bg="#ffaa88",
            command=self.occupy_spot_FÁ
        )
        self.btn_occupy.pack(pady=10)

        self.btn_free = tk.Button(
            self.right_frame,
            text="TÁVOZÁS",
            width=20,
            bg="#aaddff",
            command=self.free_spot_FÁ
        )
        self.btn_free.pack(pady=10)

    def occupy_spot_FÁ(self):
        if not self.selected_spot:
            messagebox.showwarning("Figyelem", "Előbb válassz ki egy parkolóhelyet!")
            return

        data = self.spots[self.selected_spot]

        if data["foglalt"] == "foglalt":
            messagebox.showerror(
                "Hiba",
                "Ez a parkolóhely FOGLALT."
            )
            return

        plate = self.entry_plate.get().strip()
        if plate == "":
            messagebox.showwarning("Hiba", "Adj meg egy rendszámot!")
            return

        data["foglalt"] = "foglalt"
        data["rendszám"] = plate

        kezdes = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["kezdes"] = kezdes

        data["button"].config(bg="red")

        AdatokSQL_FÁ.save_spot(self.selected_spot, "foglalt", plate,kezdes)

        messagebox.showinfo(
            "Parkolás elindítva",
            f"A(z) {self.selected_spot} hely sikeresen lefoglalva!\n\n"
            f"Rendszám: {plate}\n"
            f"Kezdeti idő: {kezdes}"
        )

    def free_spot_FÁ(self):
        if not self.selected_spot:
            messagebox.showwarning("Figyelem", "Előbb válassz ki egy parkolóhelyet!")
            return

        data = self.spots[self.selected_spot]
        if data.get("kezdes", "") == "":
            messagebox.showwarning("Hiba", "Ez a hely jelenleg SZABAD, nincs mit felszabadítani.")
            return

        kezdes_str = data["kezdes"]
        kezdes = datetime.strptime(kezdes_str, "%Y-%m-%d %H:%M:%S")
        vege = datetime.now()
        vege_str = vege.strftime("%Y-%m-%d %H:%M:%S")

        eltelt = vege - kezdes
        eltelt_mp = eltelt.total_seconds()
        eltelt_ora = int(eltelt_mp / 3600)
        eltelt_perc = int((eltelt_mp % 3600) / 60)
        if eltelt_perc >  0:
            fizetendo = (eltelt_ora+1) * 500
        else:
            fizetendo = eltelt_ora*500

        fizeto_ablak = tk.Toplevel(self.root)
        fizeto_ablak.title("Fizetés")
        fizeto_ablak.geometry("350x300")

        tk.Label(fizeto_ablak, text=f"Parkolóhely: {self.selected_spot}", font=("Arial", 12)).pack(pady=5)
        tk.Label(fizeto_ablak, text=f"Rendszám: {data['rendszám']}", font=("Arial", 11)).pack(pady=5)
        tk.Label(fizeto_ablak, text=f"Kezdés: {kezdes_str}", font=("Arial", 11)).pack(pady=5)
        tk.Label(fizeto_ablak, text=f"Befejezés: {vege_str}", font=("Arial", 11)).pack(pady=5)

        tk.Label(fizeto_ablak, text=f"Eltelt idő: {eltelt_ora} óra {eltelt_perc} perc", font=("Arial", 11)).pack(pady=10)
        tk.Label(fizeto_ablak, text=f"Fizetendő összeg: {fizetendo} Ft", font=("Arial", 14, "bold")).pack(pady=10)

        def fizetes_gomb():
            data["foglalt"] = "szabad"
            data["rendszám"] = ""
            data["kezdes"] = ""

            data["button"].config(bg="green")
            self.entry_plate.delete(0, tk.END)

            AdatokSQL_FÁ.save_spot(self.selected_spot, "szabad", "", "")

            fizeto_ablak.destroy()

        tk.Button(fizeto_ablak, text="Fizetés",height=5, width=30, bg="#88ff88", command=fizetes_gomb).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingGUI_FÁ(root)
    root.mainloop()
