import os
import cv2
import glob
import numpy as np
import subprocess
import multi_color_hist as mch
import matplotlib.pyplot as plt


def unwarp(img, src, i, hw, M):
    path = "rectified/%03d.png" % i
    hist_path = "rectified/hist_%03d.png" % i
    h, w = hw
    # use cv2.warpPerspective() to warp your image to a top-down view
    warped = cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_LINEAR)
    # warped = warped[25:360,22:365,:]
    # warped = warped[44:-26, 46:-30,:] # T:B,R:L
    warped = warped[69:334, 68:335, :] # T:B,R:L
    warped = mch.add_hist_grid(warped, hist_path)

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    f.subplots_adjust(hspace=.2, wspace=.1)
    ax1.imshow(img)
    x = [src[0][0], src[2][0], src[3][0], src[1][0], src[0][0]]
    y = [src[0][1], src[2][1], src[3][1], src[1][1], src[0][1]]
    ax1.plot(x, y, color='blue', alpha=0.5, linewidth=1, solid_capstyle='butt', zorder=2)
    ax1.set_ylim([h, 0])
    ax1.set_xlim([0, w])
    ax1.set_title('Original', fontsize=30)
    ax2.imshow(cv2.flip(warped, 1))
    ax2.set_title('Homographied', fontsize=30)
    #plt.show()
    plt.savefig(path)
    plt.clf()
    plt.close("all")

    # resize so heights are the same
    hist_grid = cv2.imread(hist_path)
    transformed = cv2.imread(path)
    # cv2.imshow('image', hist_grid)
    # cv2.waitKey(0)
    hist_grid = cv2.resize(hist_grid, (1000, 1000))
    combined = np.concatenate((transformed[:,:-150,:], hist_grid[:,100:,:]), axis=1)
    cv2.imwrite(path, combined)

    return

# We will first manually select the source points
# we will select the destination point which will map the source points in
# original image to destination points in unwarped image
src = np.float32([(127, 132),   # left
                  (300,  69),   # top
                  (300, 245),   # bottom
                  (470,  133)]) # right

dst = np.float32([(300, 100),
                  (100, 100),
                  (300, 300),
                  (100, 300)])

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
    unwarp(im, src, i, (h,w), M)
    #im = im[:,::-1,::-1]
    # path = "rectified/%03d.png" % i
    # cv2.imwrite(path, im)
    i += 1

# clean up all the color histogram plots
subprocess.call([
    'rm', 'rectified/hist_*.png'
])

out_fps = "10"
in_fps = "10"
subprocess.call([
    'ffmpeg', '-y', '-framerate', in_fps, '-i', 'rectified/%03d.png', '-r', out_fps, '-pix_fmt', 'yuv420p',
    'erect_arena_3.mp4'
])
# clean up!
for file_name in glob.glob("rectified/*.png"):
    os.remove(file_name)