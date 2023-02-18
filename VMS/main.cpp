//#include <arpa/inet.h>
#include <unistd.h>
#include <ctime>
#include <fstream>
#include <iostream>

//#include "opencv2/opencv.hpp"
//#include "opencv2/core.hpp"
//#include "opencv2/videoio.hpp"
//#include "opencv2/imgproc.hpp"

#include "raspicam/raspicam.h"

int main()
{
	raspicam::RaspiCam Camera; //Camera object
	// Open camera 
    std::cout << "Opening Camera..." << std::endl;
	if (!Camera.open())
    {
        std::cerr <<"Error opening camera" << std::endl;
        return -1;
    }
	// Wait a while until camera stabilizes
    std::cout <<"Sleeping for 3 secs" << std::endl;
	sleep(3);

	// Capture
	Camera.grab();

	// Allocate memory
	unsigned char *data = new unsigned char[Camera.getImageTypeSize(raspicam::RASPICAM_FORMAT_RGB)];

	// Extract the image in rgb format
	Camera.retrieve(data, raspicam::RASPICAM_FORMAT_RGB); // Get camera image

	// Save
	std::ofstream outFile("raspicam_image.ppm",std::ios::binary);
	outFile<< "P6\n" << Camera.getWidth() << " " << Camera.getHeight() << " 255\n";
	outFile.write ( ( char* ) data, Camera.getImageTypeSize ( raspicam::RASPICAM_FORMAT_RGB ) );
    std::cout << "Image saved at raspicam_image.ppm" << std::endl;

    // Free resources and exit
	delete[] data;
    return 0;
}
