# Color Image Enhancement Using the Support Fuzzification in the Framework of the Logarithmic Model 

This is an implementation of [Color Image Enhancement Using the Support Fuzzification in the Framework of the Logarithmic Model](https://www.researchgate.net/publication/237202014_Color_Image_Enhancement_Using_the_Support_Fuzzification_in_the_Framework_of_the_Logarithmic_Model)


### Prerequisites
- cv2
- numpy
- scipy


### Running code
main.py contains all what you need

assign the global variable n,m and gamma as you wish

assign the img_name variable with the image file name(without extension) you want to enahance (by default it should bee a PNG file but you can change the code in the functions: colored_enhancing() , gray_enhancing())

finally, calling the function:

colored_enhancing() for enhancing colored images (obviously)

gray_enhancing() for enhancing gray images


### Note
all image files must be located at .\project_folder\test_images


### Results
Test 1


![](https://github.com/ivan-abboud/Image_enhancement_with_fuzzy_logic/blob/master/Results/cells.PNG) 
![n=2 ,m=2 ,gamma=2](https://github.com/ivan-abboud/Image_enhancement_with_fuzzy_logic/blob/master/Results/cells2x2x2.png)
![n=2 ,m=2 ,gamma=2](https://github.com/ivan-abboud/Image_enhancement_with_fuzzy_logic/blob/master/Results/cells2x2x4.png)


Test 2


![](https://github.com/ivan-abboud/Image_enhancement_with_fuzzy_logic/blob/master/Results/miss.PNG) 
![](https://github.com/ivan-abboud/Image_enhancement_with_fuzzy_logic/blob/master/Results/miss1x1x1.png) 
![n=2 ,m=2 ,gamma=2](https://github.com/ivan-abboud/Image_enhancement_with_fuzzy_logic/blob/master/Results/miss2x2x2.png)
![n=2 ,m=2 ,gamma=2](https://github.com/ivan-abboud/Image_enhancement_with_fuzzy_logic/blob/master/Results/miss2x2x4.png)


Test 3


![](https://github.com/ivan-abboud/Image_enhancement_with_fuzzy_logic/blob/master/Results/road.PNG) 
![n=2 ,m=2 ,gamma=2](https://github.com/ivan-abboud/Image_enhancement_with_fuzzy_logic/blob/master/Results/road2x2x2.png)


further tests can be seen in Results folder


## Acknowledgments

Damascus University
Department of Artifcial Intelligence

5th year students
hope this could help you
feel free to report any problem
