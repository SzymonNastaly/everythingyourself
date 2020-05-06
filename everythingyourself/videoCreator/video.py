import os

from PIL import Image
import imageio
import moviepy.editor as mpe

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def render_video(id, fps, greenscreen=(200, 5)):
    # open coordinates and parse into list of lists
    coordinates_path = os.path.join(BASE_DIR, 'videoCreator/coordinates.txt')
    with open(coordinates_path) as f:
        lines = f.read().splitlines()

    coordinates = []
    for line in lines:
        frame_coordinates = line.split(',')
        frame_coordinates = list(map(int, frame_coordinates))
        coordinates.append(frame_coordinates)

    # create one image per coordinate
    tmp_face_path = 'media/faces/cropped-img_{}.png'.format(id)
    face_path = os.path.join(BASE_DIR, tmp_face_path)
    face = Image.open(face_path, 'r').convert('RGBA')

    counter = 0
    for coord in coordinates:
        print("start of loop")
        whole_img = Image.new('RGBA', (1280, 720), (0, 255, 0, 255))
        whole_img.paste(face, coord, face)
        if counter < 10:
            filename = '000{}.png'.format(counter)
        elif counter < 100:
            filename = '00{}.png'.format(counter)
        elif counter < 1000:
            filename = '0{}.png'.format(counter)
        else:
            filename = '{}.png'.format(counter)
        # filepath = 'images/{}/{}.png'.format(id, filename)
        part_path = 'media/created_images/{}'.format(filename)
        filepath = os.path.join(BASE_DIR, part_path)
        whole_img.save(filepath, format="png")
        counter += 1


    # create video with greenscreen-bg of face-animation
    # direc = 'images/{}'.format(id)
    direc = os.path.join(BASE_DIR, 'media/created_images')
    files = os.listdir(direc)
    files.sort()
    images = []


    for file_name in files:
        if file_name.endswith('.png'):
            file_path = os.path.join(direc, file_name)
            images.append(imageio.imread(file_path))
    facevideo = 'media/created_videos/greenscreen-{}.mp4'.format(id)
    imageio.mimsave(facevideo, images, fps=fps)

    # lay greenscreen video over background and export resulting video
    background_path = os.path.join(BASE_DIR, 'media/background/bg_clip.mp4')
    background = mpe.VideoFileClip(background_path)
    clip = mpe.VideoFileClip(facevideo)
    masked_clip = clip.fx(mpe.vfx.mask_color, color=[0, 255, 0], thr=greenscreen[0], s=greenscreen[1])
    final_clip = mpe.CompositeVideoClip([
        background,
        masked_clip
    ]).set_duration(clip.duration)
    exportfile = 'media/created_videos/export-{}.mp4'.format(id)
    final_clip.write_videofile(exportfile)

    return exportfile