import cv2
import aircv as ac
import os
from cok_tool import click,snap,back
# print circle_center_pos
def draw_circle(img, pos, circle_radius, color, line_width):
    cv2.circle(img, pos, circle_radius, color, line_width)
    cv2.imshow('objDetect', imsrc) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def hero(pic='',devices=''):
    if pic == '':
        src_pic=snap(device,0)
    else :
        src_pic=pic
    imsrc = ac.imread(src_pic)
    imobj = ac.imread('base.jpg')

    # find the match position
    
    pos = ac.find_template(imsrc, imobj)
    print pos['result']
    click(pos['result'][0],pos['result'][1],0,devices)
    click(530,1550,0,devices) #start fight
    click(865,1810,8,devices)  #fighting
    back(devices)
    #os.system("del %s"%src_pic)
def getbox(pic='',device=''):
    if pic == '':
        src_pic=snap(device,0)
    else :
        src_pic=pic
    imsrc = ac.imread(src_pic)
    imobj = ac.imread('box.jpg')

    # find the match position
    
    pos = ac.find_template(imsrc, imobj)
    print pos['result']
    click(pos['result'][0],pos['result'][1],2,device)
    click(530,1515,2,device)
if __name__ == "__main__":
    mi6='1f33ee18'

    #getbox("127.0.0.1:62028")
    pic=snap("127.0.0.1:62028",0)
    hero(pic,"127.0.0.1:62028")
    getbox(pic,"127.0.0.1:62028")

    exit(0)
    for i in xrange(3):
        hero("127.0.0.1:62028")
    #exit(0)
    # circle_center_pos = pos['result']
    # circle_radius = 50
    # color = (0, 255, 0)
    # line_width = 10

    # draw circle
    # draw_circle(imsrc, circle_center_pos, circle_radius, color, line_width)