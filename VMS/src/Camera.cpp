#include "Camera.h"


namespace VMS {

    Camera::Camera()
    {
        // m_Capture = std::make_shared<cv::VideoCapture>(0);
        m_Capture = cv::VideoCapture(0);
        //if (!m_Capture.isOpened())
        //{
        //    LOG("[ERROR] Couldn't create camera");
        //}
        // std::string imagePath = "../../img/template.png";
        // cv::Mat m_Template = cv::imread(imagePath);
    }

    


}

