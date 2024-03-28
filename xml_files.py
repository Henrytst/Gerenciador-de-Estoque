import os
import xml.etree.ElementTree as Et
from datetime import date
from pathlib import Path

# Obtendo o caminho do diretório do script
base_path = Path(__file__).resolve().parent

class Read_xml():
    def __init__(self,directory) -> None:
        self.directory = directory

    def all_files(self):

        return [ os.path.join(self.directory, arq) for arq in os.listdir(self.directory)
        if arq.lower().endswith(".xml")]
    
    def nfe_data(self, xml):

        root = Et.parse(xml).getroot()
        nsNFe = {"ns": "http://www.portalfiscal.inf.br/nfe"}

        #DADOS DA NFE
        NFe = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:nNF", nsNFe))
        serie = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:serie", nsNFe))
        data_emissao = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:dhEmi", nsNFe))
        data_emissao = F"{data_emissao[8:10]}/{data_emissao[5:7]}/{data_emissao[:4]}"

        #DADOS EMITENTES
        chave = self.check_none(root.find("./ns:protNFe/ns:infProt/ns:chNFe", nsNFe))
        cnpj_emitente = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:emit/ns:CNPJ", nsNFe))
        nome_emitente = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:emit/ns:xNome", nsNFe))

        cnpj_emitente = self.format_cnpj(cnpj_emitente)
        valorNfe = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vNF", nsNFe))
        data_importacao = date.today()
        data_importacao = data_importacao.strftime('%d/%m/%Y')
        data_saida = ""
        usuario = ''

        itemNota = 1
        notas = []

        for item in root.findall("./ns:NFe/ns:infNFe/ns:det", nsNFe):
             # DADOS DO ITEM =======================================================================================
            cod = self.check_none(item.find(".ns:prod/ns:cProd", nsNFe)) 
            qntd = self.check_none(item.find(".ns:prod/ns:qCom", nsNFe))  
            descricao = self.check_none(item.find(".ns:prod/ns:xProd", nsNFe))
            unidade_medida = self.check_none(item.find(".ns:prod/ns:uCom", nsNFe))
            valorProd = self.check_none(item.find (".ns:prod/ns:vProd", nsNFe))

            dados = [NFe, serie, data_emissao,chave, cnpj_emitente, nome_emitente,
             valorNfe, itemNota,  cod, qntd, descricao, unidade_medida, valorProd,
             data_importacao, usuario, data_saida]

            notas.append(dados)
            itemNota +=1
        return notas

    def check_none(self, var):
        if var == None:
            return ""
        else:
            try:
                return var.text.replace('.',',')
            except:
                var.text

    def format_cnpj(self, cnpj):
        try:
            cnpj = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}.'
            return cnpj
        
        except:
            return ""

if __name__ == "__main__":
    xml = Read_xml(base_path / 'arq')
    all = xml.all_files()

    for i in all:
        result = xml.nfe_data(i)

    print(result)

    print(xml)