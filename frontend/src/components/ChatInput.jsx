import { useState } from "react";
import API from "../services/api";

function ChatInput({
  chats,
  setChats,
  activeChatId,
  setLoading
}) {

  const [question, setQuestion] =
    useState("");

  const sendQuestion = async () => {

    if (!question.trim()) return;

    const currentChat =
      chats.find(
        c => c.id === activeChatId
      );

    if (!currentChat) return;

    const updatedMessages = [

      ...currentChat.messages,

      {
        sender: "You",
        text: question
      }

    ];

    setChats(prev =>

      prev.map(chat =>

        chat.id === activeChatId

          ? {
              ...chat,
              messages: updatedMessages
            }

          : chat

      )

    );

    setLoading(true);

    try {

      await API.post(
        "/chat/save",
        {
          chat_id: activeChatId,
          messages: updatedMessages
        }
      );

      const response =
  await API.post(
    "/chat",
    {
      question,
      history: updatedMessages
    },
    {
      timeout: 120000
    }
  );

      const answer =
        response.data.answer;

      const sources =
        response.data.sources || [];

      let finalAnswer = answer;

if (
  answer !==
  "I could not find that information in the documents."
  &&
  sources.length > 0
) {

  const sourceText = sources
    .map(
      source =>
        `${source.file} (Page ${source.page})`
    )
    .join("\n");

  finalAnswer +=
    `\n\nSources:\n${sourceText}`;
}

const botMessage = {
  sender: "Bot",
  text: finalAnswer
};

      const finalMessages = [

        ...updatedMessages,

        botMessage

      ];

      setChats(prev =>

        prev.map(chat =>

          chat.id === activeChatId

            ? {
                ...chat,
                messages: finalMessages
              }

            : chat

        )

      );

      await API.post(
        "/chat/save",
        {
          chat_id: activeChatId,
          messages: finalMessages
        }
      );

    }

    catch (error) {

      console.error(error);

    }

    finally {

      setLoading(false);

    }

    setQuestion("");

  };

  return (

    <div className="chat-input-container">

      <input

        value={question}

        onChange={(e) =>
          setQuestion(e.target.value)
        }

        onKeyDown={(e) => {

          if (e.key === "Enter") {

            sendQuestion();

          }

        }}

        placeholder="Ask a question..."

      />

      <button
        onClick={sendQuestion}
      >
        Send
      </button>

    </div>

  );

}

export default ChatInput;