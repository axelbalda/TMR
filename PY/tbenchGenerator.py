import re
import sys

# Test it out
#N = int(input("What is the order of the whished NMR? "))
##if N < 3 :
##    N = 3
##    print("Wrong value (<3) : N = 3 by default")

N = 3

filename  = sys.argv[1]                                                                                 # Initial testbench
filename2 = sys.argv[2]                                                                                 # New testbench after redundancy
filename3 = sys.argv[3]                                                                                 # Top simulation file containing all IOs names

try :                                                                                                   
    f  = open(filename,  'r')                                                                           # Try to open the initial testbench file
except FileNotFoundError :                                                                              # If the file can't be found
    print(re.split(r"[\\]", filename)[-1], "not found")                                                 # Corresponding error message
    exit(-1)                                                                                            # Exit program

try :
    f2 = open(filename2, 'w')                                                                           # Try to open the new testbench file
except FileNotFoundError :                                                                              # If the file can't be found
    print(re.split(r"[\\]", filename2)[-1], "not found")                                                # Corresponding error message
    exit(-1)                                                                                            # Exit program

try :
    f3 = open(filename3, 'r')                                                                           # Try to open the new testbench file
except FileNotFoundError :                                                                              # If the file can't be found
    print(re.split(r"[\\]", filename3)[-1], "not found")                                                # Corresponding error message
    exit(-1)                                                                                            # Exit program
    
clkKeyword = [r'CLK', r'Clock', r'inClock', r'C ']                                                      # Possible clock names

enableWrite = 1                                                                                         # Flag to enable writing
enableCopy = 0                                                                                          # Flag to enable copying

for count, line in enumerate(f):                                                                        # Lecture une ?? une des lignes du fichier 'initial testbench'
    if enableWrite == 1 :                                                                               # Si l'??criture est autoris??e
        f2.write(line)                                                                                  # On recopie la ligne actuelle
        if enableCopy == 1 :                                                                            # Si la copie est autoris??e
            if "begin" in line.lower() :                                                                # Si on d??tecte le mot cl?? 'begin'
                pass                                                                                    # On ne fait rien
            elif "wait" in line.lower() :                                                               # Si on d??tecte le mot cl?? 'wait'
                pass                                                                                    # On ne fait rien
            elif "end process" in line.lower() :                                                        # Si on d??tecte les mots cl??s 'end process'
                pass                                                                                    # On ne fait rien
            else :                                                                                      # Sinon
                if any(ii in clkKeyword for ii in line) :                                               # Si la ligne contient le nom de l'horloge
                    continue                                                                            # On ne fait rien 
                else :                                                                                  # Sinon
                    for k in range(N-1) :                                                               # On va faire la redondance sur la ligne actuelle
                            dupliK = line.split()                                                       # On extrait chaque mot de la ligne
                            dupliK[0] = dupliK[0] + "_NMR" + str(k+2)                                   # On r??cup??re le nom du signal ?? tripliquer et on lui ajoute la marque de redondance
                            dupliK = '\t' + ' '.join(dupliK) + '\n'                                     # On r??-assemble la ligne
                            f2.write(dupliK)                                                            # On ??crit cette nouvelle ligne ?? la suite du fichier
        
    if "signal" in line.lower() :                                                                       # Si on d??tecte le mot cl?? 'signal'
        if any(ii in clkKeyword for ii in line) :                                                       # Si la ligne contient le nom de l'horloge 
            continue                                                                                    # On ne fait rien
        else :                                                                                          # Sinon
            for i in range(N-1) :                                                                       # On va faire la redondance sur le signal actuel
                dupli = line.split()                                                                    # On extrait chaque mot de la ligne 
                dupli[1] = dupli[1] + "_NMR" + str(i+2)                                                 # On r??cup??re le nom du signal ?? tripliquer et on lui ajoute la marque de redondance 
                dupli = ' '.join(dupli) + '\n'                                                          # On r??-assemble la ligne
                f2.write(dupli)                                                                         # On ??crit cette nouvelle ligne ?? la suite du fichier

    if "map" in line.lower() :                                                                          # Si on d??tecte le mot cl?? 'map'
        enableWrite = 0                                                                                 # On d??sactive l'??criture
        i = 0                                                                                           # On initialise une variable i ?? 0
        j = 0                                                                                           # On initialise une variable j ?? 0
        commaFlag = 0                                                                                   # On initialise une variable qui d??tecte les virgules ?? 0
        for count2, line2 in enumerate(f3):                                                             # Lecture une ?? une des lignes du fichier 'top simulation'
            if ("input" in line2 or "output" in line2) :                                                # Si on d??tecte un des mots cl??s 'input' ou 'output'
                if commaFlag == 1 :                                                                     # Gestion de la virgule en fin de ligne par rapport ?? la ligne pr??c??dente
                    toWrite = ',\n'                                                                     # Si la ligne pr??c??dente contenait une virgule en fin de ligne, on doit ajouter aussi une virgule ?? la fin de sa redondance
                    f2.write(toWrite)                                                                   # On ??crit cette virgule
                toRecover = re.split(r"[ ,;]", line2)                                                   # On extrait les mots de la ligne
                toRecover[:] = (value for value in toRecover if value != "")                            # On supprime les caract??res vide
                toWrite = '\t\t' + toRecover[1] + " => "                                                # On r??cup??re le nom de l'IO et on ajoute l'assignation
                toWrite += toRecover[1]                                                                 # On compl??te la variable pr??c??dente avec le m??me nom de l'IO
                f2.write(toWrite)                                                                       # On ??crit cette nouvelle ligne
                commaFlag = 1                                                                           # On indique qu'il faudra ajouter une virgule en fin de ligne s'il existe une prochaine ligne a tripliqu??
        commaFlag = 0                                                                                   # On remet ?? 0 la variable g??rant les virgules
        f2.write('\n')                                                                                  # On ??crit un saut ?? la ligne
        
    if enableWrite == 0 :                                                                               # Si l'??criture n'est pas autoris??e
        if ");" in line :                                                                               # Si on arrive ?? la fin d'un bloc
            enableWrite = 1                                                                             # On autorise l'??criture
            f2.write(line)                                                                              # On ??crit la ligne courante
        else :                                                                                          # Sinon
            enableWrite = 0                                                                             # On d??sactive l'??criture

    if "process" in line.lower() :                                                                      # Si on d??tecte le mot cl?? 'process' dans la ligne
        enableCopy = 1                                                                                  # On autorise la copie
        
    if enableCopy == 1 :                                                                                # Si la copie est autoris??e
        if "end process" in line.lower() :                                                              # Si on d??tecte les mots cl??s 'end process' dans la ligne
            enableCopy = 0                                                                              # On d??sactive la copie
        else :                                                                                          # Sinon
            enableCopy = 1                                                                              # On autorise la copie
                
        

f3.close()                                                                                              # On ferme le fichier 
f2.close()                                                                                              # On ferme le fichier
f.close()                                                                                               # On ferme le fichier
