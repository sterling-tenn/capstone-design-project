"use client";

import React, { useEffect, useState } from "react";
import { Col, Divider, Row, Button, Card, Typography, Modal, Steps, Result, Form, Upload, Spin, Image } from 'antd';
import { CheckCircleTwoTone, ExclamationCircleTwoTone, InboxOutlined } from "@ant-design/icons";

const { Title } = Typography;

const steps = [
    { title: 'Add a map', content: 'First-content' },
    { title: 'Sending your map to CargoBuddy', content: 'Second-content' },
    { title: 'Complete!', content: 'Third-content' }
];

const MapActions: React.FC = () => {
    const [modalOpen, setModalOpen] = useState<boolean>(false);
    const [current, setCurrent] = useState<number>(0);
    const [fileList, setFileList] = useState<any[]>([]);
    const [uploading, setUploading] = useState<boolean>(false);
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

            // TODO: Make API call to send image to the robot
            setTimeout(() => {
                setUploading(false);
                saveImageOnLocalStorage()
                setCurrent(2);
            }, 5000);
        }
    }, [current]);

    const saveImageOnLocalStorage = () => {
        const file = fileList[0]?.originFileObj;
        if (!file) return
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            const base64String = reader.result as string;
            localStorage.setItem("savedImage", base64String); // Save image to localStorage
            setSavedImage(base64String); // Update state to display the image
            console.log("Image saved to localStorage!");
        };
    }

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
            form.resetFields();
        }
        setModalOpen((prev) => !prev);
    };

    const isNextDisabled = current === 0 ? fileList.length === 0 : uploading;

    return (
        <Col xs={24} md={18} lg={12}>
            <Card style={{ borderRadius: "12px", padding: 12, boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
                <Title level={3}>{savedImage ? <CheckCircleTwoTone /> : <ExclamationCircleTwoTone />} Map</Title>
                <Divider />
                <Row gutter={[8, 8]} wrap={true}>
                    {(!savedImage) ? (
                        <>
                            <Title level={5}>
                                No map uploaded! Please upload your home's floorplan.
                            </Title>
                            <Col xs={24}>
                                <Button onClick={toggleOpenModal} type="primary" size="large" shape="round">
                                    Add a Map
                                </Button>
                            </Col>
                        </>
                    ) : (
                        // I don't want the new floorplan to be shown in the background
                        // while the modal is still open
                        // that would be confusing
                        !modalOpen && (
                            <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                                <Title level={5}>Current Floorplan:</Title>
                                <Image
                                    src={savedImage}
                                    alt="Saved Floorplan"
                                    width={200}
                                    style={{ borderRadius: "8px", marginBottom: "12px" }}
                                />
                                <Col xs={24}>
                                    <Button onClick={toggleOpenModal} type="primary" size="large" shape="round">
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
            >
                <Steps current={current} items={steps.map((item) => ({ key: item.title, title: item.title }))} />

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
                    <Result status="success" title="You're all set!" />
                )}

                {/* Navigation Buttons */}
                <div style={{ marginTop: 24 }}>
                    {current < steps.length - 1 && (
                        <Button type="primary" onClick={next} disabled={isNextDisabled}>
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
