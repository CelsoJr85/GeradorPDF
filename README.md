# Gerador de PDF Python 🐍📄

Uma biblioteca completa para gerar PDFs a partir de textos, dados de cadastro e converter diferentes tipos de arquivos para PDF.

## 🚀 Instalação

### 1. Clone ou baixe os arquivos
```bash
git clone https://github.com/CelsoJr85/GeradorPDF
cd gerador-pdf
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute o exemplo
```bash
python gerador_pdf.py
```

## 📋 Funcionalidades

- ✅ Gerar PDF de textos simples
- ✅ Criar PDFs de dados de cadastro
- ✅ Gerar PDFs com tabelas formatadas
- ✅ Converter TXT para PDF
- ✅ Converter CSV para PDF (como tabela)
- ✅ Converter DOCX para PDF
- ✅ Templates customizáveis
- ✅ Formatação automática
- ✅ Suporte a caracteres especiais (UTF-8)

## 🔧 Como Usar

### Uso Básico

```python
from gerador_pdf import GeradorPDF

# Criar uma instância
gerador = GeradorPDF()

# Gerar PDF de texto simples
texto = "Meu conteúdo aqui..."
gerador.gerar_pdf_texto(texto, "meu_documento.pdf", "Título do Documento")
```

### Funções Auxiliares (Mais Simples)

```python
from gerador_pdf import criar_pdf_simples, salvar_cadastro_como_pdf, converter_arquivo_para_pdf

# PDF simples
criar_pdf_simples("Meu texto", "documento.pdf", "Título")

# Salvar cadastro
dados = {'nome': 'João', 'email': 'joao@email.com'}
salvar_cadastro_como_pdf(dados, "cadastro.pdf")

# Converter arquivo
converter_arquivo_para_pdf("documento.txt")
```

## 💡 Exemplos Práticos

### 1. PDF de Texto Simples

```python
gerador = GeradorPDF()

texto = """
Relatório Mensal - Janeiro 2025

Este relatório apresenta os resultados do mês de janeiro.

Principais conquistas:
- Aumento de 15% nas vendas
- Melhoria na satisfação do cliente
- Implementação de novo sistema

Próximos passos:
- Expansão para novos mercados
- Treinamento da equipe
- Otimização de processos
"""

gerador.gerar_pdf_texto(texto, "relatorio_janeiro.pdf", "Relatório Mensal")
```

### 2. Cadastro de Cliente

```python
# Dados do cliente
cliente = {
    'nome': 'Maria Silva Santos',
    'cpf': '123.456.789-00',
    'rg': '12.345.678-9',
    'data_nascimento': '15/03/1985',
    'email': 'maria.santos@email.com',
    'telefone': '(11) 98765-4321',
    'endereco': 'Rua das Flores, 123, Apt 45',
    'cidade': 'São Paulo',
    'estado': 'SP',
    'cep': '01234-567'
}

# Gerar PDF com template específico
gerador.gerar_pdf_formulario(cliente, "cadastro_maria.pdf", "cadastro_pessoa")
```

### 3. Relatório com Tabela

```python
# Dados de vendas
vendas = [
    ['Produto', 'Quantidade', 'Valor Unit.', 'Total'],
    ['Notebook Dell', '5', 'R$ 2.500,00', 'R$ 12.500,00'],
    ['Mouse Wireless', '20', 'R$ 45,00', 'R$ 900,00'],
    ['Teclado Mecânico', '10', 'R$ 150,00', 'R$ 1.500,00'],
    ['Monitor 24"', '8', 'R$ 800,00', 'R$ 6.400,00']
]

gerador.gerar_pdf_tabela(vendas, "relatorio_vendas.pdf", "Relatório de Vendas - Janeiro 2025")
```

### 4. Converter Arquivos

```python
# Converter diferentes tipos de arquivo
gerador.converter_txt_para_pdf("ata_reuniao.txt", "ata_reuniao.pdf")
gerador.converter_csv_para_pdf("dados_clientes.csv", "relatorio_clientes.pdf")
gerador.converter_docx_para_pdf("proposta_comercial.docx", "proposta_comercial.pdf")
```

## 🎨 Customização

### Personalizando Estilos

```python
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

class MeuGeradorPDF(GeradorPDF):
    def __init__(self):
        super().__init__()
        
        # Criar estilo personalizado
        self.estilo_destaque = ParagraphStyle(
            'Destaque',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.blue,
            spaceAfter=15,
            fontName='Helvetica-Bold'
        )
    
    def gerar_pdf_personalizado(self, conteudo, nome_arquivo):
        # Use self.estilo_destaque nos seus parágrafos
        pass
```

### Adicionando Logo ou Imagens

```python
from reportlab.platypus import Image

def adicionar_logo(self, story):
    try:
        logo = Image("logo.png", width=2*inch, height=1*inch)
        story.append(logo)
        story.append(Spacer(1, 12))
    except:
        pass  # Logo não encontrado
```

### Criando Templates Personalizados

```python
def gerar_pdf_contrato(self, dados_contrato, nome_arquivo):
    doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
    story = []
    
    # Cabeçalho
    story.append(Paragraph("CONTRATO DE PRESTAÇÃO DE SERVIÇOS", self.styles['Title']))
    story.append(Spacer(1, 20))
    
    # Partes do contrato
    story.append(Paragraph("CONTRATANTE:", self.styles['Heading2']))
    story.append(Paragraph(dados_contrato['contratante'], self.custom_style))
    
    story.append(Paragraph("CONTRATADO:", self.styles['Heading2']))
    story.append(Paragraph(dados_contrato['contratado'], self.custom_style))
    
    # Cláusulas
    for i, clausula in enumerate(dados_contrato['clausulas'], 1):
        titulo = f"CLÁUSULA {i}ª"
        story.append(Paragraph(titulo, self.styles['Heading2']))
        story.append(Paragraph(clausula, self.custom_style))
        story.append(Spacer(1, 10))
    
    doc.build(story)
```

### Configurações de Página

```python
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import cm

# Customizar margens
doc = SimpleDocTemplate(
    nome_arquivo,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm
)
```

## 🔄 Casos de Uso Comuns

### 1. Sistema de Cadastro

```python
def processar_cadastro(dados_formulario):
    # Validar dados
    if not dados_formulario.get('nome'):
        return False, "Nome é obrigatório"
    
    # Salvar no banco de dados
    # ... código do banco ...
    
    # Gerar PDF
    nome_arquivo = f"cadastro_{dados_formulario['nome'].replace(' ', '_')}.pdf"
    gerador = GeradorPDF()
    sucesso = gerador.gerar_pdf_formulario(dados_formulario, nome_arquivo, "cadastro_pessoa")
    
    return sucesso, nome_arquivo
```

### 2. Relatórios Automáticos

```python
def gerar_relatorio_mensal():
    from datetime import datetime
    
    # Buscar dados do mês
    dados = buscar_dados_mes_atual()
    
    # Gerar nome do arquivo
    mes_ano = datetime.now().strftime("%m_%Y")
    nome_arquivo = f"relatorio_{mes_ano}.pdf"
    
    # Criar PDF
    gerador = GeradorPDF()
    gerador.gerar_pdf_tabela(dados, nome_arquivo, f"Relatório Mensal - {mes_ano}")
    
    return nome_arquivo
```

### 3. Conversão em Lote

```python
import os

def converter_pasta_para_pdf(pasta_origem):
    gerador = GeradorPDF()
    arquivos_convertidos = []
    
    for arquivo in os.listdir(pasta_origem):
        if arquivo.endswith(('.txt', '.csv', '.docx')):
            caminho_completo = os.path.join(pasta_origem, arquivo)
            sucesso = converter_arquivo_para_pdf(caminho_completo)
            
            if sucesso:
                arquivos_convertidos.append(arquivo)
    
    return arquivos_convertidos
```

## ⚙️ Configurações Avançadas

### Formatação de Datas

```python
from datetime import datetime

def formatar_data_brasileira(data):
    return data.strftime("%d/%m/%Y")

def adicionar_rodape_com_data(story):
    data_atual = formatar_data_brasileira(datetime.now())
    rodape = f"Documento gerado em {data_atual}"
    story.append(Spacer(1, 20))
    story.append(Paragraph(rodape, self.styles['Normal']))
```

### Numeração de Páginas

```python
from reportlab.platypus import PageBreak

class NumerosPagina:
    def __init__(self, canvas, doc):
        self.canvas = canvas
        self.doc = doc
    
    def draw(self):
        # Adicionar número da página
        page_num = self.canvas.getPageNumber()
        text = f"Página {page_num}"
        self.canvas.drawRightString(200*mm, 20*mm, text)
```

## 🐛 Solução de Problemas

### Problema: Erro de encoding
**Solução:** Certifique-se de que seus arquivos estão em UTF-8
```python
with open('arquivo.txt', 'r', encoding='utf-8') as f:
    conteudo = f.read()
```

### Problema: PDF não abre
**Solução:** Verifique se o arquivo foi criado completamente
```python
import os
if os.path.exists(nome_arquivo) and os.path.getsize(nome_arquivo) > 0:
    print("PDF criado com sucesso!")
```

### Problema: Tabela muito larga
**Solução:** Ajuste o tamanho das colunas
```python
tabela = Table(dados, colWidths=[2*inch, 1*inch, 1.5*inch])
```

## 📝 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar e modificar conforme necessário.

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📞 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique se todas as dependências estão instaladas
2. Consulte a seção de solução de problemas
3. Abra uma issue no repositório

---

**Desenvolvido com ❤️ em Python**
