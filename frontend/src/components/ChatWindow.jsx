import Message from "./Message";
import { useEffect, useRef } from "react";

function ChatWindow({

  messages,
  loading

}) {

  const bottomRef =
    useRef(null);

  useEffect(() => {

    bottomRef.current?.scrollIntoView({
      behavior: "smooth"
    });

  }, [messages, loading]);

  return (

    <div className="chat-window">

      {messages.length === 0 && (

        <div
          style={{
            color: "#888",
            textAlign: "center",
            marginTop: "50px"
          }}
        >
          Start a conversation...
        </div>

      )}

      {messages.map((msg, index) => (

        <Message
          key={index}
          sender={msg.sender}
          text={msg.text}
        />

      ))}

      {loading && (

        <div className="thinking">

          Thinking...

        </div>

      )}

      <div ref={bottomRef}></div>

    </div>

  );

}

export default ChatWindow;