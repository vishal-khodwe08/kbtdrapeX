import cv2
import mediapipe as mp
import numpy as np
import uuid

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def generate_saree_tryon(person_path, saree_path):

    person = cv2.imread(person_path)
    saree = cv2.imread(saree_path)

    person_rgb = cv2.cvtColor(person, cv2.COLOR_BGR2RGB)

    results = pose.process(person_rgb)

    h, w, _ = person.shape

    if results.pose_landmarks:

        left_shoulder = results.pose_landmarks.landmark[11]
        right_shoulder = results.pose_landmarks.landmark[12]
        left_hip = results.pose_landmarks.landmark[23]

        x1 = int(left_shoulder.x * w)
        y1 = int(left_shoulder.y * h)

        x2 = int(right_shoulder.x * w)
        y2 = int(right_shoulder.y * h)

        x3 = int(left_hip.x * w)
        y3 = int(left_hip.y * h)

        saree_resized = cv2.resize(saree, (abs(x2-x1)+150, abs(y3-y1)+200))

        overlay = person.copy()

        y_offset = y1
        x_offset = x1 - 70

        sh, sw, _ = saree_resized.shape

        overlay[y_offset:y_offset+sh, x_offset:x_offset+sw] = saree_resized

        output = cv2.addWeighted(overlay, 0.7, person, 0.3, 0)

    else:
        output = person

    filename = "outputs/" + str(uuid.uuid4()) + ".jpg"

    cv2.imwrite(filename, output)

    return filename