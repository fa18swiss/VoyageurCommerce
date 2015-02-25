sélection (élitisme) :
récupère les 10 meilleures solutions à chaque passe

mutation :
- Choisis aléatoirement le type de mutation à effectuer
- une mutation inverse 2 villes dans une solution
- l'autre mutation inverse toutes les villes entre 2 villes dans une solution

croisement simple :
1) prends 2 solutions
2) choisis un nombre aléatoire entre 0 et la taille d'une solution
3) construit 2 sous solutions :
3a) toutes les villes de la 1ere solution jusqu'au nombre aléatoire
3b) toutes les villes de la 2eme solution jusqu'au nombre aléatoire
4) construit le reste des sous solutions par rapport aux villes manquantes de l'autre solution, 
c'est à dire sous solution 1 remplit avec les villes manquantes de la solution 2, vice versa

croisement complexe :
1) prends 2 solutions
2) choisis une ville au hasard dans la 1ere solution
3) cherche la ville suivante dans les 2 solutions et récupère la distance la plus courte
3a) si une ville est déjà présente dans la solution, chercher une autre aléatoirement
4) construit une solution avec ces villes jusqu'à toutes les avoir placés