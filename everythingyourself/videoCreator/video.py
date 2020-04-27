import os

from PIL import Image
import imageio
import moviepy.editor as mpe

def create_video(id, fps, greenscreen=(200, 5)):
    # open coordinates and parse into list of lists
    with open('coordinates.txt') as f:
        lines = f.read().splitlines()

    coordinates = []
    for line in lines:
        frame_coordinates = line.split(',')
        frame_coordinates = list(map(int, frame_coordinates))
        coordinates.append(frame_coordinates)

    # create one image per coordinate
    filename_face = 'face.png'
    face = Image.open(filename_face, 'r').convert('RGBA')

    counter = 0
    for coord in coordinates:
        whole_img = Image.new('RGBA', (1280, 720), (0, 255, 0, 255))
        whole_img.paste(face, coord, face)
        if counter < 10:
            filename = '000{}'.format(counter)
        elif counter < 100:
            filename = '00{}'.format(counter)
        elif counter < 1000:
            filename = '0{}'.format(counter)
        else:
            filename = '{}'.format(counter)
        filepath = 'images/{}/{}.png'.format(id, filename)
        whole_img.save(filepath, format="png")
        counter += 1

        # create video with greenscreen-bg of face-animation
        direc = 'images/{}'.format(id)
        files = os.listdir(direc)
        files.sort()
        images = []

        for file_name in files:
            if file_name.endswith('.png'):
                file_path = os.path.join(direc, file_name)
                images.append(imageio.imread(file_path))
        facevideo = 'greenscreen-{}.mp4'.format(id)
        imageio.mimsave(filename, images, fps=fps)

        # lay greenscreen video over background and export resulting video
        background = mpe.VideoFileClip('bg_clip.mp4')
        clip = mpe.VideoFileClip(facevideo)
        masked_clip = clip.fx(mpe.vfx.mask_color, color=[0, 255, 0], thr=greenscreen[0], s=greenscreen[1])
        final_clip = mpe.CompositeVideoClip([
            background,
            masked_clip
        ]).set_duration(clip.duration)
        exportfile = 'export-{}.mp4'.format(id)
        final_clip.write_videofile(exportfile)