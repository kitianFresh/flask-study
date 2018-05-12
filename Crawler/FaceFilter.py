# -*- coding: utf-8 -*-

import os
import sys
import urllib2
import itertools
import mimetools
import mimetypes
from cStringIO import StringIO
import urllib
import urllib2
import pprint
import json
import pymysql

class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return
    
    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))
        return
    
    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.  
        parts = []
        part_boundary = '--' + self.boundary
        
        # Add the form fields
        parts.extend(
            [ part_boundary,
              'Content-Disposition: form-data; name="%s"' % name,
              '',
              value,
            ]
            for name, value in self.form_fields
            )
        
        # Add the files to upload
        parts.extend(
            [ part_boundary,
              'Content-Disposition: file; name="%s"; filename="%s"' % \
                 (field_name, filename),
              'Content-Type: %s' % content_type,
              '',
              body,
            ]
            for field_name, filename, content_type, body in self.files
            )
        
        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)

def getMysqlConn():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd=os.getenv("MYSQL_PASSWORD"), db='huajiaogirls', charset='utf8mb4')
    return conn

def insertBeautyFace(data):
    conn = getMysqlConn()
    cur = conn.cursor()
    try:
        cur = conn.cursor()
        cur.execute("USE huajiaogirls")
        cur.execute("set names utf8mb4")
        cur.execute("INSERT INTO Tbl_Beauty_Face (FImageUrl, FImageOriginal, FImageFiltered, FImageLandmarks) VALUES (%s, %s, %s, %s)", (data['FImageUrl'], data['FImageOriginal'], data['FImageFiltered'], data['FImageLandmarks'])
        )
        conn.commit()
    except pymysql.err.InternalError as e:
        print 'insertBeautyFace Except'
        print(e)

# get all face image names
def getBeautyFace(num):
    conn = getMysqlConn()
    cur = conn.cursor()
    try:
        cur = conn.cursor()
        cur.execute("USE huajiaogirls")
        cur.execute("set names utf8mb4")
        cur.execute("SELECT FImageOriginal FROM Tbl_Beauty_Face ORDER BY FFaceId DESC LIMIT " + str(num))
        ret = cur.fetchall()
        faces = []
        for face in ret:
            faces.append(face[0].split('/')[-1])
        return faces
    except:
        print("getBeautyFace except")
        return None

def rectify(x, y, size):
        return (x-size, y-size, x+size, y+size)

def draw_contour(draw, landmarks, size=5, fill=(255,0,0,128)):
    # draw contour
    contours = []
    x = landmarks['contour_chin']['x']
    y = landmarks['contour_chin']['y']
    contours.append(rectify(x,y,size))
    for i in range(1,10):
        x = landmarks['contour_left' + str(i)]['x']
        y = landmarks['contour_left' + str(i)]['y']
        contours.append(rectify(x,y,size))
        x = landmarks['contour_right' + str(i)]['x']
        y = landmarks['contour_right' + str(i)]['y']
        contours.append(rectify(x,y,size))
    
    for contour in contours:
        draw.ellipse(contour,fill=fill)

def draw_mouth(draw, landmarks, size=3, fill=(255,255,0,128)):
    # draw mouth
    for key, value in landmarks.iteritems():
        if 'mouth' in key:
            draw.ellipse(rectify(value['x'], value['y'], size), fill=fill)

def draw_nose(draw, landmarks, size=3, fill=(0,255,255,128)):
    # draw nose
    for key, value in landmarks.iteritems():
        if 'nose' in key:
            draw.ellipse(rectify(value['x'], value['y'], size), fill=fill)

def draw_left_eye(draw, landmarks, size=3, fill=(0,255,0,128)):
    # draw left eye and eyebrow
    for key, value in landmarks.iteritems():
        if 'left_eye' in key:
            draw.ellipse(rectify(value['x'], value['y'], size), fill=fill)

def draw_right_eye(draw, landmarks, size=3, fill=(0,255,0,128)):
    # draw right eye and eyebrow
    for key, value in landmarks.iteritems():
        if 'right_eye' in key:
            draw.ellipse(rectify(value['x'], value['y'], size), fill=fill)

def draw_all(draw, landmarks, size=3, fill=(255,255,0,128)):
   
    for key, value in landmarks.iteritems():
        draw.ellipse(rectify(value['x'], value['y'], size), fill=fill)

def detect_face(path, show=False, apiUrl="https://api-cn.faceplusplus.com/facepp/v3/detect", output="/home/kinny/Study/Crawler/images/huajiaogirlfaces"):
    # Create the form with simple fields
    form = MultiPartForm()
    form.add_field("api_key", "DfpzY7qZ8IyCf3ThIcHomfBS65YcGH6k")
    form.add_field("api_secret", "k7gqF6OD7v77zUxA5B3Ge9EQCRoJ75mq")
    form.add_field("return_landmark", "1")
    
    image = open(path, 'rb')
    # Add a fake file
    form.add_file('image_file', image.name, 
                  fileHandle=image)
    
    # Build the request
    apiUrl = apiUrl + '?return_attributes=gender,age'
    request = urllib2.Request(apiUrl)
    body = str(form)
    request.add_header('Content-type', form.get_content_type())
    request.add_header('Content-length', len(body))
    request.add_data(body)
    pp = pprint.PrettyPrinter()
    r = urllib2.urlopen(request)
    features = json.loads(r.read())
    # pp.pprint(features)
    # response [] means no faces
    if not features['faces']:
        print path + " contains no faces!"
        return
    
    from PIL import Image, ImageDraw
    im_original = Image.open(path)
    #im_original.show()
    # use another copy of original image , or the draw operation will destroy original one if you save
    im = im_original.copy()
    draw = ImageDraw.Draw(im)
    landmarks = features['faces'][0]['landmark']
    attributes = features['faces'][0]['attributes']
    if len(features['faces']) > 2:
        print path + " detect too many faces, filtered"
        return 
    for face in features['faces']:
        if face['attributes']['gender']['value'] == 'Male':
            print path + " detect man face, filtered"
            return
    draw_contour(draw, landmarks, 5)
    draw_mouth(draw, landmarks, 3)
    draw_nose(draw, landmarks, 3)
    draw_left_eye(draw, landmarks, 3)
    draw_right_eye(draw, landmarks, 3)
    #draw_all(draw, landmarks, 3)
    if show:
        #im_original.show()
        im.show()
    marked_output = os.path.join(output, 'marked')
    if not os.path.exists(marked_output):
        os.mkdir(marked_output)
    im.save(os.path.join(marked_output, os.path.basename(image.name)))
    clear_output = os.path.join(output, 'clear')
    if not os.path.exists(clear_output):
        os.mkdir(clear_output)
    im_original.save(os.path.join(clear_output, os.path.basename(image.name)))
    # sync to mysql 
    data = {
        "FImageUrl": "http://image.huajiao.com/" + os.path.basename(image.name), 
        "FImageOriginal": clear_output, 
        "FImageFiltered": marked_output, 
        "FImageLandmarks": json.dumps(landmarks)
    }
    insertBeautyFace(data)
    print "save detected face image to " + marked_output
    image.close()
    del draw


def detect_faces(imageNums=10, show=False, apiUrl="https://api-cn.faceplusplus.com/facepp/v3/detect", input='/home/kinny/Study/Crawler/images/huajiaogirls', output="/home/kinny/Study/Crawler/images/huajiaogirlfaces"):
    count = 0
    image_names = os.listdir(input)
    detected_face_image_names = getBeautyFace(imageNums)
    
    for image in image_names:
        path = os.path.join(input, image)
        if count == imageNums:
            break
        if image in detected_face_image_names:
            print path + " have already detected"
            continue
        print "detect " + path
        detect_face(path, show, apiUrl, output)
        count += 1
        # avoid api invoke concurrency limits
        from time import sleep
        sleep(5)

def main(argv):
    if len(argv) == 3:
        nums = argv[1]
        show = True if argv[2] == "true" else False
        detect_faces(imageNums=nums, show=show)
    elif len(argv) == 5:
        nums = argv[1]
        show = True if argv[2] == "true" else False
        inputs = argv[3]
        output = argv[4]
        detect_faces(imageNums=nums, show=show, input=inputs, output=output)
    else:
        print("Usage: python FaceFilter.py <Nums><show:true/false><input><output>")
        exit()	
	


if __name__ == '__main__':
   main(sys.argv)
