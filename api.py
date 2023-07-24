import json, requests, socket
TIMEOUT = 60 * 3

class API:   

    def __init__(self):
        super(API, self).__init__()
        self.server = None

    def setServer(self, server):
        self.server = "{0}".format(server)

    def getServer(self):
        return self.server

    def httpGet(self, url): 
        headers = {}
        session = requests.Session()
        session.trust_env = False
        response = session.get(url, headers=headers, timeout=TIMEOUT)
        self.checkError(response)
        return response

    def checkError(self, response):
        if response.status_code == 404:
            raise Exception('Servidor não encontrado!')
        if response.status_code == 413:
            raise Exception('Request Entity Too Large!')
        if response.status_code == 504:
            raise Exception('Tempo excedido!')
        if response.status_code == 403:
            raise Exception('Token expirado, faça o login novamente!')
        if not response.ok:
            raise Exception(response.json()['message'])

    #http://10.25.163.10:1337/uploads/rotacao_edif_bda057872b.PNG
    def getNews(self):
        response = self.httpGet(
            url="{0}/atualizacoes".format(self.getServer())
        )
        if response:
            return response.json()
        return {}