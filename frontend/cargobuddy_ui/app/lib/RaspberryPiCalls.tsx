const sendText = async (msg: string) => {
    try {
        const res = await fetch("/api/send-text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg }),
        });

        console.log("Response status:", res.status);

        if (!res.ok) {
            const errorText = await res.text().catch(() => "Unknown server error");
            return { error: errorText ?? "Unknown error" };
        }

        const data = await res.json();
        return data;
    } catch (error) {
        console.error("API Request failed:", error);
        return { error: error instanceof Error ? error.message : "Unknown error" };
    }
};

export const sendImage = async (
    imageBase64: string,
    start: { x: number; y: number; adjustedX: number; adjustedY: number } | null,
    dest: { x: number; y: number; adjustedX: number; adjustedY: number } | null
) => {
    try {
        const res = await fetch("/api/send-img", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ imageBase64, start, dest }),
        });

        console.log("Response status:", res.status);

        if (!res.ok) {
            const errorText = await res.text().catch(() => "Unknown server error");
            return { error: errorText ?? "Unknown error" };
        }

        const data = await res.json();
        return data;
    } catch (error) {
        console.error("API Request failed:", error);
        return { error: error instanceof Error ? error.message : "Unknown error" };
    }
};

// send over the floorplan with a marker value


// moving robot manually
export const moveForward = async () => { return await sendText("move-forward"); }
export const moveBackwards = async () => { return await sendText("move-backward"); }
export const turnLeft = async () => { return await sendText("turn-left"); }
export const turnRight = async () => { return await sendText("turn-right"); }
export const stop = async () => { return await sendText("stop"); }
export const autoMcl = async () => { return await sendText("auto-mcl"); }
// TODO: figure out what to do for automcl 2
export const autoMcl2 = async () => { return await sendText("auto-mcl"); }

