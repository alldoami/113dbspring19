import tensorflow as tf
print(tf.__version__)
import cv2
print(cv2.__version__)
import time
import os
import numpy as np
import posenet
from collections import deque


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return 180*(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))/np.pi

def findMax(q): #Finds the maximum height
	if q[3] < q[0] and q[3] < q[1] and q[3] < q[2] and q[3] < q[4] and q[3] < q[5] and q[3] < q[6]:
		return q[3]
	else:
		return 0

def findMin(q): #Finds the minimum height
	if q[3] > q[0] and q[3] > q[1] and q[3] > q[2] and q[3] > q[4] and q[3] > q[5] and q[3] > q[6]:
		return q[3]
	else:
		return 0

def compareTolerance(list_current, average_prev, tolerance):
    print(list_current)
    average_current = np.mean(np.asarray(list_current))
    difference = np.abs(average_current - average_prev)
    if difference < tolerance*average_current:
        return False
    else:
        return True

    
def main():
    path_input = './exercises'
    path_output = './output' #pictures of minimum
    print_min = True
    model_number = 101
    scale_factor = 0.2
    delay = 3 #queue delay
    exercise = "squat_side"
    video_format = ".avi"
    body_points = {'rightShoulder':None,'rightWrist':None,'rightElbow':None,'leftShoulder':None,'leftWrist':None,'leftElbow':None,'rightHip':None,'leftHip':None,'rightKnee':None,'leftKnee':None}
    body_points_score = {'rightShoulder':None,'rightWrist':None,'rightElbow':None,'leftShoulder':None,'leftWrist':None,'leftElbow':None,'rightHip':None,'leftHip':None,'rightKnee':None,'leftKnee':None}
    
    with tf.Session() as sess:
        model_cfg, model_outputs = posenet.load_model(model_number, sess)
        output_stride = model_cfg['output_stride']
        cap = cv2.VideoCapture(exercise+video_format)
        cap.set(3, 1080)
        cap.set(4, 1920)
        #coordinate queue
        runningQ = deque()
        #create other queues to get more info
        moreInfoQ = deque()
        imageQ = deque()
        infoQ = deque()
        start = time.time()
        frame_count = 0
        picture_count = 1
        delay_count = 0
        avg_count = 10
        avg_counter = 0
        threshold = 0
        tolerance = 0.2
        next_maxima = 'N/A'
        maxima_text = 'N/A'
        max_count = 0
        # keeps track of prev average
        prev_average = 0
        init_position = 0
        c_r = deque()
        c_l = deque()
        # hips past knees
        hips = []
        # maximum angles
        st = []
        # minimum angles
        sb = []
        while True:
            res, img = cap.read()
            if not res:
                break
            else:
                input_image, display_image, output_scale = posenet.process_input(img, scale_factor, output_stride)
            info_dict = {"Body Points": None, "Body Points Score": None, "Scores Right": None, "Scores Left": None, "Image": None}
        
           
            #input_image, display_image, output_scale = posenet.read_cap(
              #  cap, scale_factor=0.2, output_stride=output_stride)
            
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
            
            # CHANGE THE RESOLUTION OF THE OUTPUT VIDEO
            #overlay_image = cv2.resize(overlay_image, (1920, 1080))
            overlay_image = cv2.resize(overlay_image, (600, 900))
            
            # RESET VARIABLES FOR FOUND MAXIMA
            maxima_found = False
            
            # APPEND THE IMAGE TO THE IMAGEQ
            imageQ.append(overlay_image)
            for pi in range(len(pose_scores)):
                if pose_scores[pi] == 0.:
                    break
                #logging.warning('Pose #%d, score = %f' % (pi, pose_scores[pi]))
                for ki, (s, c) in enumerate(zip(keypoint_scores[pi, :], keypoint_coords[pi, :, :])):
                    if posenet.PART_NAMES[ki] == "leftEye":
                        #print('Keypoint %s, score = %f, coord = %s' % (posenet.PART_NAMES[ki], s, c))
                        #adding coordinate to running queue
                        runningQ.append(c[0])
                        #append more infomation to other queues here
                        
                        #if length equals 7, then will see if mid point is the min
                        if init_position == 0:
                            init_position = c[0]
                        if len(runningQ) == 7:
                            if findMin(runningQ) != 0 and compareTolerance(runningQ,prev_average, tolerance):
                                maxima_found = True
                                maxima_text = 'Minimum'
                                prev_average = np.mean(np.asarray(runningQ))
                                print(maxima_text)
                                max_count += 1
                            if findMax(runningQ) != 0 and compareTolerance(runningQ,prev_average, tolerance):
                                maxima_found = True
                                maxima_text = 'Maximum'
                                prev_average = np.mean(np.asarray(runningQ))
                                print(maxima_text)
                                max_count += 1
                            runningQ.popleft()
                            
                            #popleft to all other queues you create for more info here
                    if posenet.PART_NAMES[ki] in body_points:
                        body_points[posenet.PART_NAMES[ki]] = c
                        body_points_score[posenet.PART_NAMES[ki]] = s
            
                            
                        
            
            #Calculate the average confidence score of the shoulder, elbow, and wrist
            confidence_right = body_points_score['rightShoulder'] + body_points_score['rightElbow'] + body_points_score['rightWrist']
            confidence_left = body_points_score['leftShoulder'] + body_points_score['leftElbow'] + body_points_score['leftWrist']
            confidence_right /= 3
            confidence_left /= 3
            
            # STORE INFORMATION INTO DICTIONARY
            info_dict['Body Points'] = body_points
            info_dict['Body Points Score'] = body_points_score
            info_dict['Scores Right'] = confidence_right
            info_dict['Scores Left'] = confidence_left
            info_dict['Image'] = overlay_image
            
            if delay_count < delay:
                infoQ.append(info_dict)
                delay_count+=1
            else:
                oldQ = infoQ.popleft()
                infoQ.append(info_dict)
                
            if avg_counter < avg_count:    
                c_r.append(confidence_right)
                c_l.append(confidence_left)
                avg_counter += 1
            else:
                c_r.popleft()
                c_l.popleft()
                c_r.append(confidence_right)
                c_l.append(confidence_left)
            
            # MAKE IT SO WE CAN ONLY HAVE ALTERNATING MAXIMUM AND MINIMUM
            if next_maxima == 'N/A':
                next_maxima = maxima_text
            elif maxima_text != next_maxima:
                next_maxima = maxima_text
            else: 
                maxima_found = False
            
            
            if print_min and maxima_found: 
                avg_r = 0
                avg_l = 0
                for i in np.arange(avg_count):
                    avg_r += c_r[i]
                    avg_l += c_l[i]
                avg_r /= avg_count
                avg_l /= avg_count
                if (avg_r > threshold and avg_l > threshold) or (oldQ['Scores Right'] > threshold and oldQ['Scores Left'] > threshold):
                    #Calculate angle between shoulder and wrist using the elbow as the origin
                    if(oldQ['Body Points']['leftHip'][0] < oldQ['Body Points']['leftKnee'][0]*1.3 and oldQ['Body Points']['leftHip'][0] > oldQ['Body Points']['leftKnee'][0]*0.7):
                        hips.append(1)
                        print('ADDED')
                    else:
                        hips.append(0)
                        print('NOT ADDED')

                    angle_right = angle((oldQ['Body Points']['rightShoulder']-oldQ['Body Points']['rightElbow']),(oldQ['Body Points']['rightWrist']-oldQ['Body Points']['rightElbow']))
                    angle_left = angle((oldQ['Body Points']['leftShoulder']-oldQ['Body Points']['leftElbow']),(oldQ['Body Points']['leftWrist']-oldQ['Body Points']['leftElbow']))
                    if maxima_text == 'Maximum':
                        st.append(angle_right)
                        st.append(angle_left)
                    else:
                        sb.append(angle_right)
                        sb.append(angle_left)
                    print('For image number: ', picture_count)
                    print(maxima_text, ' Height Found')
                    print('Angle Right: %f degrees with confidence %f and average confidence %f' %(angle_right,oldQ['Scores Right'],avg_r))
                    print('Angle Left: %f degrees with confidence %f and average confidence %f' %(angle_left,oldQ['Scores Left'],avg_l))
                    print()
                    cv2.imwrite(r'C:\Users\Allison\Desktop\113dbspring19-master\posenet-python-master\posenet-python-master\output' + maxima_text + ' ' + exercise + ' ' +  str(picture_count) + '.jpg',oldQ['Image'])
                    
                    picture_count += 1
            cv2.imshow('posenet', overlay_image)
            frame_count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        st = np.asarray(st)
        sb = np.asarray(sb)
        hips = np.asarray(hips)

        print('Average number of times hips passed knees: %f' %(np.mean(hips)))
        print('The maximum angle average is %f and the standarad deviation is %f'% (np.mean(st),np.std(st)))
        print('The minimum angle average is %f and the standarad deviation is %f'% (np.mean(sb),np.std(sb)))
        print(max_count)
        cap.release()
        cv2.destroyAllWindows();
        print('Average FPS: ', frame_count / (time.time() - start))

if __name__ == "__main__":
    main()
