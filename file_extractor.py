from pypdf import PdfReader 
  
reader = PdfReader('karmaYoga.pdf') 
  
print(len(reader.pages)) 
txt_file = 'karmayoga.txt'

with open(txt_file,'a+') as f:
    for page in reader.pages:
        text = page.extract_text()
        f.write(text)


