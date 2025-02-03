"use client"

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Card, Layout, Typography } from "antd";
import { Col, Row } from 'antd';
import FavoriteActions from "./components/FavoriteActions";
import MapActions from "./components/MapActions";
import RemoteControl from "./components/RemoteControl";
import NewJobAction from "./components/NewJobAction";

const { Header, Content } = Layout;
const { Title } = Typography;

export default function Home() {
  // TODO: make parent cards 100% width of the col they're part of
  const [actions, setActions] = useState<any[]>([])

  useEffect(() => {
    const existingActions = JSON.parse(localStorage.getItem("actions") || "[]");
    setActions(existingActions)
  }, []);

  const handleSetAction = (actionName: string, info: any) => {
    console.log("action name", actionName);
    const existingActions = JSON.parse(localStorage.getItem("actions") || "[]");
    const updatedActions = Array.isArray(existingActions) ? [...existingActions, { actionName, info }] : [{ actionName, info }];
    localStorage.setItem("actions", JSON.stringify(updatedActions));
    setActions(updatedActions);
  };


  return (
    <Layout style={{ minHeight: "100vh", background: "#f0f2f5", padding: "16px" }}>
      {/* Header */}
      <Header style={{ display: "flex", justifyContent: "right", alignItems: "center", background: "white", borderRadius: "8px", padding: "16px" }}>
        <NewJobAction handleSetAction={handleSetAction} />
      </Header>

      <Content style={{ marginTop: "24px" }}>
        <Row style={{ flexDirection: "column" }} align="middle" gutter={[12, 12]} wrap={true}>
          <Col xs={24} md={18} lg={12}>
            <Card style={{ textAlign: "center", borderRadius: "12px", boxShadow: "0 2px 8px rgba(0,0,0,0.1)", minWidth: "100%" }}>
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
          <MapActions />
          <FavoriteActions favoriteActions={actions} />
          <RemoteControl />
        </Row>
      </Content>
    </Layout>
  );
}
