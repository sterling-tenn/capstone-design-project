"use client";

import React, { useState, useEffect } from "react";
import { Button, Modal, Form, Image, Typography, Input, Space } from "antd";
import { PlusOutlined, CloseOutlined } from "@ant-design/icons";
import { getImageSizeFromBase64 } from "../lib/ImagesCalls";

const { Title, Text } = Typography;

interface NewJobActionProps {
    handleSetAction: (
        actionName: string,
        start: { x: number; y: number; adjustedX: number; adjustedY: number } | null,
        destination: { x: number; y: number; adjustedX: number; adjustedY: number } | null
    ) => void;
}

const NewJobAction: React.FC<NewJobActionProps> = ({ handleSetAction }) => {
    const [modalOpen, setModalOpen] = useState<boolean>(false);
    const [floorplan, setFloorplan] = useState<string | null>(null);
    const [startMarker, setStartMarker] = useState<{ x: number; y: number; adjustedX: number; adjustedY: number } | null>(null);
    const [destinationMarker, setDestinationMarker] = useState<{ x: number; y: number; adjustedX: number; adjustedY: number } | null>(null);
    const [form] = Form.useForm();

    // Fetch stored floorplan
    useEffect(() => {
        const storedImage = localStorage.getItem("savedImage");
        if (storedImage) {
            setFloorplan(storedImage);
        }
    }, []);

    useEffect(() => {
        console.log("Start Marker:", startMarker);
        console.log("Destination Marker:", destinationMarker);
    }, [startMarker, destinationMarker]);

    // Open modal and reset markers
    const openModal = () => {
        setStartMarker(null);
        setDestinationMarker(null);
        setModalOpen(true);
        form.resetFields();

        const storedImage = localStorage.getItem("savedImage");
        if (storedImage) {
            setFloorplan(storedImage);
        }
    };

    // Close modal
    const closeModal = () => {
        setModalOpen(false);
        form.resetFields();
        setStartMarker(null);
        setDestinationMarker(null);
    };

    // Clear markers function
    const clearMarkers = () => {
        setStartMarker(null);
        setDestinationMarker(null);
    };

    // Handle marker placement
    const handleImageClick = async (e: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (!floorplan) return;

        const rect = e.currentTarget.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        try {
            const { width: imgWidth, height: imgHeight } = await getImageSizeFromBase64(floorplan);
            const adjustedX = Math.round((x / rect.width) * imgWidth);
            const adjustedY = Math.round((y / rect.height) * imgHeight);

            if (!startMarker) {
                setStartMarker({ x, y, adjustedX, adjustedY });
                console.log(`🟢 Start Marker Set: (${x}, ${y}), Adjusted: (${adjustedX}, ${adjustedY})`);
            } else if (!destinationMarker) {
                setDestinationMarker({ x, y, adjustedX, adjustedY });
                console.log(`🔴 Destination Marker Set: (${x}, ${y}), Adjusted: (${adjustedX}, ${adjustedY})`);
            }
        } catch (error) {
            console.error("❌ Error getting image size:", error);
        }
    };

    const handleSubmit = async () => {
        try {
            const values = await form.validateFields();

            if (!startMarker || !destinationMarker) {
                console.error("🚨 Both start and destination markers are required!");
                return;
            }

            console.log("Form values:", values);
            console.log("Start marker:", startMarker);
            console.log("Destination marker:", destinationMarker);
            handleSetAction(values.jobName, startMarker, destinationMarker);

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

                    {/* Dynamic Message */}
                    <Text type="secondary" style={{ fontSize: "16px", display: "block", marginBottom: "12px" }}>
                        {!startMarker
                            ? "🟢 Set the starting location of the robot."
                            : !destinationMarker
                            ? "🔴 Select the destination of the robot."
                            : "✅ Markers set. Click 'Submit' to continue or 'Clear Markers' to reset."}
                    </Text>

                    <Form.Item
                        label={<Title level={5}>Tap on the map below to set a start and destination point.</Title>}
                    >
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
                                {startMarker && (
                                    <div
                                        style={{
                                            position: "absolute",
                                            top: startMarker.y,
                                            left: startMarker.x,
                                            width: "14px",
                                            height: "14px",
                                            backgroundColor: "green",
                                            borderRadius: "50%",
                                            transform: "translate(-50%, -50%)",
                                            pointerEvents: "none",
                                            border: "2px solid white",
                                        }}
                                    />
                                )}
                                {destinationMarker && (
                                    <div
                                        style={{
                                            position: "absolute",
                                            top: destinationMarker.y,
                                            left: destinationMarker.x,
                                            width: "14px",
                                            height: "14px",
                                            backgroundColor: "red",
                                            borderRadius: "50%",
                                            transform: "translate(-50%, -50%)",
                                            pointerEvents: "none",
                                            border: "2px solid white",
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

                    {/* Clear Markers Button */}
                    {startMarker || destinationMarker ? (
                        <Space style={{ width: "100%", display: "flex", justifyContent: "center" }}>
                            <Button type="default" danger onClick={clearMarkers} icon={<CloseOutlined />}>
                                Clear Markers
                            </Button>
                        </Space>
                    ) : null}
                </Form>
            </Modal>
        </>
    );
};

export default NewJobAction;
