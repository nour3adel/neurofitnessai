import cv2
import os
import mediapipe as mp
import numpy as np
import pygame
from django.contrib.staticfiles.storage import staticfiles_storage
from gtts import gTTS



# -------------------------------------------
# Live webcam
# -------------------------------------------

# Inizializza pygame
pygame.init()

# Carica il suono
perfectSound = pygame.mixer.Sound('D:\\Programming\\projects\\graduation projects\\Seminar 2\\Main\\neurofitness\\static\\audio\\good.mp3')
badSound = pygame.mixer.Sound('D:\\Programming\\projects\\graduation projects\\Seminar 2\\Main\\neurofitness\\static\\audio\\bad.mp3')

class LiveWebCam:

    def __init__(self):
        self.cap = None
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        )
        self.flag = False
        self.situpflag = True
        self.correctreps = 0
        self.incorrectreps = 0
        self.stage = ""
        self.feedback = ""
        self.is_camera_started = False
        self.file_path = None
        self.flag_count_cor = False
        self.prev_angle1=0
        self.prev_angle2=0
        self.done=False
        self.notdone=False
        self.elbow_done=False
        self.elbow_notdone=False
        self.workouts = {
            "Incline Barbell Bench Press": self.BenchPress,
            "Sit Up": self.Situp,
            "Chest Fly Machine": self.ChestFlyMachine,
            "Dumbbell Curl":self.Dumbell_bicepscurl,
            "Barbell Curl":self.barbellcurl,
            # Add more workouts here
        }

    def __del__(self):
        self.stop_capture()  # Stop camera when object is deleted

    def _save_temp_file(self, video_file):
        temp_dir = "media/uploads"  # Specify your temporary directory
        file_path = os.path.join(temp_dir, video_file.name)
        with open(file_path, "wb+") as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)
        return file_path
    
#region[black] Handle Capture

    def _handle_capture(self, start):
        if start == self.is_camera_started:
            return False
        if start:
            self.cap = cv2.VideoCapture(self.file_path if self.file_path else 0)
            if not self.cap.isOpened():
                raise RuntimeError("Failed to open capture device.")
            self.is_camera_started = True
            self.correctreps = 0
            self.incorrectreps = 0
            self.stage = ""
            self.feedback = ""
            self.flag = False
            self.situpflag = True
            self.flag_count_cor = False
            self.prev_angle1=0
            self.prev_angle2=0
            self.done=False
            self.notdone=False
            self.elbow_done=False
            self.elbow_notdone=False
            self.workouts = {
                "Incline Barbell Bench Press": self.BenchPress,
                "Sit Up": self.Situp,
                "Chest Fly Machine": self.ChestFlyMachine,
                "Dumbbell Curl":self.Dumbell_bicepscurl,
                "Barbell Curl":self.barbellcurl,
                # Add more workouts here
            }
        else:
            if self.cap is not None:
                self.cap.release()
            self.is_camera_started = False
            if self.file_path and os.path.exists(self.file_path):
                os.remove(self.file_path)
                self.file_path = None
        return True

#endregion

#region[Teal] Start Capture
    
    def start_capture(self, vid=None):
        if vid is not None:
            self.file_path = self._save_temp_file(vid)
        return self._handle_capture(True)

#endregion 
 
#region[Salmon] Stop Capture   

    def stop_capture(self):
        return self._handle_capture(False)
    
#endregion

#region[brown] Calculate Angle

    def calculate_angle(self, a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
            a[1] - b[1], a[0] - b[0]
        )
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

#endregion

#region[pink] Calculate Distance
 
    def calculate_distance(self, a, b):
        # Convert points to NumPy arrays
        a = np.array(a)
        b = np.array(b)

        # Calculate the distance
        distance = np.linalg.norm(b - a)

        return distance
    
#endregion
    
#region[purple]    Check Visibility

    def check_visibility(self, results):
   
        main_landmarks = [0, 11, 12, 13, 14, 15, 16, 23, 24] # Lista dei landmark principali
        try:
            for index in main_landmarks:
                landmark = results.pose_landmarks.landmark[index]
                if float(landmark.visibility) <= 0.3:
                    return False
        except:
            return False
        return True
    
#endregion

#region[green] Workouts

    def BenchPress(self, landmarks):

        # Get coordinates
        shoulderl = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].z,
        ]
        elbowl = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].z,
        ]
        wristl = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y,
            landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].z,
        ]

        shoulderr = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z,
        ]
        elbowr = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].z,
        ]
        wristr = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].z,
        ]

        hipl = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y,
            landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].z,
        ]
        hipr = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].z,
        ]

        # Calculate angle
        angle1 = self.calculate_angle(shoulderl, elbowl, wristl)
        angle2 = self.calculate_angle(shoulderr, elbowr, wristr)
        angle3 = self.calculate_angle(hipl, shoulderl, elbowl)
        angle4 = self.calculate_angle(hipr, shoulderr, elbowr)

        # Curl counter logic
        if angle1 < 65 and angle2 < 65:
            self.stage = "down"
            self.flag = False
            if angle3 > 77 and angle4 > 77:
                self.feedback = "close your hands"
                badSound.play()
                self.flag = True

        if angle1 > 100 and self.stage == "down" and angle2 > 100 and self.flag is True:
            self.stage = "up"
            self.incorrectreps += 1
            print("Incorrects Reps :", self.incorrectreps)

        if (
            angle1 > 100
            and self.stage == "down"
            and angle2 > 100
            and self.flag is False
        ):
            self.stage = "up"
            self.correctreps += 1
            self.feedback = "Perfect"
            perfectSound.play()
            
            print("Corrects Reps :", self.correctreps)
            
    def Situp(self, landmarks):

        
        left_hip = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y,
        ]
        left_knee = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y,
        ]
        left_ankle = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y,
        ]
        right_hip = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y,
        ]
        right_knee = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y,
        ]
        right_ankle = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y,
        ]
        left_elbow = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
        ]
        left_shoulder = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
        ]
        right_elbow = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
        ]
        right_shoulder = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
        ]
        
        left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
        left_shoulder_angle   = self.calculate_angle(left_elbow,left_shoulder,left_hip)
        right_shoulder_angle = self.calculate_angle(right_elbow,right_shoulder,right_hip)
        left_hip_angle = self.calculate_angle(left_shoulder, left_hip,left_knee)
        right_hip_angle = self.calculate_angle(right_shoulder, right_hip,right_knee)
        
        if (left_shoulder_angle >= 13 or right_shoulder_angle<3) and (left_knee_angle <= 90 or right_knee_angle <=90) and (left_hip_angle < 55 or right_hip_angle < 60):
                        self.stage = "up"
        if (left_hip_angle > 130 or right_hip_angle > 130) and self.stage == 'up':
                    self.stage = "down"
                    if self.situpflag==False:
                        self.incorrectreps += 1
                        print("Incorrect Reps :", self.incorrectreps)
                        self.situpflag = True
                    else:
                        self.correctreps += 1
                        print("Correct Reps :", self.correctreps)
                        self.feedback = "Perfect"
                        perfectSound.play()

        if (left_hip_angle > 130 or right_hip_angle > 130) and self.stage == 'down':
                self.stage = "down"
                

        if (left_hip_angle <= 29 or right_hip_angle <= 29) and self.stage == 'up':
                self.feedback = "Keep your shoulder slightly away from your knee"
                badSound.play()
                self.situpflag = False
                                          
    def ChestFlyMachine(self, landmarks):

        left_shoulder = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
        ]
        left_elbow = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
        ]
        left_wrist = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y,
        ]

        right_wrist = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
        ]

        left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)

        distance = self.calculate_distance(right_wrist, left_wrist)

        if distance > 0.38:
            self.stage = "Open"
        if (distance > 0.38) and self.flag == True:
            self.stage = "Open"
            if self.flag_count_cor == False:
                self.incorrectreps += 1
                print("Incorrect Reps :", self.incorrectreps)
            else:
                self.correctreps += 1
                print("Correct Reps :", self.correctreps)
                self.feedback = "Perfect"
                perfectSound.play()
            self.flag = False
        if (distance < 0.09) and self.stage == "Open":
            self.stage = "Close"
            self.flag = True
        if (distance < 0.09) and self.stage == "Close":
            self.stage = "Close"
            self.flag = True
        if (left_elbow_angle < 135) and self.stage == "Close" and distance < 0.09:
            self.flag_count_cor = False
            self.feedback = "Make your elbow straight"
            badSound.play()

        elif (left_elbow_angle > 135) and self.stage == "Close":
            self.flag_count_cor = True

    def barbellcurl(self, landmarks):
        left_shoulder = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
        ]
        
        right_shoulder = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
        ]
        left_elbow = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
        ]
        
        right_elbow = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
        ]
        left_wrist = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y,
        ]

        right_wrist = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
        ]
        Left_hip = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y,
        ]
                
        Right_hip = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y,
        ]
                        
        Left_knee = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y,
        ]
                                
        Right_knee = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y,
        ]


        #calculate the angles 
        Left_shoulder_angle=self.calculate_angle(Left_hip,left_shoulder,left_elbow)
        Right_shoulder_angle=self.calculate_angle(Right_hip,right_shoulder,right_elbow)
        Left_elbow_angle=self.calculate_angle(left_shoulder,left_elbow,left_wrist)
        Right_elbow_angle=self.calculate_angle(right_shoulder,right_elbow,right_wrist)
        Left_hip_angle=self.calculate_angle(left_shoulder,Left_hip,Left_knee)
        Right_hip_angle=self.calculate_angle(right_shoulder,Right_hip,Right_knee)

    
        #two sides
        if round(Left_elbow_angle)>=self.prev_angle1:
            self.prev_angle1=round(Left_elbow_angle)
        else:
            if Left_elbow_angle>160 and Right_elbow_angle>160:
                if self.stage =="UP" or self.stage=="" :
                    self.stage ="DOWN" 
                    if self.done==True and self.notdone==False:
                        self.correctreps+=1
                        print("Correct Reps :", self.correctreps)
                        self.done=False
                    if self.notdone==True and self.done==False :
                        self.incorrectreps+=1
                        print("Incorrect Reps :", self.incorrectreps)
                        self.notdone=False    
                    self.prev_angle1=round(Left_elbow_angle)
                    self.prev_angle2=round(Left_elbow_angle)
        if round(Left_elbow_angle)<=self.prev_angle2:
            self.prev_angle2=round(Left_elbow_angle)
            
        else:

            if (Left_elbow_angle<=30 and Left_shoulder_angle<=20 and Left_hip_angle>168) and (Right_elbow_angle<=30 and Right_shoulder_angle<=20 and Right_hip_angle>168) and self.stage=="DOWN" and self.done ==False:
                self.stage="UP"
                self.done=True

            elif ((140>=Left_elbow_angle>30 or Left_shoulder_angle>20 or Left_hip_angle<168)or(140>=Right_elbow_angle>30 or Right_shoulder_angle>20 or Right_hip_angle<168)) and self.stage=="DOWN" and self.notdone==False :
                if self.prev_angle2<=30:
                        self.elbow_done=True    
                        self.stage="UP"
                if 140>=Left_elbow_angle>30 or 140>=Right_elbow_angle>30:
                    self.feedback = "Narrow your elbows"
                    self.stage="UP"
                    self.notdone=True
                    self.elbow_notdone=True

                if Left_shoulder_angle>20 or Right_shoulder_angle>20:
                    self.feedback = "keep your arms straight down"
                    if self.elbow_done==True or self.elbow_notdone==True :
                        self.notdone=True   

                if Left_hip_angle<168 or Right_hip_angle<168:
                    self.feedback = "keep your hips straight"
                    if self.elbow_done==True or self.elbow_notdone==True :
                        self.notdone=True
                self.elbow_done=False 
                self.elbow_notdone=False 
            self.prev_angle1=round(Left_elbow_angle)
            self.prev_angle2=round(Left_elbow_angle)

    def Dumbell_bicepscurl(self, landmarks):

        left_shoulder = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
        ]
        
        right_shoulder = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
        ]
        left_elbow = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
        ]
        
        right_elbow = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
        ]
        left_wrist = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y,
        ]

        right_wrist = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
        ]
        Left_hip = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y,
        ]
                
        Right_hip = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y,
        ]
                        
        Left_knee = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y,
        ]
                                
        Right_knee = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y,
        ]


        #calculate the angles 
        Left_shoulder_angle=self.calculate_angle(Left_hip,left_shoulder,left_elbow)
        Right_shoulder_angle=self.calculate_angle(Right_hip,right_shoulder,right_elbow)
        Left_elbow_angle=self.calculate_angle(left_shoulder,left_elbow,left_wrist)
        Right_elbow_angle=self.calculate_angle(right_shoulder,right_elbow,right_wrist)
        Left_hip_angle=self.calculate_angle(left_shoulder,Left_hip,Left_knee)
        Right_hip_angle=self.calculate_angle(right_shoulder,Right_hip,Right_knee)

    
        #two sides
        if round(Left_elbow_angle)>=self.prev_angle1:
            self.prev_angle1=round(Left_elbow_angle)
        else:
            if Left_elbow_angle>160 or Right_elbow_angle>160:
                if self.stage =="UP" or self.stage=="" :
                    self.stage ="DOWN" 
                    if self.done==True and self.notdone==False:
                        self.correctreps+=1
                        self.done=False
                    if self.notdone==True and self.done==False :
                        self.incorrectreps+=1
                        self.notdone=False    
                    self.prev_angle1=round(Left_elbow_angle)
                    self.prev_angle2=round(Left_elbow_angle)
        if round(Left_elbow_angle)<=self.prev_angle2:
            self.prev_angle2=round(Left_elbow_angle)
            
        else:

            if (Left_elbow_angle<=30 and Left_shoulder_angle<=20 and Left_hip_angle>168) or (Right_elbow_angle<=30 and Right_shoulder_angle<=20 and Right_hip_angle>168) and self.stage=="DOWN" and self.done ==False:
                self.stage="UP"
                self.done=True

            elif ((140>=Left_elbow_angle>30 or Left_shoulder_angle>20 or Left_hip_angle<168)or(140>=Right_elbow_angle>30 or Right_shoulder_angle>20 or Right_hip_angle<168)) and self.stage=="DOWN" and self.notdone==False :
                if self.prev_angle2<=30:
                        self.elbow_done=True    
                        self.stage="UP"
                if 140>=Left_elbow_angle>30 or 140>=Right_elbow_angle>30:
                    self.feedback = "Narrow your elbows"
                    self.stage="UP"
                    self.notdone=True
                    self.elbow_notdone=True

                if Left_shoulder_angle>20 or Right_shoulder_angle>20:
                    self.feedback = "keep your arms straight down"
                    if self.elbow_done==True or self.elbow_notdone==True :
                        self.notdone=True   

                if Left_hip_angle<168 or Right_hip_angle<168:
                    self.feedback = "keep your hips straight"
                    if self.elbow_done==True or self.elbow_notdone==True :
                        self.notdone=True
                self.elbow_done=False 
                self.elbow_notdone=False 
            self.prev_angle1=round(Left_elbow_angle)
            self.prev_angle2=round(Left_elbow_angle)

#endregion

#region[Red] Get Frames

    def get_frame(self, workout_name):

        while self.is_camera_started:
            success, frame = self.cap.read()
            if not success:
                # Log a message instead of raising an error
                print("Failed to read frame from camera.")
                break  # Break out of the loop if failed to read frame

            # # Increment counter
            # self.counter += 1

            # Recolor image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_frame.flags.writeable = False

            # Make detection
            results = self.pose.process(rgb_frame)

            # Recolor back to BGR
            rgb_frame.flags.writeable = True

            rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            if self.check_visibility(results) and results.pose_landmarks:
                self.feedback = " "
            
                landmarks = results.pose_landmarks.landmark
                workout = self.workouts.get(workout_name)
                

                if workout:
                    workout(landmarks)
                else:
                    print("No Workout")

            
            else:
                self.feedback = "⚠️Please move away from the camera a bit"
                badSound.play()

            # Render detections
            frame_with_landmarks = self.render_pose(results, frame)

            # Encode frame to jpeg
            ret, jpeg = cv2.imencode(".jpg", frame_with_landmarks)
            if not ret:
                # Log a message instead of raising an error
                print("Failed to encode frame to jpeg.")
                break  # Break out of the loop if failed to encode frame
            yield jpeg.tobytes(), results.pose_landmarks

#endregion

#region[White] Render Pose

    def render_pose(self, results, frame):
        if results.pose_landmarks:
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(
                    color=(224, 224, 224), thickness=2, circle_radius=2
                ),
                mp_drawing.DrawingSpec(
                    color=(255, 255, 0), thickness=1, circle_radius=2
                ),
            )
        return frame

#endregion

#region[blue] Get Camera Status

    def get_camera_status(self):
        return (
            self.is_camera_started,
            self.stage,
            self.correctreps,
            self.incorrectreps,
            self.feedback,
        )

#endregion