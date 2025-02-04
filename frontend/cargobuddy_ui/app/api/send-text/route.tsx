import { NextResponse } from "next/server";
import net from "net";

const HOST = "192.168.226.60";
const PORT = 5000;

// send Text
export async function POST(req: Request) {
    try {
        const { message } = await req.json();

        if (!message) {
            return NextResponse.json({ error: "Message is required" }, { status: 400 });
        }

        return new Promise((resolve, reject) => {
            const client = new net.Socket();

            client.connect(PORT, HOST, () => {
                console.log("Connected to server");

                // Step 1: Send header (1 = text)
                const headerBuffer = Buffer.alloc(4);
                headerBuffer.writeUInt32BE(1, 0);
                client.write(headerBuffer);

                // Step 2: Send message
                client.write(message, "utf-8");
            });

            // Step 3: Receive response
            client.on("data", (data) => {
                const response = data.toString();
                console.log("Received:", response);
                resolve(response);
                client.end(); // Close connection after response
            });

            // Handle Errors
            client.on("error", (err) => {
                console.error("Connection error:", err.message);
                reject(err);
            });

            // Handle Connection Close
            client.on("close", () => {
                console.log("Connection closed");
            });
        });
    } catch (error) {
        return NextResponse.json({ error }, { status: 500 });
    }
}
