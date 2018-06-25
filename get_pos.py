import cv2
import aircv as ac
import os
from cok_tool import click,snap
# print circle_center_pos
def draw_circle(img, pos, circle_radius, color, line_width):
    cv2.circle(img, pos, circle_radius, color, line_width)
    cv2.imshow('objDetect', imsrc) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    mi6='1f33ee18'
    src_pic=snap(mi6,0)
    imsrc = ac.imread(src_pic)
    imobj = ac.imread('base.jpg')

    # find the match position
    
    pos = ac.find_template(imsrc, imobj)
    print pos['result']
    click(pos['result'][0],pos['result'][1],0,mi6)
    click(530,1550,0,mi6)
    #exit(0)
    # circle_center_pos = pos['result']
    # circle_radius = 50
    # color = (0, 255, 0)
    # line_width = 10

    # draw circle
    # draw_circle(imsrc, circle_center_pos, circle_radius, color, line_width)