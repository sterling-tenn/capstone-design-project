import React, { useState } from 'react';
import { Upload, Button, Card, message } from 'antd';
import { UploadOutlined, DeleteOutlined, RightOutlined } from '@ant-design/icons';
import { motion } from 'framer-motion';
import './Upload.css'; // Custom CSS file for centering

const UploadComponent = () => {
    const [fileList, setFileList] = useState([]);
    const [previewUrl, setPreviewUrl] = useState(null);

    // Motion variants for animations
    const fadeIn = {
        hidden: { opacity: 0 },
        visible: { opacity: 1, transition: { duration: 0.8 } },
    };

    const handleUploadChange = ({ fileList }) => {
        setFileList(fileList);
        // TODO: API call to store the image tied to the user
        if (fileList.length > 0 && fileList[0].originFileObj) {
            const file = fileList[0].originFileObj;
            const imageUrl = URL.createObjectURL(file);
            setPreviewUrl(imageUrl);
        } else {
            setPreviewUrl(null);
        }
    };

    return (
        <motion.div
            initial="hidden"
            animate="visible"
            variants={fadeIn}
            className="upload-container"
        >
            <Card
                title={<h2>Upload Your Floorplan</h2>}
                icon={<UploadOutlined />}
                className="upload-card"
                style={{
                    maxWidth: '500px',
                    margin: '0 auto',
                    padding: '20px',
                }}
            >
                {/* Ant Design Upload component */}
                <Upload
                    accept="image/*"
                    fileList={fileList}
                    onChange={handleUploadChange}
                    beforeUpload={() => false} // Prevent automatic upload
                    maxCount={1} // Allow only one image upload
                >
                    <Button icon={<UploadOutlined />} type="primary">
                        Click to Upload
                    </Button>
                </Upload>

                {/* Animate and display uploaded image */}
                {previewUrl && (
                    <motion.div
                        className="preview-container"
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.5, ease: 'easeInOut' }}
                        style={{ marginTop: '20px' }}
                    >
                        <h3>Your Floorplan Preview:</h3>
                        <img
                            src={previewUrl}
                            alt="Uploaded Floorplan"
                            style={{
                                maxWidth: '100%',
                                height: 'auto',
                                border: '1px solid #ddd',
                                padding: '10px',
                                borderRadius: '8px',
                                boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
                            }}
                        />
                    </motion.div>
                )}
                {/* if user made a mistake, they can remove the image */}
                {previewUrl && (
                    <motion.div
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        style={{ marginTop: '20px' }}
                    >
                        <Button type="primary" danger size="large" icon={<DeleteOutlined />} onClick={() => setPreviewUrl(null)}>
                            Remove Image
                        </Button>
                    </motion.div>
                )}
                {/* Show the next button if an image is uploaded */}
                {previewUrl && (
                    <motion.div
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        style={{ marginTop: '20px' }}
                    >
                        <Button type="primary" size="large" icon={<RightOutlined />} onClick={() => message.error('Sorry! Application still under construction.')}>
                            Next
                        </Button>
                    </motion.div>
                )}
            </Card>
        </motion.div>
    );
};

export default UploadComponent;
