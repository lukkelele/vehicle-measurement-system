#include <stdio.h>
#include <functional>
#include <memory>
#include <string>


#include <opencv2/core/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/videoio.hpp>

#include "Log.h"

namespace VMS {


    class Camera
    {
    public:
        Camera();
        ~Camera() = default;

    private:
        // std::shared_ptr<cv::VideoCapture> m_Capture;
        cv::VideoCapture m_Capture;
    };

}
