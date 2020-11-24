import os
import cv2
import glob
import numpy as np
import subprocess
import matplotlib.pyplot as plt


def unwarp(img, src, dst, i, hw, M):
    h, w = hw
    # use cv2.warpPerspective() to warp your image to a top-down view
    warped = cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_LINEAR)
    warped = warped[:,:400,:]
    grid_inc = warped.shape[0] / 10
    for j in range(10):
        # make line all the way across
        cv2.line(warped, (int(j*grid_inc), 0), (int(j*grid_inc), h), (255, 0, 0, 0.4), thickness=1)
        cv2.line(warped, (0, int(j*grid_inc)), (w, int(j*grid_inc)), (255, 0, 0, 0.4), thickness=1)

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    f.subplots_adjust(hspace=.2, wspace=.1)
    ax1.imshow(img)
    x = [src[0][0], src[2][0], src[3][0], src[1][0], src[0][0]]
    y = [src[0][1], src[2][1], src[3][1], src[1][1], src[0][1]]
    ax1.plot(x, y, color='red', alpha=0.5, linewidth=2, solid_capstyle='butt', zorder=2)
    ax1.set_ylim([h, 0])
    ax1.set_xlim([0, w])
    ax1.set_title('Original', fontsize=30)
    ax2.imshow(cv2.flip(warped, 1))
    ax2.set_title('Homographied', fontsize=30)
    #plt.show()
    path = "rectified/%03d.png" % i
    plt.savefig(path)
    plt.close()
    return warped

# We will first manually select the source points
# we will select the destination point which will map the source points in
# original image to destination points in unwarped image
src = np.float32([(10, 124),     # left
                  (299,  33),   # top
                  (299, 370),   # bottom
                  (589,  124)]) # right

dst = np.float32([(400, 0),
                  (0, 0),
                  (400, 400),
                  (0, 400)])

cap = cv2.VideoCapture('test.mp4')
i = 0
setup = False
while cap.isOpened():
    ret, im = cap.read()
    if not setup:
        h, w = im.shape[:2]
        M = cv2.getPerspectiveTransform(src, dst)
        setup = True
    if im is None: break
    im = im[:,:,::-1]
    im = unwarp(im, src, dst, i, (h,w), M)
    #im = im[:,::-1,::-1]
    # path = "rectified/%03d.png" % i
    # cv2.imwrite(path, im)
    i += 1

out_fps = "10"
in_fps = "10"
subprocess.call([
    'ffmpeg', '-framerate', in_fps, '-i', 'rectified/%03d.png', '-r', out_fps, '-pix_fmt', 'yuv420p',
    'erect_arena.mp4'
])
# clean up!
for file_name in glob.glob("rectified/*.png"):
    os.remove(file_name)