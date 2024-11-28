/**
 * @file joy_to_platform_vel_controller.cpp
 * @author Azmyin Md. Kamal
 * @brief TwistMux is configured to recevie Twist messages which may not work with DiffDrive/Ackermann controllers in Gazebo Harmonic.
 * TwistStamped messages are required by these controllers. This node acts as a converter between the two twist message forms.
 * @version 1.0
 * @date 2024-11-28
 * 
 * @copyright Copyright (c) 2024
 * 
 */

// Includes

// C++ includes
#include <map>
#include <memory>
#include <set>
#include <string>
// ROS2 includes
#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <geometry_msgs/msg/twist_stamped.hpp>
#include <rclcpp/rclcpp.hpp>
#include <rclcpp_components/register_node_macro.hpp>
#include <sensor_msgs/msg/joy.hpp>

class TwistMuxToPlatfromController : public rclcpp::Node
{
public:
    /**
     * @brief This object takes in a Twist message from joy_teleop/cmd_vel like systems, converts it to TwistStamped message and publishes it.
     * The output should go to a desired velocity controller
     * @param options 
     */
    TwistMuxToPlatfromController(const rclcpp::NodeOptions &options)
        : Node("twist_to_twist_stamped_node", options)
    {
        // Declare and get parameters
        this->declare_parameter<std::string>("input_joy_topic", "not_given");
        this->declare_parameter<std::string>("controller_cmd_vel", "not_given");

        // Recover topic names
        rclcpp::Parameter param1 = this->get_parameter("input_joy_topic");
        input_twistmux_topic_ = param1.as_string();
        rclcpp::Parameter param2 = this->get_parameter("controller_cmd_vel");
        output_controller_topic_ = param2.as_string();

        
        // Subscriber: Listen for output from Twist mux server
        subscriber_ = this->create_subscription<geometry_msgs::msg::TwistStamped>(output_controller_topic_, rclcpp::QoS(10), 
                                        std::bind(&TwistMuxToPlatfromController::sub_callback, this, std::placeholders::_1));
        
        // Publisher: Send TwistStamped message to controller i.e. DiffDrive/Ackermann
        publisher_ = this->create_publisher<geometry_msgs::msg::TwistStamped>(output_topic_, 10);

        // Debug messages
        RCLCPP_INFO(this->get_logger(), "TwistMuxToPlatfromController Listening on topic: %s", input_topic_.c_str());
        RCLCPP_INFO(this->get_logger(), "TwistMuxToPlatfromController Publishing on topic: %s", output_topic_.c_str());
        
    }

    void TwistMuxToPlatfromController::sub_callback(const geometry_msgs::msg::TwistStamped::SharedPtr& twist_msg)
    {
        std::cout <<"FOO"<<std::endl;
    }

private:
    std::string input_twistmux_topic_;
    std::string output_controller_topic_;
    rclcpp::Publisher<geometry_msgs::msg::TwistStamped>::SharedPtr publisher_;
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr subscriber_;
};

// Main function
int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);

    // Spin the node
    rclcpp::spin(std::make_shared<TwistMuxToPlatfromController>(rclcpp::NodeOptions()));

    rclcpp::shutdown();
    return 0;
}