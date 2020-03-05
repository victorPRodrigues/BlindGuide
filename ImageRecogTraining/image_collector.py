import cv2


def store_frame(timestamp, destiny, counter):
    video.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
    caught, image = video.read()
    if caught:
        cv2.imwrite(f'{destiny}/image{counter}.jpg', image)

    return caught


if __name__ == '__main__':
    videos_src = ['up', 'down', 'hole']
    img_destiny = ['up_frames', 'down_frames', 'h_frames']
    prev_destiny = ''
    image_counter = 1

    for src, destiny in zip(videos_src, img_destiny):
        video = cv2.VideoCapture(src)
        timestamp = 0
        rate = 1

        if destiny != prev_destiny:
            image_counter = 1

        prev_destiny = destiny
        caught = store_frame(timestamp, destiny, image_counter)
        while caught:
            image_counter += 1
            timestamp = round(timestamp + rate, 2)
            caught = store_frame(timestamp, destiny, image_counter)

    print('Done!')
