"use client";

import React, { useEffect, useState } from "react";
import { Col, Divider, Row, Button, Card, Typography, Modal, Steps, Result, Form, Upload, Spin } from 'antd';
import { CheckCircleTwoTone, ExclamationCircleTwoTone, InboxOutlined } from "@ant-design/icons";

const { Title } = Typography;

const steps = [
    {
        title: 'Add a map',
        content: 'First-content',
    },
    {
        title: 'Sending your map to CargoBuddy',
        content: 'Second-content',
    },
    {
        title: 'Complete!',
        content: 'Third-content',
    }
];

const MapActions: React.FC<{ data: any[] }> = ({ data }) => {
    const [modalOpen, setModalOpen] = useState<boolean>(false);
    const [current, setCurrent] = useState<number>(0);
    const [fileList, setFileList] = useState<any[]>([]);
    const [form] = Form.useForm();

    useEffect(() => {
        if (current === 1) {
            let file = fileList.length > 0 ? fileList[0] : null;

            // Make API call to send it to the robot
            console.log("file: ", file);


        }
    }, [current]);

    const handleFileChange = ({ fileList }: any) => {
        setFileList(fileList);
        form.setFieldsValue({ fileUpload: fileList }); // Keep form value in sync
    };

    const next = () => {
        setCurrent((cur) => cur + 1);
    };

    const prev = () => {
        setCurrent((cur) => cur - 1);
    };

    const toggleOpenModal = () => {
        if (!modalOpen) {
            setCurrent(0); // Reset to first step
            setFileList([]); // Clear file list when reopening
            form.resetFields();
        }
        setModalOpen((prev) => !prev);
    };

    const statusIcon = data.length === 0 ? <ExclamationCircleTwoTone /> : <CheckCircleTwoTone />;
    const items = steps.map((item) => ({ key: item.title, title: item.title }));

    return (
        <Col xs={24} md={18} lg={12}>
            <Card style={{ borderRadius: "12px", padding: 12, boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
                <Title level={3}> {statusIcon} Map </Title>
                <Divider />
                <Row gutter={[8, 8]} wrap={true}>
                    {data.length === 0 && (
                        <>
                            <Title level={5}>
                                There is no map loaded! To ensure that you can use the robot, please load your home's floorplan.
                            </Title>
                            <Col xs={24}>
                                <Button onClick={toggleOpenModal} type="primary" size="large" shape="round">
                                    Add a Map
                                </Button>
                            </Col>
                        </>
                    )}
                </Row>
            </Card>

            <Modal
                title="Submit a Map"
                open={modalOpen}
                onCancel={toggleOpenModal}
                footer={null}
            >
                <Steps current={current} items={items} />

                {/* Step 1: File Upload */}
                {current === 0 && (
                    <Form form={form}>
                        <Form.Item name="fileUpload" noStyle>
                            <Upload.Dragger
                                maxCount={1}
                                listType="picture"
                                fileList={fileList}
                                onChange={handleFileChange}
                                beforeUpload={() => false} // Prevent automatic upload
                            >
                                <p className="ant-upload-drag-icon">
                                    <InboxOutlined />
                                </p>
                                <p className="ant-upload-text">Click or drag a file to upload</p>
                                <p className="ant-upload-text">Only one image is allowed</p>
                            </Upload.Dragger>
                        </Form.Item>
                    </Form>
                )}

                {/* Step 2: Send Floorplan to robot */}
                {current === 1 && (
                    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: "12px" }}>
                        <Spin size="large" />
                        <Title level={5} style={{ textAlign: "center" }}>
                            Sending your floorplan to the robot! Please wait.
                        </Title>
                    </div>
                )}

                {/* Step 3: All done! */}
                {current === 2 && (
                    <Result
                        status="success"
                        title="You're all set!"
                    />
                )}


                {/* Navigation Buttons */}
                <div style={{ marginTop: 24 }}>
                    {current < steps.length - 1 && (
                        <Button type="primary" onClick={next} disabled={fileList.length === 0}>
                            Next
                        </Button>
                    )}
                    {current === steps.length - 1 && (
                        <Button type="primary" onClick={toggleOpenModal}>
                            Done
                        </Button>
                    )}
                    {current > 0 && (
                        <Button style={{ margin: '0 8px' }} onClick={prev}>
                            Previous
                        </Button>
                    )}
                </div>
            </Modal>
        </Col>
    );
};

export default MapActions;
