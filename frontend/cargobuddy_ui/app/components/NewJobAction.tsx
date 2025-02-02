"use client";

import React, { useState, useEffect } from "react";
import { Button, Modal, Form, Image, Typography, Input } from "antd";
import { PlusOutlined } from "@ant-design/icons";


const { Title } = Typography;

interface NewJobActionProps {
    handleSetAction: (actionName: string, info: object) => void;
}

const NewJobAction: React.FC<NewJobActionProps> = ({ handleSetAction }) => {
    const [modalOpen, setModalOpen] = useState<boolean>(false);
    const [floorplan, setFloorplan] = useState<string | null>(null);
    const [marker, setMarker] = useState<{ x: number; y: number } | null>(null);
    const [form] = Form.useForm();

    // Fetch the stored floorplan from localStorage
    useEffect(() => {
        const storedImage = localStorage.getItem("savedImage");
        if (storedImage) {
            setFloorplan(storedImage);
        }
    }, []);

    // Open modal and reset form/marker
    const openModal = () => {
        setMarker(null); // Reset marker
        setModalOpen(true);
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
    const handleImageClick = (e: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (!floorplan) return;

        const rect = e.currentTarget.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        setMarker({ x, y });
    };

    // Handle form submission
    const handleSubmit = () => {
        console.log("Marker position:", marker);
        // TODO: figure out how to actually send the end marker position lol
        closeModal();
        // idk what to put for info yet
        let job = form.getFieldValue("jobName");
        handleSetAction(job, {}); // Ensure `handleSetAction` is called with correct params
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
                        name="jobName" // Correctly associate form state
                        rules={[{ required: true, message: "Please enter a job name!" }]} // Optional validation
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
