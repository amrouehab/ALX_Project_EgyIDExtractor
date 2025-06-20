from flask import Flask, request, jsonify
import cv2
import numpy as np
from IDCroper  import CardExtractor
from  DBHelper import SQLDatabase
import os,threading,time
import json
import queue
selectedtresh=0
app = Flask(__name__)
def find_and_draw_lines(image):
    # Get image dimensions
    height, width = image.shape[:2]

    # Find horizontal line
    horizontal_line_y = None
    for y in range(height):
        for x in range(width):
            # Check if pixel is black
            if image[y, x] == 0:
                horizontal_line_y = y
                break
        if horizontal_line_y is not None:
            break

    # Draw horizontal line if found
    if horizontal_line_y is not None:
        cv2.line(image, (0, horizontal_line_y), (width - 1, horizontal_line_y), (255, 255, 255), 1)

    # Find vertical line
    vertical_line_x = None
    for x in range(width):
        for y in range(height):
            # Check if pixel is black
            if image[y, x] == 0:
                vertical_line_x = x
                break
        if vertical_line_x is not None:
            break

    # Draw vertical line if found
    if vertical_line_x is not None:
        cv2.line(image, (vertical_line_x, 0), (vertical_line_x, height - 1), (255, 255, 255), 1)

    return image
def preprocess_image(card_image,char,scantype,tresh):
     # Convert the image to grayscale
    tresh=int(tresh)
    gray = cv2.cvtColor(card_image, cv2.COLOR_BGR2GRAY)
    if scantype == "Scanner":
        trsh=145
    else:
        trsh=120

    if char=='B':
        trsh=trsh-10     
    _, thresh = cv2.threshold(gray, tresh, 255, cv2.THRESH_BINARY_INV + cv2.ADAPTIVE_THRESH_MEAN_C)
    final_image = cv2.bitwise_not(thresh)
 
    return final_image
# Function to preprocess the image
def deskew(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold the image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Get the orientation of the object
    angle = 0.0
    if len(contours) > 0:
        rect = cv2.minAreaRect(contours[0])
        angle = rect[2]
        
    # Correct skew angle
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    
    # Perform rotation
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return rotated
def extract_id_card_From_ScannerImage(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   # Load the original image
    original_image = image

    # Define the kernel for morphological operations
    kernel = np.ones((5, 5), np.uint8)

    # Perform dilation
    dilated_image = cv2.dilate(original_image, kernel, iterations=1)

    # Perform erosion
    eroded_image = cv2.erode(original_image, kernel, iterations=1)

    # Calculate the morphological gradient (difference between dilation and erosion)
    morphological_gradient = cv2.subtract(dilated_image, eroded_image)

    # Save the result
    cv2.imwrite('morphological_gradient.jpg', morphological_gradient)
        
    edges = cv2.Canny(morphological_gradient, 50, 150)

    # Apply Canny edge detection
    kernel = np.ones((7, 7), np.uint8)  # Long horizontal line kernel
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)
    cv2.imwrite('dilated_edges.jpg', dilated_edges)

    # Thresholding (if necessary)
    _, edges = cv2.threshold(dilated_edges, 100, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    max_area=0
    # Filter contours based on area and aspect ratio
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        # Assuming the ID card has a certain aspect ratio and area
        if 0.6< aspect_ratio < 2.7 and area > 8000: 
             if area > max_area:
                 max_area = area
                 id_card = image[y:y+h, x:x+w]

    # If no ID card contour found, return None
    return id_card
def extract_largest_contour(image):
    # Step 3: Detect contours
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)   
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Step 4: Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Step 5: Extract the bounding box coordinates of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Step 6: Create a new image with the same dimensions as the bounding box
    new_image = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Step 7: Copy the region defined by the bounding box from the original image to the new image
    new_image[:, :] = image[y:y+h, x:x+w]
    
    # Step 8: Return the new image
    return new_image

def BeginProcessing(image,char,scantype,tresh):
    try:
     # Detect the card in the input image
        if scantype == "Scanner":
             card = extract_id_card_From_ScannerImage(image)
        else:
             card = extract_largest_contour(image)   
        # Save the detected card as a new image
        if char == 'F':
         cv2.imwrite('Frontdetected_card.jpg', card)
         cv2.imwrite('FrontOriginal.jpg', image)
        elif char == 'B':
         cv2.imwrite('Backdetected_card.jpg', card)
         cv2.imwrite('BackOriginal.jpg', image)
        else:
            raise ValueError("Invalid character provided. Please provide 'F' for front ID data or 'B' for back ID data.")    
        print("Card detected")
        processed=preprocess_image(card,char,scantype,tresh)
        print("processed")
        cv2.imwrite('processd_id.jpg', processed)
        IDExtractor= CardExtractor(processed,card)
        print("IDExtractor" +char)
        if char=='F':
            jsonstring=IDExtractor.getFront_IDData()
        elif char=='B':
            jsonstring=IDExtractor.getBack_IDData()   
        else:
            raise ValueError("Invalid character provided. Please provide 'F' for front ID data or 'B' for back ID data.")      
        
        return jsonstring, 200
    except Exception as e:
        print("Error", e.message)
        return jsonify({'error': str(e)}), 500


@app.route('/recognize-text/<char>/<int:threshold>', methods=['POST'])
def recognize_text(char, threshold):
    if 'image' not in request.files:
        return jsonify({'error': 'No image sent'}), 400
    image_file = request.files['image']   
    try:
        # Read the image file directly using OpenCV
        image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        retMessage = BeginProcessing(image, char, "Image", threshold)   
        return retMessage
    except Exception as e:
        print("Error", e.message)
        return jsonify({'error': str(e)}), 500

    
@app.route('/save', methods=['POST'])
def save_to_database():
    try:
        # Extract JSON data from the request
        record = request.get_json()        
        # Call the SaveTODataBase function
        success, message = SaveTODataBase(record)     
        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500    
    
def SaveTODataBase(record):
    try:
        # Get database connection parameters from environment variables
        server = os.getenv('DATABASE_SERVER_IP', 'default_server_ip')
        database = os.getenv('DATABASE_NAME', 'default_database_name')
        username = os.getenv('DATABASE_USERNAME', 'default_username')
        password = os.getenv('DATABASE_PASSWORD', 'default_password')

        # Initialize SQLDatabase object
        db = SQLDatabase(server=server,
                         database=database,
                         username=username,
                         password=password)
        
        # Check if database connection is already established
        if not db.connection:
            # Connect to the database
            db.connect()
        
        # Check if the database exists
        if not db.database_exists(database):
            # Create the database
            db.create_database(database)

        # Check if table exists
        table_name = 'IDs'  # Adjust table name accordingly
        if not db.table_exists(table_name):
            # Create a table (assuming record provides column names)
            columns = record.keys()
            db.create_table(table_name, columns)

        # Insert record
        db.insert_record(table_name, record)

        return True, "Data saved successfully"
    except Exception as e:
        return False, str(e)
@app.route('/')
def home():
    return "OCR Server is running..."

@app.route('/check-file/', methods=['POST'])
def check_file():
    print(request)
    data = request.data.decode('utf-8')
    print("Data received:", data)  # Add this line to print the received data
    try:
        data_dict = json.loads(data)
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    if 'directory_path'  not in data_dict or  'side' not in data_dict:
        print("no data found")
        return jsonify({'error': 'Directory path not provided in the request body'}), 400

    directory_path = data_dict['directory_path']
    side=data_dict['side']
    tresh=data_dict['treshold']
    print(tresh)
    if not os.path.isabs(directory_path):
        print("Directory path must be absolute")
        return jsonify({'error': 'Directory path must be absolute'}), 400

    if not os.path.exists(directory_path):
        return jsonify({'file_found': False}), 200
    # Create a queue to store the result from the thread
    result_queue = queue.Queue()
    # Start a new thread to check for file presence
    thread = threading.Thread(target=check_file_presence, args=(directory_path,side,tresh,result_queue))
    thread.start()
    print("thread started")

    thread.join()
    print("thread finished")
    # Check if there's a result in the queue
    if not result_queue.empty():     
        result = result_queue.get()
        
        return result[0], result[1]
    else:
        return jsonify({'thread_started': True, 'result': "No result from thread"}), 200

 #Function to check for the presence of the  scanner image in a specific path 
def check_file_presence(dirpath, char,tresh, result_queue):
    timeout = 10  # Timeout in seconds
    start_time = time.time()

    while time.time() - start_time < timeout:
        if os.path.exists(dirpath):
            files = os.listdir(dirpath)
            for file in files:
                file_path = os.path.join(dirpath, file)
                if os.path.isfile(file_path):
                    print("File found: " + file_path)
                    # Pass the file path to the other function for processing
                    image = cv2.imread(file_path, cv2.IMREAD_ANYCOLOR)
                    print(tresh)
                    retMesage=BeginProcessing(image,char,"Scanner",tresh)   
                    result_queue.put(retMesage)
                    
                    return retMesage
        print("Waiting for directory to be created: " + dirpath)
        time.sleep(1)  # Check every 1 second
    result_queue.put("Error checking directory")
    return "Error checking directory"



if __name__ == '__main__':
    app.run(debug=True)
