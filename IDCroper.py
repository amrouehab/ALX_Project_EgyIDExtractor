import cv2
import json
from OCRExtractor import OCREngine
import datetime
import re
import numpy as np

class CardExtractor:
    def __init__(self, card_image_path):
        self.card_image = cv2.imread(card_image_path)
        self.card_width_mm = 85.6
        self.card_height_mm = 54.0
        self.pixels_per_mm_width = self.card_image.shape[1] / self.card_width_mm
        self.pixels_per_mm_height = self.card_image.shape[0] / self.card_height_mm

    def reduce_black_space(self, binary_image_path):
      # Load the binary image
      image = cv2.imread(binary_image_path, cv2.IMREAD_GRAYSCALE)

      # Apply morphological operations to reduce black space
      kernel = np.ones((5,5), np.uint8)
      dilated = cv2.dilate(image, kernel, iterations=1)
      eroded = cv2.erode(dilated, kernel, iterations=1)

      # Perform connected component analysis
      num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(eroded, connectivity=8)

      # Extract individual words based on bounding boxes
      words = []
      for i in range(1, num_labels):  # Skip background (label 0)
        x, y, w, h, _ = stats[i]
        word = image[y:y+h, x:x+w]

        # Resize word to have consistent height
        target_height = 32  # Adjust as needed
        word_resized = cv2.resize(word, (int(w * target_height / h), target_height))
        words.append(word_resized)

      # Concatenate words horizontally to form a single sentence image
      sentence_image = np.concatenate(words, axis=1)

      return sentence_image

    def extract_data_area(self, dataTop, dataBottom, dataLeft, dataRight):
        top = int(dataTop * self.pixels_per_mm_height)
        bottom = self.card_image.shape[0] - int(dataBottom * self.pixels_per_mm_height)
        left = int(dataLeft * self.pixels_per_mm_width)
        right = self.card_image.shape[1] - int(dataRight * self.pixels_per_mm_width)
        data_area = self.card_image[top:bottom, left:right]
        return data_area

    def save_data_area(self, data_area, output_path):
        cv2.imwrite(output_path, data_area)
        print("Data area extraction completed successfully.")

    def extractName(self, OCR):
        name_data = self.extract_data_area(13.0, 34.0, 30.0, 2.0)
        self.save_data_area(name_data, '1st_name_data_area.jpg')
        name = OCR.extract_arabic_text('1st_name_data_area.jpg')
        name_data = self.extract_data_area(19.0, 29.0, 30.0, 2.0)
        self.save_data_area(name_data, '2nd_name_data_area.jpg')
        name2 = OCR.extract_arabic_text('2nd_name_data_area.jpg')
        return name+" "+name2
    
    def extractAddress(self, OCR):
        address_data = self.extract_data_area(24.0, 25.0, 30.0, 2.0)
        self.save_data_area(address_data, '1staddress_data_area.jpg')
        address = OCR.extract_arabic_text('1staddress_data_area.jpg')

        address_data = self.extract_data_area(29.0, 19.0, 30.0, 2.0)
        self.save_data_area(address_data, '2ndaddress_data_area.jpg')
        address2 = OCR.extract_arabic_text('2ndaddress_data_area.jpg')

        return address+" "+address2
    def extractID(self, OCR):
        id_data = self.extract_data_area(40.0, 5.0, 30.0, 2.0)
        self.save_data_area(id_data, 'id_data_area.jpg')
        ID = OCR.extract_numbers('id_data_area.jpg')
        return ID

    def getFront_IDData(self):
        OCR = OCREngine()
       
        name =self.extractName(OCR)
        address = self.extractAddress(OCR)
        ID=self.extractID(OCR)      
        DOB = self.extract_date_from_id(ID)

        face_data = self.extract_data_area(5.0, 20.0, 2.0, 60.0)
        self.save_data_area(face_data, 'face_data_area.jpg')

        # Store data in a dictionary
        data = {
            "name": name,
            "address": address,
            "ID": ID,
            "DOB": DOB
        }

        # Convert dictionary to JSON string
        json_data = json.dumps(data)
        return json_data
    
  
    def extract_date_from_id(self,id_number):
      # Extract millennium indicator, year, month, and day
      millennium_indicator = int(str(id_number)[0])
      year = int(str(id_number)[1:3])
      month = int(str(id_number)[3:5])
      day = int(str(id_number)[5:7])
      print("MIllinum="+str(millennium_indicator)+"year="+str(year),"month="+str(month), "dat="+str(day))
    
      # Determine the full year based on the millennium indicator
      if millennium_indicator == 2:
        year += 1900
      elif millennium_indicator == 3:
        year += 2000    
      # Return the date as a datetime object
      return  f"{year}-{month:02d}-{day:02d}" 
    
    def find_religion(self,text):
     try:
        # Define regular expressions for the words "مسلم" and "مسيحي"
        muslim_pattern = re.compile('مسلم')
        christian_pattern = re.compile('مسيحي')

        # Split the text into lines and iterate through each line
        for line in text.split('\n'):
            # Search for the words in the line
            muslim_match = muslim_pattern.search(line)
            christian_match = christian_pattern.search(line)

            # Return the appropriate word if found in the line
            if muslim_match:
                return "مسلم"
            elif christian_match:
                return "مسيحي"

        # If no match found in any line, return None
        return None
     except Exception as e:
        print("Error:", e)
        return None

    def find_gender(self,text):
     try:
      
        male_pattern = re.compile('ذكر')
        female_pattern = re.compile('انثي')

        # Split the text into lines and iterate through each line
        for line in text.split('\n'):
            # Search for the words in the line
            male_match = male_pattern.search(line)
            female_match = female_pattern.search(line)

            # Return the appropriate word if found in the line
            if male_match:
                return "ذكر",'m'
            elif female_match:
                return "انثي",'f'

        # If no match found in any line, return None
        return "",''
     except Exception as e:
        print("Error:", e)
        return "", '' 
     
    def find_Mstatus(self,text,gender):
     try:
        if gender ==  'm':
           single_pattern= re.compile('أعزب')
           single='أعزب'
           married_pattern= re.compile('متزوج')
           married='متزوج'
           divorced_pattern=re.compile('مطلق')
           div='مطلق'
           armal_pattern=re.compile('ارمل')
           arm='ارمل'
        else:
           single_pattern= re.compile('عزباء')
           single='عزباء'
           married_pattern= re.compile('متزوجة')
           married='متزوجة'
           divorced_pattern=re.compile('مطلقة')
           div='مطلقة'
           armal_pattern=re.compile('ارملة')
           arm='ارملة'   


        # Split the text into lines and iterate through each line
        for line in text.split('\n'):
            # Search for the words in the line
            singlepattern = single_pattern.search(line)
            marriedpattern = married_pattern.search(line)
            divorcedpattern=divorced_pattern.search(line)
            armalpattern=armal_pattern.search(line)
            # Return the appropriate word if found in the line        
            if singlepattern:
                return single
            elif marriedpattern:
                return married
            elif divorcedpattern:
                return div
            elif armalpattern:
                return arm

        # If no match found in any line, return None
        return None
     except Exception as e:
        print("Error:", e)
        return None  
    def getBack_IDData(self):
      OCR = OCREngine()
      # Extract profession data
      profession_data = self.extract_data_area(7.5, 38.0, 20.0, 16.0)
      self.save_data_area(profession_data, 'profession_data_area.jpg')
      profession = OCR.extract_arabic_text('profession_data_area.jpg')    
      # Extract religion data
      # religion_data = self.extract_data_area(13.0, 32.0, 45.0, 17.0)
      religion_data = self.extract_data_area(16.0, 32.0, 18.0, 16.5)
      self.save_data_area(religion_data, 'religion_data_area.jpg')
      combined=self.reduce_black_space('religion_data_area.jpg')
      self.save_data_area(combined, 'combined_data_area.jpg')
      compinedtext = OCR.extract_arabic_text('combined_data_area.jpg')
      print('compinedtext', compinedtext)
      religion=self.find_religion(compinedtext)
    
      # Extract gender data
      gender,g=self.find_gender(compinedtext)
      print (gender,g)
      # Extract marital status data
      marital_status=self.find_Mstatus(compinedtext,g)
      # Extract End data
      enddate_data = self.extract_data_area(25.0, 23.0, 20.0, 39.0)
      self.save_data_area(enddate_data, 'enddate_data_area.jpg')
      enddate = OCR.extract_arabic_text('enddate_data_area.jpg')

      # Extract husband's name data
      husband_name_data = self.extract_data_area(25.0, 20.0, 30.0, 2.0)
      self.save_data_area(husband_name_data, 'husband_name_data_area.jpg')
      husband_name = OCR.extract_arabic_text('husband_name_data_area.jpg')
    
      # Store data in a dictionary
      data = {
        'profession': profession,
        'religion': religion,
        'gender': gender,
        'marital_status': marital_status,
        'enddate': enddate,
        'husband_name': husband_name
      }

      # Convert dictionary to JSON string
      json_data = json.dumps(data)
      return json_data


