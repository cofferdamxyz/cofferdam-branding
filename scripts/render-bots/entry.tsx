import { createRoot } from "react-dom/client"
import { RobotHead } from "robot-heads"
const q = new URLSearchParams(location.search)
const state = (q.get("state") ?? "idle") as any
const size = Number(q.get("size") ?? 760)
// render.sh passes each bot's shape and colours; the defaults are the
// Engineering bot's.
createRoot(document.getElementById("root")!).render(
  <RobotHead
    shape={(q.get("shape") ?? "rectangle") as any}
    state={state}
    size={size}
    color={q.get("color") ?? "#3c8aff"}
    trimColor={q.get("trim") ?? "#b5cff7"}
    screenColor="#e8f2ff"
    paused
    interactive={false}
    antenna={q.get("antenna") === "1"}
    floorShadow={false}
    seed={0.3}
  />
)
