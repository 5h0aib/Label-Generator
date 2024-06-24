from reportlab.lib.pagesizes import inch
from PyPDF2 import PdfWriter, PdfReader, Transformation
import io
from reportlab.pdfgen.canvas import Canvas
from datetime import datetime

import gspread

gc = gspread.service_account(filename="creds.json")
sh = gc.open("FlawedSheet").get_worksheet(2)


class GenerateFromTemplate:
    def __init__(self,template):
        self.template_pdf = PdfReader(open(template, "rb"))
        self.template_page= self.template_pdf.pages[0]

        self.packet = io.BytesIO()
        self.c = Canvas(self.packet,pagesize=(4.1*inch,6.1*inch))

    
    def addText(self,text,point):
        self.c.drawString(point[0],point[1],text)

    def addBigText(self, text, point):
        # Define the maximum width for the big text
        max_width = 250

        words = text.split()  # Split text into words
        x, y = point  # Initial coordinates

        temp_line = ""
        for word in words:
            word_width = self.c.stringWidth(word)  # Calculate the width of the word

            # If adding the current word exceeds the maximum width
            if self.c.stringWidth(temp_line + " " + word) > max_width:
                self.c.drawString(x, y, temp_line.strip())  # Draw the line
                y -= 20  # Move to the next line
                temp_line = word  # Start a new line with the current word
            else:
                temp_line += " " + word  # Add the word to the current line

        # Draw the remaining line
        if temp_line:
            self.c.drawString(x, y, temp_line.strip())

    def merge(self):
        self.c.save()
        self.packet.seek(0)
        result_pdf = PdfReader(self.packet)
        result = result_pdf.pages[0]

        self.output = PdfWriter()

        op = Transformation().rotate(0).translate(tx=0, ty=0)
        result.add_transformation(op)
        self.template_page.merge_page(result)
        self.output.add_page(self.template_page)
    
    def generate(self,dest):
        outputStream = open(dest,"wb")
        self.output.write(outputStream)
        outputStream.close()

def getListFromSheet():
    
    values_list = sh.col_values(5)
    # Initialize a list to store the indices
    indices_of_no = []

    # Iterate through the list and check for "No"
    for index, value in enumerate(values_list):
        if "No" in str(value):  # Convert to string to handle non-string values
            indices_of_no.append(index+1)


    cells_needed = {'order_id':'c','name':'f','address':'g','number':'h'}

    # Initialize a list to store dictionaries
    result_list = []

    # Iterate through the indices and construct dictionaries
    for index in indices_of_no:
        temp_dict = {}
        for key, col_letter in cells_needed.items():
            temp_dict[key] = col_letter + str(index)
        result_list.append(temp_dict)

    return result_list


result_list = getListFromSheet()

# List to store instances of GenerateFromTemplate
gen_list = []

# Loop through result_list and create instances of GenerateFromTemplate
for result in result_list:
    gen = GenerateFromTemplate("template_two.pdf")
    gen.addText(f"Name: {sh.acell(result['name']).value}", (15, 317))
    gen.addText(f"Number: {sh.acell(result['number']).value}", (15, 290))
    gen.addBigText(f"Address: {sh.acell(result['address']).value}", (15, 263))
    gen.addText(f"Order Id: {sh.acell(result['order_id']).value}", (15, 192))
    gen.merge()
    gen_list.append(gen)

merged_pdf = PdfWriter()

for gen in gen_list:
    for page in gen.output.pages:
        merged_pdf.add_page(page)


# Get today's date
today = datetime.today()

# Format the date as "25th_May_2024"
formatted_date = today.strftime("%dth%B_%Y")

# Use the formatted date in your PDF generation function
output_pdf_name = f"output_pdfs/ShippingLabels({formatted_date})3.pdf"

# Write the merged PDF to a file
with open(output_pdf_name, "wb") as output_pdf:
    merged_pdf.write(output_pdf)


print("Done")