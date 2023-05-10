from django.views import View
from django.views.generic import TemplateView
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render

### ------ reportlab imports ------ ###
from reportlab.platypus import Paragraph, Table, TableStyle, LongTable
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from reportlab.lib import colors
from ..printer_data import *

styles = getSampleStyleSheet()
set_fonts()
styleErro = ParagraphStyle('erro',
                           fontSize=20,
                           textColor="Red",
                           parent=styles['Normal'],
                           alignment=1,
                           spaceBefore=0,
                           spaceAfter=14)

styleTitulo = ParagraphStyle('titulo',
                           fontSize=16,
                           parent=styles['Normal'],
                           alignment=1,
                           spaceBefore=10,
                           spaceAfter=16)


styleTableBairro = TableStyle([('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                               ('BOTTOMPADDING', (0, 0), (0, -1), 6),

                               ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                               ('FONTNAME', (0, 0), (-1, 0), 'ArialN'),

                               # posições são baseadas matriz
                               # posição M[2][0] até M[2][-1]. -1 faz referencia ao fim
                               ('SPAN', (2, 0), (2, -1)),  # faz o span em uma coluna
                               ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                               ('ALIGN', (4, 0), (4, -1), 'CENTER'),

                               ('FONTSIZE', (0, 0), (-1, -1), 12),
                               ('FONTSIZE', (0, 0), (-1, 0), 14),
                               ('TEXTCOLOR', (0, 0), (1, -1), colors.black)]
                              )


styleTableNormal = [('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('FONTNAME', (0, 0), (-1, 0), 'ArialN'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Arial'),

                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                    ('BOTTOMPADDING', (0, 0), (0, -1), 6),
                    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('RIGHTPADDING', (0, 0), (0, -1), 20),
                    ('LEFTPADDING', (1, 0), (1, -1), 20),
                    ('FONTSIZE', (0, 0), (-1, -1), 12),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('TEXTCOLOR', (0, 0), (1, -1), colors.black)]


styleTableReferencia = [('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('FONTNAME', (0, 0), (-1, 0), 'ArialN'),
                        ('BOTTOMPADDING', (0, 0), (0, -1), 6),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                        ('LEFTPADDING', (0, 0), (-1, -1), 3),
                        ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),


                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('FONTSIZE', (0, 0), (-1, 0), 11),
                        ('TEXTCOLOR', (0, 0), (1, -1), colors.black)]


styleFicha = [('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('FONTNAME', (0, 1), (-1, -1), 'Arial'),

                        # ('FONTNAME', (4, 0), (4, 0), 'ArialN'),

                        ('SPAN', (1, 0), (2, 0)), # nome

                        ('SPAN', (4, 0), (5, 0)),  #apelido
                        ('SPAN', (0, 4), (1, 4)),  #Labe cor raca
                        ('SPAN', (4, 4), (5, 4)), # escolaridade
                        ('SPAN', (0, 5), (1, 5)),  #Labe trabalho
                        ('SPAN', (4, 5), (5, 5)), # renda

                        ('BOTTOMPADDING', (0, 0), (0, -1), 6),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                        ('LEFTPADDING', (0, 0), (-1, -1), 6),

                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),


                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),

                        ('FONTSIZE', (0, 0), (-1, -1), 12),
                        
                        ('TEXTCOLOR', (0, 0), (1, -1), colors.black)]


@method_decorator(login_required, name='dispatch')
class PrinterTableView(View):
    def get(self, request, *args, **kwargs):
        argumento = self.kwargs['filter']
        # print(argumento)
        data = []
        text = []
        if argumento == "por_bairros":
            data = printer_total_bairro()
            tabela = Table(data)
            tabela.setStyle(styleTableBairro)
            text.append(tabela)
        elif argumento == "por_ruc":
            data = printer_total_ruc()
            tabela = Table(data)
            tabela.setStyle(styleTableNormal)
            text.append(tabela)
        elif argumento == "por_cras":
            data = printer_total_cras()
            tabela = Table(data)
            tabela.setStyle(styleTableNormal)
            text.append(tabela)
        elif argumento == "tudo":
            data1 = printer_total_bairro()
            data2 = printer_total_ruc()
            data3 = printer_total_cras()

            tabela1 = Table(data1)
            tabela2 = Table(data2)
            tabela3 = Table(data3)
            tabela1.setStyle(styleTableBairro)
            tabela2.setStyle(styleTableNormal)
            tabela3.setStyle(styleTableNormal)
            espaco = Paragraph(f"<br/>", styleErro)
            text = [tabela1, espaco, tabela2, espaco, tabela3]

        elif argumento == "referencias":
            data = printer_referecias()
            tabela = LongTable(data, colWidths=[35, 165, 110, 145, 85],repeatRows=1)
            tabela.setStyle(styleTableReferencia)
            text.append(tabela)
        else:
            text.append(Paragraph(f"ERRO na geração do documento", styleErro))
        buffer = gerar_doc(text)
        
        return FileResponse(buffer, filename=f'termo_entrega_orgão.pdf')




@method_decorator(login_required, name='dispatch')
class PrinterReferenciasTableView(TemplateView):
    template_name = 'cadastros/forms/form_printer.html'
    def get(self, request, *args, **kwargs):
        bairros = Bairro.objects.select_related().all()
        context = {"bairros":bairros}
        return render(request, self.template_name,context) #FileResponse(buffer, filename=f'termo_entrega_orgão.pdf')
    
    def post(self, request, *args, **kwargs):
        # print(request.POST)
        cras = request.POST['cras'] if request.POST['cras'] != '-------' else "Todos"
        bairro = request.POST['bairro'] if request.POST['bairro'] != '' else "Todos"
        ruc = request.POST['ruc'] if request.POST['ruc'] != '-------' else "Todos"
        lista_cadastro = []
        if not cras and not bairro and not ruc:
            
            data = printer_referecias()
        else:
            print("Filtro")
            cadastros = Cadastro.objects.select_related().all()
            print(len(cadastros))
            if bairro != "Todos" and cras !="Todos" and ruc !="Todos":
                cadastros = cadastros.filter(endereco__bairro__nome=bairro, abrangencia=cras, endereco__ruc=ruc)
            elif cras !="Todos" and bairro != "Todos":
                cadastros = cadastros.filter(abrangencia=cras, endereco__bairro__nome=bairro,)
               
            elif cras !="Todos" and ruc != "Todos":
                cadastros = cadastros.filter(abrangencia=cras, endereco__ruc=ruc)
            elif ruc !="Todos" and bairro != "Todos":
                cadastros = cadastros.filter(endereco__ruc=ruc,endereco__bairro__nome=bairro,)
            
            elif ruc !="Todos":
                cadastros = cadastros.filter(endereco__ruc=ruc)
            elif cras !="Todos" and ruc != "Todos":
                cadastros = cadastros.filter(abrangencia=cras)
            elif bairro != "Todos":
                cadastros = cadastros.filter(endereco__bairro__nome=bairro)
            
               
            print(len(cadastros))
            data = printer_referecias(cadastros)
        text = []
        tabela = LongTable(data, colWidths=[35, 160, 120,70, 85, 90],repeatRows=1)
        tabela.setStyle(styleTableReferencia)
        text.append(tabela)
        
        if not data:
            text.append(Paragraph(f"ERRO na geração do documento", styleErro))
        buffer = gerar_doc(text)
        
        return FileResponse(buffer, filename=f'termo_entrega_orgão.pdf')
        

@method_decorator(login_required, name='dispatch')
class PrinterFichaView(View):
    def get(self, request, *args, **kwargs):
        argumento = self.kwargs['pk']
        
        data = printer_ficha(self.kwargs['pk'])
        text = []
        text.append(Paragraph(f"<b>Ficha Cadastral</b>", styleTitulo))
        if data:
            # data = printer_referecias()
            tabela = Table(data, colWidths=[65, 100, 110, 95, 70, 90])
            tabela.setStyle(styleFicha)
            text.append(tabela)
        else:
            text.append(Paragraph(f"ERRO na geração do documento", styleErro))
        buffer = gerar_doc(text, "Ficha - Dados Cadastrais")
        
        return FileResponse(buffer, filename=f'termo_entrega_orgão.pdf')