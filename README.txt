s�lection (�litisme) :
r�cup�re les 10 meilleures solutions � chaque passe

mutation :
- Choisis al�atoirement le type de mutation � effectuer
- une mutation inverse 2 villes dans une solution
- l'autre mutation inverse toutes les villes entre 2 villes dans une solution

croisement simple :
1) prends 2 solutions
2) choisis un nombre al�atoire entre 0 et la taille d'une solution
3) construit 2 sous solutions :
3a) toutes les villes de la 1ere solution jusqu'au nombre al�atoire
3b) toutes les villes de la 2eme solution jusqu'au nombre al�atoire
4) construit le reste des sous solutions par rapport aux villes manquantes de l'autre solution, 
c'est � dire sous solution 1 remplit avec les villes manquantes de la solution 2, vice versa

croisement complexe :
1) prends 2 solutions
2) choisis une ville au hasard dans la 1ere solution
3) cherche la ville suivante dans les 2 solutions et r�cup�re la distance la plus courte
3a) si une ville est d�j� pr�sente dans la solution, chercher une autre al�atoirement
4) construit une solution avec ces villes jusqu'� toutes les avoir plac�s