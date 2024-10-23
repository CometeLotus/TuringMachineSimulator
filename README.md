
# Simulateur de Machine de Turing

## Description

Ce projet est un **simulateur de Machine de Turing** qui permet l'exécution pas à pas de machines de Turing dans un **terminal** ou via une **interface graphique** utilisant `tkinter`. Il propose également une fonctionnalité permettant de **lier deux machines de Turing** pour en créer une machine combinée. Le simulateur fonctionne à partir de fichiers décrivant les états et transitions de la machine.

## Fonctionnalités

- **Affichage des détails** : Affiche la structure détaillée d'une machine de Turing.
- **Simulation dans le terminal** : Exécute la machine de Turing pas à pas avec un affichage dans le terminal.
- **Simulation graphique** : Exécute la machine pas à pas avec une représentation visuelle dans une interface graphique.
- **Liaison de machines** : Combine deux machines de Turing en une seule.

## Prérequis

- Python 3.x
- `tkinter` (pour l'interface graphique)
- `Pillow` (pour la gestion des images dans l'interface graphique)

Vous pouvez installer les dépendances avec :

```bash
pip install tkinter Pillow
```

## Comment Utiliser

### 1. Interface en Ligne de Commande

Le simulateur supporte différentes commandes pour effectuer diverses actions. Voici le format général d'utilisation :

```bash
python Turingmachine.py [action] [options]
```

#### Actions :

- `Détails [entrée] [fichier]` : Affiche la structure détaillée de la machine de Turing à partir de l'entrée et du fichier fourni.
- `Terminal [entrée] [fichier]` : Exécute la machine de Turing pas à pas dans le terminal.
- `Graphique [entrée] [fichier]` : Exécute la machine pas à pas via une fenêtre graphique.
- `LinkMachines [fichier1] [fichier2]` : Lie deux machines de Turing décrites dans les fichiers fournis.

#### Options :
- **[entrée]** : Le mot d'entrée pour la machine de Turing.
- **[fichier]** : Chemin vers le fichier contenant la description de la machine de Turing.

### 2. Exemples d'Utilisation

- **Afficher les détails de la machine** :
  ```bash
  python Turingmachine.py Détails "10101" "Machines/Binary_palindrome.txt"
  ```

- **Exécuter la machine dans le terminal** :
  ```bash
  python Turingmachine.py Terminal "10101" "Machines/Binary_palindrome.txt"
  ```

- **Exécuter la machine avec une interface graphique** :
  ```bash
  python Turingmachine.py Graphique "10101" "Machines/Binary_palindrome.txt"
  ```

- **Lier deux machines de Turing** :
  ```bash
  python Turingmachine.py LinkMachines "Machines/Machine1.txt" "Machines/Machine2.txt"
  ```

## 3. Format d'une machine de Turing

Une machine de Turing est définie à l'aide d'un fichier texte structuré de la manière suivante :

1. **Nom de la machine** : La première ligne contient le nom de la machine.
2. **État initial** : La deuxième ligne contient l'état initial de la machine (Il doit s'appeller **I**).
3. **État final** : La troisième ligne contient l'état final de la machine (Il doit s'appeller **F**).
4. **Transitions** : À partir de la quatrième ligne, les transitions sont définies en deux étapes :
   - Première ligne : L'état courant suivi du symbole lu sur la bande.
   - Deuxième ligne : L'état de transition, le symbole à écrire sur la bande, et la direction du déplacement de la tête (`<` pour gauche, `>` pour droite, ou `-` pour rester sur place).

### Exemple de format :

```txt
Search0   # Nom de la machine
I         # État initial
F         # État final

I,1       # Transition : Si l'état est I et le symbole lu est 1
I,1,>     # Action : Reste dans l'état I, écrit 1, et déplace la tête à droite

I,0       # Transition : Si l'état est I et le symbole lu est 0
F,0,-     # Action : Passe à l'état F, écrit 0, et reste sur place
```

## Interface Graphique

Lorsque vous exécutez la commande `Graphique`, le simulateur affiche une fenêtre avec :

- **Image de la machine**.
- **Compteur de pas**.
- **État actuel**.
- **Visualisation de la bande** pour chaque étape, avec le mouvement de la tête et le contenu de la bande.

Utilisez le bouton `▶❙` pour simuler l'étape suivante.

