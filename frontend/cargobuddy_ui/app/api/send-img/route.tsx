import net from "net";
import { NextResponse } from "next/server";
import { Jimp } from "jimp";
import { rgbaToInt } from "@jimp/utils";

/**
 * API route to receive a Base64-encoded image and send it to a TCP server.
 * @param req - The incoming request (expects JSON with a Base64 string).
 * @returns JSON response.
 */

const HOST = "192.168.226.60";
const PORT = 5000;

// send Image
// We usually use this function when sending an image - most likely to be floorplan
// the pi received the floorplan and converts it to a grid system
// now, TODO is how to send the destination coords for it

const addMarkerToImage = async (
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


export async function POST(req: Request) {
    try {
        // Parse the request body
        const { imageBase64, x, y } = await req.json();

        if (!imageBase64) {
            return NextResponse.json({ error: "No image data provided" }, { status: 400 });
        }

        // Convert Base64 string to Buffer
        const markedImageBase64 = await addMarkerToImage(imageBase64, x, y)

        const imageBuffer = Buffer.from(markedImageBase64, "base64");
        const imageSize = imageBuffer.length;

        console.log("✅ Received Base64 image:", imageSize, "bytes");

        // Step 1: Establish TCP connection to send the image
        return new Promise((resolve, reject) => {
            const client = new net.Socket();

            client.connect(PORT, HOST, () => {
                console.log("✅ Connected to TCP server");

                // Step 2: Send header (2 = image)
                const headerBuffer = Buffer.alloc(4);
                headerBuffer.writeUInt32BE(2, 0);
                client.write(headerBuffer);

                // Step 3: Send image size
                const sizeBuffer = Buffer.alloc(4);
                sizeBuffer.writeUInt32BE(imageSize, 0);
                client.write(sizeBuffer);

                // Step 4: Send image data
                client.write(imageBuffer);
                console.log("📤 Image sent successfully!");
            });

            // Step 5: Receive response from TCP server
            client.on("data", (data) => {
                const response = data.toString();
                console.log("📩 TCP Server Response:", response);
                client.end(); // Close connection
                resolve(NextResponse.json({ message: "Image sent successfully!", response }, { status: 200 }));
            });

            // Handle errors
            client.on("error", (err) => {
                console.error("❌ TCP Connection Error:", err.message);
                reject(NextResponse.json({ error: "TCP Connection Failed", details: err.message }, { status: 500 }));
            });

            // Handle connection close
            client.on("close", () => {
                console.log("🔌 TCP Connection closed");
            });
        });
    } catch (error) {
        console.error("❌ API Error:", error);
        return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
    }
}
