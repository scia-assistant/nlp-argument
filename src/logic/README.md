## Loi into logic

### Questions à poser

- Comment obtient-on la nationnalité française ?

### Article 388

Le mineur est l'individu de l'un ou l'autre sexe qui n'a point encore l'âge de dix-huit ans accomplis.

### Article 413-1

Le mineur est émancipé de plein droit par le mariage.

### Article 144

Le mariage ne peut être contracté avant dix-huit ans révolus.

### Article 1240 (Responsabilité civile pour faute)

> Tout fait quelconque de l'homme, qui cause à autrui un dommage, oblige celui par la faute duquel il est arrivé à le réparer.

Formalisation :

F(a, b) : "a cause un dommage à b."
R(a, b) : "a doit réparer le dommage causé à b."
D(a) : "a a commis une faute."

Règle formalisée :

> ∀a,b(F(a,b)∧D(a)⟹R(a,b))

### Article 1241

> Chacun est responsable du dommage qu'il a causé non seulement par son fait, mais encore par sa négligence ou par son imprudence.

### Article 6 (Ordre public et bonnes mœurs)

> "On ne peut déroger, par des conventions particulières, aux lois qui intéressent l'ordre public et les bonnes mœurs."

Formalisation :

L(x) : "x est une loi d'ordre public."
D(y) : "y déroge à une loi."
N(y) : "y est nulle."

Règle formalisée :

> ∀x,y(L(x)∧D(y)⟹N(y))

### Article 371-1 - Autorité parentale

> "L'autorité parentale est un ensemble de droits et de devoirs ayant pour finalité l'intérêt de l'enfant. Elle appartient aux père et mère jusqu'à la majorité ou l'émancipation de l'enfant."

Formalisation :

AP(p, e) : "p a l'autorité parentale sur e."
Parent(p, e) : "p est un parent de e."
Major(e) : "e est majeur."
Emancipe(e) : "e est émancipé."
Règle formalisée :

> ∀p,e((Parent(p,e)∧¬Major(e)∧¬Emancipe(e))⟹AP(p,e))

### Exemple 5 : Article 1384 (ancien) - Responsabilité du fait des choses que _l'on a sous sa garde

> "On est responsable non seulement du dommage que l'on cause par son propre fait, mais encore de celui qui est causé par le fait des personnes dont on doit répondre, ou des choses que l'on a sous sa garde."

Formalisation :

Responsable(x, z) : "x est responsable du dommage z."
FaitPropre(x, z) : "x a causé directement le dommage z."
Repond(x, y) : "x doit répondre des actes de y."
Garde(x, o) : "x a la garde de l’objet o."
FaitObjet(o, z) : "l'objet o a causé le dommage z."

Règle formalisée :

> ∀x,z(Responsable(x,z)⟺(FaitPropre(x,z)∨∃y(Repond(x,y)∧Responsable(y,z))∨∃o(Garde(x,o)∧FaitObjet(o,z))))

### Article 1243

"Le propriétaire d'un animal, ou celui qui s'en sert, pendant qu'il est à son usage, est responsable du dommage que l'animal a causé, soit que l'animal fût sous sa garde, soit qu'il fût égaré ou échappé."


### Article 1244

Le propriétaire d'un bâtiment est responsable du dommage causé par sa ruine, lorsqu'elle est arrivée par une suite du défaut d'entretien ou par le vice de sa construction.

### Article 1242

On est responsable non seulement du dommage que l'on cause par son propre fait, mais encore de celui qui est causé par le fait des personnes dont on doit répondre, ou des choses que l'on a sous sa garde.

Toutefois, celui qui détient, à un titre quelconque, tout ou partie de l'immeuble ou des biens mobiliers dans lesquels un incendie a pris naissance ne sera responsable, vis-à-vis des tiers, des dommages causés par cet incendie que s'il est prouvé qu'il doit être attribué à sa faute ou à la faute des personnes dont il est responsable.

Cette disposition ne s'applique pas aux rapports entre propriétaires et locataires, qui demeurent régis par les articles 1733 et 1734 du code civil.

Le père et la mère, en tant qu'ils exercent l'autorité parentale, sont solidairement responsables du dommage causé par leurs enfants mineurs habitant avec eux.

Les maîtres et les commettants, du dommage causé par leurs domestiques et préposés dans les fonctions auxquelles ils les ont employés ;
Chatgpt : "L'employeur est responsable du dommage causé par ses employés dans l'exercice de leurs fonctions."


Les instituteurs et les artisans, du dommage causé par leurs élèves et apprentis pendant le temps qu'ils sont sous leur surveillance.

La responsabilité ci-dessus a lieu, à moins que les père et mère et les artisans ne prouvent qu'ils n'ont pu empêcher le fait qui donne lieu à cette responsabilité.

En ce qui concerne les instituteurs, les fautes, imprudences ou négligences invoquées contre eux comme ayant causé le fait dommageable, devront être prouvées conformément au droit commun, par le demandeur à l'instance.

### 1733 (on parle certainement du propriétaire d'un immeuble)

Il répond de l'incendie, à moins qu'il ne prouve :

Que l'incendie est arrivé par cas fortuit ou force majeure, ou par vice de construction.

Ou que le feu a été communiqué par une maison voisine.

### 1734

S'il y a plusieurs locataires, tous sont responsables de l'incendie, proportionnellement à la valeur locative de la partie de l'immeuble qu'ils occupent ;

A moins qu'ils ne prouvent que l'incendie a commencé dans l'habitation de l'un d'eux, auquel cas celui-là seul en est tenu ;

Ou que quelques-uns ne prouvent que l'incendie n'a pu commencer chez eux, auquel cas ceux-là n'en sont pas tenus.
