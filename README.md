# project-1

REQUIREMENTS:

	-Python 3.5
	-TensorFlow(https://www.tensorflow.org/versions/master/get_started/os_setup#download-and-setup)
	-NumPy(http://www.lfd.uci.edu/~gohlke/pythonlibs/)
	-SciPy(http://www.lfd.uci.edu/~gohlke/pythonlibs/)
	-Pillow(http://www.lfd.uci.edu/~gohlke/pythonlibs/)
	FIND AND DOWNLOAD THESE THREE PACKAGES FROM THE WEBSITE ABOVE AND USE (PIP INSTALL PATHTOPACKAGE.whl) TO INSTALL THESE PACKAGES
	-Pre-trained VGG network 
		(imagenet-vgg-verydeep-19.mat)
		url:http://www.vlfeat.org/matconvnet/models/beta16/imagenet-vgg-verydeep-19.mat


RUNNING:

	python neural_style.py --content <content file> --styles <style file> --output <output file>
	Run python neural_style.py --help to see a list of all options.
	Use --checkpoint-output and --checkpoint-iterations to save checkpoint images.

Examples:

input image:
	
![alt text](https://github.com/lihengbin333/project-1/blob/master/2-content.jpg?raw=true)

Citation

If you use this implementation in your work, please cite the following:

	@misc{athalye2015neuralstyle,
  	author = {Anish Athalye},
	 title = {Neural Style},
 	 year = {2015},
  	howpublished = {\url{https://github.com/anishathalye/neural-style}},
  	note = {commit xxxxxxx}
	}
