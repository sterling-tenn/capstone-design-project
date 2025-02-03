import { NextResponse } from "next/server";
import net from "net";

const HOST = "192.168.1.135";
const PORT = 5000;

export async function POST(req: Request) {
    try {
        const { message } = await req.json();

        if (!message) {
            return NextResponse.json({ error: "Message is required" }, { status: 400 });
        }

        return new Promise((resolve, reject) => {
            const client = new net.Socket();

            client.connect(PORT, HOST, () => {
                console.log("✅ Connected to Raspberry Pi server");
                client.write(message);
            });

            client.on("data", (data) => {
                console.log("📩 Received:", data.toString());
                client.end(); // Close after receiving response
                resolve(NextResponse.json({ response: data.toString() }));
            });

            client.on("error", (err) => {
                console.error("❌ Connection error:", err.message);
                reject(NextResponse.json({ error: err.message }, { status: 500 }));
            });

            client.on("close", () => {
                console.log("🔴 Connection closed");
            });
        });
    } catch (error) {
        return NextResponse.json({ error }, { status: 500 });
    }
}
