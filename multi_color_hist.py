import matplotlib.pyplot as plt
import numpy as np
import cv2

def add_hist_grid(im, path):
    '''
        im - opencv2 image format
    '''
    # Notice the equal aspect ratio
    p_h, p_w = 8, 8 
    fig = plt.figure(figsize=(16, 16)) 

    ax = []
    init = False
    for i in range(p_h * p_w):
        if init == False:
            init = True
            ax.append(fig.add_subplot(p_h, p_w, i+1))
            ax[0].set_ylim([0, 1e3])
            #ax[0].set_xlim([0, 104])
        else:
            ax.append(fig.add_subplot(p_h, p_w, i+1, sharey=ax[0], sharex=ax[0]))

    #im = cv2.imread(path)
    h, w = im.shape[:2]
    # im[:,:,0] = 80
    # im[:,:,1] = 160
    # im[:,:,2] = 240
    print(h,w)
    grid_w_inc = w / 8
    grid_h_inc = h / 8

    # cv2 is BGR channel format
    ch_colors = ["blue", "green", "red"]
    for i, a in enumerate(ax):
        a.set_xticklabels([])
        a.set_yticklabels([])
        # must be 8 bit array mask. Non-zero elements in the mask become input
        mask = np.zeros((h, w), np.uint8)
        grid_x = i % p_w
        grid_y = i // p_h
        x1 = int(grid_x * grid_w_inc)
        x2 = int(x1 + grid_w_inc)
        y1 = int(grid_y * grid_h_inc)
        y2 = int(y1 + grid_h_inc)
        # cv2 is [H,W] format
        mask[y1:y2, x1:x2] = 1 
        mask = mask[:, ::-1]
        for j in [0, 1, 2]:
            ch_hist = cv2.calcHist([im], [j], mask, [128], [0, 256])
            a.plot(ch_hist, color=ch_colors[j])

    # make grid
    for j in range(-1, 9):
        cv2.line(im, (int(j*grid_h_inc), 0), (int(j*grid_h_inc), w), (255, 0, 0), thickness=1)
        cv2.line(im, (0, int(j*grid_w_inc)), (h, int(j*grid_w_inc)), (255, 0, 0), thickness=1)

    fig.subplots_adjust(wspace=0, hspace=0)
    plt.savefig(path)

    plt.clf()
    plt.close("all")
    return im

if __name__ == "__main__":
    im = cv2.imread("test.png", "hist_test.png")
    add_hist_grid(im)