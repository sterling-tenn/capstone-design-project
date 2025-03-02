"use client";

import { Col, Divider, Card, Typography, Flex, FloatButton, notification } from 'antd';
import {
    UpOutlined,
    RightOutlined,
    DownOutlined,
    CloseOutlined,
    LeftOutlined,
} from '@ant-design/icons';
import { moveBackwards, moveForward, turnLeft, turnRight, stop } from '../lib/RaspberryPiCalls';

const { Title, Text } = Typography;

const BOX_SIZE = 100;
const BUTTON_SIZE = 40;

const wrapperStyle: React.CSSProperties = {
    width: '100%',
    height: '250px',
    overflow: 'hidden',
    position: 'relative',
};

const boxStyle: React.CSSProperties = {
    width: BOX_SIZE,
    height: BOX_SIZE,
    position: 'relative',
    margin: "auto",
};

const insetInlineEnd = [
    (BOX_SIZE - BUTTON_SIZE) / 2,
    -(BUTTON_SIZE / 2),
    (BOX_SIZE - BUTTON_SIZE) / 2,
    BOX_SIZE - BUTTON_SIZE / 2,
];

const bottom = [
    BOX_SIZE - BUTTON_SIZE / 2,
    (BOX_SIZE - BUTTON_SIZE) / 2,
    -BUTTON_SIZE / 2,
    (BOX_SIZE - BUTTON_SIZE) / 2,
];

const icons = [
    <UpOutlined key="up" />,
    <RightOutlined key="right" />,
    <DownOutlined key="down" />,
    <LeftOutlined key="left" />,
];

const RemoteControl: React.FC = () => {

    const [api, contextHolder] = notification.useNotification();

    const handleStop = async () => {
        await stop();
    };

    const success = (msg: string) => {
        api.success({
            message: "Success",
            description: msg,
            placement: "topRight",
        });
    };

    const error = (msg: string) => {
        api.error({
            message: "Error",
            description: msg,
            placement: "topRight",
        });
    };


    const handleClick = async (direction: string) => {
        let res = null;

        switch (direction) {
            case "top":
                res = await moveForward();
                break;
            case "right":
                res = await turnRight();
                break;
            case "left":
                res = await turnLeft();
                break;
            case "bottom":
                res = await moveBackwards();
                break;
            default:
                console.error("Invalid direction:", direction);
                return;
        }

        if (res.status === 200) {
            success("CargoBuddy should be moving now!")
        } else {
            error("Could not send command to CargoBuddy, please try again later.")
        }
    };

    return (
        <Col xs={24} md={18} lg={12} style={{ width: "100%"}}>
            {contextHolder}
            <Card style={{ borderRadius: "12px", padding: 12, boxShadow: "0 2px 8px rgba(0,0,0,0.1)", height: "100%" }}>
                <Title level={3}>Remote Control</Title>
                <Divider />
                <Text>Click on the D-pad below to move the robot manually.</Text>
                <Flex justify="center" align="center" style={wrapperStyle}>
                    <div style={boxStyle}>
                        {/* Directional Buttons */}
                        {(["top", "right", "bottom", "left"] as const).map((placement, i) => {
                            const style: React.CSSProperties = {
                                position: "absolute",
                                insetInlineEnd: insetInlineEnd[i],
                                bottom: bottom[i],
                                backgroundColor: "#1890ff",
                            };
                            return (
                                <FloatButton
                                    key={placement}
                                    style={style}
                                    icon={icons[i]}
                                    onClick={() => handleClick(placement)}
                                />
                            );
                        })}
                        {/* STOP Button in the Center */}
                        <FloatButton
                            style={{
                                position: "absolute",
                                top: "50%",
                                left: "50%",
                                transform: "translate(-50%, -50%)",
                                width: 50,
                                height: 50,
                                borderRadius: "50%",
                                backgroundColor: "#ff4d4f",
                                color: "white",
                                fontSize: 24,
                                boxShadow: "0px 0px 10px rgba(0, 0, 0, 0.2)",
                            }}
                            icon={<CloseOutlined />} // STOP icon
                            onClick={handleStop}
                        />
                    </div>
                </Flex>
            </Card>
        </Col>
    );
};

export default RemoteControl;
