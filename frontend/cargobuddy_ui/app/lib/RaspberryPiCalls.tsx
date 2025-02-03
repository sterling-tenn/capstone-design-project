const sendMessage = async (msg: string) => {
    try {
        const res = await fetch("/api/raspberry-pi", {
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
        console.log("Response from API:", data);
        return data;
    } catch (error) {
        console.error("API Request failed:", error);
        return { error: error instanceof Error ? error.message : "Unknown error" };
    }
};


// moving robot manually
export const moveForward = async () => { return await sendMessage("move-forward"); }
export const moveBackwards = async () => { return await sendMessage("move-backward"); }
export const turnLeft = async () => { return await sendMessage("turn-left"); }
export const turnRight = async () => { return await sendMessage("turn-right"); }
export const stop = async () => { return await sendMessage("stop"); }
