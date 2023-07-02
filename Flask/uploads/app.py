from flask import Flask, render_template, request, session
import cv2
import pickle
import cvzone
import numpy as np
import ibm_db
import re

app = Flask(__name__)
app.sceret_key = 'a'
conn = ibm_db.connect(Database=;Hostname=;PORT =;Security = SSL; SSLServerCertificate = ;UID=;PWD=)
print("connected")

if __name__ =="main":
    app_run(debug=True)



@app.route('/')
def project():

    return render_template('index.html')

@app.route('/hero')
def home():

    return render_template('index.html')

@app.route('/model')
def model():

    return render_template('model.html')

@app.route('/login')
def login():

    return render_template('login.html')

@app.route("/reg", methods=['POST', 'GET'])
def signup():
    msg = ''
    if request.method == 'POST':
        name= request.form["name"]

        email = request.form["email"]

        password request.form["password"]

        sql = "SELECT * FROM REGISTER WHERE name= ?"

        stmt = ibm_db.prepare (conn, sql)

        ibm_db.bind_param(stmt, 1, name)

        ibm_db.execute(stmt)

        account = ibm_db.fetch_assoc(stmt)

        print (account)

        if account:
            return render_template('login.html', error=True)
        
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):

        msg = "Invalid Email Address!"

       else:
           insert_sql = "INSERT INTO REGISTER VALUES (?,?,?)"
           prep_stmt = ibm_db.prepare(conn, insert_sql)
           ibm_db.bind_param (prep_stmt, 1, name)
           ibm_db.bind_param (prep_stmt, 2, email)
           ibm_db.bind_param (prep_stmt, 3, password)
           ibm_db.execute(prep_stmt)
           msg = "You have successfully registered !"

    return render_template('login.html', msg=msg)

@app.route("/log", methods=['POST', 'GET'])
def login1():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        sql = "SELECT * FROM REGISTER WHERE EMAIL= ? AND PASSWORD=?" # from db2 sql table
        stmt = ibm_db.prepare (conn, sql)
# this username & password should be same as db-2 details & order also
       ibm_db.bind_param(stmt, 1, email)
       ibm_db.bind_param(stmt,2, password)
       ibm_db.execute(stmt)
       account = ibm_db.fetch_assoc(stmt)
       print (account)

       if account:
           session['Loggedin'] = True
           session['id'] = account ['EMAIL']
           session ['email'] = account ['EMAIL']
           return render_template('model.html')

      else:
          msg = "Incorrect Email/password"
          return render_template('login.html', msg=msg)

   else:
     return render_template('login.html')

@app.route('/predict_live')
def liv_pred():
    cap = cv2.VideoCapture('CarParkingInput.mp4')
    with open('parkingSlotPosition', 'rb')as f:
    posList= pickle.load(f)
    width,height = 107, 48


def checkParkingSpace(imgPro): 
    spaceCounter = 0
    for pos in posList:
        x, y = pos
# Crop the image based on ROI
        imgCrop = imgPro[y:y - + height, x:x + width]
# Counting the pixel values from cropped image count = cv2.countNonZero(imgCrop)
        if count < 900:
            color= (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color= (0, 0, 255)
            thickness = 2
# Draw the rectangle based on the condition defined above
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness) 
# Display the available parking slot count / total parking slot count 
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len (posList)}', (100, 50), scale=3, thickness=5, offset=20, color=(0,2000))

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.cv2.CAP_PROP_POS_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES)

# Reading frame by frame from video
    success, img = cap.read()
# Converting to gray scale image
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1) # Applying blur to image
# Applying threshold to the image
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur (imgThreshold, 5) # Applying blur to image
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
# Passing dilate image to the function
    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    
    if cv2.waitkey(1) & 0xFF == ord('q'):
        break
    
    if __name__ == "__main__":
        app.run(debug=True)
 
    


