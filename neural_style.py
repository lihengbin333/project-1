# Copyright (c) 2015-2016 Anish Athalye. Released under GPLv3.
#####################################
#@misc{athalye2015neuralstyle,
#  author = {Anish Athalye},
#  title = {Neural Style},
#  year = {2015},
#  howpublished = {\url{https://github.com/anishathalye/neural-style}},
#}
#####################################
#############import modules##########

import os                                           

import numpy as np
import scipy.misc

from stylize import stylize

import math
from argparse import ArgumentParser

#####################################

# default arguments
CONTENT_WEIGHT = 5e0
STYLE_WEIGHT = 1e2
TV_WEIGHT = 1e2
LEARNING_RATE = 1e1
STYLE_SCALE = 1.0
ITERATIONS = 1000
VGG_PATH = 'imagenet-vgg-verydeep-19.mat'

#this creates parser that uses to recognize command line input#################################

def build_parser():
    parser = ArgumentParser()

    #recognize input image and store to "content"
    parser.add_argument('--content',
            dest='content', help='content image',
            metavar='CONTENT', required=True)

    #recognize style images and store to "styles"
    parser.add_argument('--styles',
            dest='styles',
            nargs='+', help='one or more style images',
            metavar='STYLE', required=True)

    #recognize output image and store to "output"
    parser.add_argument('--output',
            dest='output', help='output path',
            metavar='OUTPUT', required=True)

    #recognize iterations and able to change it, default iterations is initialized above(1000)
    parser.add_argument('--iterations', type=int,
            dest='iterations', help='iterations (default %(default)s)',
            metavar='ITERATIONS', default=ITERATIONS)

    #set iterations printing frequency
    parser.add_argument('--print-iterations', type=int,
            dest='print_iterations', help='statistics printing frequency',
            metavar='PRINT_ITERATIONS')

    #set checkpoint output file format
    parser.add_argument('--checkpoint-output',
            dest='checkpoint_output', help='checkpoint output format, e.g. output%%s.jpg',
            metavar='OUTPUT')

    #set checkpoint frequency
    parser.add_argument('--checkpoint-iterations', type=int,
            dest='checkpoint_iterations', help='checkpoint frequency',
            metavar='CHECKPOINT_ITERATIONS')

    #set image width
    parser.add_argument('--width', type=int,
            dest='width', help='output width',
            metavar='WIDTH')

    #set style images' scales
    parser.add_argument('--style-scales', type=float,
            dest='style_scales',
            nargs='+', help='one or more style scales',
            metavar='STYLE_SCALE')

    #set path to network
    parser.add_argument('--network',
            dest='network', help='path to network parameters (default %(default)s)',
            metavar='VGG_PATH', default=VGG_PATH)

    #set content weight-how much to weight the content recoonstruction term
    parser.add_argument('--content-weight', type=float,
            dest='content_weight', help='content weight (default %(default)s)',
            metavar='CONTENT_WEIGHT', default=CONTENT_WEIGHT)

    #set style weight-how much to weight the style reconstruction term
    parser.add_argument('--style-weight', type=float,
            dest='style_weight', help='style weight (default %(default)s)',
            metavar='STYLE_WEIGHT', default=STYLE_WEIGHT)

    #set the weight for blending the style of style images
    parser.add_argument('--style-blend-weights', type=float,
            dest='style_blend_weights', help='style blending weights',
            nargs='+', metavar='STYLE_BLEND_WEIGHT')

    #set weight of total-variation regularization
    parser.add_argument('--tv-weight', type=float,
            dest='tv_weight', help='total variation regularization weight (default %(default)s)',
            metavar='TV_WEIGHT', default=TV_WEIGHT)

    #set learning rate
    parser.add_argument('--learning-rate', type=float,
            dest='learning_rate', help='learning rate (default %(default)s)',
            metavar='LEARNING_RATE', default=LEARNING_RATE)

    #set initial image path
    parser.add_argument('--initial',
            dest='initial', help='initial image',
            metavar='INITIAL')
    return parser

###################################################################################################

def main():
    #call build_parser method
    parser = build_parser()                
    options = parser.parse_args()
    
    #check "imagenet-vgg-verydeep-19.mat" exists or not
    if not os.path.isfile(options.network):
        parser.error("Network %s does not exist. (Did you forget to download it?)" % options.network)

    #call imread method to store input images to content_image
    content_image = imread(options.content)

    #call inread method to store multiple style images to style_images
    style_images = [imread(style) for style in options.styles]

    #set image's width to user's input if it's not null
    width = options.width
    if width is not None:
        #form new images' shape by new width--new shape = (((row/column)*width),width)
        new_shape = (int(math.floor(float(content_image.shape[0]) /
                content_image.shape[1] * width)), width)
        #resize input images by new shape
        content_image = scipy.misc.imresize(content_image, new_shape)
    target_shape = content_image.shape

    #for each style images, resize these style images with style scale that user enter or default.
    for i in range(len(style_images)):
        style_scale = STYLE_SCALE
        if options.style_scales is not None:
            style_scale = options.style_scales[i]
        style_images[i] = scipy.misc.imresize(style_images[i], style_scale *
                target_shape[1] / style_images[i].shape[1])

    #set style blend weights. If it's null then it equals to (1/number of style image)
    #else it equals to (each style_blend_weights/sum of style_blend_weights)
    style_blend_weights = options.style_blend_weights
    if style_blend_weights is None:
        # default is equal weights
        style_blend_weights = [1.0/len(style_images) for _ in style_images]
    else:
        total_blend_weight = sum(style_blend_weights)
        style_blend_weights = [weight/total_blend_weight
                               for weight in style_blend_weights]

    #initize the image 
    initial = options.initial
    if initial is not None:
        initial = scipy.misc.imresize(imread(initial), content_image.shape[:2])

    if options.checkpoint_output and "%s" not in options.checkpoint_output:
        parser.error("To save intermediate images, the checkpoint output "
                     "parameter must contain `%s` (e.g. `foo%s.jpg`)")
    #call stylize function which yields tuples(iteration, image) and the for loop will access these elements
    for iteration, image in stylize(
        network=options.network,
        initial=initial,
        content=content_image,
        styles=style_images,
        iterations=options.iterations,
        content_weight=options.content_weight,
        style_weight=options.style_weight,
        style_blend_weights=style_blend_weights,
        tv_weight=options.tv_weight,
        learning_rate=options.learning_rate,
        print_iterations=options.print_iterations,
        checkpoint_iterations=options.checkpoint_iterations
    ):

        #set output file path 
        output_file = None
        if iteration is not None:
            if options.checkpoint_output:
                output_file = options.checkpoint_output % iteration
        else:
            output_file = options.output
        if output_file:
            imsave(output_file, image)

#function for reading image through path as an array
def imread(path):
    img = scipy.misc.imread(path).astype(np.float)
    if len(img.shape) == 2:
        # grayscale
        img = np.dstack((img,img,img))
    return img

#function for saving output image to target path
def imsave(path, img):
    img = np.clip(img, 0, 255).astype(np.uint8)
    scipy.misc.imsave(path, img)


if __name__ == '__main__':
    main()
