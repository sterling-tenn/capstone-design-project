"use client";
import { Col, Divider, Row, Button, Card, Typography, notification } from "antd";
import { CaretRightOutlined, HeartFilled } from "@ant-design/icons";
import { autoMcl, autoMcl2, sendImage } from "../lib/RaspberryPiCalls";

const { Title } = Typography;

interface Action {
    actionName: string;
    start: { x: number; y: number, adjustedX: number, adjustedY: number };
    dest: { x: number; y: number, adjustedX: number, adjustedY: number };
    runMclCommand: Number;
}

interface FavoriteActionsProps {
    favoriteActions: Action[];
}

interface ActionButtonProps {
    action: Action;
}

// Action Button Component
const ActionButton: React.FC<ActionButtonProps> = ({ action }) => {
    const [api, contextHolder] = notification.useNotification();

    const { actionName, start, dest, runMclCommand } = action;

    const inProgress = (msg: string) => {
        api.info({
            message: "Sending",
            description: msg,
            placement: "topRight",
        });
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

    const handleClick = async () => {
        const savedFloorplan = localStorage.getItem("savedImage");
        if (savedFloorplan) {
        try {
                inProgress("Sending command to CargoBuddy")
                // const res = await sendImage(savedFloorplan, start, dest);
                const res = runMclCommand === 0 ? await autoMcl() : await autoMcl2();
            } catch (err) {
                error("Error sending command to CargoBuddy, please try again later.");
            }
        } else {
            console.log("No saved floorplan!");
            error("No saved floorplan found. Please upload one first.");
        }
    };

    return (
        <Col>
            {contextHolder}
            <Button
                type="primary"
                onClick={handleClick}
                size="large"
                style={{ height: 92 }}
                icon={<CaretRightOutlined style={{ fontSize: 30 }} />}
            >
                <b>{actionName}</b>
            </Button>
        </Col>
    );
};

// Favorite Actions Component
const FavoriteActions: React.FC<FavoriteActionsProps> = ({ favoriteActions }) => {
    return (
        <Col xs={24} md={18} lg={12} style={{ width: "100%" }}>
            <Card style={{ minWidth: 200, borderRadius: "12px", padding: 12, boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
                <Title level={3}> <HeartFilled /> Favorites</Title>
                <Divider />

                {favoriteActions.length > 0 ? (
                    <Row gutter={[8, 8]} wrap justify="start">
                        {favoriteActions.map((action, i) => (
                            <ActionButton key={i} action={action} />
                        ))}
                    </Row>
                ) : (
                    <Title level={5} style={{ textAlign: "center", color: "#888" }}>
                        You do not have any actions saved.
                    </Title>
                )}
            </Card>
        </Col>
    );
};

export default FavoriteActions;
