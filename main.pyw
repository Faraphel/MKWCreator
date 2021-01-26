from tkinter import *
from tkinter import messagebox, filedialog, ttk
import os
import subprocess
import shutil
from threading import Thread

class main():
    def __init__(self):
        self.root = Tk()
        self.root.title("MKWii Creator")

        self.frame_SelectGameFile = LabelFrame(self.root, text="Fichier du jeu")
        self.frame_SelectGameFile.grid(row=1, column=1, sticky="NEWS")
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
        self.button_EditROM = Button(self.frame_ActionGameFile, text="Modifier la ROM", relief=RIDGE, command=self.edit_game)
        self.progressbar_Action = ttk.Progressbar(self.frame_ActionGameFile)


        self.frame_CupManager = LabelFrame(self.root, text="Coupe")
        self.button_CupManagerLeft = Button(self.frame_CupManager, width=2, text="<")
        self.button_CupManagerLeft.grid(row=1, column=1, rowspan=2, sticky="NEWS")

        self.button_CupManager = []
        for x in range(4):
            for y in range(2):
                self.button_CupManager.append(Button(self.frame_CupManager, text=(x*2)+y, width=6, height=3))
                self.button_CupManager[-1].grid(row=y+1, column=x+2)

        self.button_CupManagerRight = Button(self.frame_CupManager, width=2, text=">")
        self.button_CupManagerRight.grid(row=1, column=6, rowspan=2, sticky="NEWS")

        self.frame_RaceManager = LabelFrame(self.frame_CupManager, text="Course")
        self.frame_RaceManager.grid(row=10, column=1, columnspan=6, sticky="NEWS")
        self.button_RaceManager = []
        for x in range(4):
            self.button_CupManager.append(Button(self.frame_RaceManager, text=x, width=35))
            self.button_CupManager[-1].grid(row=x, column=1, sticky="NEWS")


    def ask_game_file(self):
        path = filedialog.askopenfilename()
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
            self.button_ExtractROM.grid(row=2, column=1, sticky="NEWS")
            self.button_InstallLECODE.grid_forget()
            self.button_EditROM.grid_forget()

        else:
            self.button_ExtractROM.grid_forget()
            if os.path.exists(f"{self.path}/files/rel/lecode-PAL.bin"):
                self.button_InstallLECODE.grid_forget()
                self.button_EditROM.grid(row = 4, column = 1, sticky = "NEWS")

            else:
                self.button_InstallLECODE.grid(row = 3, column = 1, sticky = "NEWS")
                self.button_EditROM.grid_forget()


    def extract_game(self):
        def main():
            dir = filedialog.askdirectory()
            if dir:
                self.progressbar_Action.grid(row = 100, column = 1, sticky = "NEWS")
                self.button_ExtractROM.grid_forget()

                self.progressbar_Action.config(mode="indeterminate")
                self.progressbar_Action.start(50)

                p = subprocess.Popen(f"wit EXTRACT \"{self.path}\" \"{dir}\" --overwrite", shell=True)
                p.wait()

                self.progressbar_Action.grid_forget()
                self.path = dir
                self.file_type = "dol"
                self.refresh_action_frame()

        Thread(target=main).start()


    def install_lecode(self):
        def main():
            # visuel
            self.progressbar_Action.grid(row = 100, column = 1, sticky = "NEWS")
            self.progressbar_Action.config(mode = "determinate")
            self.progressbar_Action['maximum'] = 100
            self.progressbar_Action["value"] = 0
            self.button_InstallLECODE.grid_forget()

            # commande de patch
            p = subprocess.Popen(f"wstrt patch \"{self.path}/sys/main.dol\" --clean-dol --add-lecode", shell=True)
            p.wait()

            # patch des menus
            for file in ["Award", "Channel", "Event", "Globe", "MenuMulti", "MenuOther", "MenuSingle", "Present", "Race", "Title"]:
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
                    if os.path.exists(subfile): shutil.copy(f"./assets/{replace_path[subfile]}", subfile)

                if file in ["Channel", "MenuMulti", "MenuSingle"]:
                    shutil.copy(f"./assets/ct_icons-default.tpl", f"./.tmp/{file}/button/timg/ct_icons.tpl")
                    shutil.copy(f"./assets/ct_icons-default.tpl", f"./.tmp/{file}/control/timg/ct_icons.tpl")

                    # patch des fichiers de langage des menus
                    for language in "EFGIS":
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

                        p = subprocess.Popen(f"wszst CREATE \"{tmp_path}\" --DEST \"{szs_path}\" --overwrite")
                        p.wait()

                        shutil.rmtree(tmp_path)


                p = subprocess.Popen(f"wszst CREATE \"./.tmp/{file}\" --DEST \"{self.path}/files/Scene/UI/{file}.szs\" --overwrite")
                p.wait()

                shutil.rmtree(f"./.tmp/{file}")



            # patch des vidéos de présentation
            for file in ["banana", "cup_select", "flower", "kinoko", "konoha", "koura", "special", "star", "thunder"]:
                shutil.copy("./assets/video.thp", f"{self.path}/files/thp/course/{file}.thp")

            # correction des courses
            if not(os.path.exists("./.tmp/Track/")): os.makedirs("./.tmp/Track/")


            for file in os.listdir(f"{self.path}/files/Race/Course/"):
                if os.path.isfile(f"{self.path}/files/Race/Course/{file}"):
                    _, extension = os.path.splitext(file)
                    if extension == ".szs":
                        shutil.move(f"{self.path}/files/Race/Course/{file}", f"./.tmp/Track/{file}")

            # application du patch
            p = subprocess.Popen(f"wlect patch ./assets/lecode-PAL.bin -od \"{self.path}/files/rel/lecode-PAL.bin\" --track-dir "+\
                                 f"\"{self.path}/files/Race/Course\" --copy-tracks ./.tmp/Track/ --le-define "+\
                                 f"./assets/CTFILE-default.txt --lpar ./assets/lpar-default.txt --overwrite")
            p.wait()

            self.progressbar_Action.grid_forget()
            self.refresh_action_frame()

        Thread(target=main).start()


    def edit_game(self):
        self.frame_CupManager.grid(row=1, column=2, rowspan=2, sticky="NEWS")

#TODO: wimgt encode "src" --DEST "dst" -x tpl.CMPR    pour convertir un .png en .tpl
#TODO: Menu pour créer des coupes & configurer les courses

Main = main()
mainloop()