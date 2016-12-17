# -*- coding: utf-8 -*-

import os
import urllib2
import itertools
import mimetools
import mimetypes
from cStringIO import StringIO
import urllib
import urllib2
import pprint
import json

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

def rectify(x, y, size):
        return (x-size, y-size, x+size, y+size)

def draw_contour(draw, landmarks, size=5, fill=(255,0,0,128)):
    # draw contour
    contours = []
    x = landmarks['contour_chin']['x']
    y = landmarks['contour_chin']['y']
    contours.append((x-5,y-5,x+5,y+5))
    for i in range(1,10):
        x = landmarks['contour_left' + str(i)]['x']
        y = landmarks['contour_left' + str(i)]['y']
        contours.append((x-5, y-5, x+5, y+5))
        x = landmarks['contour_right' + str(i)]['x']
        y = landmarks['contour_right' + str(i)]['y']
        contours.append((x-5, y-5, x+5, y+5))
    
    for contour in contours:
        draw.ellipse(contour,fill=fill)

def draw_mouth(draw, landmarks, size=3, fill=(255,255,0,128)):
    # draw mouth
    mouths = []
    mouths.append(rectify(landmarks['mouth_left_corner']['x'], landmarks['mouth_left_corner']['y'], size))
    mouths.append(rectify(landmarks['mouth_right_corner']['x'], landmarks['mouth_right_corner']['y'], size))
    mouths.append(rectify(landmarks['mouth_lower_lip_bottom']['x'], landmarks['mouth_lower_lip_bottom']['y'], size))
    mouths.append(rectify(landmarks['mouth_lower_lip_top']['x'], landmarks['mouth_lower_lip_top']['y'], size))
    mouths.append(rectify(landmarks['mouth_upper_lip_bottom']['x'], landmarks['mouth_upper_lip_bottom']['y'], size))
    mouths.append(rectify(landmarks['mouth_upper_lip_top']['x'], landmarks['mouth_upper_lip_top']['y'], size))
    mouths.append(rectify(landmarks['mouth_lower_lip_left_contour1']['x'], landmarks['mouth_lower_lip_left_contour1']['y'], size))
    mouths.append(rectify(landmarks['mouth_lower_lip_left_contour2']['x'], landmarks['mouth_lower_lip_left_contour2']['y'], size))
    mouths.append(rectify(landmarks['mouth_lower_lip_left_contour3']['x'], landmarks['mouth_lower_lip_left_contour3']['y'], size))
    mouths.append(rectify(landmarks['mouth_lower_lip_right_contour1']['x'], landmarks['mouth_lower_lip_right_contour1']['y'], size))
    mouths.append(rectify(landmarks['mouth_lower_lip_right_contour2']['x'], landmarks['mouth_lower_lip_right_contour2']['y'], size))
    mouths.append(rectify(landmarks['mouth_lower_lip_right_contour3']['x'], landmarks['mouth_lower_lip_right_contour3']['y'], size)) 
    mouths.append(rectify(landmarks['mouth_upper_lip_left_contour1']['x'], landmarks['mouth_upper_lip_left_contour1']['y'], size))
    mouths.append(rectify(landmarks['mouth_upper_lip_left_contour2']['x'], landmarks['mouth_upper_lip_left_contour2']['y'], size))
    mouths.append(rectify(landmarks['mouth_upper_lip_left_contour3']['x'], landmarks['mouth_upper_lip_left_contour3']['y'], size))
    mouths.append(rectify(landmarks['mouth_upper_lip_right_contour1']['x'], landmarks['mouth_upper_lip_right_contour1']['y'], size))
    mouths.append(rectify(landmarks['mouth_upper_lip_right_contour2']['x'], landmarks['mouth_upper_lip_right_contour2']['y'], size))
    mouths.append(rectify(landmarks['mouth_upper_lip_right_contour3']['x'], landmarks['mouth_upper_lip_right_contour3']['y'], size))      
    
    for mouth in mouths:
        draw.ellipse(mouth, fill=fill)

def draw_nose(draw, landmarks, size=3, fill=(0,255,255,128)):
    # draw nose
    noses = []
    noses.append(rectify(landmarks['nose_left']['x'], landmarks['nose_left']['y'], size)) 
    noses.append(rectify(landmarks['nose_right']['x'], landmarks['nose_right']['y'], size)) 
    noses.append(rectify(landmarks['nose_contour_left1']['x'], landmarks['nose_contour_left1']['y'], size))
    noses.append(rectify(landmarks['nose_contour_left2']['x'], landmarks['nose_contour_left2']['y'], size))
    noses.append(rectify(landmarks['nose_contour_left3']['x'], landmarks['nose_contour_left3']['y'], size))
    noses.append(rectify(landmarks['nose_contour_right1']['x'], landmarks['nose_contour_right1']['y'], size))
    noses.append(rectify(landmarks['nose_contour_right2']['x'], landmarks['nose_contour_right2']['y'], size))  
    noses.append(rectify(landmarks['nose_contour_right3']['x'], landmarks['nose_contour_right3']['y'], size))
    
    for nose in noses:
        draw.ellipse(nose, fill=fill)

def draw_left_eye(draw, landmarks, size=3, fill=(0,255,0,128)):
    # draw left eye and eyebrow
    lefteyes = []
    lefteyes.append(rectify(landmarks['left_eye_bottom']['x'], landmarks['left_eye_bottom']['y'], size))
    lefteyes.append(rectify(landmarks['left_eye_center']['x'], landmarks['left_eye_center']['y'], size))
    lefteyes.append(rectify(landmarks['left_eye_left_corner']['x'], landmarks['left_eye_left_corner']['y'], size))
    lefteyes.append(rectify(landmarks['left_eye_lower_left_quarter']['x'], landmarks['left_eye_lower_left_quarter']['y'], size))
    lefteyes.append(rectify(landmarks['left_eye_lower_right_quarter']['x'], landmarks['left_eye_lower_right_quarter']['x'], size))
    lefteyes.append(rectify(landmarks['left_eye_pupil']['x'], landmarks['left_eye_pupil']['y'], size))
    lefteyes.append(rectify(landmarks['left_eye_right_corner']['x'], landmarks['left_eye_right_corner']['y'], size))
    lefteyes.append(rectify(landmarks['left_eye_top']['x'], landmarks['left_eye_top']['y'], size))
    lefteyes.append(rectify(landmarks['left_eye_upper_left_quarter']['x'], landmarks['left_eye_upper_left_quarter']['y'], size))
    lefteyes.append(rectify(landmarks['left_eye_upper_right_quarter']['x'], landmarks['left_eye_upper_right_quarter']['y'], size))
    lefteyes.append(rectify(landmarks['left_eyebrow_left_corner']['x'], landmarks['left_eyebrow_left_corner']['y'], size))
    lefteyes.append(rectify(landmarks['left_eyebrow_lower_left_quarter']['x'], landmarks['left_eyebrow_lower_left_quarter']['y'], size))
    lefteyes.append(rectify(landmarks['left_eyebrow_lower_middle']['x'], landmarks['left_eyebrow_lower_middle']['y'], size))
    lefteyes.append(rectify(landmarks['left_eyebrow_lower_right_quarter']['x'], landmarks['left_eyebrow_lower_right_quarter']['y'], size))
    lefteyes.append(rectify(landmarks['left_eyebrow_right_corner']['x'], landmarks['left_eyebrow_right_corner']['y'], size))
    lefteyes.append(rectify(landmarks['left_eyebrow_upper_left_quarter']['x'], landmarks['left_eyebrow_upper_left_quarter']['y'], size))
    lefteyes.append(rectify(landmarks['left_eyebrow_upper_middle']['x'], landmarks['left_eyebrow_upper_middle']['y'], size))
    lefteyes.append(rectify(landmarks['left_eyebrow_upper_right_quarter']['x'], landmarks['left_eyebrow_upper_right_quarter']['y'], size))

    for eye in lefteyes:
        draw.ellipse(eye, fill=fill)

def draw_right_eye(draw, landmarks, size=3, fill=(0,255,0,128)):
    # draw right eye and eyebrow
    righteyes = []
    righteyes.append(rectify(landmarks['right_eye_bottom']['x'], landmarks['right_eye_bottom']['y'], size))
    righteyes.append(rectify(landmarks['right_eye_center']['x'], landmarks['right_eye_center']['y'], size))
    righteyes.append(rectify(landmarks['right_eye_left_corner']['x'], landmarks['right_eye_left_corner']['y'], size))
    righteyes.append(rectify(landmarks['right_eye_lower_left_quarter']['x'], landmarks['right_eye_lower_left_quarter']['y'], size))
    righteyes.append(rectify(landmarks['right_eye_lower_right_quarter']['x'], landmarks['right_eye_lower_right_quarter']['x'], size))
    righteyes.append(rectify(landmarks['right_eye_pupil']['x'], landmarks['right_eye_pupil']['y'], size))
    righteyes.append(rectify(landmarks['right_eye_right_corner']['x'], landmarks['right_eye_right_corner']['y'], size))
    righteyes.append(rectify(landmarks['right_eye_top']['x'], landmarks['right_eye_top']['y'], size))
    righteyes.append(rectify(landmarks['right_eye_upper_left_quarter']['x'], landmarks['right_eye_upper_left_quarter']['y'], size))
    righteyes.append(rectify(landmarks['right_eye_upper_right_quarter']['x'], landmarks['right_eye_upper_right_quarter']['y'], size))
    righteyes.append(rectify(landmarks['right_eyebrow_left_corner']['x'], landmarks['right_eyebrow_left_corner']['y'], size))
    righteyes.append(rectify(landmarks['right_eyebrow_lower_left_quarter']['x'], landmarks['right_eyebrow_lower_left_quarter']['y'], size))
    righteyes.append(rectify(landmarks['right_eyebrow_lower_middle']['x'], landmarks['right_eyebrow_lower_middle']['y'], size))
    righteyes.append(rectify(landmarks['right_eyebrow_lower_right_quarter']['x'], landmarks['right_eyebrow_lower_right_quarter']['y'], size))
    righteyes.append(rectify(landmarks['right_eyebrow_right_corner']['x'], landmarks['right_eyebrow_right_corner']['y'], size))
    righteyes.append(rectify(landmarks['right_eyebrow_upper_left_quarter']['x'], landmarks['right_eyebrow_upper_left_quarter']['y'], size))
    righteyes.append(rectify(landmarks['right_eyebrow_upper_middle']['x'], landmarks['right_eyebrow_upper_middle']['y'], size))
    righteyes.append(rectify(landmarks['right_eyebrow_upper_right_quarter']['x'], landmarks['right_eyebrow_upper_right_quarter']['y'], size))

    for eye in righteyes:
        draw.ellipse(eye, fill=fill)

def draw_all(draw, landmarks, size=3, fill=(255,255,0,128)):
   
    for key, value in landmarks.iteritems():
        draw.ellipse(rectify(value['x'], value['y'], size), fill=fill)

def detect_face(path, show=False, apiUrl="https://api-cn.faceplusplus.com/facepp/v3/detect", output="/home/kinny/Study/Crawler/images/huajiaogirlfaces"):
    # Create the form with simple fields
    form = MultiPartForm()
    form.add_field("api_key", "9vCBl6liohIj_a3PyGslySkJp1q4tf5H")
    form.add_field("api_secret", "BVt1JGKV8jujzqi6dj751VksZ8ZPKHu7")
    form.add_field("return_landmark", "1")
    
    image = open(path, 'rb')
    # Add a fake file
    form.add_file('image_file', image.name, 
                  fileHandle=image)
    
    # Build the request
    request = urllib2.Request(apiUrl)
    body = str(form)
    request.add_header('Content-type', form.get_content_type())
    request.add_header('Content-length', len(body))
    request.add_data(body)
    pp = pprint.PrettyPrinter()
    r = urllib2.urlopen(request)
    features = json.loads(r.read())
    #pp.pprint(features)
    if not features['faces']:
        print path + " contains no faces!"
        return
    
    from PIL import Image, ImageDraw
    im_original = Image.open(path)
    
    # use another copy of original image , or the draw operation will destroy original one if you save
    im = im_original.copy()
    draw = ImageDraw.Draw(im)
    landmarks = features['faces'][0]['landmark']
    draw_contour(draw, landmarks, 5)
    draw_mouth(draw, landmarks, 3)
    draw_nose(draw, landmarks, 3)
    draw_left_eye(draw, landmarks, 3)
    draw_right_eye(draw, landmarks, 3)
    #draw_all(draw, landmarks, 3)
    if show:
        im_original.show()
        im.show()
    out = os.path.join(output, os.path.basename(image.name))
    im.save(out)
    print "save detected face image to " + out
    image.close()
    del draw


def detect_faces(imageNums=10, apiUrl="https://api-cn.faceplusplus.com/facepp/v3/detect", dirs='/home/kinny/Study/Crawler/images/huajiaogirls'):
    count = 0
    files = os.listdir(dirs)
    for file in files:
        if count == imageNums:
            break
        path = os.path.join(dirs, file)
        print "detect " + path
        detect_face(path, True, apiUrl)
        count += 1
        # avoid concurrency limits
        from time import sleep
        sleep(4)
    

if __name__ == '__main__':
   detect_faces(5)
