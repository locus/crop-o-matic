from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image


# Global variable that holds pictures to be processed.
pics_set = set()

# Global variable that holds a handle to the currently loaded picture.
ptk_img = None
pil_img = None
pil_resized_ratio = 1.0 # How much the PIL image was resized.
pil_img_filename = None

# Global variables that gives information about the geometry of the currently
# loaded picture (the one that is in the canvas at this moment).
left_limit, right_limit, top_limit, bottom_limit = 0, 0, 0, 0

# Corners of the cropping rectangle. Relative to the top-left of the loaded
# picture and NOT to the canvas! So (0,0,0,0) points to the top-left corner
# of the picture.
rx1, ry1, rx2, ry2 = 0, 0, 0, 0


def move_rectangle(event):

    x1, y1, x2, y2 = canvas.coords('r')
    rect_width, rect_height = x2 - x1, y2 - y1
    new_x1, new_y1 = event.x - rect_width / 2, event.y - rect_height / 2
    new_x2, new_y2 = event.x + rect_width / 2, event.y + rect_height / 2

    # Only move the rectangle if it stays on the picture.
    if new_x1 < left_limit:
        new_x1 = left_limit
        new_x2 = left_limit + rect_width
    if new_x2 > right_limit:
        new_x2 = right_limit
        new_x1 = right_limit - rect_width
    if new_y1 < top_limit:
        new_y1 = top_limit
        new_y2 = top_limit + rect_height
    if new_y2 > bottom_limit:
        new_y2 = bottom_limit
        new_y1 = bottom_limit - rect_height

    global rx1, ry1, rx2, ry2
    rx1, ry1 = new_x1 - left_limit, new_y1 - top_limit
    rx2, ry2 = new_x2 - left_limit, new_y2 - top_limit

    canvas.coords('r', new_x1, new_y1, new_x2, new_y2)


def choose_pic_files(*args):

    # Build a list of supported image types to feed to the 'Open Images' dialog.
    supported_filetypes = ['png', 'jpeg', 'jpg', 'bmp', 'gif', 'tiff']
    supported_ext = []
    for t in supported_filetypes:
        ext = '*.' + t
        supported_ext.append(('Image', ext))
        supported_ext.append(('Image', ext.upper()))

    # Ask the user for a selection of image filenames (possible to select many).
    filenames = filedialog.askopenfilenames(
        parent=root,
        title="Choose pictures to import...",
        filetypes=supported_ext)
    filenames = set(filenames) # Ensure structure is a set.

    # If no pictures were selected, do nothing.
    if not filenames or len(filenames) == 0:
        write_log('no files selected')
        return

    # Add filenames to the set.
    global pics_set
    before_len = len(pics_set)
    pics_set.update(filenames)
    write_log('{} new loaded'.format(len(pics_set) - before_len))

    load_pic()


def load_pic():

    canvas.delete(ALL)

    global ptk_img, pil_image
    pil_image = None
    ptk_image = None

    # Do nothing if there are no pictures in the set.
    if len(pics_set) == 0:
        write_log('ERROR no pictures in set')
        return
    filename = pics_set.pop()
    load_specific_pic(filename)


def load_specific_pic(filename):

    # Load the image using Pillow (PIL) and resize so it fits the canvas.
    global pil_img, pil_img_filename
    pil_img_filename = filename
    pil_img = Image.open(filename)
    biggest = max(pil_img.size[0], pil_img.size[1])
    smallest = min(pil_img.size[0], pil_img.size[1])
    if epsilon_close(biggest / smallest, 1.77, 0.005):
        write_log('{} already fixed'.format(filename))
        load_pic() # Load another picture if this one is already at 1.77 ratio.
        return

    put_into_canvas(pil_img, filename)


def put_into_canvas(image, filename=None):

    canvas.delete(ALL)

    global ptk_img, pil_image
    pil_image = image
    ptk_image = None

    canvas_width, canvas_height = canvas.winfo_width(), canvas.winfo_height()
    image_size = fits_best((canvas_width, canvas_height), image.size)
    image_resized = image.resize(image_size, Image.BILINEAR)

    # Keep track of the amount of resizing we did to the picture, beacuse
    # the coords of the cropping rectangle are relative to the resized picture,
    # therefore to correctly crop a picture we need to scale the cropping zone
    # by the inverse of the amount of resizing we did here.
    global pil_resized_ratio
    pil_resized_ratio = image.size[0] / image_resized.size[0]
    if not epsilon_close(pil_resized_ratio, 1.0, 0.0001):
        write_log("resized to {0:.2f}%".format(100 / pil_resized_ratio))

    ptk_img = ImageTk.PhotoImage(image_resized)
    x, y = canvas_width / 2, canvas_height / 2
    canvas.create_image(x, y, image=ptk_img, tags='c')

    global left_limit, right_limit, top_limit, bottom_limit
    left_limit, right_limit = x - image_size[0] / 2, x + image_size[0] / 2
    top_limit, bottom_limit = y - image_size[1] / 2, y + image_size[1] / 2

    # Create a rectangle with a 1.77 aspect ratio that is as big as possible,
    # while still being contained in the picture we just loaded.
    rectangle_width, rectangle_height = biggest_fit(image_size, 1.77)
    canvas.create_rectangle(
        x - rectangle_width / 2, y - rectangle_height / 2,
        x + rectangle_width / 2, y + rectangle_height / 2,
        outline='red', width=4, tags='r')

    # Set the position of the rectangle relative to the picture in the canvas.
    global rx1, ry1, rx2, ry2
    rx1 = x - rectangle_width / 2 - left_limit
    ry1 = y - rectangle_height / 2 - top_limit
    rx2 = x + rectangle_width / 2 - left_limit
    ry2 = y + rectangle_height / 2 - top_limit

    write_log('loaded {}'.format(filename))


def fits_best(canvas_size, image_size):

    canvas_width, canvas_height = canvas_size
    picture_width, picture_height = image_size
    resized_width, resized_height = picture_width, picture_height
 
    if picture_width > canvas_width:
        resized_width = canvas_width
        resized_height *= canvas_width / picture_width
    
    if resized_height > canvas_height:
        resized_width *= canvas_height / resized_height
        resized_height = canvas_height

    resized_width = int(resized_width)
    resized_height = int(resized_height)
    return (resized_width, resized_height)


def biggest_fit(image_size, ratio):

    # Consider two rectangles: one where the ratio is width:height (normal) and
    # another one (r2) where the ratio is height:width. Return the rectangle
    # with the biggest area.
    image_width, image_height = image_size
    r1 = fits_best(image_size, (image_width, image_width * ratio))
    r2 = fits_best(image_size, (image_height * ratio, image_height))

    if r1[0] * r1[1] > r2[0] * r2[1]:
        return r1
    return r2


def epsilon_close(a, b, eps):
    return abs(a - b) <= eps


def crop_current(event=None):

    # Do nothing if there are no pictures in the canvas.
    if not pil_img:
        write_log("ERROR no pictures to crop")
        return

    # Scale up the cropping rectangle, so that it is relative to the real
    # picture and not the resized one.
    srx1, sry1 = rx1 * pil_resized_ratio, ry1 * pil_resized_ratio
    srx2, sry2 = rx2 * pil_resized_ratio, ry2 * pil_resized_ratio

    pil_img_cropped = pil_img.crop((srx1, sry1, srx2, sry2))
    write_log("cropped pic!")

    # Override the uncropped pic with the cropped version.
    pil_img_cropped.save(pil_img_filename)

    # This loads the next picture in the set, or clears the canvas if none.
    load_pic()


def write_log(msg):
    log['state'] = 'normal'
    log.insert('end', msg + '\n')
    log['state'] = 'disabled'


def autorotate_changed(*args):
    pass


root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.title("Crop-O-Matic")

# Make the window full screen
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f'{width}x{height}')

content = ttk.Frame(root, padding=3)
content.grid(column=0, row=0, sticky=(N, S, W, E))
content.columnconfigure(0, weight=1)
content.rowconfigure(1, weight=1)

tools = ttk.Frame(content)
tools.grid(column=0, row=0, columnspan=2, sticky=(N, S, W, E))

root.bind_all('c', crop_current)

ttk.Button(tools, text="Import pics", command=choose_pic_files).grid(
    column=0, row=0, sticky=W)

canvas = Canvas(content)
canvas.grid(column=0, row=1, pady=(3,0), sticky=(N, S, W, E))
canvas.configure(background='white')
canvas.bind('<1>', move_rectangle)
canvas.bind('<B1-Motion>', move_rectangle)

log = Text(content, state='disabled', width=40)
log.grid(column=1, row=1, pady=(3,0), sticky=(N, S))

root.mainloop()
