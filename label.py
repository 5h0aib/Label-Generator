from __future__ import absolute_import,annotations
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from PIL import Image, ImageDraw, ImageFont

logo = Image.open("ff.png")
hwc = Image.open("hwc.png")
umb = Image.open("umb.png")
qr = Image.open("qr.png")
stoic = Image.open("img.png")

logo = logo.resize((440*3, 200*3))  # Adjusted size
hwc = hwc.resize((400, 400))       # Adjusted size
umb = umb.resize((400, 400))       # Adjusted size
qr = qr.resize((480*2, 480*2))       # Adjusted size
stoic =stoic.resize((450,1500))
# Create a 4x6 label image
label_img = Image.new("RGB", (960*2, 1440*2), color="white")  # Adjusted size

label_img.paste(logo, (20, 0))       # Adjusted position
label_img.paste(hwc, (950, 1450))      # Adjusted position
label_img.paste(umb, (1400, 1450))      # Adjusted position
label_img.paste(qr, (920, 1900))   
label_img.paste(stoic,(200,1350))    # Adjusted position

draw = ImageDraw.Draw(label_img)

draw.line([(1250, 45), (1250, 550)], fill="black", width=4)   # Adjusted position and thickness
draw.line([(45, 550), (1870, 550)], fill="black", width=4)   # Adjusted position and thickness

# Outline 
draw.line([(45, 45), (45, 2850)], fill="black", width=10) 
draw.line([(45, 2850), (1870, 2850)], fill="black", width=10) 
draw.line([(45, 45), (1870, 45)], fill="black", width=10) 
draw.line([(1870, 45), (1870, 2850)], fill="black", width=10) 


draw.line([(45, 800), (1870, 800)], fill="black", width=4) 
draw.line([(45, 1370), (1870, 1370)], fill="black", width=4) 
draw.line([(930, 1370), (930, 2850)], fill="black", width=4) 
draw.line([(930, 1920), (1870, 1920)], fill="black", width=4) 

font = ImageFont.truetype('monst.ttf', 80)   # Adjusted font size
draw.text((1280, 140), "FlawedFits", fill="black", font=font)   # Adjusted position
draw.text((1280, 260), "Dhaka", fill="black", font=font)         # Adjusted position
draw.text((1280, 380), "Bangladesh", fill="black", font=font)   # Adjusted position

font = ImageFont.truetype('monst.ttf', 100)   # Adjusted font size
draw.text((250, 610), "Order No: 24A423TU14GZ9F ", fill="black", font=font)   # Adjusted position

draw.text((85, 850), "Name: John Doe John Doe ", fill="black", font=font)      # Adjusted position
draw.text((85 ,1020), "Mobile: (+880) 1859598249", fill="black", font=font)    # Adjusted position
draw.text((85, 1190), "Address: 123 Shipping St", fill="black", font=font) 

# font = ImageFont.truetype('monst.ttf', 95)   # Adjusted font size
# draw.text((95, 1850), "Don't explain", fill="black", font=font) 
# draw.text((95, 2000), "your philosophy.", fill="black", font=font)
# draw.text((95, 2150), "Embody it.", fill="black", font=font)  

# Save the label image to a file
label_img.save("shipping_labels.png")

image = Image.open("shipping_labels.png")

# Create a PDF file
pdf_file = "shipping_labels.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)

# Draw the image on the PDF
c.drawImage("shipping_labels.png", 0, 0, width=letter[0], height=letter[1])

# Save the PDF
c.save()
