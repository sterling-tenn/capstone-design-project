"use client";

import React, { useEffect, useState } from "react";
import { Col, Divider, Row, Button, Card, Typography, Modal, Steps, Result, Form, Upload, Spin, Image } from 'antd';
import { CheckCircleTwoTone, ExclamationCircleTwoTone, InboxOutlined } from "@ant-design/icons";

const { Title } = Typography;

const steps = [
    { title: 'Add a map', content: 'First-content' },
    { title: 'Sending your map to CargoBuddy', content: 'Second-content' },
    { title: 'Result', content: 'Third-content' }
];

const MapActions: React.FC = () => {
    const [modalOpen, setModalOpen] = useState<boolean>(false);
    const [current, setCurrent] = useState<number>(0);
    const [fileList, setFileList] = useState<any[]>([]);
    const [uploading, setUploading] = useState<boolean>(false);
    const [uploadingFailure, setUploadingFailure] = useState<boolean>(false)
    const [savedImage, setSavedImage] = useState<string | null>(null);
    const [form] = Form.useForm();

    // Load saved image from localStorage when the component mounts
    useEffect(() => {
        const storedImage = localStorage.getItem("savedImage");
        if (storedImage) {
            setSavedImage(storedImage);
        }
    }, []);

    useEffect(() => {
        if (current === 1) {
            setUploading(true);
            console.log("File being processed: ", fileList);

            sendAndSaveFloorplan()
                .then(() => {
                    setUploadingFailure(false);
                    setCurrent(2);
                })
                .catch(() => {
                    setUploadingFailure(true);
                    setCurrent(2);
                })
                .finally(() => {
                    setUploading(false);
                });
        }
    }, [current]);

    const sendAndSaveFloorplan = async () => {
        const file = fileList[0]?.originFileObj;
        if (!file) return;
        const reader = new FileReader();
        reader.readAsDataURL(file);

        return new Promise<void>((resolve, reject) => {
            reader.onload = async () => {
                try {
                    const base64String = reader.result as string;
                    localStorage.setItem("savedImage", base64String);
                    setSavedImage(base64String);
                    console.log("✅ Image saved to localStorage!");

                    resolve();
                } catch (error) {
                    console.error("❌ Error sending image:", error);
                    setUploadingFailure(true);
                    reject();
                }
            };
        });
    };


    const handleFileChange = ({ fileList }: any) => {
        setFileList(fileList);
    };

    const next = () => setCurrent((cur) => cur + 1);

    const prev = () => {
        if (current === 2) {
            setCurrent(0);
        } else {
            setCurrent((cur) => cur - 1);
        }
    };

    const toggleOpenModal = () => {
        if (!modalOpen) {
            setCurrent(0);
            setFileList([]);
            setUploading(false);
            setUploadingFailure(false);
            form.resetFields();
        }
        setModalOpen((prev) => !prev);
    };

    const isNextDisabled = current === 0 ? fileList.length === 0 : uploading;

    return (
        <Col xs={24} md={18} lg={12} style={{ width: "100%" }}>
            <Card style={{ width: "100%", borderRadius: "12px", padding: 12, boxShadow: "0 2px 8px rgba(0,0,0,0.1)", display: "flex", flexDirection: "column" }}>
                <Title level={3} style={{ width: "100%" }}>
                    {savedImage ? <CheckCircleTwoTone /> : <ExclamationCircleTwoTone />} Map
                </Title>
                <Divider />
                <Row gutter={[8, 8]} wrap={true} style={{ width: "100%" }}>
                    {!savedImage ? (
                        <>
                            <Title level={5} style={{ width: "100%", textAlign: "center" }}>
                                No map uploaded! Please upload your home's floorplan.
                            </Title>
                            <Col xs={24} style={{ display: "flex", justifyContent: "center" }}>
                                <Button onClick={toggleOpenModal} type="primary" size="large" shape="round" style={{ width: "100%" }}>
                                    Add a Map
                                </Button>
                            </Col>
                        </>
                    ) : (
                        !modalOpen && (
                            <div style={{ width: "100%", display: "flex", flexDirection: "column", alignItems: "center" }}>
                                <Title level={5} style={{ width: "100%", textAlign: "center" }}>Current Floorplan:</Title>

                                <div style={{ display: "flex", justifyContent: "center", width: "100%" }}>
                                    <Image
                                        src={savedImage}
                                        alt="Saved Floorplan"
                                        style={{ borderRadius: "8px", marginBottom: "12px", maxWidth: "300px", width: "100%", objectFit: "contain" }}
                                    />
                                </div>

                                <Col xs={24} style={{ display: "flex", justifyContent: "center" }}>
                                    <Button onClick={toggleOpenModal} type="primary" size="large" shape="round" style={{ maxWidth: "300px", width: "100%" }}>
                                        Change Current Map
                                    </Button>
                                </Col>
                            </div>

                        )
                    )}
                </Row>
            </Card>

            <Modal
                title="Submit a Map"
                open={modalOpen}
                onCancel={toggleOpenModal}
                footer={null}
                style={{ maxWidth: "80%" }}
            >
                <Steps
                    direction="vertical"
                    current={current}
                    style={{ marginBottom: 12, width: "100%" }}
                    items={steps.map((item) => ({ key: item.title, title: item.title }))}
                />

                {/* Step 1: File Upload */}
                {current === 0 && (
                    <Form form={form} style={{ width: "100%" }}>
                        <Form.Item name="fileUpload" noStyle style={{ width: "100%" }}>
                            <Upload.Dragger
                                maxCount={1}
                                listType="picture"
                                fileList={fileList}
                                onChange={handleFileChange}
                                beforeUpload={() => false}
                                style={{ width: "100%" }}
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
                    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: "12px", width: "100%" }}>
                        <Spin size="large" />
                        <Title level={5} style={{ textAlign: "center", width: "100%" }}>
                            Sending your floorplan to the robot! Please wait.
                        </Title>
                    </div>
                )}

                {/* Step 3: All done! */}
                {current === 2 && (
                    uploadingFailure ? <Result status="error" title="Could not send your floorplan to CargoBuddy."
                        subTitle="Please try again later."
                        style={{ width: "100%" }} />
                        : <Result status="success" title="You're all set!" style={{ width: "100%" }} />
                )}

                {/* Navigation Buttons */}
                <div style={{ marginTop: 24, display: "flex", justifyContent: "space-between", width: "100%" }}>
                    {current > 0 && (
                        <Button style={{ marginRight: 8, flexGrow: 1 }} onClick={prev}>
                            Previous
                        </Button>
                    )}
                    {current < steps.length - 1 && (
                        <Button type="primary" onClick={next} disabled={isNextDisabled} style={{ flexGrow: 1 }}>
                            Next
                        </Button>
                    )}
                    {current === steps.length - 1 && (
                        <Button type="primary" onClick={toggleOpenModal} style={{ flexGrow: 1 }}>
                            Done
                        </Button>
                    )}
                </div>
            </Modal>
        </Col>

    );
};

export default MapActions;
