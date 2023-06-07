import cv2
import glob
import re
import os
import time
import multiprocessing

def process_frame(frame):
    img, save_path, count = frame
    cv2.imwrite(save_path + "frame_%d.jpg" % count, img)

if __name__ == "__main__":
    start = time.time()
    
    vid_path = "./" + "Video_Media" + ".mp4"
    save_path = "./outputs/"
    output_name = "./" + "Output_Name" + ".mp4"
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # Taking the video file
    vidcap = cv2.VideoCapture(vid_path)
    success, image = vidcap.read()
    count = 1
    success = True
    
    # Images are saving frame by frame
    frames = []
    while success:
        success, image = vidcap.read()
        if success:
            frames.append((image, save_path, count))
            count += 1
    
    vidcap.release()
    
    # Creating a pool of processes
    pool = multiprocessing.Pool()
    
    # Saving images in barallel
    pool.map(process_frame, frames)
    pool.close()
    pool.join()
    
    img_array = []
    size = None
    
    # Taking the images which will transform to video
    image_files = sorted(glob.glob(save_path + "frame_*.jpg"), key=lambda x: int(re.findall(r'\d+', x)[0]))
    for filename in image_files:
        img = cv2.imread(filename)
        
        if size is None:
            height, width, _ = img.shape
            size = (width, height)
        
        img_array.append(img)
    
    out = cv2.VideoWriter(output_name, cv2.VideoWriter_fourcc(*'mp4v'), 30, size)
    
    for img in img_array:
        out.write(img)
    
    out.release()
    
    print("Took",time.time() - start, "second")
	
