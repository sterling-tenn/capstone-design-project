"use client"
import { Col, Divider, Row, Space } from 'antd';
import { Button, Card, Typography } from "antd";
import { CaretRightOutlined, HeartFilled } from "@ant-design/icons";

const { Title } = Typography;

const ActionButton: React.FC = ({ name, link }) => {
    return (
        <Col>
            <Button type="primary" size="large" style={{ height: 92 }}
                icon={<CaretRightOutlined style={{ fontSize: 30 }} />}>
                <b>{name}</b>
            </Button>
        </Col>
    )
}

const FavoriteActions: React.FC = ({ favoriteActions }) => {
    return (
        <Col xs={24} md={18} lg={12}>
            <Card style={{ borderRadius: "12px", padding: 12, boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
                <Title level={3}> <HeartFilled /> Favorites</Title>
                <Divider />
                <Row gutter={[8, 8]} wrap={true}>
                    <ActionButton name={"Kitchen"} link="" />
                    <ActionButton name={"Kitchen"} link="" />
                    <ActionButton name={"Kitchen"} link="" />
                </Row>
            </Card>
        </Col>
    )
}

export default FavoriteActions;
