Author : Quentin Guellaën
Date : 20/05/2020

Nous, étudiant.e.s en 4SRC, approchons de la fin de notre cursus INSA et naturellement, nous nous sommes demandé.e.s quel rôle nous voulions avoir dans la société,
et quel.le.s ingénieur.e.s nous voudrions être. Notre vision du métier d’ingénieur.e est celle de quelqu’un qui a un impact positif sur le monde en 
répondant à ses problématiques. Nous ne pouvons plus nier l'urgence climatique mondial et l'augmentation de la pollution. 
Ainsi, il a été assez évident pour notre groupe de porter un projet tourné vers l'éco-responsabilité, ou du moins la sensibilisation à la pollution. 
En effet, face au problème de la pollution, troisième cause de mortalité en France, la fenêtre d’action que nous avons est très réduite en temps. 
C'est pourquoi nous avons décidé de créer un dispositif de surveillance de la qualité de l'air.

Ce repository contient l'intégralité du code nécessaire au fonctionnement de l'interface utilisateur tel qu'elle a été présenté lors de la soutenance finale du 06/05/20



Récapitulatif des outils de développement et des versions :

La version de MySQL utilisée a été déterminante pour le choix des versions des autres logiciels et paquets utilisés.

Nous avons utilisés la dernière version stable en date de MySQL : version 8.0.19

Cette version de MySQL n’est compatible qu’avec python version 3.6 ou inférieur.

Nous avons utilisé la dernière version de python compatible : version 3.6.8

Pour ajouter les librairies nécessaires au projet nous utilisons pip : version 20.1.1


Les paquets pip à télécharger sont : 

Click        v 7.0
Flask        v 1.1.1
Flask-MySQLdb v 0.2.0
itsdangerous  v 1.1.0
Jinja2       v 2.10.3
MarkupSafe   v 1.1.1
mysqlclient  v 1.4.6
passlib      v 1.7.2
pip          v 20.1.1
setuptools   v 40.6.2
WTForms     v  2.2.1


La BDD utilisée comporte 4 tables :

capteur1
gps
trajets
users

Elles sont décrite comme suit : 

capteur1 :
+---------+-------+------+-----+---------+----------------+
| Field   | Type  | Null | Key | Default | Extra          |
+---------+-------+------+-----+---------+----------------+
| id      | int   | NO   | PRI | NULL    | auto_increment |
| value10 | float | YES  |     | NULL    |                |
| value25 | float | YES  |     | NULL    |                |
| date    | date  | YES  |     | NULL    |                |
| time    | time  | YES  |     | NULL    |                |
+---------+-------+------+-----+---------+----------------+

gps : 
+-------+-------+------+-----+---------+----------------+
| Field | Type  | Null | Key | Default | Extra          |
+-------+-------+------+-----+---------+----------------+
| id    | int   | NO   | PRI | NULL    | auto_increment |
| lat   | float | YES  |     | NULL    |                |
| lng   | float | YES  |     | NULL    |                |
| time  | time  | YES  |     | NULL    |                |
| date  | date  | YES  |     | NULL    |                |
+-------+-------+------+-----+---------+----------------+

trajets : 
+----------+--------------+------+-----+-------------------+-------------------+
| Field    | Type         | Null | Key | Default           | Extra             |
+----------+--------------+------+-----+-------------------+-------------------+
| id       | int          | NO   | PRI | NULL              | auto_increment    |
| name     | varchar(100) | YES  |     | NULL              |                   |
| date     | timestamp    | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| username | varchar(30)  | YES  |     | NULL              |                   |
| date_beg | date         | YES  |     | NULL              |                   |
| date_end | date         | YES  |     | NULL              |                   |
| time_end | time         | YES  |     | NULL              |                   |
| time_beg | time         | YES  |     | NULL              |                   |
+----------+--------------+------+-----+-------------------+-------------------+

users : 
+---------------+--------------+------+-----+-------------------+-------------------+
| Field         | Type         | Null | Key | Default           | Extra             |
+---------------+--------------+------+-----+-------------------+-------------------+
| id            | int          | NO   | PRI | NULL              | auto_increment    |
| name          | varchar(100) | YES  |     | NULL              |                   |
| email         | varchar(100) | YES  |     | NULL              |                   |
| register_date | timestamp    | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| username      | varchar(30)  | YES  |     | NULL              |                   |
| password      | varchar(100) | YES  |     | NULL              |                   |
+---------------+--------------+------+-----+-------------------+-------------------+


L’interface utilise l’outil de cartographie de google : Google maps API. C’est une API gratuite pour de petits projet tels que celui-ci. 
Nous disposons d’une clé unique qui nous permet d’exploiter les fonctionnalités. Cependant elle est rattaché à un compte google privé. 
Il sera sûrement nécessaire à l’avenir d’obtenir une clé publique pour que le projet ne dépende plus d’un compte privé. 
L’API KEY est pour le moment : AIzaSyDUBqBVIz2K2vN9D0-Tm9GiZ7-xw8h95C4

Nous avons aussi utilisé du content delivery network grâce à BootstrapCDN. Son utilisation est bien documentée sur : https://getbootstrap.com/docs/4.3/getting-started/introduction/





