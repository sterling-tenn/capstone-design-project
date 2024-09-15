import React from 'react';
import { Button, Row, Col, Card, Typography, Layout, Divider } from 'antd';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { UploadOutlined, ArrowRightOutlined, MobileOutlined, HomeOutlined, SafetyOutlined } from '@ant-design/icons';
import './Homepage.css';

const { Title, Paragraph } = Typography;
const { Header, Content, Footer } = Layout;

// Motion Variants for animations
const fadeInUp = {
    hidden: { opacity: 0, y: 50 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
};

const fadeInLeft = {
    hidden: { opacity: 0, x: -50 },
    visible: { opacity: 1, x: 0, transition: { duration: 0.8 } },
};

const fadeInRight = {
    hidden: { opacity: 0, x: 50 },
    visible: { opacity: 1, x: 0, transition: { duration: 0.8 } },
};

const staggerContainer = {
    hidden: { opacity: 1 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.3,
        },
    },
};

const Homepage = () => {
    const navigate = useNavigate();

    return (
        <Layout className="homepage-layout">
            {/* Hero Section */}
            <Header className="header">
                <motion.div
                    className="hero-content"
                    initial="hidden"
                    animate="visible"
                    variants={staggerContainer}
                >
                    <motion.h1 variants={fadeInUp}>
                        Move Freely with <span className="highlight">CargoBuddy</span>
                    </motion.h1>
                    <motion.p variants={fadeInUp}>
                        CargoBuddy is an autonomous robot designed to help you move items around your house.
                    </motion.p>
                    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                        <Button type="primary" size="large" icon={<ArrowRightOutlined />} className='get-started-btn' onClick={() => navigate("/upload")}>
                            Get Started
                        </Button>
                    </motion.div>
                </motion.div>
            </Header>
            <Divider />
            {/* Key Features Section */}
            <Content className="content">
                <Content className="content">
                    <motion.div className="features-section" initial="hidden" whileInView="visible" variants={fadeInUp}>
                        <Title level={2}>Key Features</Title>
                        <Paragraph>Discover what makes CargoBuddy unique and helpful.</Paragraph>

                        <Row gutter={[16, 16]} className="features-row">
                            <Col xs={24} sm={12} lg={6}>
                                <motion.div variants={fadeInLeft}>
                                    <Card className="feature-card" title="Autonomous Navigation" icon={<HomeOutlined style={{ fontSize: "4em" }} />}>
                                        <p><UploadOutlined /> CargoBuddy learns your home’s layout and navigates independently.</p>
                                    </Card>
                                </motion.div>
                            </Col>
                            <Col xs={24} sm={12} lg={6}>
                                <motion.div variants={fadeInUp}>
                                    <Card className="feature-card" title="App Controlled" icon={<MobileOutlined style={{ fontSize: "4em" }} />}>
                                        <p><MobileOutlined /> Control CargoBuddy using our easy-to-use app.</p>
                                    </Card>
                                </motion.div>
                            </Col>
                            <Col xs={24} sm={12} lg={6}>
                                <motion.div variants={fadeInRight}>
                                    <Card className="feature-card" title="Safe & Reliable" icon={<UploadOutlined style={{ fontSize: "4em" }} />}>
                                        <p><SafetyOutlined /> Built-in sensors avoid obstacles and ensure safety while moving.</p>
                                    </Card>
                                </motion.div>
                            </Col>
                        </Row>
                    </motion.div>
                    <Divider />
                    <motion.div className="how-it-works-section" initial="hidden" whileInView="visible" variants={staggerContainer}>
                        <Title level={2}>How It Works</Title>
                        <Paragraph>
                            Easily control CargoBuddy with just a few simple steps. Upload your home floorplan, and we’ll take care of the rest.
                        </Paragraph>

                        <Row className="how-it-works-steps">
                            <Col xs={24} sm={8}>
                                <motion.div className="step" variants={fadeInUp}>
                                    <UploadOutlined style={{ fontSize: '4em' }} />
                                    <p>Step 1: Upload your floorplan</p>
                                </motion.div>
                            </Col>
                            <Col xs={24} sm={8}>
                                <motion.div className="step" variants={fadeInUp}>
                                    <HomeOutlined style={{ fontSize: '4em' }} />
                                    <p>Step 2: We map your home for CargoBuddy</p>
                                </motion.div>
                            </Col>
                            <Col xs={24} sm={8}>
                                <motion.div className="step" variants={fadeInUp}>
                                    <MobileOutlined style={{ fontSize: '4em' }} />
                                    <p>Step 3: Control CargoBuddy with the app</p>
                                </motion.div>
                            </Col>
                        </Row>
                    </motion.div>
                </Content>
                <Divider />
            </Content>

            {/* Footer */}
            <Footer className="footer">
                <motion.div initial="hidden" animate="visible" variants={fadeInUp}>
                    <Paragraph>© 2024 CargoBuddy</Paragraph>
                </motion.div>
            </Footer>
        </Layout>
    );
};

export default Homepage;
