"use client"
import { Col, Divider, Card, Typography, Flex, FloatButton } from 'antd';
import {
    UpOutlined,
    RightOutlined,
    DownOutlined,
    LeftOutlined,
} from '@ant-design/icons';

const { Title, Text } = Typography;

const BOX_SIZE = 100;
const BUTTON_SIZE = 40;

const wrapperStyle: React.CSSProperties = {
    width: '100%',
    height: '200px',
    overflow: 'hidden',
    position: 'relative',
};

const boxStyle: React.CSSProperties = {
    width: BOX_SIZE,
    height: BOX_SIZE,
    position: 'relative',
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
    const handleClick = (direction: string) => {
        // Make call to robot to move
        console.log(`Button clicked: ${direction}`);
    };

    return (
        <Col xs={24} md={18} lg={12} style={{ height: 300 }}>
            <Card style={{ borderRadius: "12px", padding: 12, boxShadow: "0 2px 8px rgba(0,0,0,0.1)", height: "100%" }}>
                <Title level={3}> Remote Control</Title>
                <Divider />
                <Text>Click on the D-pad below to move the robot manually.</Text>
                <Flex justify="center" align="center" style={wrapperStyle}>
                    <div style={boxStyle}>
                        {(['top', 'right', 'bottom', 'left'] as const).map((placement, i) => {
                            const style: React.CSSProperties = {
                                position: 'absolute',
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
                    </div>
                </Flex>
            </Card>
        </Col>
    );
};

export default RemoteControl;
