import cv2
import time
from mtcnn import MTCNN

last_pos = -1
def main():
    global last_pos
    detector = MTCNN() #deklaracja detektora

    cap = cv2.VideoCapture(0)
    while True:
        ret, image= cap.read()
        if not ret:
            raise IOError("webcam failure")
        if image is not None:
          
            t=time.time()
            result = detector.detect_faces(image) #predykcja
            czas=time.time()-t
            #print('Czas: ',czas)
            if len(result) >0:
                confidence = result[0]['confidence']
           
                bottom_left_x = result[0]['box'][0]
                bottom_left_y = result[0]['box'][1]
                width = result[0]['box'][2]
                heigh = result[0]['box'][3]
                x1 = bottom_left_x + heigh
                y1 = bottom_left_y
                x2 = bottom_left_x
                y2 = bottom_left_y + width
                cv2.rectangle(image,(x1,y1),(x2,y2),(0,int(255*confidence),0),3)
                
                leftEye = result[0]['keypoints']['left_eye']
                rightEye = result[0]['keypoints']['right_eye']
                nose = result[0]['keypoints']['nose']
                leftMouth = result[0]['keypoints']['mouth_left']
                rightMouth = result[0]['keypoints']['mouth_right']
        
                cv2.circle(image, (leftEye[0],leftEye[1]), radius=0, color=(0, 0, int(255*confidence)), thickness=5)
                cv2.circle(image, (rightEye[0],rightEye[1]), radius=0, color=(0, 0, int(255*confidence)), thickness=5)
                cv2.circle(image, (nose[0],nose[1]), radius=0, color=(0, 0, int(255*confidence)), thickness=5)
                cv2.circle(image, (leftMouth[0],leftMouth[1]), radius=0, color=(0, 0, int(255*confidence)), thickness=5)
                cv2.circle(image, (rightMouth[0],rightMouth[1]), radius=0, color=(0, 0, int(255*confidence)), thickness=5)
           
                
                
                if last_pos == -1:
                    last_pos = nose
                else:
                    xDecision = "moving right" if last_pos[0]-10 > nose[0] else "moving left" if last_pos[0]+10 < nose[0] else "not moving"
                    yDecision = "moving up" if last_pos[1]-5 > nose[0] else "moving down" if last_pos[1]+5 < nose[1] else "not moving" 
                    print(f"x: {xDecision}, y: {yDecision}")
            
            cv2.imshow("Output", image)
            #print(result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

   
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
