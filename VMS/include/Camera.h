#include <functional>
#include <memory>
#include <string>
#include <mutex>

#include <opencv2/core.hpp>
#include <opencv2/core/mat.hpp>
#include <opencv2/core/utility.hpp>

#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>

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
