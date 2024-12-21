from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
         self.set_font("helvetica","B",15)
         width = self.get_string_width(self.title)+6
         self.set_x((210-width)/2)
         self.set_draw_color(0,80,180)
         self.set_fill_color(230,230,0)
         self.set_text_color(220,50,50)
         self.set_line_width(1)
         self.cell(width,9,self.title,align="C",fill=True)
         self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica","I",12)
        self.set_text_color(128)
        self.cell(0,10,f"Page{self.page_no()}", align="C")

    def chapter_title(self,num,label):
        self.set_font("helvetica","",12)
        self.set_fill_color(200,220,255)
        self.cell(0,6,f"Chapter {num} : {label}",align="L",fill=True)
        self.ln(8)

    def chapter_body(self, filepath):
        with open(filepath,"rb") as fh:
                txt = fh.read().decode('latin-1')
        self.set_font("Times",size =12)
        self.multi_cell(0, 5, txt)
        self.ln()
        self.set_font("Times",style="I",size=12)
        self.cell(0,5, "End of excerpt")
        self.ln()

    def print_chapter(self,num,title,filepath,output_file):
       self.add_page()
       self.chapter_title(num,title)
       self.chapter_body(filepath)
       
       
           
pdf = PDF()
pdf.set_title("100 Ways to learn to programming")
pdf.set_author("Eric Fitch")
#This creates one chapter
pdf.print_chapter(1,"GETTING STARTED WITH PROGRAMMING","para.txt", "sample.pdf")

pdf.print_chapter(2,"WHICH PROGRAMMING LANGUAGE TO LEARN","para.txt", "sample.pdf")

pdf.output("sample.pdf")