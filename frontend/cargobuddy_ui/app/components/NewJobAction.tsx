"use client";

import React, { useState, useEffect } from "react";
import { Button, Modal, Form, Image, Typography, Input } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { getImageSizeFromBase64 } from "../lib/ImagesCalls";

const { Title } = Typography;

interface NewJobActionProps {
    handleSetAction: (actionName: string, dest: { x: number; y: number, adjustedX: number, adjustedY: number } | null) => void;
}

const NewJobAction: React.FC<NewJobActionProps> = ({ handleSetAction }) => {
    const [modalOpen, setModalOpen] = useState<boolean>(false);
    const [floorplan, setFloorplan] = useState<string | null>(null);
    const [marker, setMarker] = useState<{ x: number; y: number, adjustedX: number, adjustedY: number } | null>(null);
    const [form] = Form.useForm();

    // Fetch the stored floorplan from localStorage
    useEffect(() => {
        const storedImage = localStorage.getItem("savedImage");
        if (storedImage) {
            setFloorplan(storedImage);
        }
    }, []);

    useEffect(() => {
        console.log(marker);
    }, [marker]);

    // Open modal and reset form/marker
    const openModal = () => {
        setMarker(null); // Reset marker
        setModalOpen(true);
        form.resetFields(); // Reset form fields when modal opens

        const storedImage = localStorage.getItem("savedImage");
        if (storedImage) {
            setFloorplan(storedImage);
        }
    };

    // Close modal and reset form
    const closeModal = () => {
        setModalOpen(false);
        form.resetFields();
        setMarker(null);
    };

    // Handle marker placement on the floorplan

    
    const handleImageClick = async (e: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (!floorplan) return;
    
        const rect = e.currentTarget.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
    
        try {
            const { width: imgWidth, height: imgHeight } = await getImageSizeFromBase64(floorplan);
    
            const adjustedX = Math.round((x / rect.width) * imgWidth);
            const adjustedY = Math.round((y / rect.height) * imgHeight);
    
            setMarker({ x, y, adjustedX, adjustedY });
            console.log(`🖍 Click Position: (${x}, ${y}), Adjusted: (${adjustedX}, ${adjustedY})`);
        } catch (error) {
            console.error("❌ Error getting image size:", error);
        }
    };

    const handleSubmit = async () => {
        try {
            const values = await form.validateFields();

            console.log("Form values:", values);
            console.log("Marker position:", marker);
            handleSetAction(values.jobName, marker);

            closeModal();
        } catch (errorInfo) {
            console.error("Validation failed:", errorInfo);
        }
    };

    return (
        <>
            <Button type="primary" size="large" shape="round" onClick={openModal} icon={<PlusOutlined />}>
                New job
            </Button>
            <Modal
                title="Create a New Job"
                open={modalOpen}
                onCancel={closeModal}
                onOk={handleSubmit}
                okText="Submit"
                width={600}
            >
                <Form form={form} layout="vertical">
                    <Form.Item
                        label="Job Name"
                        name="jobName"
                        rules={[{ required: true, message: "Please enter a job name!" }]}
                    >
                        <Input placeholder="Enter job name" />
                    </Form.Item>
                    <Form.Item label={<Title level={5}>On the map below, tap and mark a point where you want the robot to go.</Title>}>
                        {floorplan ? (
                            <div
                                style={{
                                    position: "relative",
                                    width: "100%",
                                    cursor: "crosshair",
                                    border: "1px solid #ddd",
                                }}
                                onClick={handleImageClick}
                            >
                                <Image
                                    src={floorplan}
                                    alt="Floorplan"
                                    width="100%"
                                    preview={false}
                                    style={{ borderRadius: "8px" }}
                                />
                                {marker && (
                                    <div
                                        style={{
                                            position: "absolute",
                                            top: marker.y,
                                            left: marker.x,
                                            width: "12px",
                                            height: "12px",
                                            backgroundColor: "red",
                                            borderRadius: "50%",
                                            transform: "translate(-50%, -50%)",
                                            pointerEvents: "none",
                                        }}
                                    />
                                )}
                            </div>
                        ) : (
                            <Title level={5} style={{ color: "red" }}>
                                No floorplan found. Please upload one first.
                            </Title>
                        )}
                    </Form.Item>
                </Form>
            </Modal>
        </>
    );
};

export default NewJobAction;
