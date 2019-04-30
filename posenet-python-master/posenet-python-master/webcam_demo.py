import tensorflow as tf
import cv2
import time
import argparse
import os
import logging
import posenet
from collections import deque
import upload_file_gui as upload_file_gui

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=int, default=101)
parser.add_argument('--cam_id', type=int, default=0)
parser.add_argument('--cam_width', type=int, default=1280)
parser.add_argument('--cam_height', type=int, default=720)
parser.add_argument('--scale_factor', type=float, default=0.7125)
args = parser.parse_args()

def findMin(q):
	if q[3] < q[0] and q[3] < q[1] and q[3] < q[2] and q[3] < q[4] and q[3] < q[5] and q[3] < q[6]:
		return q[3]
	else:
		return 0

def findMax(q):
	if q[3] > q[0] and q[3] > q[1] and q[3] > q[2] and q[3] > q[4] and q[3] > q[5] and q[3] > q[6]:
		return q[3]
	else:
		return 0

def main():
    with tf.Session() as sess:
        model_cfg, model_outputs = posenet.load_model(args.model, sess)
        output_stride = model_cfg['output_stride']
        #cap = cv2.VideoCapture(args.cam_id)
        fileUploaded = upload_file_gui.uploadFileGUI()
        logging.warning(fileUploaded)
        cap = cv2.VideoCapture(fileUploaded)
        #cap.set(3, args.cam_width)
        #cap.set(4, args.cam_height)
        cap.set(3, 1080)
        cap.set(4, 1920)

        start = time.time()
        frame_count = 0
        #coordinate queue
        runningQ = deque()

        #create other queues to get more info
        moreInfoQ = deque()
        while True:
            input_image, display_image, output_scale = posenet.read_cap(
                cap, scale_factor=0.4, output_stride=output_stride)
            #output_stride
            #args.scale_factor
            heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
                model_outputs,
                feed_dict={'image:0': input_image}
            )

            pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multi.decode_multiple_poses(
                heatmaps_result.squeeze(axis=0),
                offsets_result.squeeze(axis=0),
                displacement_fwd_result.squeeze(axis=0),
                displacement_bwd_result.squeeze(axis=0),
                output_stride=output_stride,
                max_pose_detections=10,
                min_pose_score=0.15)

            keypoint_coords *= output_scale

            # TODO this isn't particularly fast, use GL for drawing and display someday...
            overlay_image = posenet.draw_skel_and_kp(
                display_image, pose_scores, keypoint_scores, keypoint_coords,
                min_pose_score=0.15, min_part_score=0.1)

            overlay_image = cv2.resize(overlay_image, (600, 900))

            for pi in range(len(pose_scores)):
                if pose_scores[pi] == 0.:
                    break
                #logging.warning('Pose #%d, score = %f' % (pi, pose_scores[pi]))
                for ki, (s, c) in enumerate(zip(keypoint_scores[pi, :], keypoint_coords[pi, :, :])):
                	if posenet.PART_NAMES[ki] == "nose":
                	    logging.warning('Keypoint %s, score = %f, coord = %s' % (posenet.PART_NAMES[ki], s, c))
                	   	#adding coordinate to running queue
                	    runningQ.append(c[0])
                	    #append more infomation to other queues here

                	    #if length equals 7, then will see if mid point is the min
                	    if len(runningQ) == 7:
                	    	if findMin(runningQ) != 0:
                	    		logging.warning('FOUND MIN')
                	    		logging.warning(findMin(runningQ))
                	    	if findMax(runningQ) != 0:
                	    		logging.warning('FOUND MAX')
                	    		logging.warning(findMax(runningQ))
                	    	runningQ.popleft()
                	    	#popleft to all other queues you create for more info here

            cv2.imshow('posenet', overlay_image)
            frame_count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print('Average FPS: ', frame_count / (time.time() - start))


if __name__ == "__main__":
    main()
