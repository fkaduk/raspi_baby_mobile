import cv2
import mediapipe as mp


def test_extract_orientation_from_frame():
    degrees_tolerance = 2

    def test_extract_right_orientation_from_frame():
        image_path = "tests/baby_right.jpg"
        reference_orientation = 45

        img = cv2.imread(image_path)
        facemesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)

        orientation = extract_head_orientation_from_frame(img, facemesh=facemesh)

        assert (reference_orientation - degrees_tolerance) < orientation["yaw"]
        assert (reference_orientation + degrees_tolerance) > orientation["yaw"]
