"use client"
import { useState } from "react";
import { motion } from "framer-motion";
import { MenuOutlined, PlusOutlined, ThunderboltOutlined } from "@ant-design/icons";
import { Button, Card, Layout, Typography } from "antd";
import { Col, Row } from 'antd';
import FavoriteActions from "./components/FavoriteActions";
import MapActions from "./components/MapActions";

const { Header, Content } = Layout;
const { Title, Text } = Typography;

export default function Home() {
  return (
    <Layout style={{ minHeight: "100vh", background: "#f0f2f5", padding: "16px" }}>
      {/* Header */}
      <Header style={{ display: "flex", justifyContent: "right", alignItems: "center", background: "white", borderRadius: "8px", padding: "16px" }}>
        <Button type="primary" size="large" shape="round" icon={<PlusOutlined />}>New job</Button>
      </Header>

      <Content style={{ marginTop: "24px" }}>
        <Row style={{ flexDirection: "column"}} gutter={[12, 12]} wrap={true}>
          <Col xs={24} md={18} lg={12}>
            <Card style={{ textAlign: "center", borderRadius: "12px", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
              <motion.img
                src="/robot.jpg"
                alt="Robot Vacuum"
                style={{ width: "150px", height: "150px", margin: "12px 0px" }}
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              />
              <Title level={2}>Welcome home.</Title>
            </Card>
          </Col>
          <MapActions data={[]} />
          <FavoriteActions />
        </Row>
      </Content>

    </Layout>
  );
}
