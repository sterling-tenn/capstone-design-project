import { Jimp } from "jimp";
import { rgbaToInt } from "@jimp/utils";

export const getImageSizeFromBase64 = (base64Image: string): Promise<{ width: number; height: number }> => {
    return new Promise((resolve, reject) => {
        const img = new window.Image();
        img.src = base64Image;
        img.onload = () => resolve({ width: img.naturalWidth, height: img.naturalHeight });
        img.onerror = (err) => reject(err);
    });
};

export const addMarkerToImage = async (
    base64Image: string,
    x: number,
    y: number
): Promise<string> => {
    try {
        // Decode Base64 into a Jimp image
        const buffer = Buffer.from(base64Image.split(",")[1], "base64");
        const image = await Jimp.read(buffer);

        // Ensure image dimensions are known
        const width = image.bitmap.width;
        const height = image.bitmap.height;
        console.log(`📏 Image dimensions: ${width} x ${height}`);

        // Convert screen x, y to actual image pixels
        const adjustedX = x;
        const adjustedY = y;
        console.log(`✅ Adjusted Coordinates: (${adjustedX}, ${adjustedY})`);

        // Define marker size and color (Red: #FF0000)
        const markerSize = 10;
        const markerColor = rgbaToInt(255, 0, 0, 255);

        // Draw a circular marker
        for (let dx = -markerSize; dx <= markerSize; dx++) {
            for (let dy = -markerSize; dy <= markerSize; dy++) {
                if (Math.sqrt(dx * dx + dy * dy) <= markerSize) {
                    const markerX = adjustedX + dx;
                    const markerY = adjustedY + dy;
                    // Ensure marker stays inside the image bounds
                    if (markerX >= 0 && markerX < width && markerY >= 0 && markerY < height) {
                        image.setPixelColor(markerColor, markerX, markerY);
                    }
                }
            }
        }

        // Convert modified image back to Base64
        const modifiedBase64 = await image.getBase64("image/png");
        console.log("✅ Marker placed successfully!");
        console.log(modifiedBase64)
        return modifiedBase64;
    } catch (error) {
        console.error("❌ Error modifying image:", error);
        throw error;
    }
};
