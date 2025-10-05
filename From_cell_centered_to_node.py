import numpy as np
import os
os.chdir(r"C:\Users\aliac\Desktop\Tesi_Magistrale\Esercitazione_CFD")
# Inizializzo valore variabili 

cells_xy= []         # [(x_c,y_c),....]  
cells_vars=[]        # [[rho_c, P_c, u_c, v_c, M, S],....]
nodes = []         # [(ids, x, y), ...]
sec = None

# Apro il file 
with open(r"C:\Users\aliac\Desktop\Tesi_Magistrale\Esercitazione_CFD\Euler_2D\1000.txt","r") as f:

    # Gestisco il file per inserire i valori che mi servono nelle rispettive variabili 
    for riga in f:
        eids=[]
        s = riga.strip()
        if not s or s.startswith("#"): continue
        if s.startswith("[") and s.endswith("]"):
            sec = s[1:-1].upper(); continue
        parts = s.split()

        if sec == "VALORI_ELEMENTI":        #  x_c y_c rho_c P_c u_c v_c M S
           
           try:
               float(parts[-1]); float(parts[-2])
           except ValueError:
               continue
           
           
           if len(parts) >= 3:             # if utilizzato per evitare possibili messaggi di errore 
                xc, yc=map(float, parts[:2])
                var=list(map(float, parts[2:]))
                cells_xy.append((xc, yc))
                cells_vars.append(var)
           else:
                print("Errore nelle righe di Valori_Elementi")    

        elif sec == "NODI":

            try:
               float(parts[-1]); float(parts[-2])
            except ValueError:
               continue
           
            if len(parts) >= 3:
                x, y = map(float, parts[-2:])

                for d in parts[:-2]:
                    if int(d)>0:
                        eids.append(int(d))

                nodes.append((eids, x, y))
            else:
                print("Errore nelle righe di Nodi")    
            

# Converto le liste in array in modo tale da poter lavorare con numpy
    
centroids = np.array(cells_xy, float)
values    = np.array(cells_vars, float)

# Scrivo una funzione che prede come input i valori delle coordinate di un nodo e gli ID degli elementi che condividono quel nodo e mi restituisce il valore della rispettiva variabile i-esima
def ls_value_at(x, y, eids,i):
    if len(eids) >= 3:
        C = centroids[np.array(eids)-1]           # sottraggo 1 perchè gli indici in python partono da 0 mentre gli Id degli elementi partono da 1
        f = values[np.array(eids)-1,i]              # sottraggo 1 perchè gli indici in python partono da 0 mentre gli Id degli elementi partono da 1
        X = np.c_[np.ones(len(C)), C]             # concateno per colonne per creare un arrey del tipo [1,x_c,y_c]
        beta = np.linalg.lstsq(X, f, rcond=None)[0] # utilizzo la funzione lstsq che mi risolve il sistema con i minimi quadrati. Prendo il primo elemento della tupla che mi restituisce rispettivamente un array con i parametri [c,b,a]
        return float(beta[0] + beta[1]*x + beta[2]*y)
    elif len(eids) == 2:                          # Se un nodo ha solo due celle vicine faccio la media 
        return float(values[np.array(eids)-1,i].mean())
    elif len(eids) == 1:                          # Se un nodo ha solo una cella vicina prendo il valore di quella cella 
        return float(values[eids[0]-1,i])
    else:
        return float("nan")

out = []
for eids, x, y in nodes:
    val=f"{x} {y} "
    for i in range(0,values.shape[1]):
        v = ls_value_at(x, y, eids,i)
        val=val+ f"{v} "

    out.append(val)
    

with open("cellcentered_to_node_1.txt","w") as fo:
    fo.write("\n".join(out))

print("OK -> nodal_from_cc.txt")
