from PIL import Image, ImageDraw


# Calculate alpha given a 0-100% opacity value.
opacity = lambda transparency: (int(255 * (transparency/100.)),)  # Returns a monuple.


def draw_transp_line(image, xy, color, width=1, joint=None):
    """ Draw line with transparent color on the specified image. """
    if len(color) < 4:  # Missing alpha?
        color += opacity(100)  # Opaque since alpha wasn't specified.

    # Make an overlay image the same size as the specified image, initialized to
    # a fully transparent (0% opaque) version of the line color, then draw a
    # semi-transparent line on it.
    overlay = Image.new('RGBA', image.size, color[:3]+opacity(0))
    draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
    # draw = ImageDraw.Draw(image)
    draw.line(xy, color, width, joint)
    # Alpha composite the overlay image onto the original.
    image.alpha_composite(overlay)
