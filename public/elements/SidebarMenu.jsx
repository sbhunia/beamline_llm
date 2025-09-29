// public/elements/SidebarMenu.jsx
export default function SidebarMenu(props) {
  const buttons = props?.buttons ?? [];

  const btnStyle = {
    width: "100%",
    marginBottom: "8px",
    padding: "10px 12px",
    borderRadius: "10px",
    border: "1px solid #ddd",
    background: "#f4f4f4",
    cursor: "pointer",
    textAlign: "left",
    fontWeight: 600
  };

  return (
    <div style={{ padding: "8px" }}>
      {buttons.map((b) => (
        <button
          key={b.name}
          style={btnStyle}
          onClick={() => callAction({ name: b.name, payload: { from: "sidebar" } })}
        >
          {b.label || b.name}
        </button>
      ))}
    </div>
  );
}
