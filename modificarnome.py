import os
from PIL import Image

pasta_exemplos = 'C:/Users/WorkStation/Desktop/exemplos'


extensoes_imagem = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')


contador = 1

for arquivo in os.listdir(pasta_exemplos):
    caminho_arquivo = os.path.join(pasta_exemplos, arquivo)
    
    
    if arquivo.lower().endswith(extensoes_imagem) and os.path.isfile(caminho_arquivo):
        try:
           
            imagem = Image.open(caminho_arquivo)
            
            
            imagem = imagem.convert('RGB')
            
            
            novo_nome = f'placa{contador}.jpg'
            novo_caminho = os.path.join(pasta_exemplos, novo_nome)
            
           
            imagem.save(novo_caminho)
            print(f'Imagem {arquivo} renomeada e salva como {novo_nome}')
            
          
            os.remove(caminho_arquivo)
            
          
            contador += 1
        except Exception as e:
            print(f'Erro ao processar {arquivo}: {e}')
