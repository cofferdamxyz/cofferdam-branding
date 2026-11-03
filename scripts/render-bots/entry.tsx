import { createRoot } from "react-dom/client"
import { RobotHead } from "robot-heads"
const q = new URLSearchParams(location.search)
const state = (q.get("state") ?? "idle") as any
const size = Number(q.get("size") ?? 760)
createRoot(document.getElementById("root")!).render(
  <RobotHead
    shape="rectangle"
    state={state}
    size={size}
    color="#3c8aff"
    trimColor="#b5cff7"
    screenColor="#e8f2ff"
    paused
    interactive={false}
    antenna={q.get("antenna") === "1"}
    floorShadow={false}
    seed={0.3}
  />
)
