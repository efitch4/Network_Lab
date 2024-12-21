from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        pass
    
    def footer(self):
        pass
        
    def chapter_title(self,num,label):
        pass
    
    def chapter_body(self, filepath):
        with open(filepath,"rb") as fh:
                txt = fh.read().decode('latin-1')
        self.set_font("Times",size =12)
        self.multi_cell(0, 5, txt)
        self.ln()
        self.set_font(family="times",style="I",size=0)
        self.cell(0,5, "End of excerpt")
        

    def print_chapter(self, filepath,output_file):
       self.add_page()
       self.chapter_body(filepath)
       self.output(output_file)
       
           
pdf = PDF()
#This creates one chapter
pdf.print_chapter("para.txt","sample.pdf")
# pdf.output("sample.pdf")