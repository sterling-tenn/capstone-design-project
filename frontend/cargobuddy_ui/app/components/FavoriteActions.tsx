"use client";
import { Col, Divider, Row, Button, Card, Typography } from "antd";
import { CaretRightOutlined, HeartFilled } from "@ant-design/icons";

const { Title } = Typography;

interface Action {
    actionName: string;
    info: any;
}

interface FavoriteActionsProps {
    favoriteActions: Action[];
}

interface ActionButtonProps {
    action: Action;
}

// Action Button Component
const ActionButton: React.FC<ActionButtonProps> = ({ action }) => (
    <Col>
        <Button
            type="primary"
            size="large"
            style={{ height: 92 }}
            icon={<CaretRightOutlined style={{ fontSize: 30 }} />}
        >
            <b>{action.actionName}</b>
        </Button>
    </Col>
);

// Favorite Actions Component
const FavoriteActions: React.FC<FavoriteActionsProps> = ({ favoriteActions }) => {
    return (
        <Col xs={24} md={18} lg={12}>
            <Card style={{ borderRadius: "12px", padding: 12, boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
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
