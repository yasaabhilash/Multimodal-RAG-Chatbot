function Message({ sender, text }) {

  return (

    <div
      className={
        sender === "You"
          ? "user-message"
          : "bot-message"
      }
    >

      <strong>
        {sender}
      </strong>

      <p
        style={{
          whiteSpace: "pre-wrap",
          marginTop: "8px"
        }}
      >
        {text}
      </p>

    </div>

  );

}

export default Message;