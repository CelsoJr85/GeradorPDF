import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
import json
import csv
from docx import Document
from PIL import Image
import pandas as pd


class GeradorPDF:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_style = ParagraphStyle(
            'Custom',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            encoding='utf-8'
        )

    def gerar_pdf_texto(self, texto, nome_arquivo, titulo=None):
        """
        Gera PDF a partir de texto simples

        Args:
            texto (str): Texto para incluir no PDF
            nome_arquivo (str): Nome do arquivo PDF a ser criado
            titulo (str): Título opcional para o documento
        """
        try:
            doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
            story = []

            # Adiciona título se fornecido
            if titulo:
                titulo_style = ParagraphStyle(
                    'Titulo',
                    parent=self.styles['Heading1'],
                    fontSize=16,
                    spaceAfter=12,
                    alignment=1  # Centralizado
                )
                story.append(Paragraph(titulo, titulo_style))
                story.append(Spacer(1, 12))

            # Adiciona o texto
            paragrafos = texto.split('\n')
            for paragrafo in paragrafos:
                if paragrafo.strip():
                    story.append(Paragraph(paragrafo, self.custom_style))
                else:
                    story.append(Spacer(1, 6))

            doc.build(story)
            print(f"PDF criado com sucesso: {nome_arquivo}")
            return True

        except Exception as e:
            print(f"Erro ao criar PDF: {str(e)}")
            return False

    def gerar_pdf_cadastro(self, dados_cadastro, nome_arquivo):
        """
        Gera PDF a partir de dados de cadastro

        Args:
            dados_cadastro (dict): Dicionário com dados do cadastro
            nome_arquivo (str): Nome do arquivo PDF
        """
        try:
            doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
            story = []

            # Título
            titulo = Paragraph("RELATÓRIO DE CADASTRO", self.styles['Title'])
            story.append(titulo)
            story.append(Spacer(1, 12))

            # Data de geração
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            data_para = Paragraph(f"Gerado em: {data_atual}", self.styles['Normal'])
            story.append(data_para)
            story.append(Spacer(1, 20))

            # Dados do cadastro
            for chave, valor in dados_cadastro.items():
                linha = f"<b>{chave.upper()}:</b> {valor}"
                story.append(Paragraph(linha, self.custom_style))
                story.append(Spacer(1, 6))

            doc.build(story)
            print(f"PDF de cadastro criado: {nome_arquivo}")
            return True

        except Exception as e:
            print(f"Erro ao criar PDF de cadastro: {str(e)}")
            return False

    def gerar_pdf_tabela(self, dados_tabela, nome_arquivo, titulo="Relatório de Dados"):
        """
        Gera PDF com dados em formato de tabela

        Args:
            dados_tabela (list): Lista de listas com dados da tabela
            nome_arquivo (str): Nome do arquivo PDF
            titulo (str): Título do relatório
        """
        try:
            doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
            story = []

            # Título
            story.append(Paragraph(titulo, self.styles['Title']))
            story.append(Spacer(1, 12))

            # Tabela
            tabela = Table(dados_tabela)
            tabela.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            story.append(tabela)
            doc.build(story)
            print(f"PDF com tabela criado: {nome_arquivo}")
            return True

        except Exception as e:
            print(f"Erro ao criar PDF com tabela: {str(e)}")
            return False

    def converter_txt_para_pdf(self, arquivo_txt, nome_pdf=None):
        """
        Converte arquivo TXT para PDF
        """
        try:
            if nome_pdf is None:
                nome_pdf = arquivo_txt.replace('.txt', '.pdf')

            with open(arquivo_txt, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()

            return self.gerar_pdf_texto(conteudo, nome_pdf, "Documento Convertido")

        except Exception as e:
            print(f"Erro ao converter TXT para PDF: {str(e)}")
            return False

    def converter_csv_para_pdf(self, arquivo_csv, nome_pdf=None):
        """
        Converte arquivo CSV para PDF
        """
        try:
            if nome_pdf is None:
                nome_pdf = arquivo_csv.replace('.csv', '.pdf')

            # Lê o CSV
            df = pd.read_csv(arquivo_csv)

            # Converte para lista de listas
            dados = [df.columns.tolist()] + df.values.tolist()

            return self.gerar_pdf_tabela(dados, nome_pdf, "Dados do CSV")

        except Exception as e:
            print(f"Erro ao converter CSV para PDF: {str(e)}")
            return False

    def converter_docx_para_pdf(self, arquivo_docx, nome_pdf=None):
        """
        Converte arquivo DOCX para PDF (extrai apenas o texto)
        """
        try:
            if nome_pdf is None:
                nome_pdf = arquivo_docx.replace('.docx', '.pdf')

            # Lê o documento Word
            doc = Document(arquivo_docx)
            texto_completo = []

            for paragrafo in doc.paragraphs:
                texto_completo.append(paragrafo.text)

            conteudo = '\n'.join(texto_completo)
            return self.gerar_pdf_texto(conteudo, nome_pdf, "Documento Word Convertido")

        except Exception as e:
            print(f"Erro ao converter DOCX para PDF: {str(e)}")
            return False

    def gerar_pdf_formulario(self, dados_formulario, nome_arquivo, template="padrao"):
        """
        Gera PDF formatado a partir de dados de formulário

        Args:
            dados_formulario (dict): Dados do formulário
            nome_arquivo (str): Nome do arquivo PDF
            template (str): Tipo de template a usar
        """
        try:
            doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
            story = []

            if template == "cadastro_pessoa":
                # Template específico para cadastro de pessoa
                story.append(Paragraph("FICHA DE CADASTRO PESSOAL", self.styles['Title']))
                story.append(Spacer(1, 20))

                # Dados pessoais
                story.append(Paragraph("DADOS PESSOAIS", self.styles['Heading2']))
                story.append(Spacer(1, 12))

                campos_pessoais = ['nome', 'cpf', 'rg', 'data_nascimento', 'email', 'telefone']
                for campo in campos_pessoais:
                    if campo in dados_formulario:
                        texto = f"<b>{campo.replace('_', ' ').title()}:</b> {dados_formulario[campo]}"
                        story.append(Paragraph(texto, self.custom_style))
                        story.append(Spacer(1, 6))

                # Endereço
                story.append(Spacer(1, 20))
                story.append(Paragraph("ENDEREÇO", self.styles['Heading2']))
                story.append(Spacer(1, 12))

                campos_endereco = ['endereco', 'cidade', 'estado', 'cep']
                for campo in campos_endereco:
                    if campo in dados_formulario:
                        texto = f"<b>{campo.replace('_', ' ').title()}:</b> {dados_formulario[campo]}"
                        story.append(Paragraph(texto, self.custom_style))
                        story.append(Spacer(1, 6))

            else:
                # Template padrão
                story.append(Paragraph("RELATÓRIO DE DADOS", self.styles['Title']))
                story.append(Spacer(1, 20))

                for chave, valor in dados_formulario.items():
                    texto = f"<b>{chave.replace('_', ' ').title()}:</b> {valor}"
                    story.append(Paragraph(texto, self.custom_style))
                    story.append(Spacer(1, 8))

            # Rodapé com data
            story.append(Spacer(1, 30))
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            rodape = f"Documento gerado em {data_atual}"
            story.append(Paragraph(rodape, self.styles['Normal']))

            doc.build(story)
            print(f"PDF de formulário criado: {nome_arquivo}")
            return True

        except Exception as e:
            print(f"Erro ao criar PDF de formulário: {str(e)}")
            return False


# Funções auxiliares para uso direto
def criar_pdf_simples(texto, nome_arquivo, titulo=None):
    """Função simples para criar PDF de texto"""
    gerador = GeradorPDF()
    return gerador.gerar_pdf_texto(texto, nome_arquivo, titulo)


def salvar_cadastro_como_pdf(dados, nome_arquivo):
    """Função para salvar dados de cadastro como PDF"""
    gerador = GeradorPDF()
    return gerador.gerar_pdf_cadastro(dados, nome_arquivo)


def converter_arquivo_para_pdf(arquivo_origem, tipo_arquivo=None):
    """Função genérica para converter arquivos para PDF"""
    gerador = GeradorPDF()

    if tipo_arquivo is None:
        # Detecta o tipo pela extensão
        extensao = arquivo_origem.split('.')[-1].lower()
    else:
        extensao = tipo_arquivo.lower()

    if extensao == 'txt':
        return gerador.converter_txt_para_pdf(arquivo_origem)
    elif extensao == 'csv':
        return gerador.converter_csv_para_pdf(arquivo_origem)
    elif extensao == 'docx':
        return gerador.converter_docx_para_pdf(arquivo_origem)
    else:
        print(f"Tipo de arquivo não suportado: {extensao}")
        return False


# Exemplo de uso
if __name__ == "__main__":
    # Cria uma instância do gerador
    gerador = GeradorPDF()

    # Exemplo 1: PDF de texto simples
    texto_exemplo = """
    Este é um exemplo de texto que será convertido em PDF.

    O texto pode conter múltiplos parágrafos e será formatado
    automaticamente no documento PDF.

    Esta é uma ferramenta útil para gerar documentos rapidamente.
    """

    gerador.gerar_pdf_texto(texto_exemplo, "exemplo_texto.pdf", "Documento de Exemplo")

    # Exemplo 2: PDF de cadastro
    dados_pessoa = {
        'nome': 'João Silva',
        'cpf': '123.456.789-00',
        'email': 'joao@email.com',
        'telefone': '(11) 99999-9999',
        'endereco': 'Rua das Flores, 123',
        'cidade': 'São Paulo',
        'estado': 'SP'
    }

    gerador.gerar_pdf_formulario(dados_pessoa, "cadastro_joao.pdf", "cadastro_pessoa")

    # Exemplo 3: PDF com tabela
    dados_tabela = [
        ['Nome', 'Idade', 'Cidade'],
        ['Ana', '25', 'Rio de Janeiro'],
        ['Pedro', '30', 'São Paulo'],
        ['Maria', '28', 'Belo Horizonte']
    ]

    gerador.gerar_pdf_tabela(dados_tabela, "tabela_exemplo.pdf", "Lista de Pessoas")

    print("Exemplos de PDF criados com sucesso!")