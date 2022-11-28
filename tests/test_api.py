import requests

###############################################################################
#                                                                             #
#                                                                             #
#                                Constantes                                   #
#                                                                             #
#                                                                             #
###############################################################################

# "scheme" : le protocol a utiliser pour les requette
scheme = "http://"

# "baseUrl" : url racine du serveur web
baseUrl = "truthseeker.simailadjalim.fr"

# "url" : url qui sera utilisé pour les requettes de test
url = scheme+baseUrl

# page d'accueil
accueil = "/"





def test_que_la_page_daccueil_existe():
    page = requests.get(url+accueil)
    assert page.status_code == 200

def test_que_la_page_de_mentions_legales_existe():
    page = requests.get(url+mentionsLegales)
    assert page.status_code == 200

def test_que_la_page_de_contact_existe():
    page = requests.get(url+pageDeContact)
    assert page.status_code == 200

