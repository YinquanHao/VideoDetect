import os
import cv2
import time
import argparse
import multiprocessing
import numpy as np
import tensorflow as tf
import imageio
import sys
imageio.plugins.ffmpeg.download()
from matplotlib import pyplot as plt
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from PIL import Image
from moviepy.editor import VideoFileClip

CWD_PATH = os.getcwd()
print(sys.argv[1])
def main(argv):
	# Path to frozen detection graph. This is the actual model that is used for the object detection.
	MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
	PATH_TO_CKPT = os.path.join(CWD_PATH,  'object_detection', MODEL_NAME, 'frozen_inference_graph.pb')

	# List of the strings that is used to add correct label for eachPATH_TO_CKPT box.
	PATH_TO_LABELS = os.path.join(CWD_PATH, 'object_detection', 'data', 'mscoco_label_map.pbtxt')
	PATH_TO_OUTPUT_IMG = os.path.join(CWD_PATH,  'output_imgs')

	print("PATH_TO_CKPT:",PATH_TO_CKPT)
	print("PATH_TO_LABELS:",PATH_TO_LABELS)
	category_index = load_label(PATH_TO_LABELS)

	# First test on images
	PATH_TO_TEST_IMAGES_DIR = 'object_detection/test_images'
	TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 4) ]
	print("TEST_IMAGE_PATHS:",TEST_IMAGE_PATHS)
	# Size, in inches, of the output images.
	IMAGE_SIZE = (12, 8)

	for image_path in TEST_IMAGE_PATHS:
	  	image = Image.open(image_path)
	  	print("z:",image_path)
	  	image_np = load_image_into_numpy_array(image)
	  	plt.imshow(image_np)
	  	print(image.size, image_np.shape)
	  	print("d")


	detection_graph = tf.Graph()

	with detection_graph.as_default():
		od_graph_def = tf.GraphDef()
		with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
			serialized_graph = fid.read()
			od_graph_def.ParseFromString(serialized_graph)
			tf.import_graph_def(od_graph_def, name='')

	with detection_graph.as_default():
		with tf.Session(graph=detection_graph) as sess:
			print("b")
			ct = 0
			for image_path in TEST_IMAGE_PATHS:
				image = Image.open(image_path)
				image_np = load_image_into_numpy_array(image)
				print(image_path)
				image_process = detect_objects(image_np, sess, detection_graph,category_index)
				print(image_process.shape)
				plt.figure(figsize=IMAGE_SIZE)
				plt.imshow(image_process)
				#plt.show()
				plt.savefig(PATH_TO_OUTPUT_IMG+'/'+str(ct) + '.jpg')
				print(str(ct) + '.jpg')
				ct = ct+1
	def process_image(image):
		print('enter process_image')
		with detection_graph.as_default():
			with tf.Session(graph=detection_graph) as sess:
				image_process = detect_objects(image, sess, detection_graph,category_index)
				return image_process
	white_output = 'output/'+ argv + 'out.mp4'
	clip1 = VideoFileClip('input/'+ argv +'.mp4').subclip(0,5)
	white_clip = clip1.fl_image(process_image)
	white_clip.write_videofile(white_output, audio=False)



def load_label(PATH_TO_LABELS):
	NUM_CLASSES = 90
	# Loading label map
	label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
	categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
	category_index = label_map_util.create_category_index(categories)
	print("Finished Load label:")
	return category_index

def detect_objects(image_np, sess, detection_graph,category_index):
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Actual detection.
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8)
    return image_np

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)





if __name__ == "__main__":
	main(sys.argv[1])
