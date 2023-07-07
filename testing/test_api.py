import pytest 
import unittest

import requests
import json



#TestCase : un scénario de test est créé comme une classe fille
# les tests individuels sont défnis par des méthodes dont les noms commencent par test_: 
    # test_exist_file : exitence de fichier

 # Le coeur de chq test est une appel à assertEqual pour vérifier un résultat attendu : assertTrue ou assertFalse ou 
 # assertRAise pour vérifier qu'une exception particulière est levée
class TestAPI(unittest.TestCase):
    URL = "https://oc-api-flask-mh.onrender.com"


    def test_get_all(self):
        # ...
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)

    def test_get_list_id(self):
        # ...
        resp = requests.get(self.URL + "/api/list_id/")
        self.assertEqual(resp.status_code, 200)

    def test_get_feat_desc(self):
        # ...
        resp = requests.get(self.URL + "/api/feat_desc")
        self.assertEqual(resp.status_code, 200)

    def test_get_data_cust(self):
        # ...
        resp = requests.get(self.URL + "/api/get_data_cust/?SK_ID_CURR=100042")
        self.assertEqual(resp.status_code, 200)

    def test_get_mean(self):
        # ...
        resp = requests.get(self.URL + "/api/mean/")
        self.assertEqual(resp.status_code, 200)

    def test_get_scoring_cust(self):
        # ...
        resp = requests.get(self.URL + "/api/scoring_cust/?SK_ID_CURR=100067")
        self.assertEqual(resp.status_code, 200)   

    def test_get_feat_imp(self):
        # ...
        resp = requests.get(self.URL + "/api/feat_imp")
        self.assertEqual(resp.status_code, 200)  

    def test_get_neigh(self):
        # ...
        resp = requests.get(self.URL + "/api/neigh_cust/?SK_ID_CURR=100038")
        self.assertEqual(resp.status_code, 200)  

if __name__ == "__main__":
    tester = TestAPI()
    #unittest.main(verbosity=2)
