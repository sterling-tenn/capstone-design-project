import net from "net";
import { NextResponse } from "next/server";

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
export async function POST(req: Request) {
    try {
        // Parse the request body
        const { imageBase64 } = await req.json();

        if (!imageBase64) {
            return NextResponse.json({ error: "No image data provided" }, { status: 400 });
        }

        // Convert Base64 string to Buffer
        const imageBuffer = Buffer.from(imageBase64, "base64");
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
