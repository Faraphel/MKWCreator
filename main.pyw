from tkinter import *
from tkinter import messagebox, filedialog, ttk
import os
import subprocess
import shutil
from threading import Thread
from PIL import Image, ImageTk, ImageDraw, ImageFont
import json

track2ID = {
    "Circuit Luigi (slot 1.1)": [0x75, 0x08],
    "Prairie Meuh Meuh (slot 1.2)": [0x77, 0x01],
    "Gorge Champignon (slot 1.3)": [0x79, 0x02],
    "Usine Toad (slot 1.4)": [0x7B, 0x04],

    "Circuit Mario (slot 2.1)": [0x7D, 0x00],
    "Supermarché Coco (slot 2.2)": [0x7F, 0x05],
    "Pic DK (slot 2.3)": [0x81, 0x06],
    "Mine Wario (slot 2.4)": [0x83, 0x07],

    "Circuit Daisy (slot 3.1)": [0x87, 0x09],
    "Cap Koopa (slot 3.2)": [0x85, 0x0F],
    "Bois Vermeil (slot 3.3)": [0x8F, 0x0B],
    "Volcan Grondant (slot 3.4)": [0x8B, 0x03],

    "Ruines Sec Sec (slot 4.1)": [0x89, 0x0E],
    "Route Clair de Lune (slot 4.2)": [0x8D, 0x0A],
    "Château de Bowser (slot 4.3)": [0x91, 0x0C],
    "Route Arc-en-Ciel (slot 4.4)": [0x93, 0x0D],

    "GCN Plage Peach (slot 5.1)": [0xA5, 0x10],
    "DS Cascades Yoshi (slot 5.2)": [0xAD, 0x14],
    "SNES Vallée Fantôme 2 (slot 5.3)": [0x97, 0x19],
    "N64 Autodrome Mario (slot 5.4)": [0x9F, 0x1A],

    "N64 Royaume Sorbet (slot 6.1)": [0x9D, 0x1B],
    "GBA Plage Maskass (slot 6.2)": [0x95, 0x1F],
    "DS Quartier Delfino (slot 6.3)": [0xAF, 0x17],
    "GCN Stade Waluigi (slot 6.4)": [0xA9, 0x12],

    "DS Désert du Soleil (slot 7.1)": [0xB1, 0x15],
    "GBA Château de Bowser 3 (slot 7.2)":[0x9B, 0x1E],
    "N64 Jungle DK (slot 7.3)": [0xA1, 0x1D],
    "GCN Circuit Mario (slot 7.4)": [0xA7, 0x11],

    "SNES Circuit Mario 3 (slot 8.1)": [0x99, 0x18],
    "DS Jardin Peach (slot 8.2)": [0xB3, 0x16],
    "GCN Montagne DK (slot 8.3)": [0xAB, 0x13],
    "N64 Château de Bowser (slot 8.4)": [0xA3, 0x1C],

    "Block Plaza (battle slot 1.1)": [0xB7, 0x21],
    "Quai Delfino (battle slot 1.2)": [0xB5, 0x20],
    "Stade de Funky Kong (battle slot 1.3)": [0xB9, 0x23],
    "Roulette Chomp (battle slot 1.4)": [0xBB, 0x22],
    "Désert Thwomp (battle slot 1.5)": [0xBD, 0x24],

    "SNES Circuit de Bataille 4 (battle slot 2.1)": [0xC3, 0x27],
    "GBA Circuit de Bataille 3 (battle slot 2.2)": [0xC5, 0x28],
    "N64 Gratte-ciel (battle slot 2.3)": [0xC7, 0x29],
    "GCN Cookie Arena (battle slot 2.4)": [0xBF, 0x25],
    "DS Maison de l'Aube (battle slot 2.5)": [0xC1, 0x26],

    "Colisée Galactique": [0xC9, 0x36],
}

class main():
    def __init__(self):
        self.root = Tk()
        self.root.title("MKWii Creator")
        self.root.resizable(False, False)

        self.frame_SelectGameFile = LabelFrame(self.root, text="Fichier du jeu")
        self.frame_SelectGameFile.grid(row=1, column=1)
        Label(self.frame_SelectGameFile, text="Sélectionné la ROM (.iso, .wbfs, main.dol de votre MKWii)").grid(row=1, column=1, columnspan=2, sticky="NEWS")
        self.entry_SelectGameFile = Entry(self.frame_SelectGameFile, width = 50)
        self.entry_SelectGameFile.grid(row=2, column=1, sticky="NEWS")
        self.button_SelectGameFile = Button(self.frame_SelectGameFile, text="...", relief=RIDGE, command=self.ask_game_file)
        self.button_SelectGameFile.grid(row=2, column=2, sticky="NEWS")
        self.button_ConfirmSelectGameFile = Button(self.frame_SelectGameFile, text="Utiliser comme dossier de jeu", relief=RIDGE, command=self.select_game_file)
        self.button_ConfirmSelectGameFile.grid(row=3, column=1, columnspan=2, sticky="NEWS")

        self.frame_ActionGameFile = LabelFrame(self.root, text="Action")
        self.label_GameInformation = Label(self.frame_ActionGameFile, text="")
        self.label_GameInformation.grid(row=1, column=1)
        self.button_ExtractROM = Button(self.frame_ActionGameFile, text="Extraire le jeu", relief=RIDGE, command=self.extract_game)
        self.button_InstallLECODE = Button(self.frame_ActionGameFile, text="Installer LE-CODE", relief=RIDGE, command=self.install_lecode)

        self.frame_ActionGameEditROM = Frame(self.frame_ActionGameFile)
        self.button_ImportROM = Button(self.frame_ActionGameEditROM, text="Importer un pack de courses", relief=RIDGE, command=self.import_track_pack)
        self.button_ImportROM.grid(row=1,column=1, sticky="NEWS")
        self.button_ExportROM = Button(self.frame_ActionGameEditROM, text="Exporter un pack de courses", relief=RIDGE, command=self.export_track_pack)
        self.button_ExportROM.grid(row=2,column=1, sticky="NEWS")
        self.button_ImportMultipleRace = Button(self.frame_ActionGameEditROM, text="Importer plusieurs courses", relief=RIDGE, command=self.import_multiple_race)
        self.button_ImportMultipleRace.grid(row=3,column=1, sticky="NEWS")
        self.button_PatchROM = Button(self.frame_ActionGameEditROM, text="Patcher le jeu", relief=RIDGE, command=self.patch_game)
        self.button_PatchROM.grid(row=4, column=1, sticky="NEWS")
        self.progressbar_Action = ttk.Progressbar(self.frame_ActionGameFile)
        self.label_Action = Label(self.frame_ActionGameFile)


        self.frame_CupManager = LabelFrame(self.root, text="Coupe")
        self.cup_offset = 0
        Label(self.frame_CupManager, text="Choississez la coupe à modifier :").grid(row=1, column=1, columnspan=10)
        self.button_CupManagerLeft = Button(self.frame_CupManager, width=2, text="<", command=self.cup_left, relief=RIDGE)
        self.button_CupManagerLeft.grid(row=2, column=1, rowspan=2, sticky="NEWS")

        self.button_CupManager = []
        self.button_CupManagerImg = {}
        for x in range(4):
            for y in range(2):
                self.button_CupManager.append(Button(self.frame_CupManager, width=64, height=64, bg="black"))
                self.button_CupManager[-1].grid(row=y+2, column=x+2)

        self.button_CupManagerRight = Button(self.frame_CupManager, width=2, text=">", command=self.cup_right, relief=RIDGE)
        self.button_CupManagerRight.grid(row=2, column=6, rowspan=2, sticky="NEWS")

        self.frame_CupNameManager = Frame(self.frame_CupManager)
        Label(self.frame_CupNameManager, text="Choississez le nom de la coupe :").grid(row=1, column=1, columnspan=2)
        self.entry_CupNameManager = Entry(self.frame_CupNameManager, width=40)
        self.entry_CupNameManager.grid(row=2, column=1, sticky="NEWS")
        self.button_CupNameManager = Button(self.frame_CupNameManager, text="Sauver", width=10, relief=RIDGE)
        self.button_CupNameManager.grid(row=2, column=2, sticky="NEWS")

        self.frame_CupIconManager = Frame(self.frame_CupManager)
        Label(self.frame_CupIconManager, text="Choississez l'icone de la coupe :").grid(row=1, column=1)
        self.button_CupIconManager = Button(self.frame_CupIconManager, width=128, height=128, bg="black")
        self.button_CupIconManager.grid(row=2, column=1)

        self.frame_RaceManager = LabelFrame(self.frame_CupManager, text="Course")
        Label(self.frame_RaceManager, text="Choississez la course à modifier :").grid(row=1, column=1, columnspan=10)

        self.button_RaceManager = []
        for x in range(4):
            self.button_RaceManager.append(Button(self.frame_RaceManager, width=45))
            self.button_RaceManager[x].grid(row=x+2, column=1, sticky="NEWS")

        self.button_DeleteCupManager = Button(self.frame_CupManager, text="Supprimer", fg="red", relief=RIDGE)

        self._add_img_raw = Image.open(f"./assets/add.png")
        self._add_img = ImageTk.PhotoImage(self._add_img_raw.resize((64, 64)))


    def ask_game_file(self):
        path = filedialog.askopenfilename(filetypes = (("Jeu Wii", r"*.iso *.wbfs main.dol"),))
        if path:
            self.entry_SelectGameFile.delete(0, END)
            self.entry_SelectGameFile.insert(END, path)


    def select_game_file(self):
        self.path = self.entry_SelectGameFile.get()
        self.file_type = None
        if os.path.exists(self.path):
            _, extension = os.path.splitext(self.path)
            if extension.upper() == ".WBFS": self.file_type = "wbfs"
            elif extension.upper() == ".ISO": self.file_type = "iso"
            elif extension.upper() == ".DOL":
                self.file_type = "dol"
                self.path = self.path[:-len("/sys/main.dol")]
            else:
                messagebox.showerror("Erreur", "Ce format de fichier n'est pas supporté.")
                return

        else:
            messagebox.showerror("Erreur", "Le fichier entré n'existe pas.")
            return

        self.refresh_action_frame()


    def refresh_action_frame(self):
        self.label_GameInformation.config(text = f"chemin du jeu : {self.path}\ntype : {self.file_type}")
        self.frame_ActionGameFile.grid(row=2, column=1, sticky = "NEWS")

        if self.file_type in ["wbfs", "iso"]:
            self.button_ExtractROM.grid(row=2,column=1,sticky="NEWS")
            self.button_InstallLECODE.grid_forget()
            self.frame_ActionGameEditROM.grid_forget()

        else:
            self.button_ExtractROM.grid_forget()
            if os.path.exists(f"{self.path}/files/.MKCreator/"):
                self.button_InstallLECODE.grid_forget()
                self.frame_ActionGameEditROM.grid(row=4,column=1,sticky="NEWS")
                self.edit_game()

            else:
                self.button_InstallLECODE.grid(row=3,column=1,sticky="NEWS")
                self.frame_ActionGameEditROM.grid_forget()


    def extract_game(self):
        def main():
            dir = filedialog.askdirectory()
            if dir:
                self.progressbar_Action.grid(row = 100, column = 1, sticky = "NEWS")
                self.label_Action.grid(row = 101, column = 1, sticky = "NEWS")
                self.label_Action.config(text = "Extraction du jeu en cours...")
                self.button_ExtractROM.grid_forget()

                self.progressbar_Action.config(mode="indeterminate")
                self.progressbar_Action.start(50)

                p = subprocess.Popen(f"wit EXTRACT \"{self.path}\" \"{dir}\" --overwrite", shell=True)
                p.wait()

                self.progressbar_Action.grid_forget()
                self.label_Action.grid_forget()
                self.path = dir
                self.file_type = "dol"
                self.refresh_action_frame()

        Thread(target=main).start()


    def install_lecode(self):
        def main():
            # visuel
            self.progressbar_Action.grid(row = 100, column = 1, sticky = "NEWS")
            self.progressbar_Action.config(mode = "determinate")
            self.label_Action.grid(row = 101, column = 1, sticky = "NEWS")
            self.progressbar_Action.stop()
            self.progressbar_Action['maximum'] = 57
            self.progressbar_Action["value"] = 0
            self.button_InstallLECODE.grid_forget()

            # commande de patch
            self.label_Action.config(text="Modification de main.dol...")
            self.progressbar_Action.step(1)
            p = subprocess.Popen(f"wstrt patch \"{self.path}/sys/main.dol\" --clean-dol --add-lecode", shell=True)
            p.wait()

            # patch des menus
            for file in ["Award", "Channel", "Event", "Globe", "MenuMulti", "MenuOther", "MenuSingle", "Present", "Race", "Title"]:
                self.label_Action.config(text=f"Extraction du fichier {file}.szs...")
                self.progressbar_Action.step(1)
                p = subprocess.Popen(f"wszst EXTRACT \"{self.path}/files/Scene/UI/{file}.szs\" --DEST \"./.tmp/{file}\"")
                p.wait()

                replace_path = {
                    f"./.tmp/{file}/button/blyt/cup_icon_64x64_common.brlyt": "cup_icon_64x64_common.brlyt",
                    f"./.tmp/{file}/button/ctrl/Back.brctr": "Back.brctr",
                    f"./.tmp/{file}/button/ctrl/CupSelectCup.brctr": "CupSelectCup.brctr",
                    f"./.tmp/{file}/control/blyt/cup_icon_64x64_common.brlyt": "cup_icon_64x64_common.brlyt",
                    f"./.tmp/{file}/control/ctrl/CourseSelectCup.brctr": "CourseSelectCup.brctr",
                    f"./.tmp/{file}/demo/blyt/course_name.brlyt": "course_name.brlyt",
                    f"./.tmp/{file}/demo/timg/tt_hatena_64x64.tpl": "tt_hatena_64x64.tpl"
                }

                for subfile in replace_path:
                    self.label_Action.config(text=f"Remplacement des fichiers de {file}.szs ({subfile})...")
                    if os.path.exists(subfile): shutil.copy(f"./assets/{replace_path[subfile]}", subfile)

                if file in ["Channel", "MenuMulti", "MenuSingle"]:
                    self.label_Action.config(text=f"Remplacement des icones de {file}.szs...")
                    self.progressbar_Action.step(1)
                    shutil.copy(f"./assets/ct_icons-default.tpl", f"./.tmp/{file}/button/timg/ct_icons.tpl")
                    shutil.copy(f"./assets/ct_icons-default.tpl", f"./.tmp/{file}/control/timg/ct_icons.tpl")

                    # patch des fichiers de langage des menus
                    for language in "EFGIS":
                        self.label_Action.config(text=f"Remplacement des fichiers langues de {file}_{language}.szs...")
                        self.progressbar_Action.step(1)
                        szs_path = f"{self.path}/files/Scene/UI/{file}_{language}.szs"
                        tmp_path = f"./.tmp/{file}_{language}"
                        if os.path.exists(szs_path):
                            p = subprocess.Popen(f"wszst EXTRACT \"{szs_path}\" --DEST \"{tmp_path}\"")
                            p.wait()
                            if os.path.exists(f"{tmp_path}/message/Common.bmg"):
                                p = subprocess.Popen(f"wbmgt decode \"{tmp_path}/message/Common.bmg\" --overwrite")
                                p.wait()
                                p = subprocess.Popen(
                                    f"wbmgt encode \"{tmp_path}/message/Common.txt\" --overwrite --le-code")
                                p.wait()
                                os.remove(f"{tmp_path}/message/Common.txt")

                        self.label_Action.config(text=f"Finalisation de {file}_{language}.szs...")
                        self.progressbar_Action.step(1)
                        p = subprocess.Popen(f"wszst CREATE \"{tmp_path}\" --DEST \"{szs_path}\" --overwrite")
                        p.wait()

                        shutil.rmtree(tmp_path)


                self.label_Action.config(text=f"Finalisation de {file}.szs...")
                self.progressbar_Action.step(1)
                p = subprocess.Popen(f"wszst CREATE \"./.tmp/{file}\" --DEST \"{self.path}/files/Scene/UI/{file}.szs\" --overwrite")
                p.wait()

                shutil.rmtree(f"./.tmp/{file}")


            # patch des vidéos de présentation
            for file in ["banana", "cup_select", "flower", "kinoko", "konoha", "koura", "special", "star", "thunder"]:
                self.label_Action.config(text=f"Patch du fichier vidéo {file}...")
                shutil.copy("./assets/video.thp", f"{self.path}/files/thp/course/{file}.thp")

            # correction des courses
            if not(os.path.exists(f"{self.path}/files/.MKCreator/Track/")): os.makedirs(f"{self.path}/files/.MKCreator/Track/")
            if not(os.path.exists(f"{self.path}/files/.MKCreator/Track-Original/")): os.makedirs(f"{self.path}/files/.MKCreator/Track-Original/")
            if not (os.path.exists(f"{self.path}/files/.MKCreator/auto-add/")): os.makedirs(f"{self.path}/files/.MKCreator/auto-add/")

            for file in os.listdir(f"{self.path}/files/Race/Course/"):
                if os.path.isfile(f"{self.path}/files/Race/Course/{file}"):
                    _, extension = os.path.splitext(file)
                    if extension == ".szs":
                        self.label_Action.config(text=f"Correction de la course {file}...")
                        shutil.move(f"{self.path}/files/Race/Course/{file}", f"{self.path}/files/.MKCreator/Track-Original/{file}")

            # application du patch
            self.label_Action.config(text=f"Patch de LE-CODE.bin")
            p = subprocess.Popen(f"wlect patch ./assets/lecode-PAL.bin -od \"{self.path}/files/rel/lecode-PAL.bin\" --track-dir "+\
                                 f"\"{self.path}/files/Race/Course\" --copy-tracks \"{self.path}/files/.MKCreator/Track-Original/\" --le-define "+\
                                 f"./assets/CTFILE-default.txt --lpar ./assets/lpar-default.txt --overwrite")
            p.wait()

            # création des fichiers nécéssaires pour l'application
            if not(os.path.exists(f"{self.path}/files/.MKCreator")): os.makedirs(f"{self.path}/files/.MKCreator")
            shutil.copytree("./assets/cup_icon/", f"{self.path}/files/.MKCreator/cup_icon/")
            shutil.copy("./assets/config-fr.json", f"{self.path}/files/.MKCreator/config.json")


            self.label_Action.config(text=f"Création du dossier auto-add...")
            self.progressbar_Action.step(1)
            p = subprocess.Popen(f"wszst autoadd -q \"{self.path}/files/.MKCreator/Track-Original/\" --dest " + \
                                 f"\"{self.path}/files/.MKCreator/auto-add/\" --remove-dest --preserve")
            p.wait()

            self.progressbar_Action.grid_forget()
            self.label_Action.grid_forget()
            self.refresh_action_frame()

        Thread(target=main).start()


    def edit_game(self):
        self.frame_CupManager.grid(row=1, column=2, rowspan=2, sticky="NEWS")
        with open(f"{self.path}/files/.MKCreator/config.json", "rb") as file:
            self.config = json.load(file)
        self.refresh_cup_menu()


    def refresh_cup_menu(self):
        for x in range(4):
            for y in range(2):
                pos_index = (x * 2) + y
                index = pos_index + (self.cup_offset * 2)

                if str(index) in self.config["cup"]:
                    self.button_CupManagerImg[index] = ImageTk.PhotoImage(Image.open(f"{self.path}/files/.MKCreator/cup_icon/{index}.png").resize((64,64)))
                    self.button_CupManager[pos_index].config(image=self.button_CupManagerImg[index], command=lambda i=index:self.select_cup(i), bg="black")

                else:
                    self.button_CupManager[pos_index].config(image=self._add_img, bg="gray", command=self.create_new_cup)
                    self.button_CupManager[pos_index].grid(row=y+2, column=x+2)


    def cup_left(self):
        if self.cup_offset > 0:
            self.cup_offset -=1
            self.refresh_cup_menu()


    def cup_right(self):
        if self.cup_offset < (len(self.config["cup"]) // 2 - 3):
            self.cup_offset +=1
            self.refresh_cup_menu()


    def select_cup(self, index):
        self.frame_CupNameManager.grid(row=10, column=1, columnspan=10)
        self.frame_CupIconManager.grid(row=20, column=1, columnspan=10)
        self.frame_RaceManager.grid(row=100, column=1, columnspan=6, sticky="NEWS")
        self.button_DeleteCupManager.grid(row=101,column=1,columnspan=10, sticky="W")

        _cup_config = self.config["cup"][str(index)]

        self.entry_CupNameManager.config(state=NORMAL)
        self.entry_CupNameManager.delete(0, END)
        self.entry_CupNameManager.insert(0, _cup_config["name"])

        self.button_CupNameManager.config(command=lambda i=index:self.change_cup_name(i))
        self.button_DeleteCupManager.config(command=lambda i=index:self.delete_cup(i))

        self._selected_cup_img = ImageTk.PhotoImage(Image.open(f"{self.path}/files/.MKCreator/cup_icon/{index}.png"))
        self.button_CupIconManager.config(image=self._selected_cup_img, command=lambda i=index:self.select_new_cup_icon(i))

        if _cup_config["locked"]:
            self.entry_CupNameManager.config(state=DISABLED)
            self.button_CupIconManager.config(state=DISABLED)
            self.button_DeleteCupManager.config(state=DISABLED)
            self.button_CupNameManager.config(state=DISABLED)
        else:
            self.button_CupIconManager.config(state=NORMAL)
            self.button_DeleteCupManager.config(state=NORMAL)
            self.button_CupNameManager.config(state=NORMAL)

        for x in range(4):
            self.button_RaceManager[x].config(text=_cup_config["courses"][str(x)]["name"], command=lambda t=index,r=x:self.edit_track(t,r))
            if _cup_config["locked"]: self.button_RaceManager[x].config(state=DISABLED)
            else: self.button_RaceManager[x].config(state=NORMAL)


    def create_new_cup(self):
        tl = Toplevel()
        tl.title("Nouvelle Coupe")
        tl.resizable(False, False)

        cup_id = len(self.config["cup"])
        new_icon = self.generate_cup_icon(cup_id - 8)
        new_icon_tk = ImageTk.PhotoImage(new_icon)

        def select_icon():
            nonlocal new_icon, new_icon_tk
            path = filedialog.askopenfilename(filetypes = (("Icone coupe", r"*.png"),))
            tl.focus_force()
            if path:
                if os.path.exists(path):
                    new_icon = Image.open(path).resize((128,128))
                    new_icon_tk = ImageTk.PhotoImage(new_icon.resize((64,64)))
                    button_NewCupIcon.config(image=new_icon_tk)

        Label(tl, text="Choississez un nom pour votre coupe :").grid(row=1, column=1)
        entry_NewCupName = Entry(tl)
        entry_NewCupName.grid(row=2,column=1,sticky="NEWS")
        Label(tl, text="Choississez une icone pour votre coupe :").grid(row=3, column=1)
        button_NewCupIcon = Button(tl, image=new_icon_tk, command=select_icon)
        button_NewCupIcon.grid(row=4, column=1)

        def confirm():
            nonlocal new_icon, cup_id
            cup_name = entry_NewCupName.get()
            if cup_name.replace(" ", "") != "":

                self.new_cup(cup_id, new_icon, cup_name)

                self.refresh_cup_menu()
                tl.destroy()
                self.root.focus_force()

            else:
                messagebox.showerror("Erreur", "Veuillez choisir un nom pour votre coupe.")

        Button(tl, text="Confirmer", relief=RIDGE, command = confirm).grid(row=5, column=1, sticky="E")


    def select_new_cup_icon(self, index):
        path = filedialog.askopenfilename(filetypes = (("Icone coupe", r"*.png"),))
        if path:
            if os.path.exists(path):
                _cup_img = Image.open(path).resize((128,128))
                _cup_img.save(f"{self.path}/files/.MKCreator/cup_icon/{index}.png")
                self._selected_cup_img = ImageTk.PhotoImage(_cup_img)
                self.button_CupIconManager.config(image=self._selected_cup_img)
                self.refresh_cup_menu()
            else:
                messagebox.showerror("Erreur", "Ce fichier n'existe pas.")


    def change_cup_name(self, index):
        self.config["cup"][str(index)]["name"] = self.entry_CupNameManager.get()
        self.save_config()


    def delete_cup(self, index):
        ans = messagebox.askyesno("Confirmer", f"Voulez-vous vraiment supprimer la coupe {self.config['cup'][str(index)]['name']} ?")
        if ans:
            total_cup = len(self.config["cup"])
            os.remove(f"{self.path}/files/.MKCreator/cup_icon/{index}.png")
            self.config["cup"].pop(str(index))

            for i in range(index+1, total_cup):
                self.config["cup"][str(i-1)] = self.config["cup"].pop(str(i))

                os.rename(f"{self.path}/files/.MKCreator/cup_icon/{i}.png", f"{self.path}/files/.MKCreator/cup_icon/{i-1}.png")

            self.save_config()
            self.refresh_cup_menu()


    def edit_track(self, cup_index, course_index):
        tl = Toplevel()
        tl.title("Modifier la course")
        tl.resizable(False, False)

        def select_file():
            path = filedialog.askopenfilename(filetypes = (("Fichier course", r"*.szs *.wbz"),))
            tl.focus_force()
            if path:
                if os.path.exists(path):
                    name = self.get_track_name(path)
                    Property = path[path.find("[")+1:path.rfind("]")]
                    try:
                        r = Property.find("r")
                        if r != -1:
                            Type = Property[r+1:r+3]
                            Type = ((int(Type[0]) - 1) * 4) + (int(Type[1]) - 1)
                            listbox_MusicType.current(Type)
                            listbox_TrackType.current(Type)
                    except: pass

                    entry_CoursePath.delete(0, END)
                    entry_CoursePath.insert(0, path)
                    entry_CourseName.delete(0, END)
                    entry_CourseName.insert(0, name)
                else:
                    messagebox.showerror("Erreur", "Ce fichier n'existe pas.")

        Label(tl, text="Fichier du jeu :").grid(row=1, column=1)
        entry_CoursePath = Entry(tl, width=40)
        entry_CoursePath.grid(row=2, column=1, sticky="NEWS")
        Button(tl, text="...", relief=RIDGE, command=select_file).grid(row=2, column=2, sticky="NEWS")

        Label(tl, text="Nom de la course :").grid(row=3, column=1, columnspan=2)
        entry_CourseName = Entry(tl, width=50)
        entry_CourseName.grid(row=4, column=1, sticky="NEWS", columnspan=2)

        Label(tl, text="Musique de la course :").grid(row=5, column=1, columnspan=2)
        listbox_MusicType = ttk.Combobox(tl, width=50, values=list(track2ID.keys()))
        listbox_MusicType.current(0)
        listbox_MusicType.grid(row=6, column=1, sticky="NEWS", columnspan=2)

        Label(tl, text="Type de la course :\n(généralement indiqué par son créateur)\n(si non spécifié, choisir slot 1.1)").grid(row=7, column=1, columnspan=2)
        listbox_TrackType = ttk.Combobox(tl, width=50, values=list(track2ID.keys()))
        listbox_TrackType.current(0)
        listbox_TrackType.grid(row=8, column=1, sticky="NEWS", columnspan=2)

        Bool_isTrackNew = BooleanVar(value=True)
        checkbutton_TrackNew = Checkbutton(tl, text="Marqué comme étant nouveau", variable=Bool_isTrackNew)
        checkbutton_TrackNew.grid(row=9, column=1, columnspan=2)

        def confirm():
            if self.new_track(entry_CoursePath.get(),
                              entry_CourseName.get(),
                              cup_index,
                              course_index,
                              Bool_isTrackNew.get(),
                              listbox_MusicType.get(),
                              listbox_TrackType.get()):

                tl.destroy()
                self.root.focus_force()


        Button(tl, text="Confirmer", command=confirm, relief=RIDGE).grid(row=10,column=1, columnspan=2, sticky="E")


    def get_track_name(self, path):
        return path.split("/")[-1].replace("_", " ").replace(".szs", "").replace(".wbz", "").split("(")[0].split("[")[0]


    def patch_game(self):
        def main():
            self.progressbar_Action.grid(row = 100, column = 1, sticky = "NEWS")
            self.label_Action.grid(row = 101, column = 1)
            self.label_Action.config(text=f"Préparation...")
            self.frame_ActionGameEditROM.grid_forget()
            self.progressbar_Action.config(mode = "determinate")
            self.progressbar_Action.stop()
            self.progressbar_Action['maximum'] = 31
            self.progressbar_Action["value"] = 0

            LE_CODE = ""
            TEXT_DATA = [
                {"slot": "703e", "name": "Aléatoire: Toutes les pistes"},
                {"slot": "703f", "name": "Aléatoire: Pistes Originales"},
                {"slot": "7040", "name": "Aléatoire: Custom Tracks"},
                {"slot": "7041", "name": "Aléatoire: Pistes Nouvelles"},
            ]
            text_index = 0
            total_cup = len(self.config["cup"])
            ct_icon = Image.new("RGBA", (128, 128*(total_cup+2)))
            base = Image.open("./assets/ct_icons-base.png")
            ct_icon.paste(base, (0, 0))

            for cup in self.config["cup"]:
                self.label_Action.config(text=f"Configuration de la coupe {cup}...")
                self.progressbar_Action.step(1)
                cup_icon = Image.open(f"{self.path}/files/.MKCreator/cup_icon/{cup}.png")
                ct_icon.paste(cup_icon, (0, (int(cup)+2)*128))

                if not(cup in ["0","1","2","3","4","5","6","7","8"]):
                    _cup_config = self.config["cup"][cup]
                    LE_CODE += f"\n\nC \"{_cup_config['name']}\""

                    for course in _cup_config["courses"]:
                        _course_config = _cup_config["courses"][course]
                        self.label_Action.config(text=f"Configuration de la course {_course_config['name']} (coupe {cup})...")
                        self.progressbar_Action.step(1)

                        flag = "0x00"
                        if _course_config["new"]: flag = "0x01"

                        LE_CODE += f"\nT {_course_config['music']};"+\
                                   f" {hex(_course_config['special'])};"+\
                                   f" {flag};"+\
                                   f" \"{_course_config['name']}\";"+\
                                   f" \"{_course_config['name']}\";"+\
                                   f" \"\""

                        TEXT_DATA.append({"slot": format(0x7044 + text_index, '02x'), "name": _course_config['name']})
                        text_index += 1

                        if _course_config["name"] == "/":
                            messagebox.showerror("Erreur", f"Une course semble ne pas avoir été configuré "+\
                                                 f"dans la coupe {_cup_config['name']} (slot {course})")

                            self.progressbar_Action.grid_forget()
                            self.label_Action.grid_forget()
                            return


            self.label_Action.config(text=f"Création du fichier CTFILE.txt...")
            self.progressbar_Action.step(1)
            shutil.copy("./assets/CTFILE-default.txt", f"{self.path}/files/.MKCreator/CTFILE.txt")
            with open(f"{self.path}/files/.MKCreator/CTFILE.txt", "a") as CTFile:
                CTFile.write(LE_CODE)


            self.label_Action.config(text=f"Configuration des icones...")
            self.progressbar_Action.step(1)
            ct_icon.save(f"{self.path}/files/.MKCreator/ct_icons.png")
            p = subprocess.Popen(f"wimgt encode \"{self.path}/files/.MKCreator/ct_icons.png\" "+\
                                 f"--DEST \"{self.path}/files/.MKCreator/ct_icons.tpl\" -x tpl.CMPR --overwrite")
            p.wait()

            for file in ["Channel", "MenuMulti", "MenuSingle"]:
                self.label_Action.config(text=f"Configuration des icones {file}.szs...")
                self.progressbar_Action.step(1)

                p = subprocess.Popen(f"wszst EXTRACT \"{self.path}/files/Scene/UI/{file}.szs\" --DEST \"./.tmp/{file}\"")
                p.wait()

                shutil.copy(f"{self.path}/files/.MKCreator/ct_icons.tpl", f"./.tmp/{file}/button/timg/ct_icons.tpl")
                shutil.copy(f"{self.path}/files/.MKCreator/ct_icons.tpl", f"./.tmp/{file}/control/timg/ct_icons.tpl")

                p = subprocess.Popen(f"wszst CREATE \"./.tmp/{file}\" --DEST \"{self.path}/files/Scene/UI/{file}.szs\" --overwrite")
                p.wait()
                shutil.rmtree(f"./.tmp/{file}")

                for language in "EFGIS":
                    self.label_Action.config(text=f"Configuration des icones {file}_{language}.szs...")
                    self.progressbar_Action.step(1)
                    szs_path = f"{self.path}/files/Scene/UI/{file}_{language}.szs"
                    tmp_path = f"./.tmp/{file}_{language}"
                    if os.path.exists(szs_path):
                        p = subprocess.Popen(f"wszst EXTRACT \"{szs_path}\" --DEST \"{tmp_path}\"")
                        p.wait()
                        if os.path.exists(f"{tmp_path}/message/Common.bmg"):
                            p = subprocess.Popen(f"wbmgt decode \"{tmp_path}/message/Common.bmg\" --overwrite")
                            p.wait()

                            with open(f"{tmp_path}/message/Common.txt", "a+") as CommonFile:
                                for line in CommonFile.readlines():
                                    for TEXT in TEXT_DATA:
                                        print(line[len(f"  {TEXT['slot']}"):])
                                        if line[len(f"  {TEXT['slot']}"):] == f"  {TEXT['slot']}":
                                            if line != f"\n  {TEXT['slot']}\t= {TEXT['name']}":
                                                pointer = CommonFile.tell()
                                                CommonFile.write(f"\n  {TEXT['slot']}\t= {TEXT['name']}")
                                                CommonFile.seek(pointer)
                                                TEXT_DATA.pop(TEXT)

                                for TEXT in TEXT_DATA:
                                    CommonFile.write(f"\n  {TEXT['slot']}\t= {TEXT['name']}")

                            p = subprocess.Popen(f"wbmgt encode \"{tmp_path}/message/Common.txt\" --overwrite --le-code")
                            p.wait()
                            os.remove(f"{tmp_path}/message/Common.txt")

                    p = subprocess.Popen(f"wszst CREATE \"{tmp_path}\" --DEST \"{szs_path}\" --overwrite")
                    p.wait()

                    shutil.rmtree(tmp_path)


            self.label_Action.config(text=f"Patch de LE-CODE.bin...")
            self.progressbar_Action.step(1)
            p = subprocess.Popen(
                f"wlect patch ./assets/lecode-PAL.bin -od \"{self.path}/files/rel/lecode-PAL.bin\" --track-dir " + \
                f"\"{self.path}/files/Race/Course\" --copy-tracks \"{self.path}/files/.MKCreator/Track/\" " + \
                f"--copy-tracks \"{self.path}/files/.MKCreator/Track-Original/\" --le-define " + \
                f"\"{self.path}/files/.MKCreator/CTFILE.txt\" --lpar ./assets/lpar-default.txt --overwrite")
            p.wait()

            self.progressbar_Action.grid_forget()
            self.label_Action.grid_forget()
            self.frame_ActionGameEditROM.grid(row = 4, column = 1, sticky = "NEWS")


        Thread(target=main).start()


    def save_config(self):
        with open(f"{self.path}/files/.MKCreator/config.json", "w") as file:
            json.dump(self.config, file)


    def import_track_pack(self):
        def main():
            path = filedialog.askopenfilename(filetypes = (("Fichier MKCTP", r"*.mkctp"),))
            if path:

                self.progressbar_Action.grid(row = 100, column = 1, sticky = "NEWS")
                self.label_Action.grid(row = 101, column = 1)
                self.label_Action.config(text=f"Importation du pack de courses...")
                self.frame_ActionGameEditROM.grid_forget()
                self.progressbar_Action.config(mode = "indeterminate")
                self.progressbar_Action.start(50)

                shutil.unpack_archive(path, f"{self.path}/files/.MKCreator/", 'zip')
                if os.path.exists(f"{self.path}/files/.MKCreator/Track-WBZ/"):
                    for track in os.listdir(f"{self.path}/files/.MKCreator/Track-WBZ/"):
                        p = subprocess.Popen(f"wszst normalize \"{self.path}/files/.MKCreator/Track-WBZ/{track}\" --szs --overwrite " + \
                                             f"--DEST \"{self.path}/files/.MKCreator/Track/{track[:-3]}szs\" " + \
                                             f"--autoadd-path \"{self.path}/files/.MKCreator/auto-add/\"")
                        p.wait()
                    shutil.rmtree(f"{self.path}/files/.MKCreator/Track-WBZ/")
                self.refresh_cup_menu()

            self.progressbar_Action.grid_forget()
            self.label_Action.grid_forget()
            self.frame_ActionGameEditROM.grid(row=4,column=1,sticky="NEWS")

        Thread(target=main).start()


    def export_track_pack(self):
        def main():
            path = filedialog.asksaveasfilename(filetypes=(("Fichier MKCTP", r"*.mkctp"),))  # Mario Kart Creator Track Pack
            if path:

                self.progressbar_Action.grid(row=100, column=1, sticky="NEWS")
                self.label_Action.grid(row=101, column=1)
                self.label_Action.config(text=f"Exportation du pack de courses...")
                self.frame_ActionGameEditROM.grid_forget()
                self.progressbar_Action.config(mode="indeterminate")
                self.progressbar_Action.start(50)

                shutil.copytree(f"{self.path}/files/.MKCreator/", "./.tmp/.MKCreator")
                shutil.rmtree("./.tmp/.MKCreator/Track-Original/") # Ces courses sont copyright.
                shutil.rmtree("./.tmp/.MKCreator/auto-add/") # Fichier librairie nécéssaire pour convertir les wbz en szs.
                if not(os.path.exists("./.tmp/.MKCreator/Track-WBZ/")): os.makedirs("./.tmp/.MKCreator/Track-WBZ/")
                for track in os.listdir("./.tmp/.MKCreator/Track/"):
                    p = subprocess.Popen(f"wszst normalize \"./.tmp/.MKCreator/Track/{track}\" --wbz --overwrite " + \
                                         f"--DEST \"./.tmp/.MKCreator/Track-WBZ/{track[:-3]}wbz\" " + \
                                         f"--autoadd-path \"{self.path}/files/.MKCreator/auto-add/\"")
                    p.wait()
                shutil.rmtree("./.tmp/.MKCreator/Track/")  # Ces courses sont copyright.
                shutil.make_archive(path, 'zip', "./.tmp/.MKCreator")
                if not(".zip" in path): path += ".zip"
                os.rename(path, path.replace(".zip", ".mkctp"))
                shutil.rmtree("./.tmp/.MKCreator/")

            self.progressbar_Action.grid_forget()
            self.label_Action.grid_forget()
            self.frame_ActionGameEditROM.grid(row=4, column=1, sticky="NEWS")

        Thread(target=main).start()


    def generate_cup_icon(self, index):
        cup_icon = Image.new("RGBA", (128, 128))
        draw = ImageDraw.Draw(cup_icon)
        font = ImageFont.truetype("./assets/SuperMario256.ttf", 90)
        draw.text((4-2, 4-2), "CT", (0, 0, 0), font=font)
        draw.text((4+2, 4-2), "CT", (0, 0, 0), font=font)
        draw.text((4-2, 4+2), "CT", (0, 0, 0), font=font)
        draw.text((4+2, 4+2), "CT", (0, 0, 0), font=font)

        draw.text((4, 4), "CT", (255, 165, 0), font=font)

        font = ImageFont.truetype("./assets/SuperMario256.ttf", 60)
        draw.text((15-2, 80-2), "%03i" % index, (0, 0, 0), font=font)
        draw.text((15+2, 80-2), "%03i" % index, (0, 0, 0), font=font)
        draw.text((15-2, 80+2), "%03i" % index, (0, 0, 0), font=font)
        draw.text((15+2, 80+2), "%03i" % index, (0, 0, 0), font=font)

        draw.text((15, 80), "%03i" % index, (255, 165, 0), font=font)

        return cup_icon


    def new_cup(self, cup_id, new_icon, cup_name):
        new_icon.save(f"{self.path}/files/.MKCreator/cup_icon/{cup_id}.png")
        self.config["cup"][str(cup_id)] = {
            "name": cup_name,
            "locked": False,
            "courses": {
                "0": {"name": "/", "music": 0x75, "special": 0x08, "new": False},
                "1": {"name": "/", "music": 0x75, "special": 0x08, "new": False},
                "2": {"name": "/", "music": 0x75, "special": 0x08, "new": False},
                "3": {"name": "/", "music": 0x75, "special": 0x08, "new": False},
            }
        }
        self.save_config()


    def new_track(self, path, name, cup_index, course_index, is_new, music_type, track_type):
        if os.path.exists(path):
            _formated_name = name.replace(" ", "")
            if (_formated_name != "") and (_formated_name != "/"):
                if music_type in track2ID:
                    if track_type in track2ID:

                        if not (os.path.exists(f"{self.path}/files/.MKCreator/Track/")):
                            os.makedirs(f"{self.path}/files/.MKCreator/Track/")

                        _, extension = os.path.splitext(path)
                        if extension == ".wbz":
                            p = subprocess.Popen(f"wszst normalize \"{path}\" --szs --overwrite " + \
                                                 f"--DEST \"{self.path}/files/.MKCreator/Track/{name}.szs\" " + \
                                                 f"--autoadd-path \"{self.path}/files/.MKCreator/auto-add/\"")
                            p.wait()
                        elif extension == ".szs":
                            shutil.copy(path, f"{self.path}/files/.MKCreator/Track/{name}.szs")

                        self.config["cup"][str(cup_index)]["courses"][str(course_index)] = {
                            "name": name,
                            "music": track2ID[music_type][0],
                            "special": track2ID[track_type][1],
                            "new": is_new,
                        }
                        self.save_config()
                        self.select_cup(cup_index)

                        return True

                    else: messagebox.showerror("Erreur", "Le type spécial de la map est invalide.")
                else: messagebox.showerror("Erreur", "La musique de la map est invalide.")
            else: messagebox.showerror("Erreur", "Le nom de la course doit être défini.")
        else: messagebox.showerror("Erreur", "Vous devez sélectionner le fichier .szs de la course.")

        return False


    def import_multiple_race(self):
        def main():
            paths = filedialog.askopenfilenames(filetypes = (("Fichier course", r"*.szs *.wbz"),))
            if paths:

                self.progressbar_Action.grid(row=100, column=1, sticky="NEWS")
                self.label_Action.grid(row=101, column=1)
                self.frame_ActionGameEditROM.grid_forget()
                self.progressbar_Action.config(mode="determinate")
                self.progressbar_Action['maximum'] = len(paths) + 1
                self.progressbar_Action["value"] = 0

                for index, path in enumerate(paths):
                    name = self.get_track_name(path)
                    self.label_Action.config(text=f"Ajout de la course \"{name}\"...")
                    self.progressbar_Action.step(1)
                    course_id = index % 4

                    Type = 0
                    Property = path[path.find("[") + 1:path.rfind("]")]
                    try:
                        r = Property.find("r")
                        if r != -1:
                            _Type = Property[r + 1:r + 3]
                            Type = ((int(_Type[0]) - 1) * 4) + (int(_Type[1]) - 1)
                    except: pass

                    special_slot = list(track2ID.keys())[Type]

                    if course_id == 0:
                        cup_id = len(self.config["cup"])
                        new_icon = self.generate_cup_icon(cup_id)
                        cup_name = "CT%03i" % cup_id
                        self.new_cup(cup_id, new_icon, cup_name)

                    self.new_track(path, name, cup_id, course_id, True, special_slot, special_slot)

            self.progressbar_Action.grid_forget()
            self.label_Action.grid_forget()
            self.frame_ActionGameEditROM.grid(row=4, column=1, sticky="NEWS")

        Thread(target=main).start()


#TODO: Vérifier les overwrites pour éviter les bugs
#TODO: Améliorer la modification des sous-fichiers des szs
#TODO: Warning sur les dossier à accent !!! impossible d'importer une course depuis l'un d'eux ! + Installer les outils wszst, ...



Main = main()
mainloop()