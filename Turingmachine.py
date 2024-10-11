from tkinter import *
from PIL import Image, ImageTk 
import time
import sys
cmpt_steps = 0

def initialise_MT (entree, fichier):
    """
    Initialise une structure Machine Turing a partir d'un mot d'entrée 
    et d'un fichier contenant une description d'une Machine de Turing
    """
    #a préciser le format du fichier en entrée
    MT = {
        "nom": "",
        "alphabet d'entree": ['1', '0'],
        "alphabet de travail": ['1', '0', '_'],
        "ensemble d'états": [],
        "état initial": "I",
        "état final": "F",
        "transitions": [],
        "état courant": "I",
        "état des bandes": [list('_'+entree)],
        "position tete de lecture":[1]
    }
    contenue_du_fichier = []
    #Stockage du contenu du fichier descriptif du MT dans la liste (contenue_du_fichier)
    with open (fichier,"r") as f:
        for ligne in f:
            ligne = ligne.replace("\n", "")
            if ligne  != '':
                contenue_du_fichier.append(ligne.split(','))
    f.close()
    MT["nom"] = contenue_du_fichier[0][0]
    MT["transitions"] = contenue_du_fichier[3:]
    nombre_de_bandes = len(MT["transitions"][0])-1
    for i in range (nombre_de_bandes-1):
        MT["état des bandes"].append([])
        MT["position tete de lecture"].append(1)
    for i in range(nombre_de_bandes):
        if len(MT["état des bandes"][i]) != 0:
            MT["état des bandes"][i].append("_")
        else:
            for j in range(3):
                MT["état des bandes"][i].append("_")
    nb_transitions = len(MT["transitions"])
    for i in range (nb_transitions):
        if MT["transitions"][i][0] not in MT["ensemble d'états"]:
            MT["ensemble d'états"].append(MT["transitions"][i][0])
    return MT

def pas_de_calcul(MT):
    nb_de_bandes = len(MT['position tete de lecture'])
    trans_a_executer = [MT["état courant"]]
    for i in range (nb_de_bandes):
        bande = MT["état des bandes"][i]
        position = MT["position tete de lecture"][i]
        trans_a_executer.append(bande[position])
    nb_transitions = len(MT["transitions"]) 
    calcul = []
    for i in range(nb_transitions):
        if MT["transitions"][i] == trans_a_executer:
            calcul = MT["transitions"][i+1]
            break
    if calcul == []:
        return "Pas de calcul Impossible"
    MT["état courant"] = calcul[0]
    ecrire_sur_bandes = calcul[1:nb_de_bandes+1]
    nouvelle_position = calcul[nb_de_bandes+1:]
    signe = []
    for i in range(nb_de_bandes):
        signe.append(0)
        bande = MT["état des bandes"][i]
        bande[MT["position tete de lecture"][i]] = ecrire_sur_bandes[i]
        MT["état des bandes"][i] = bande
        if nouvelle_position[i] == '<':
            MT["position tete de lecture"][i] -= 1
        elif  nouvelle_position[i] == '>':
            MT["position tete de lecture"][i] += 1
        if MT['état des bandes'][i][-1] != '_':
            MT['état des bandes'][i].append('_')
        if MT['état des bandes'][i][0] != '_':
            MT["état des bandes"][i].insert(0,'_')
            signe[i] = 1
            MT["position tete de lecture"][i] += 1
    return (MT, nouvelle_position, signe)
    
def simule_le_calcul(MT):
    global cmpt_steps
    if MT["état courant"] != 'F':
        tmp = pas_de_calcul(MT)
        cmpt_steps += 1
        if tmp == "Pas de calcul Impossible":  
            return "Rejected"
        else:
            return tmp
    else: 
        return "Accepted"
        
class Fenetre(Tk):
    global cmpt_steps
    M = {}
    position_depart = []
    def __init__(self, entree, fichier):
        Tk.__init__(self)
        MT = initialise_MT(entree, fichier)
        Fenetre.M = MT
        self.title("Turing Machine simulator")
        self.geometry("1366x768")
        self.resizable(width=False, height=False) 
        monimage =Image.open("machine_turing.png")
        photo = ImageTk.PhotoImage(monimage) 
        label = Label(image=photo)
        label.image = photo
        label.place(x=123.5, y=20)
        self.canvas_bandes = Canvas(self, width = 1366, height = 6350)
        self.canvas_bandes.create_rectangle(107, 3, 1257, 635, fill="white", outline="black") 
        self.canvas_bandes.create_rectangle(107, 3, 1257, 70, fill="white", outline="black")
        Label(self, text=MT["nom"], bg="white", fg="black", font=40).place(x=500, y=155)
        Label(self, text="Steps:", bg="white", fg="black", font=40).place(x=200, y=230)
        Label(self, text="State:", bg="white", fg="black", font=40).place(x=630, y=230)
        Label(self, text=MT["état courant"], bg="white", fg="black", font=40).place(x=690, y=230)
        Label(self, text=cmpt_steps, bg="white", fg="black", font=40).place(x=260, y=230)
        Button(self, text="▶❙", command=self.etape_suivante).place(x=1100, y=235)
        hauteur = 290
        y1 = 150
        y2 = 200
        y = 200
        nb_de_bandes = len(MT["état des bandes"])
        for i in range(nb_de_bandes):
            x = 133+50*(10+MT["position tete de lecture"][i])
            self.canvas_bandes.create_polygon(x, y, x-15, y+30, x+15, y+30, fill='black')
            y += 100
            etat_bande = MT["état des bandes"][i]
            x1 = 108
            x2 = 168
            for j in range(23):
                self.canvas_bandes.create_rectangle(x1, y1, x2, y2, fill="#1883e8",outline="white")  
                x1 += 50
                x2 += 50
            y1 += 100
            y2 += 100
            for k in range(len(etat_bande)):
                if 125+(k+10)*50 <= 1225 and 125+(k+10)*50 >= 125:
                    if etat_bande[k] != "_":
                        Label(self, text=etat_bande[k], bg="#1883e8", fg="black", font=40).place(x=125+(k+10)*50, y=hauteur)
            hauteur += 100
        self.canvas_bandes.place(x=0, y=130)
        Fenetre.position_depart = [625 for i in range (nb_de_bandes)]

    def etape_suivante(self):
        tmp = simule_le_calcul(Fenetre.M)
        if tmp == "Accepted":
            Label(self, text="Accepted", bg="white", fg="green", font=40).place(x=240, y=155)
        elif tmp == "Rejected":
            Label(self, text="Rejected", bg="white", fg="red", font=40).place(x=240, y=155)
        else:
            Fenetre.M = tmp[0]
            decalage = tmp[1]
            signe = tmp[2]
            Label(self, text='____________', bg="white", fg="white", font=40).place(x=690, y=230)
            Label(self, text=Fenetre.M["état courant"], bg="white", fg="black", font=40).place(x=690, y=230)
            Label(self, text=cmpt_steps, bg="white", fg="black", font=40).place(x=260, y=230)
            hauteur = 290
            nb_de_bandes = len(Fenetre.M["état des bandes"])
            y1 = 150
            y2 = 200
            for i in range(nb_de_bandes):
                etat_bande = Fenetre.M["état des bandes"][i]
                x1 = 108
                x2 = 168
                for j in range(23):
                    self.canvas_bandes.create_rectangle(x1, y1, x2, y2, fill="#1883e8",outline="white") 
                    Label(self, text='  ', bg="#1883e8").place(x=x1+20, y=y1+145)
                    x1 += 50
                    x2 += 50
                y1 += 100
                y2 += 100
                if decalage[i] == '>':
                    Fenetre.position_depart[i] -= 50
                    x = Fenetre.position_depart[i]
                    for k in range(len(etat_bande)):
                        if x <= 1225 and x >= 125:
                            if etat_bande[k] != "_":
                                Label(self, text=etat_bande[k], bg="#1883e8", fg="black", font=40).place(x=x, y=hauteur)
                        x += 50
                    hauteur += 100
                elif decalage[i] == '<':
                    if Fenetre.M["position tete de lecture"][i] != 0:
                        Fenetre.position_depart[i] += 50
                    x = Fenetre.position_depart[i]
                    for k in range(len(etat_bande)):
                        if x <= 1225 and x >= 125:
                            if etat_bande[k] != "_":
                                Label(self, text=etat_bande[k], bg="#1883e8", fg="black", font=40).place(x=x, y=hauteur)  
                        x += 50
                    hauteur += 100
                elif decalage[i] == '-':
                    x = Fenetre.position_depart[i]
                    for k in range(len(etat_bande)):
                        if x <= 1225 and x >= 125:
                            if etat_bande[k] != "_":
                                Label(self, text=etat_bande[k], bg="#1883e8", fg="black", font=40).place(x=x, y=hauteur)
                        x += 50
                    hauteur += 100

def linker(fichier1, fichier2):
    #Les noms des états de M1 doivent etre different de q0,q1,q2,q3,...
    M1 = initialise_MT("00000", fichier1)
    M2 = initialise_MT("11111", fichier2)
    M3 = {
        "nom": M1["nom"],
        "alphabet d'entree": ['1', '0'],
        "alphabet de travail": ['1', '0', '_'],
        "ensemble d'états": M1["ensemble d'états"],
        "état initial": "I",
        "état final": "F",
        "transitions": M1["transitions"],
        "état courant": M1["état courant"],
        "état des bandes": M1["état des bandes"],
        "position tete de lecture": M1["position tete de lecture"]
    }
    tmp_M2 = M2
    cpt_etat = 0
    nb_bandes = len(M2["position tete de lecture"])
    nb_etats = len(tmp_M2["ensemble d'états"])
    #La boucle renome tous les états de M2 qui sont dans M1
    for i in range(nb_etats):
        if tmp_M2["ensemble d'états"][i] in M1["ensemble d'états"] and tmp_M2["ensemble d'états"][i] != "F": 
            nouvelle_etat = 'q'+str(cpt_etat)
            for transition in tmp_M2["transitions"]:
                for j in range(len(transition)):
                    if transition[j] == tmp_M2["ensemble d'états"][i]:
                        transition[j] = nouvelle_etat
                        break
            tmp_M2["ensemble d'états"][i] = nouvelle_etat
        cpt_etat += 1
    for etat in tmp_M2:
        if etat not in M3["ensemble d'états"]:
            M3["ensemble d'états"].append(etat)
    nb_transitions = len(M3["transitions"])
    cpt_appel = 0
    for i in range(nb_transitions):
        for ele in M3["transitions"][i]:
            if ele == M2["nom"]:
                etat_arrivee = M3["transitions"][i][-1]
                del M3["transitions"][i][-1]
                del M3["transitions"][i][-1]
                tmp = M3['transitions'][i][1:nb_bandes+1]
                liste = ['q0'] + tmp
                for j in range(nb_bandes):
                    liste.append("-")
                M3["transitions"].insert(i+1,liste)
                if cpt_appel == 0:
                    for trans in tmp_M2["transitions"]:
                        if trans[0] != 'F':
                            M3["transitions"].append(trans)
                        else:
                            #########problème
                            trans[0] = etat_arrivee
                            M3["transitions"].append(trans)
                else:
                    for j in range(len(tmp_M2["transitions"])):
                        if tmp_M2["transitions"][j][0] == 'F':
                            M3["transitions"].append(tmp_M2["transitions"][j-1])
                            transition = tmp_M2["transitions"][j]
                            transition[0] = etat_arrivee
                            M3["transitions"].append(transition)
                cpt_appel += 1  
    return M3["transitions"]

def affichage_sur_terminal(entree, fichier):
    MT = initialise_MT(entree, fichier)
    global cmpt_steps
    MT["état des bandes"][0] = list('_'+entree+'_')
    nb_de_bandes = len(MT["position tete de lecture"])
    while TRUE:
        print("##########")
        print("Step: {}".format(cmpt_steps))
        print("état courant: {}".format(MT["état courant"]))
        for i in range(nb_de_bandes):
            print("BANDE {}, POSITION {}: {}".format(i+1, MT["position tete de lecture"][i], MT["état des bandes"][i]))
        print('')
        time.sleep(5)
        if MT["état courant"] != 'F':
            tmp = pas_de_calcul(MT)
            cmpt_steps += 1
            if tmp == "Pas de calcul Impossible":  
                return "Rejected"      
        else:
            return "Accepted"

if sys.argv[1] == "question1":
    if len(sys.argv) == 4:
        print(initialise_MT(sys.argv[2], sys.argv[3]))
    else:
        print("ENTREE INVALIDE!")
elif sys.argv[1] == "question4graphique":
    if len(sys.argv) == 4:
        fn = Fenetre(sys.argv[2], sys.argv[3])
        fn.mainloop()
    else:
        print("ENTREE INVALIDE!")
elif sys.argv[1] == "question4terminal":
    if len(sys.argv) == 4:
        print(affichage_sur_terminal(sys.argv[2], sys.argv[3]))
    else:
        print("ENTREE INVALIDE!")
elif sys.argv[1] == "question6":
    if len(sys.argv) == 4:
        print(linker(sys.argv[2], sys.argv[3]))
    else:
        print("ENTREE INVALIDE!")