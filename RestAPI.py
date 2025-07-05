from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from IDCroper  import CardExtractor
from  DBHelper import SQLDatabase
import os,threading,time
import json
import queue
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
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
def correct_skew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        rect = cv2.minAreaRect(largest_contour)
        angle = rect[-1]

        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        corrected_image = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return corrected_image
    else:
        return image
def CropIDFromScannerImage(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.bitwise_not(gray)

    (contours, _) = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    max_area = 0
    max_contour = None

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    if max_contour is not None:
        (x, y, w, h) = cv2.boundingRect(max_contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        cropped_image = image[y:y + h, x:x + w]
        cv2.imwrite('detected_card.jpg', image)
        cv2.imwrite('cropped_id_card.jpg', cropped_image)
        
        return cropped_image
    else:
        print("No contours found.")
        return None

def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated
def match_template(template, image_gray):
    best_match = None
    best_value = -1
    best_angle = 0
    for angle in range(0, 360, 15):  # Rotate the template from 0 to 345 degrees in steps of 15
        rotated_template = rotate_image(template, angle)
        result = cv2.matchTemplate(image_gray, rotated_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > best_value:
            best_value = max_val
            best_match = max_loc
            best_template = rotated_template
            best_angle = angle
    return best_match, best_template.shape[::-1], best_angle
def draw_rectangle(image, top_left, width_height):
    bottom_right = (top_left[0] + width_height[1], top_left[1] + width_height[0])
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    return image, bottom_right

def crop_region(image, top_left, bottom_right):
    return image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

def extract_id_card_From_ScannerImage(image):
    template_path = r'Test\template.jpg'  # Update this path
    template_image = cv2.imread(template_path)
    template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Match template
    top_left, template_size, best_angle = match_template(template_gray, gray)
   # Draw rectangle around matched region
    scanned_image_with_rect, bottom_right = draw_rectangle(image, top_left, template_size)
    cv2.imwrite('scanned_image_with_rect.jpg', scanned_image_with_rect)
    # Crop the matched region
    cropped_id_card = crop_region(image, top_left, bottom_right)

    return cropped_id_card
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
             card = CropIDFromScannerImage(image)
             if card is None:
                card = extract_id_card_From_ScannerImage(image)
        else:
             card = CropIDFromScannerImage(image)   
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
        print("Error", str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/recognize-text/<char>/<int:threshold>', methods=['POST'])
def recognize_text(char, threshold):
    if 'image' not in request.files:
        return jsonify({'error': 'No image sent'}), 400
    image_file = request.files['image']   
    try:
        # Read the image file directly using OpenCV
        image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        retMessage = BeginProcessing(image, char, "Image", threshold)   
        SaveImageToSavingDir(image)
        return retMessage
    except Exception as e:
        print("Error", str(e))
        return jsonify({'error': str(e)}), 500

    
@app.route('/save/', methods=['POST'])
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
        print(e)
        return jsonify({'error': str(e)}), 500    
def SaveImageToSavingDir(image):
    try:
        config_result = ReadConfig()
        if config_result is None:
            print("Warning: Config file not found. Skipping image save.")
            return
        savepath, b, f = config_result
        # Generate a GUID
        image_name = str(uuid.uuid4()) + '.jpg'
        # Define the path
        path = os.path.join(savepath, image_name)
        # Save the image
        cv2.imwrite(path, image)
        print(f"Image saved to: {path}")
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        # Don't fail the whole request if image saving fails

def SaveTODataBase(record):
    try:
        # Get database connection parameters from environment variables
        server = r"AMRO-PC\SQLEXPRESS"  # The 'r' before the string allows backslashes to be used as literal characters
        database = "IDExteactor"
        print("database")

        # Initialize SQLDatabase object
        db = SQLDatabase(
            server=server,
            database=database
        )      

        # Check if database connection is already established
        if not db.connection:
            # Connect to the database
            db.connect()

        # Check if the database exists
        if not db.database_exists():
            # Create the database (ensure this method is implemented if needed)
            # db.create_database(database)
            raise NotImplementedError("create_database method is not implemented.")

        print("All before creating table")
        # Check if table exists
        table_name = 'dbo.IDSamples'  # Adjust table name accordingly
        if not db.table_exists(table_name):
            # Create a table (assuming record provides column names and data types)
            columns = {col: 'VARCHAR(MAX)' for col in record.keys()}  # Example: Adjust data types as needed
            print(f"Creating table {table_name} with columns: {columns}")
            db.create_table(table_name, columns)
            print(f"Table {table_name} created successfully.")

        # Insert record
        print("Inserting record:", record)
        db.insert_record(table_name, record)
        print("Record inserted successfully.")

        return True, "Data saved successfully"
    except Exception as e:
        print(e)
        return False, str(e)


@app.route('/')
def home():
    return "OCR Server is running..."

@app.route('/check-file/', methods=['POST'])
def check_file():
    config_result = ReadConfig()
    if config_result is None:
        return jsonify({'error': 'Configuration file not found. Please set up configuration first.'}), 400
    
    savepath, backpath, frontpath = config_result
    data = request.data.decode('utf-8')
    print("Data received:", data)  # Add this line to print the received data
    try:
        data_dict = json.loads(data)
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    if 'side' not in data_dict:
        print("no data found")
        return jsonify({'error': 'the side is not provided in the request body'}), 400
    side=data_dict['side']
    if side == 'F':
        directory_path = frontpath
    elif side =='B':
        directory_path=backpath  
    else:
        directory_path = ""
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
            if len(files) >0:
                file_path = os.path.join(dirpath, files[0])
                if os.path.isfile(file_path):
                    print("File found: " + file_path)
                    # Pass the file path to the other function for processing
                    image = cv2.imread(file_path, cv2.IMREAD_ANYCOLOR)
                    print(tresh)
                    retMesage=BeginProcessing(image,char,"Scanner",tresh)   
                    result_queue.put(retMesage)
                    os.remove(file_path)
                    SaveImageToSavingDir(image)
                    return retMesage
        print("Waiting for directory to be created: " + dirpath)
        time.sleep(1)  # Check every 1 second
    result_queue.put("Error checking directory")
    return "Error checking directory"

@app.route('/save-config/', methods=['POST'])
def SaveConfig():
     # Get the JSON data from the POST request
    config_data = request.get_json()
    # Check if all required fields are present
    if not all(key in config_data for key in ("SavePath", "BackPath", "FrontPath")):
        return jsonify({"error": "Missing required configuration data."}), 400

    # Define the path where the config file will be saved
    config_file_path = os.path.join(os.getcwd(), "config.json")
    # Retrieve paths from config data
    savepath = config_data.get("SavePath", "")
    backpath = config_data.get("BackPath", "")
    frontpath = config_data.get("FrontPath", "")
    # Write the data to a JSON file
    with open(config_file_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
 # Create directories if they don't exist
    if savepath:
        os.makedirs(savepath, exist_ok=True)
        print(f"Save path created or exists: {savepath}")
    
    if backpath:
        os.makedirs(backpath, exist_ok=True)
        print(f"Back path created or exists: {backpath}")
    
    if frontpath:
        os.makedirs(frontpath, exist_ok=True)
        print(f"Front path created or exists: {frontpath}")
    return jsonify({"message": "Configuration saved successfully."}), 200


def ReadConfig():
    config_file_path = os.path.join(os.getcwd(), "config.json")
    # Ensure the file exists
    if os.path.exists(config_file_path):
        try:
            with open(config_file_path, 'r') as config_file:
                # Load the JSON data from the file
                config_data = json.load(config_file)
            
                # Extract the paths
                savepath = config_data.get("SavePath")
                backpath = config_data.get("BackPath")
                frontpath = config_data.get("FrontPath")
            
                # Print the paths
                print("Save Path:", savepath)
                print("Back Path:", backpath)
                print("Front Path:", frontpath)
                return savepath, backpath, frontpath
        except Exception as e:
            print(f"Error reading config file: {str(e)}")
            return None
    else:
        print("Config file does not exist!")
        return None
if __name__ == '__main__':
    app.run(debug=False)
