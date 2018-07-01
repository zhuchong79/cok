import pytesseract  
from PIL import Image  
  
code = pytesseract.image_to_string(Image.open('num.png'), lang="eng", config="-psm 7")  
print code  