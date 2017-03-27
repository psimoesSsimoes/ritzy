from pymongo import MongoClient
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# Rules
# if number+g we want the word after de
# if colher de sopa bem cheia de we want the word after de
# if colher de sopa de we want the word after de
# but if the word after de is molho and exists other word after we want two words
# if colheres de sopa de we wnat word after de
# if contains


# **vaca
# Cachaço
# Maça do peito
# Pá, agulha, peito alto
# Chambão
# Coberta do acém, acém comprido
# Prego do peito, aba da costela
# Rosbife, acém, redondo, vazia, entrecôte
# Lombo
# Aba grossa
# Cheio da alcatra
# Alcatra
# Pojadouro, ganso, rabadilha
# Aba delgada
#**porco
# Toucinho
# Pá,
# costeletas
# Costeletas com pé, a parte central do dorso
# lombo
# Entremeada
# toucinho
# entrecosto
