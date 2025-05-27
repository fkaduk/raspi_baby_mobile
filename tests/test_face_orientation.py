import cv2
import mediapipe as mp

import raspi_baby_mobile

degrees_tolerance = 8


def test_extract_right_orientation_from_frame():
    image_path = "tests/baby_right.jpg"
    reference_orientation = 55

    img = cv2.imread(image_path)
    facemesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)

    orientation = raspi_baby_mobile.extract_head_orientation_from_frame(img, facemesh=facemesh)
    facemesh.close()

    print(orientation["yaw"])

    assert (reference_orientation - degrees_tolerance) < orientation["yaw"]
    assert (reference_orientation + degrees_tolerance) > orientation["yaw"]


def test_extract_left_orientation_from_frame():
    image_path = "tests/baby_left.jpg"
    reference_orientation = -55

    img = cv2.imread(image_path)
    facemesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)

    orientation = raspi_baby_mobile.extract_head_orientation_from_frame(img, facemesh=facemesh)
    facemesh.close()

    print(orientation["yaw"])

    assert (reference_orientation - degrees_tolerance) < orientation["yaw"]
    assert (reference_orientation + degrees_tolerance) > orientation["yaw"]


def test_extract_center_orientation_from_frame():
    image_path = "tests/baby_center.jpg"
    reference_orientation = 0

    img = cv2.imread(image_path)
    facemesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)

    orientation = raspi_baby_mobile.extract_head_orientation_from_frame(img, facemesh=facemesh)
    facemesh.close()

    print(orientation["yaw"])

    assert (reference_orientation - degrees_tolerance) < orientation["yaw"]
    assert (reference_orientation + degrees_tolerance) > orientation["yaw"]
